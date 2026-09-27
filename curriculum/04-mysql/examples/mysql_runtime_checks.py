#!/usr/bin/env python3
"""Opt-in MySQL 9.7 course checks. Resets ONLY the named local course schema.

Run with --confirm-reset handbook_mysql_lab. No automatic compatibility fallback.
"""
import argparse
import datetime
import importlib.util
import json
import os
from pathlib import Path
import re
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from mysql_course import examples, execute

HERE = Path(__file__).resolve().parent
DATABASE = "handbook_mysql_lab"
RECORDS = examples()
CONFIG = None
PYMYSQL = None


def connect():
    return PYMYSQL.connect(**CONFIG, database=DATABASE, charset="utf8mb4", autocommit=True,
                           connect_timeout=5, read_timeout=12, write_timeout=5)


def block(conn, name):
    return execute(conn, RECORDS[name]["code"])


def one(conn, sql, parameters=None):
    with conn.cursor() as cursor:
        cursor.execute(sql, parameters)
        return cursor.fetchall() if cursor.description else cursor.rowcount


class MySQLChecks(unittest.TestCase):
    def setUp(self):
        self.db = connect()
        self.addCleanup(self.cleanup)
        execute(self.db, (HERE / "seed.sql").read_text(encoding="utf-8"))
        one(self.db, "SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ")

    def cleanup(self):
        self.db.rollback()
        self.db.close()

    def test_transaction_commit_and_rollback(self):
        self.assertEqual(block(self.db, "transaction_commit"), [((70,),), ((1, -30),)])
        self.assertEqual(block(self.db, "transaction_rollback"), [((70,),), ((1, -30),)])

    def test_conditional_debit_zero_rows(self):
        block(self.db, "transaction_commit")
        self.assertEqual(block(self.db, "conditional_debit"), [((0,),)])
        self.assertEqual(one(self.db, "SELECT credits FROM accounts WHERE id=1"), ((70,),))

    def test_optimistic_repeat_rejected(self):
        self.assertEqual(block(self.db, "optimistic_update"), [((1,),)])
        self.assertEqual(block(self.db, "optimistic_update"), [((0,),)])
        self.assertEqual(one(self.db, "SELECT credits,version FROM accounts WHERE id=1"), ((70, 1),))

    def _isolation_round(self, begin_name, expected):
        b = connect()
        self.addCleanup(b.close)
        self.assertEqual(block(self.db, begin_name), [((100,),)])
        block(b, "isolation_writer")
        self.assertEqual(block(self.db, "isolation_reader_again"), [((expected,),)])
        self.assertEqual(one(self.db, "SELECT credits FROM accounts WHERE id=1"), ((120,),))

    def test_repeatable_read(self):
        self._isolation_round("isolation_rr_begin", 100)

    def test_read_committed(self):
        self._isolation_round("isolation_rc_begin", 120)

    def test_snapshot_starts_at_first_read(self):
        b = connect()
        self.addCleanup(b.close)
        one(self.db, "START TRANSACTION")
        block(b, "isolation_writer")
        self.assertEqual(one(self.db, "SELECT credits FROM accounts WHERE id=1"), ((120,),))

    def test_locking_read_sees_current(self):
        b = connect()
        self.addCleanup(b.close)
        block(self.db, "isolation_rr_begin")
        block(b, "isolation_writer")
        self.assertEqual(one(self.db, "SELECT credits FROM accounts WHERE id=1"), ((100,),))
        self.assertEqual(block(self.db, "isolation_locking_read"), [((120,),)])

    def test_own_update_is_visible(self):
        self.assertEqual(block(self.db, "mvcc_own_write"), [((100,),), ((105,),)])
        self.assertEqual(one(self.db, "SELECT credits FROM accounts WHERE id=1"), ((100,),))

    def test_row_lock_timeout(self):
        block(self.db, "row_lock_a")
        b = connect()
        try:
            one(b, "SET SESSION innodb_lock_wait_timeout=1")
            one(b, "START TRANSACTION")
            with self.assertRaises(PYMYSQL.MySQLError) as error:
                one(b, "UPDATE accounts SET credits=credits+10 WHERE id=1")
            self.assertEqual(error.exception.args[0], 1205)
        finally:
            b.rollback()
            b.close()

    def test_row_lock_release_allows_update(self):
        block(self.db, "row_lock_a")
        started = threading.Event()
        def worker():
            b = connect()
            try:
                one(b, "SET SESSION innodb_lock_wait_timeout=5")
                one(b, "START TRANSACTION")
                started.set()
                n = one(b, "UPDATE accounts SET credits=credits+10 WHERE id=1")
                b.commit()
                return n
            finally:
                b.rollback()
                b.close()
        with ThreadPoolExecutor(max_workers=1) as pool:
            pending = pool.submit(worker)
            self.assertTrue(started.wait(3))
            self.db.commit()
            self.assertEqual(pending.result(timeout=8), 1)
        self.assertEqual(one(self.db, "SELECT credits FROM accounts WHERE id=1"), ((110,),))

    def test_range_prevents_inserting_fifteen(self):
        block(self.db, "gap_lock_a")
        b = connect()
        try:
            one(b, "SET SESSION innodb_lock_wait_timeout=1")
            one(b, "START TRANSACTION")
            with self.assertRaises(PYMYSQL.MySQLError) as error:
                one(b, "INSERT INTO lock_numbers(id) VALUES(15)")
            self.assertEqual(error.exception.args[0], 1205)
        finally:
            b.rollback()
            b.close()

    def test_deadlock_victim_not_predetermined(self):
        enabled = one(self.db, "SELECT @@global.innodb_deadlock_detect")[0][0]
        self.assertEqual(enabled, 1, "Deadlock demonstration requires detection ON")
        gate = threading.Barrier(2, timeout=5)
        def worker(first, second):
            db = connect()
            try:
                one(db, "SET SESSION innodb_lock_wait_timeout=5")
                one(db, "START TRANSACTION")
                one(db, "UPDATE accounts SET credits=credits+1 WHERE id=%s", (first,))
                gate.wait()
                one(db, "UPDATE accounts SET credits=credits+1 WHERE id=%s", (second,))
                db.commit()
                return 0
            except PYMYSQL.MySQLError as e:
                db.rollback()
                return e.args[0]
            finally:
                db.rollback()
                db.close()
        with ThreadPoolExecutor(max_workers=2) as pool:
            a = pool.submit(worker, 1, 2)
            b = pool.submit(worker, 2, 1)
            result = sorted([a.result(timeout=10), b.result(timeout=10)])
        self.assertEqual(result, [0, 1213])
        self.assertEqual(one(self.db, "SELECT credits FROM accounts ORDER BY id"), ((101,), (101,)))

    def test_check_rejects_negative(self):
        block(self.db, "constraints_setup")
        with self.assertRaises(PYMYSQL.MySQLError) as error:
            one(self.db, "INSERT INTO quota_rules VALUES(3,'invalid',-1,'x')")
        self.assertEqual(error.exception.args[0], 3819)

    def test_not_null_rejects_missing_value(self):
        block(self.db, "constraints_setup")
        with self.assertRaises(PYMYSQL.MySQLError) as error:
            one(self.db, "INSERT INTO quota_rules VALUES(3,'invalid',NULL,'x')")
        self.assertEqual(error.exception.args[0], 1048)

    def test_unique_nullable_allows_multiple_null(self):
        block(self.db, "constraints_setup")
        self.assertEqual(one(self.db, "SELECT COUNT(*) FROM quota_rules WHERE external_code IS NULL"), ((2,),))

    def test_cross_tenant_foreign_key_rejects(self):
        block(self.db, "ai_model_setup")
        with self.assertRaises(PYMYSQL.MySQLError) as error:
            one(self.db, "INSERT INTO lab_messages VALUES(3,20,1,'user','wrong tenant','2026-09-01 10:00:00')")
        self.assertEqual(error.exception.args[0], 1452)

    def test_invisible_roundtrip(self):
        block(self.db, "invisible_index")
        names = {row[2] for row in one(self.db, "SHOW INDEX FROM tasks")}
        self.assertNotIn("idx_tasks_priority", names)

    def test_explain_outputs_nonempty_not_fixed_plan(self):
        self.assertTrue(block(self.db, "plan_baseline")[-1])
        self.assertTrue(block(self.db, "plan_index")[-1])
        self.assertTrue(block(self.db, "analyze_recent")[-1])

    def test_parameter_binding_keeps_input_a_value(self):
        rows = one(self.db, "SELECT id FROM tasks WHERE title=%s", ("' OR '1'='1",))
        self.assertEqual(rows, ())

    def test_keyset_equals_second_offset_page(self):
        offset = block(self.db, "offset_page")[0]
        seek = block(self.db, "keyset_second")[0]
        self.assertEqual([r[0] for r in offset], [3, 2])
        self.assertEqual(offset, seek)

    def test_deferred_page_same_ids(self):
        rows = block(self.db, "deferred_page")[0]
        self.assertEqual([r[0] for r in rows], [3, 2])

    def test_batch_data_and_progress(self):
        block(self.db, "batch_setup")
        self.assertEqual(block(self.db, "batch_commit"), [(("a",), ("b",), ("c",)), ((1,),)])


