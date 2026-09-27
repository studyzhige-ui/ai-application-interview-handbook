# MySQL 配套实验｜按问题运行，不顺序背命令

[返回课程](../README.md) · [连接与重置](README.md)

正文负责建立概念，这里集中保存可复现操作、重置和清理。选择正在学习的一组即可；不要一次执行本文件中的全部 SQL。预期值来自明确数据与官方规则，不表示已在 MySQL 服务端跑通。

<a id="lab-02"></a>

## 02｜第一张表与连接

[回到正文](../docs/02-单表查询与增删改.md)

使用专用练习库，确认自动提交。第 02 章按建表、写入、查询、修改的顺序操作。下面的组合建表块供重复实验使用；若已有 first_tasks，先按环境页说明确认并重置，不能重复创建。

<a id="sql-environment"></a>

### `environment`

<!-- mysql-example: environment -->
```sql
SELECT VERSION() AS server_version, DATABASE() AS current_database;
```

<a id="sql-autocommit_setting"></a>

### `autocommit_setting`

<!-- mysql-example: autocommit_setting -->
```sql
SELECT @@session.autocommit AS autocommit_enabled;
```

<a id="sql-first_setup"></a>

### `first_setup`

<!-- mysql-example: first_setup -->
```sql
CREATE DATABASE IF NOT EXISTS handbook_mysql_lab
  CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE handbook_mysql_lab;

CREATE TABLE first_tasks (
    id BIGINT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    status VARCHAR(16) NOT NULL DEFAULT 'pending'
) ENGINE=InnoDB;

INSERT INTO first_tasks (id, title)
VALUES (1, '整理笔记'), (2, '练习 SQL');

SELECT id, title, status FROM first_tasks ORDER BY id;
```

