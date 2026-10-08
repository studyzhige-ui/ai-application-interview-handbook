"""Offline transport fixtures: pagination, every title, detail and byte retention."""
from __future__ import annotations
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
from jd.collection import collect_python, collect_manual, selected_sources
from jd.limits import Budget
from jd.adapters.http import requests
from jd.evidence import preserve_observation


class Response:
    def __init__(self, payload, url, status=200):
        # Intentionally retain whitespace and HTML that extraction may flatten.
        self.content = (json.dumps(payload, ensure_ascii=False, indent=1) + "\n \n").encode()
        self.status_code = status
        self.url = url
        self.ok = status < 400
        self.headers = {}
        self.text = self.content.decode()

    def json(self):
        return json.loads(self.content)

    def raise_for_status(self):
        if not self.ok:
            raise RuntimeError(f"HTTP {self.status_code}")


class TencentFixture:
    def __init__(self, fail_detail=False, total=100):
        self.calls = []
        self.responses = []
        self.fail_detail = fail_detail
        self.total = total

    def post(self, url, **kwargs):
        self.calls.append(("list", kwargs["json"]["pageIndex"]))
        page = kwargs["json"]["pageIndex"]
        titles = {1: ["算法研究员", "市场运营实习生"], 2: ["普通岗位 - 北京", "普通岗位 - 上海"]}[page]
        response = Response({"data": {"positionList": [{"postId": f"{page}-{i}", "positionTitle": title, "recruitLabelName": "实习"} for i, title in enumerate(titles)], "count": self.total}}, url)
        self.responses.append(response)
        return response

    def get(self, url, **kwargs):
        job_id = kwargs["params"]["postId"]
        self.calls.append(("detail", job_id))
        if self.fail_detail:
            raise RuntimeError("fixture detail unavailable")
        response = Response({"data": {"desc": " <p>全部原始职责。</p>\nSecond line", "request": " 不含 Agent 的要求 "}}, url)
        self.responses.append(response)
        return response


def source():
    return {"source_id": "fixture", "company": "Fixture", "mode": "tencent_campus_api", "portal": "https://join.qq.com/post.html"}