# Named-example cases execute SQL extracted from the prose. Other cases add assertion queries
# and control the order of two real connections; they do not emulate InnoDB.
CASES = {
 "filter_tasks": ([], [((1,"整理笔记"),(3,"练习 SQL"),(4,"写周报"))]),
 "common_predicates": ([], [((1,),(3,),(5,),(6,)), ((1,),(3,),(6,)), ((1,),(6,))]),
 "grouped_predicate": ([], [((1,),(3,),(4,))]),
 "null_and_count": ([], [((4,),), (), ((6,5),), ()]),
 "top_pending": ([], [((3,3),(1,2))]),
 "time_window": ([], [((1,),(2,))]),
 "grouped_count": ([], [(("done",2),("pending",3))]),
 "conditional_count": ([], [((5,2),)]),
 "distinct_owners": ([], [((1,),(2,))]),
 "left_join": ([], [((1,"小林"),(2,"小林"),(3,"小周"),(4,None),(6,"小周"))]),
 "exists_query": ([], [((1,"小林"),(2,"小周"),(3,"小陈"))]),
 "window_latest": ([], [((10,6),(20,5))]),
 "mutation_roundtrip": ([], [((90,"done"),), ((0,),)]),
 "index_before": ([], [((1,),(3,),(4,))]),
 "secondary_lookup": (["secondary_setup"], [((1,"整理笔记"),(2,"修复登录"))]),
 "secondary_covering": (["secondary_setup"], [((1,1),(2,1))]),
 "composite_query": (["composite_setup"], [((1,),(3,),(4,))]),
 "covering_query": (["covering_setup"], [((4,1),(1,2),(3,3))]),
 "noncovering_query": (["covering_setup"], [((4,"写周报",1),(1,"整理笔记",2),(3,"练习 SQL",3))]),
 "icp_query": (["icp_setup"], [((6,"整理测试"),)]),
 "date_predicates": (["optimizer_setup"], [((1,),(2,)), ((1,),(2,))]),
}
for name, (before, expected) in CASES.items():
    def check(self, name=name, before=before, expected=expected):
        for setup in before:
            block(self.db, setup)
        self.assertEqual(block(self.db, name), expected)
    setattr(MySQLChecks, "test_sql_" + name, check)