**`first_update`**：[使用正文中的这一份 SQL](../docs/02-单表查询与增删改.md#sql-first_update)。

<a id="lab-03"></a>

## 03｜类型、NULL 与关系约束

[回到正文](../docs/03-数据类型约束与表关系.md)

先加载 seed.sql。先查缺值，再创建独立的额度约束表。需要验证拒绝时一次只运行一条故意错误的写入，并阅读数据库错误；不要将整份实验一次性执行。完成后清理本组新建表。

<a id="sql-null_and_count"></a>

### `null_and_count`

<!-- mysql-example: null_and_count -->
```sql
SELECT id FROM tasks WHERE owner_id IS NULL;
-- 4
SELECT id FROM tasks WHERE owner_id = NULL;
-- 空结果；这不是判断 NULL 的正确写法
SELECT COUNT(*) AS total, COUNT(owner_id) AS assigned FROM tasks;
-- total=6，assigned=5
SELECT id FROM tasks WHERE owner_id NOT IN (1, NULL);
-- 空结果；集合里的 NULL 会影响“不在集合中”的判断
```

<a id="sql-constraints_setup"></a>

### `constraints_setup`

<!-- mysql-example: constraints_setup -->
```sql
CREATE TABLE quota_rules (
    id INT PRIMARY KEY,
    name VARCHAR(40) NOT NULL,
    quota INT NOT NULL,
    external_code VARCHAR(40) NULL,
    UNIQUE KEY uk_external_code (external_code),
    CONSTRAINT ck_quota_nonnegative CHECK (quota >= 0)
) ENGINE=InnoDB;
INSERT INTO quota_rules VALUES (1, '体验', 10, NULL), (2, '标准', 20, NULL);
SELECT id, quota FROM quota_rules ORDER BY id;
```

<a id="sql-constraints_cleanup"></a>

### `constraints_cleanup`

<!-- mysql-example: constraints_cleanup -->
```sql
DROP TABLE quota_rules;
```

**拒绝路径的核对。** `quota_rules` 建好以后，分别尝试负额度、缺失必填名称、重复相同非空唯一值；应由对应 CHECK、NOT NULL、UNIQUE 拒绝。可空唯一列的多个 NULL 则不因此冲突。运行自动检查可以逐项核对，不把“执行到一半报错”当作整组事务已经自动回滚。

<a id="lab-04"></a>

## 04｜关联、统计与结果形状

[回到正文](../docs/04-关联查询与分组统计.md)

每次从 seed.sql 的六条任务开始。先手算筛选和分组，再比较结果；LEFT JOIN 保留无负责人的任务。窗口查询和条件汇总只在遇到对应需求时练习。修改回滚实验结束后数据应恢复。

<a id="sql-filter_tasks"></a>

### `filter_tasks`

<!-- mysql-example: filter_tasks -->
```sql
SELECT id, title
FROM tasks
WHERE tenant_id = 10 AND status = 'pending'
ORDER BY id;
```

<a id="sql-common_predicates"></a>

### `common_predicates`

<!-- mysql-example: common_predicates -->
```sql
SELECT id FROM tasks WHERE priority >= 2 ORDER BY id;
-- 1, 3, 5, 6
SELECT id FROM tasks WHERE id IN (1, 3, 6) ORDER BY id;
-- 1, 3, 6
SELECT id FROM tasks WHERE title LIKE '整理%' ORDER BY id;
-- 1, 6；% 表示任意长度的文字
```

<a id="sql-grouped_predicate"></a>

### `grouped_predicate`

<!-- mysql-example: grouped_predicate -->
```sql
SELECT id FROM tasks
WHERE tenant_id = 10 AND (status = 'pending' OR priority >= 3)
ORDER BY id;
-- 1, 3, 4
```

<a id="sql-top_pending"></a>

### `top_pending`

<!-- mysql-example: top_pending -->
```sql
SELECT id, priority FROM tasks
WHERE tenant_id = 10 AND status = 'pending'
ORDER BY priority DESC, id ASC
LIMIT 2;
-- (3, 3), (1, 2)
```

<a id="sql-time_window"></a>

### `time_window`

<!-- mysql-example: time_window -->
```sql
SELECT id FROM tasks
WHERE created_at >= '2026-09-01 00:00:00'
  AND created_at <  '2026-09-02 00:00:00'
ORDER BY id;
-- 1, 2
```

**`grouped_count`**：[使用正文中的这一份 SQL](../docs/04-关联查询与分组统计.md#sql-grouped_count)。

**`conditional_count`**：[使用正文中的这一份 SQL](../docs/04-关联查询与分组统计.md#sql-conditional_count)。

<a id="sql-distinct_owners"></a>

### `distinct_owners`

<!-- mysql-example: distinct_owners -->
```sql
SELECT DISTINCT owner_id FROM tasks
WHERE tenant_id = 10 AND owner_id IS NOT NULL
ORDER BY owner_id;
-- 1, 2
```

**`left_join`**：[使用正文中的这一份 SQL](../docs/04-关联查询与分组统计.md#sql-left_join)。

**`exists_query`**：[使用正文中的这一份 SQL](../docs/04-关联查询与分组统计.md#sql-exists_query)。

**`window_latest`**：[使用正文中的这一份 SQL](../docs/04-关联查询与分组统计.md#sql-window_latest)。

<a id="sql-mutation_roundtrip"></a>

### `mutation_roundtrip`

<!-- mysql-example: mutation_roundtrip -->
```sql
INSERT INTO tasks (id, tenant_id, owner_id, title, status, priority, created_at)
VALUES (90, 10, 1, '临时练习', 'pending', 1, '2026-09-06 09:00:00');
UPDATE tasks SET status = 'done' WHERE id = 90;
SELECT id, status FROM tasks WHERE id = 90;
-- (90,done)
DELETE FROM tasks WHERE id = 90;
SELECT COUNT(*) AS remaining FROM tasks WHERE id = 90;
-- 0
```

<a id="lab-05"></a>

## 05｜索引改变了什么

[回到正文](../docs/05-SQL执行与索引基础.md)

重新加载 seed.sql，先看表与基线，再增加索引，再看计划。六行小表可能仍选择全表扫描；比较查询结果，不以某个 key 或毫秒值作硬性答案。

**`index_before`**：[使用正文中的这一份 SQL](../docs/05-SQL执行与索引基础.md#sql-index_before)。

<a id="sql-add_team_status_index"></a>

### `add_team_status_index`

<!-- mysql-example: add_team_status_index -->
```sql
CREATE INDEX idx_tasks_tenant_status ON tasks (tenant_id, status);
SHOW INDEX FROM tasks;
```

<a id="sql-index_plan"></a>

### `index_plan`

<!-- mysql-example: index_plan -->
```sql
EXPLAIN FORMAT=TRADITIONAL
SELECT id FROM tasks
WHERE tenant_id = 10 AND status = 'pending' ORDER BY id;
```

<a id="lab-06"></a>

## 06｜同一棵二级索引，返回列不同

[回到正文](../docs/06-B+树与数据组织.md)

重新加载 seed.sql。先建立负责人索引，再比较查标题和只查索引已有列。正文解释可能的回表路径；实验计划由数据库实际选择，不能当成固定性能证明。

**`secondary_setup`**：[使用正文中的这一份 SQL](../docs/05-SQL执行与索引基础.md#sql-secondary_setup)。

**`secondary_lookup`**：[使用正文中的这一份 SQL](../docs/06-B+树与数据组织.md#sql-secondary_lookup)。

<a id="sql-secondary_covering"></a>

### `secondary_covering`

<!-- mysql-example: secondary_covering -->
```sql
SELECT id, owner_id FROM tasks WHERE owner_id = 1 ORDER BY id;
-- (1,1), (2,1)
```

<a id="lab-07"></a>

## 07｜联合索引、覆盖与 ICP

[回到正文](../docs/07-联合索引覆盖与下推.md)

各小组单独从 seed.sql 开始。联合索引组：composite_setup → composite_query；覆盖组：covering_setup → covering_query → noncovering_query → covering_explain；下推组：icp_setup → icp_query。不同索引可能竞争，不要把多个实验留下的全部索引当同一基线。最后执行覆盖组清理，或统一重置。

**`composite_setup`**：[使用正文中的这一份 SQL](../docs/07-联合索引覆盖与下推.md#sql-composite_setup)。

<a id="sql-composite_query"></a>

### `composite_query`

<!-- mysql-example: composite_query -->
```sql
SELECT id FROM tasks
WHERE status = 'pending' AND tenant_id = 10
ORDER BY created_at, id;
-- 1,3,4
```

<a id="sql-covering_setup"></a>

### `covering_setup`

<!-- mysql-example: covering_setup -->
```sql
CREATE INDEX idx_tasks_tenant_status_priority
ON tasks (tenant_id, status, priority);
```

<a id="sql-covering_query"></a>

### `covering_query`

<!-- mysql-example: covering_query -->
```sql
SELECT id, priority
FROM tasks
WHERE tenant_id = 10 AND status = 'pending'
ORDER BY priority, id;
```

<a id="sql-noncovering_query"></a>

### `noncovering_query`

<!-- mysql-example: noncovering_query -->
```sql
SELECT id, title, priority
FROM tasks
WHERE tenant_id = 10 AND status = 'pending'
ORDER BY priority, id;
```

<a id="sql-icp_setup"></a>

### `icp_setup`

<!-- mysql-example: icp_setup -->
```sql
CREATE INDEX idx_tasks_tenant_created_status
ON tasks (tenant_id, created_at, status);
```

**`icp_query`**：[使用正文中的这一份 SQL](../docs/07-联合索引覆盖与下推.md#sql-icp_query)。

<a id="sql-covering_explain"></a>

### `covering_explain`

<!-- mysql-example: covering_explain -->
```sql
EXPLAIN FORMAT=TRADITIONAL
SELECT id, priority
FROM tasks
WHERE tenant_id = 10 AND status = 'pending';
```

<a id="sql-covering_cleanup"></a>

### `covering_cleanup`

<!-- mysql-example: covering_cleanup -->
```sql
DROP INDEX idx_tasks_tenant_status_priority ON tasks;
DROP INDEX idx_tasks_tenant_created_status ON tasks;
```

<a id="lab-08"></a>

## 08｜范围、统计与执行计划

[回到正文](../docs/08-执行计划与慢查询.md)

每组从 seed.sql 重新开始。日期组先建立时间索引、比较等价条件、再查看统计和清理；最近任务组先看计划，再建立匹配索引，再运行 ANALYZE。ANALYZE 真实执行查询，不能对工作库随意运行。

<a id="sql-optimizer_setup"></a>

### `optimizer_setup`

<!-- mysql-example: optimizer_setup -->
```sql
CREATE INDEX idx_tasks_created ON tasks (created_at);
```

<a id="sql-date_predicates"></a>

### `date_predicates`

<!-- mysql-example: date_predicates -->
```sql
SELECT id FROM tasks
WHERE DATE(created_at) = '2026-09-01'
ORDER BY id;

SELECT id FROM tasks
WHERE created_at >= '2026-09-01 00:00:00'
  AND created_at <  '2026-09-02 00:00:00'
ORDER BY id;
```

<a id="sql-optimizer_inspect"></a>

### `optimizer_inspect`

<!-- mysql-example: optimizer_inspect -->
```sql
SHOW INDEX FROM tasks;
ANALYZE TABLE tasks;
EXPLAIN FORMAT=TRADITIONAL
SELECT id, title FROM tasks
WHERE created_at >= '2026-09-01 00:00:00';
```

<a id="sql-optimizer_cleanup"></a>

### `optimizer_cleanup`

<!-- mysql-example: optimizer_cleanup -->
```sql
DROP INDEX idx_tasks_created ON tasks;
```

**`plan_baseline`**：[使用正文中的这一份 SQL](../docs/08-执行计划与慢查询.md#sql-plan_baseline)。

<a id="sql-plan_index"></a>

### `plan_index`

<!-- mysql-example: plan_index -->
```sql
CREATE INDEX idx_tasks_recent
ON tasks (tenant_id, status, created_at, id);

EXPLAIN FORMAT=TREE
SELECT id, title
FROM tasks
WHERE tenant_id = 10 AND status = 'pending'
ORDER BY created_at DESC, id DESC
LIMIT 2;
```

**`analyze_recent`**：[使用正文中的这一份 SQL](../docs/08-执行计划与慢查询.md#sql-analyze_recent)。

<a id="sql-plan_cleanup"></a>

### `plan_cleanup`

<!-- mysql-example: plan_cleanup -->
```sql
DROP INDEX idx_tasks_recent ON tasks;
```

<a id="lab-09"></a>

## 09｜提交、回滚与零行更新

[回到正文](../docs/09-事务与ACID.md)

重置 accounts 为每户 100、credit_events 为空。提交扣 30 后余额 70、流水一条；再执行回滚示例，余额仍 70、流水仍一条。随后条件扣 90 应影响 0 行，应用必须判断这个业务结果，不能因为没有 SQL 错误就新增成功流水。

<a id="sql-transaction_settings"></a>

### `transaction_settings`

<!-- mysql-example: transaction_settings -->
```sql
SELECT @@session.autocommit, @@session.transaction_isolation;
```

**`transaction_commit`**：[使用正文中的这一份 SQL](../docs/09-事务与ACID.md#sql-transaction_commit)。

**`transaction_rollback`**：[使用正文中的这一份 SQL](../docs/09-事务与ACID.md#sql-transaction_rollback)。

**`conditional_debit`**：[使用正文中的这一份 SQL](../docs/09-事务与ACID.md#sql-conditional_debit)。

<a id="lab-10"></a>

## 10｜两个连接观察同一条记录

[回到正文](../docs/10-隔离级别与MVCC.md)

A、B 必须是独立连接，每轮前结束双方旧事务并重置。RR 轮次：A 执行 isolation_rr_begin（100）；B 执行 isolation_writer（提交 120）；A 执行 isolation_reader_again（100，随后提交）。RC 轮次用 isolation_rc_begin 替代第一步，第二次读为 120。要比较锁定读，另开一轮：A RR 首次读 100、B 提交 120 后，A 先执行 isolation_locking_read 得 120，再 COMMIT。mvcc_own_write 是独立单连接实验，自写能读到 105，最终回滚恢复 100。

<a id="sql-isolation_rr_begin"></a>

### `isolation_rr_begin`

<!-- mysql-example: isolation_rr_begin -->
```sql
SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;
START TRANSACTION;
SELECT credits FROM accounts WHERE id = 1;
```

<a id="sql-isolation_writer"></a>

### `isolation_writer`

<!-- mysql-example: isolation_writer -->
```sql
START TRANSACTION;
UPDATE accounts SET credits = 120 WHERE id = 1;
COMMIT;
```

<a id="sql-isolation_reader_again"></a>

### `isolation_reader_again`

<!-- mysql-example: isolation_reader_again -->
```sql
SELECT credits FROM accounts WHERE id = 1;
COMMIT;
```

<a id="sql-isolation_rc_begin"></a>

### `isolation_rc_begin`

<!-- mysql-example: isolation_rc_begin -->
```sql
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
START TRANSACTION;
SELECT credits FROM accounts WHERE id = 1;
```

**`isolation_locking_read`**：[使用正文中的这一份 SQL](../docs/10-隔离级别与MVCC.md#sql-isolation_locking_read)。

<a id="sql-mvcc_own_write"></a>

### `mvcc_own_write`

<!-- mysql-example: mvcc_own_write -->
```sql
SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;
START TRANSACTION;
SELECT credits FROM accounts WHERE id = 1;
UPDATE accounts SET credits = credits + 5 WHERE id = 1;
SELECT credits FROM accounts WHERE id = 1;
ROLLBACK;
```

<a id="lab-11"></a>

## 11｜并发修改、等待与任务领取

[回到正文](../docs/11-并发修改锁与死锁.md)

每项实验前结束所有旧事务，再重置。版本检查块从 credits=100、version=0 开始：第一次影响 1 行，再次用同版本影响 0 行。记录锁实验：A 执行 row_lock_a；B 执行 row_lock_b，其中 UPDATE 等待；回 A 提交或回滚，再观察 B 继续并回滚。间隙实验：A 执行 gap_lock_a，B 执行 gap_insert_b，其中插入 15 等待；A 结束后 B 继续，最后回滚 B。不要在发生等待时重复发送同一命令。

**`optimistic_update`**：[使用正文中的这一份 SQL](../docs/11-并发修改锁与死锁.md#sql-optimistic_update)。

<a id="sql-row_lock_a"></a>

### `row_lock_a`

<!-- mysql-example: row_lock_a -->
```sql
START TRANSACTION;
SELECT credits FROM accounts WHERE id = 1 FOR UPDATE;
```

<a id="sql-row_lock_b"></a>

### `row_lock_b`

<!-- mysql-example: row_lock_b -->
```sql
SET SESSION innodb_lock_wait_timeout = 5;
START TRANSACTION;
UPDATE accounts SET credits = credits + 10 WHERE id = 1;
```

<a id="sql-gap_lock_a"></a>

### `gap_lock_a`

<!-- mysql-example: gap_lock_a -->
```sql
SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;
START TRANSACTION;
SELECT id FROM lock_numbers WHERE id BETWEEN 10 AND 20 FOR UPDATE;
```

<a id="sql-gap_insert_b"></a>

### `gap_insert_b`

<!-- mysql-example: gap_insert_b -->
```sql
SET SESSION innodb_lock_wait_timeout = 5;
START TRANSACTION;
INSERT INTO lock_numbers(id) VALUES (15);
```

<a id="sql-claim_task"></a>

### `claim_task`

<!-- mysql-example: claim_task -->
```sql
START TRANSACTION;
SELECT id FROM tasks
WHERE status = 'pending'
ORDER BY id LIMIT 1
FOR UPDATE SKIP LOCKED;
-- 应用只在取得id后，按这个id更新状态；未取得时不能继续假装领取成功。
ROLLBACK;
```

### 死锁：与单向等待分开做

结束双方旧事务，重置账户。按顺序操作：

| 步骤 | A | B |
|---|---|---|
| 1 | START TRANSACTION；将账户 1 加 1 | |
| 2 | | START TRANSACTION；将账户 2 加 1 |
| 3 | 将账户 2 加 1，等待 B | |
| 4 | | 将账户 1 加 1，形成等待环 |

每次修改使用 `UPDATE accounts SET credits=credits+1 WHERE id=相应编号;`。检测开启时，一方收到 1213，另一方可继续；不能预先指定受害者。成功方 COMMIT，双方最后都执行 ROLLBACK 清理残留。应用重试应重新开始整笔事务。要原样运行自动化双连接时，使用本目录的维护测试，而不是把两个窗口步骤拼成一个批处理文件。

<a id="lab-12"></a>

## 12｜读取日志配置

[回到正文](../docs/12-日志提交与恢复.md)

只查看当前变量，不修改全局设置。这些值不证明断电恢复已通过；本课程没有在此模拟物理持久化或实际故障恢复。

<a id="sql-durability_settings"></a>

### `durability_settings`

<!-- mysql-example: durability_settings -->
```sql
SELECT @@global.innodb_flush_log_at_trx_commit AS redo_policy,
       @@global.sync_binlog AS binlog_policy,
       @@global.log_bin AS binlog_enabled;
```

<a id="lab-13"></a>

## 13｜相同排序下比较分页

[回到正文](../docs/13-分页与查询成本.md)

重新加载 seed.sql。先 OFFSET，再按最后排序位置查询。团队 10 按创建时间和编号降序为 6、4、3、2、1；每页两条，第二页是 3、2。延迟关联减少取宽列的成本，不消除大 OFFSET 的跳过成本；查询外层仍要明确排序。

**`offset_page`**：[使用正文中的这一份 SQL](../docs/13-分页与查询成本.md#sql-offset_page)。

**`keyset_first`**：[使用正文中的这一份 SQL](../docs/13-分页与查询成本.md#sql-keyset_first)。

**`keyset_second`**：[使用正文中的这一份 SQL](../docs/13-分页与查询成本.md#sql-keyset_second)。

<a id="sql-deferred_page"></a>

### `deferred_page`

<!-- mysql-example: deferred_page -->
```sql
CREATE INDEX idx_tasks_paging ON tasks (tenant_id, created_at, id);
SELECT t.id, t.title, t.created_at
FROM tasks AS t
JOIN (
    SELECT id, created_at
    FROM tasks
    WHERE tenant_id = 10
    ORDER BY created_at DESC, id DESC
    LIMIT 2 OFFSET 2
) AS page ON page.id = t.id
ORDER BY page.created_at DESC, page.id DESC;
```

<a id="sql-paging_cleanup"></a>

### `paging_cleanup`

<!-- mysql-example: paging_cleanup -->
```sql
DROP INDEX idx_tasks_paging ON tasks;
```

<a id="lab-14"></a>

## 14｜索引变成不可见以后

[回到正文](../docs/14-主键索引与表结构演进.md)

重新加载 seed.sql 再执行本块；比较前后计划。不可见索引仍被维护，不应将它当减少写入成本的手段。练习结束重新加载 seed.sql。

<a id="sql-invisible_index"></a>

### `invisible_index`

<!-- mysql-example: invisible_index -->
```sql
CREATE INDEX idx_tasks_priority ON tasks (priority);
ALTER TABLE tasks ALTER INDEX idx_tasks_priority INVISIBLE;
SHOW INDEX FROM tasks;
ALTER TABLE tasks ALTER INDEX idx_tasks_priority VISIBLE;
DROP INDEX idx_tasks_priority ON tasks;
```

<a id="lab-15"></a>

## 15｜多值 INSERT 与事务边界

[回到正文](../docs/15-批量写入与写入成本.md)

先建立独立导入表，再执行一次多值 INSERT 并提交。实验表仍保留进度字段，用来观察“任务进度”是应用层记录，不是 COMMIT 自动生成的能力；故障重试必须核对唯一键和原提交结果，不能无条件重复执行相同插入。最后清理本组表。

<a id="sql-batch_setup"></a>

### `batch_setup`

<!-- mysql-example: batch_setup -->
```sql
CREATE TABLE import_items (
    source_key VARCHAR(40) PRIMARY KEY,
    title VARCHAR(100) NOT NULL
) ENGINE=InnoDB;
CREATE TABLE import_progress (
    job_id INT PRIMARY KEY,
    last_batch INT NOT NULL
) ENGINE=InnoDB;
INSERT INTO import_progress VALUES (1, 0);
```

**`batch_commit`**：[使用正文中的这一份 SQL](../docs/15-批量写入与写入成本.md#sql-batch_commit)。

<a id="sql-batch_cleanup"></a>

### `batch_cleanup`

<!-- mysql-example: batch_cleanup -->
```sql
DROP TABLE import_items;
DROP TABLE import_progress;
```

<a id="lab-19"></a>

## 19｜把关系约束落到应用表

[回到正文](../docs/19-AI应用数据建模.md)

本组只演示会话、消息、运行的本地关系与约束，不是整套 Agent 的生产数据库。先看创建的身份、团队关联和唯一性，再清理。外部工具和检索节点的行为不由这些建表语句保证。

<a id="sql-ai_model_setup"></a>

### `ai_model_setup`

<!-- mysql-example: ai_model_setup -->
```sql
CREATE TABLE lab_conversations (
    id BIGINT PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    title VARCHAR(100) NOT NULL,
    UNIQUE KEY uk_tenant_conversation (tenant_id, id)
) ENGINE=InnoDB;
CREATE TABLE lab_messages (
    id BIGINT PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    conversation_id BIGINT NOT NULL,
    role VARCHAR(16) NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME NOT NULL,
    CONSTRAINT fk_message_conversation
      FOREIGN KEY (tenant_id, conversation_id)
      REFERENCES lab_conversations (tenant_id, id),
    INDEX idx_message_history (tenant_id, conversation_id, created_at, id)
) ENGINE=InnoDB;
INSERT INTO lab_conversations VALUES (1, 10, '数据库练习');
INSERT INTO lab_messages VALUES
  (1, 10, 1, 'user', '什么是事务？', '2026-09-01 09:00:00'),
  (2, 10, 1, 'assistant', '先明确需要一起成立的修改。', '2026-09-01 09:00:01');
SELECT id, role FROM lab_messages
WHERE tenant_id = 10 AND conversation_id = 1
ORDER BY created_at, id;
```

<a id="sql-ai_model_cleanup"></a>

### `ai_model_cleanup`

<!-- mysql-example: ai_model_cleanup -->
```sql
DROP TABLE lab_messages;
DROP TABLE lab_conversations;
```