class CollectionTests(unittest.TestCase):
    def test_pagination_details_and_unfiltered_titles(self):
        backend = TencentFixture()
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "run"
            result = collect_python(source(), Budget(5, 20, 30), output, backend)
            self.assertEqual([call for call in backend.calls if call[0] == "list"], [("list", 1), ("list", 2)])
            self.assertEqual(len([call for call in backend.calls if call[0] == "detail"]), 4)
            self.assertEqual([job["title"] for job in result["jobs"]], ["算法研究员", "市场运营实习生", "普通岗位 - 北京", "普通岗位 - 上海"])
            self.assertEqual(result["jobs"][0]["description"], "<p>全部原始职责。</p>\nSecond line")
            for entry, response in zip(result["requests"], backend.responses):
                self.assertEqual((output / "raw" / entry["raw_file"]).read_bytes(), response.content)
                self.assertEqual(entry["sha256"], hashlib.sha256(response.content).hexdigest())
            self.assertFalse(result["model_reviewed"])
            self.assertFalse(result["complete"])
            self.assertEqual(len((output / "jobs.jsonl").read_text().splitlines()), 4)

    def test_mihoyo_unrelated_title_still_fetches_full_detail(self):
        class MihoyoFixture:
            def __init__(self): self.calls = []
            def post(self, url, **kwargs):
                self.calls.append(url)
                data = {"list": [{"id": "ordinary", "title": "普通销售实习岗"}], "total": 1} if url.endswith("/list") else {"description": "<p>完整职责</p>", "requirement": "全部要求"}
                return Response({"data": data}, url)
        backend = MihoyoFixture()
        with tempfile.TemporaryDirectory() as directory:
            result = collect_python({**source(), "mode": "mihoyo_campus_api"}, Budget(2, 10, 30), Path(directory) / "run", backend)
            self.assertEqual([url.rsplit("/", 1)[-1] for url in backend.calls], ["list", "info"])
            self.assertEqual(result["jobs"][0]["title"], "普通销售实习岗")
            self.assertEqual(result["jobs"][0]["description"], "完整职责")
            self.assertEqual(result["jobs"][0]["requirements"], "全部要求")

    def test_max_pages_stops_before_second_list_and_keeps_details(self):
        backend = TencentFixture()
        with tempfile.TemporaryDirectory() as directory:
            result = collect_python(source(), Budget(1, 20, 30), Path(directory) / "run", backend)
            self.assertEqual(result["status"], "PARTIAL")
            self.assertIn("max_pages", result["limits_hit"])
            self.assertEqual(len(result["jobs"]), 2)
            self.assertNotIn(("list", 2), backend.calls)

    def test_max_jobs_stops_before_extra_details(self):
        backend = TencentFixture()
        with tempfile.TemporaryDirectory() as directory:
            result = collect_python(source(), Budget(10, 1, 30), Path(directory) / "run", backend)
            self.assertEqual(backend.calls, [("list", 1), ("detail", "1-0")])
            self.assertEqual(len(result["jobs"]), 1)
            self.assertIn("max_jobs", result["limits_hit"])

    def test_failed_details_keep_list_records_and_failure_evidence(self):
        backend = TencentFixture(fail_detail=True, total=2)
        with tempfile.TemporaryDirectory() as directory:
            result = collect_python(source(), Budget(2, 10, 30), Path(directory) / "run", backend)
            self.assertEqual(result["status"], "PARTIAL")
            self.assertEqual(len(result["jobs"]), 2)
            self.assertEqual(len(result["failures"]), 2)
            self.assertTrue(result["requests"][1]["error"])

    def test_timeout_has_no_request_after_deadline(self):
        backend = TencentFixture()
        budget = Budget(1, 1, 1)
        budget.started -= 10
        with tempfile.TemporaryDirectory() as directory:
            result = collect_python(source(), budget, Path(directory) / "run", backend)
            self.assertEqual(result["status"], "PARTIAL")
            self.assertIn("timeout", result["limits_hit"])
            self.assertEqual(backend.calls, [])

    def test_transport_requires_explicit_scope(self):
        with self.assertRaisesRegex(RuntimeError, "disabled"):
            requests.get("https://example.invalid")

    def test_unknown_source_and_missing_enable_fail_before_writing(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "absent"
            with self.assertRaisesRegex(ValueError, "Unknown"):
                collect_manual(["does-not-exist"], enabled=True, max_pages=1, max_jobs=1, timeout_seconds=1, output=destination)
            with self.assertRaisesRegex(ValueError, "disabled"):
                collect_manual(["official-001"], enabled=False, max_pages=1, max_jobs=1, timeout_seconds=1, output=destination)
            self.assertFalse(destination.exists())

    def test_invalid_bounds(self):
        for pages, jobs, timeout in [(0, 1, 1), (1, 0, 1), (1, 1, 0), (1, 1, float("nan"))]:
            with self.assertRaises(ValueError):
                Budget(pages, jobs, timeout)

    def test_no_network_on_import_default_and_incomplete_cli(self):
        script = """
import socket, sys, runpy
sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1])
def forbidden(*args, **kwargs): raise AssertionError('Unexpected network')
socket.socket = forbidden
import jd.collection, jd.adapters.official, jd.adapters.http
namespace = runpy.run_path(sys.argv[1] + '/jd.py')
assert namespace['main']([]) == 0
try: namespace['main'](['collect', '--enable-code-collection'])
except SystemExit as exc: assert exc.code == 2
else: raise AssertionError('Missing bounds accepted')
"""
        result = subprocess.run([sys.executable, "-B", "-c", script, str(SCRIPTS)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_hard_timeout_keeps_partial_capture(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "run"
            def killed(command, **kwargs):
                self.assertEqual(kwargs["timeout"], 1)
                child = destination / "official-004"
                child.mkdir()
                (child / "jobs.jsonl").write_bytes(b'{"title":"partial"}\n')
                raise subprocess.TimeoutExpired(command, kwargs["timeout"])
            with patch("jd.collection.subprocess.run", side_effect=killed):
                result = collect_manual(["official-004"], enabled=True, max_pages=1, max_jobs=1, timeout_seconds=1, output=destination)
            self.assertEqual(result, 1)
            child = destination / "official-004"
            self.assertEqual((child / "jobs.jsonl").read_bytes(), b'{"title":"partial"}\n')
            interruption = json.loads((child / "interruption.json").read_text())
            self.assertEqual(interruption["status"], "TIMEOUT")
            self.assertEqual(interruption["preserved_partial_files"], ["jobs.jsonl"])

    def test_missing_hikvision_batch_fails_without_discovery(self):
        backend = TencentFixture()
        src = {**source(), "mode": "hikvision_campus_api"}
        with tempfile.TemporaryDirectory() as directory:
            result = collect_python(src, Budget(1, 1, 30), Path(directory) / "run", backend)
            self.assertEqual(result["status"], "BLOCKED")
            self.assertIn("explicitly registered", result["error"])
            self.assertEqual(backend.calls, [])

    def test_exact_byte_preservation(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "original.json"
            source.write_bytes(b'{"preserve": "  spaces  "}\r\n')
            result = preserve_observation(source, Path(directory) / "observations")
            self.assertEqual(source.read_bytes(), result.read_bytes())
            self.assertEqual(result, preserve_observation(source, Path(directory) / "observations"))

    def test_readonly_contracts(self):
        from jd.contracts import main
        with patch("socket.socket", side_effect=AssertionError("Unexpected network")):
            self.assertEqual(main(), 0)


if __name__ == "__main__":
    unittest.main()