def main():
    global CONFIG, PYMYSQL
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--confirm-reset', required=True, choices=[DATABASE])
    parser.add_argument('--report', type=Path, default=Path('mysql-runtime-result.json'))
    args = parser.parse_args()
    report = {"target":"MySQL 9.7.2+ within 9.7 LTS", "started_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "tests_run":0,"status":"environment_not_ready"}
    def finish(code):
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        return code
    if importlib.util.find_spec('pymysql') is None:
        report['reason']='PyMySQL is not installed; no database checks executed.'
        print(report['reason'])
        return finish(2)
    import pymysql
    PYMYSQL = pymysql
    host = os.environ.get('MYSQL_COURSE_HOST','127.0.0.1')
    if host not in {'127.0.0.1','localhost','::1'}:
        report['reason']='This course runner permits local hosts only.'
        return finish(2)
    password = os.environ.get('MYSQL_COURSE_PASSWORD')
    if not password:
        report['reason']='Set the local lab MYSQL_COURSE_PASSWORD; no checks executed.'
        return finish(2)
    try:
        port = int(os.environ.get('MYSQL_COURSE_PORT','3307'))
        if not 1 <= port <= 65535:
            raise ValueError('MYSQL_COURSE_PORT must be in 1..65535')
        CONFIG = dict(host=host, port=port,
                      user=os.environ.get('MYSQL_COURSE_USER','course'),password=password)
        db = connect()
        try:
            version = one(db,'SELECT VERSION()')[0][0]
            report['server_version']=version
            match = re.match(r'9\.7\.(\d+)',version)
            if 'mariadb' in version.lower() or not match or int(match[1]) < 2:
                raise RuntimeError('Target is MySQL 9.7.2 or later in the 9.7 series; no fallback allowed.')
            if one(db,'SELECT DATABASE()')[0][0] != DATABASE:
                raise RuntimeError('Wrong database')
        finally:
            db.close()
    except Exception as exc:
        report['reason']=str(exc)
        print(report['reason'])
        return finish(2)
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(MySQLChecks))
    report.update(status='passed' if result.wasSuccessful() else 'failed',tests_run=result.testsRun,
                  failures=[str(t) for t,_ in result.failures],errors=[str(t) for t,_ in result.errors],
                  skipped=[str(t) for t,_ in result.skipped])
    return finish(0 if result.wasSuccessful() else 1)
if __name__=='__main__':
    raise SystemExit(main())
