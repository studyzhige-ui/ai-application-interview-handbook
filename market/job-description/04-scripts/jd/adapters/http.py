"""Dormant HTTP transport: explicit collection scope, bounded time, raw capture."""
from __future__ import annotations
from contextlib import contextmanager
from contextvars import ContextVar
import hashlib
import json
from urllib.parse import quote
from ..limits import current_budget

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36"
HEADERS = {"User-Agent": UA, "Accept": "application/json, text/plain, */*", "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"}
TIMEOUT = 12
_CAPTURE = ContextVar("jd_raw_capture", default=None)
_BACKEND = ContextVar("jd_http_backend", default=None)


def _backend():
    backend = _BACKEND.get()
    if backend is None:
        try:
            import requests as backend
        except ModuleNotFoundError as exc:
            raise RuntimeError("Manual collection requires requirements.txt") from exc
    return backend


@contextmanager
def capture_scope(directory, backend=None):
    """Raw files are new observations, never rewrites of saved snapshots."""
    directory.mkdir(parents=True, exist_ok=False)
    capture = {"directory": directory, "requests": []}
    token = _CAPTURE.set(capture)
    backend_token = _BACKEND.set(backend)
    try:
        yield capture["requests"]
    finally:
        _CAPTURE.reset(token)
        _BACKEND.reset(backend_token)


def _request(target, method, url, **kwargs):
    budget = current_budget()
    capture = _CAPTURE.get()
    if capture is None:
        raise RuntimeError("A new raw-observation directory is required before network access")
    # Both connection and read timeouts are bounded by the remaining run budget.
    timeout = min(float(kwargs.get("timeout", TIMEOUT)), budget.remaining())
    kwargs["timeout"] = timeout
    # Repeated retry requests cannot bypass the global wall-clock deadline.
    entry = {"method": method.upper(), "url": url, "params": kwargs.get("params"),
             "json": kwargs.get("json"), "form": kwargs.get("data")}
    capture["requests"].append(entry)
    def event(kind):
        with (capture["directory"] / "requests.jsonl").open("a", encoding="utf-8") as stream:
            stream.write(json.dumps({"event": kind, **entry}, ensure_ascii=False) + "\n")
    event("request")
    try:
        response = getattr(target, method)(url, **kwargs)
        raw = response.content
        filename = f"{len(capture['requests']):05d}.body"
        with (capture["directory"] / filename).open("xb") as stream:
            stream.write(raw)
        entry.update({"status": response.status_code, "response_url": response.url,
                      "raw_file": filename, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
        event("response")
        if response.status_code >= 400:
            budget.failures.append({"url": url, "status": response.status_code})
        budget.remaining()
        return response
    except Exception as exc:
        entry["error"] = f"{type(exc).__name__}: {exc}"
        event("failure")
        budget.failures.append({"url": url, "error": entry["error"]})
        raise


class _Session:
    def __init__(self):
        current_budget().remaining()
        self.session = _backend().Session()
        self.headers = self.session.headers
        self.cookies = self.session.cookies

    def get(self, url, **kwargs):
        return _request(self.session, "get", url, **kwargs)

    def post(self, url, **kwargs):
        return _request(self.session, "post", url, **kwargs)


class _Transport:
    Session = _Session
    class utils:
        quote = staticmethod(quote)

    @staticmethod
    def get(url, **kwargs):
        current_budget().remaining()
        return _request(_backend(), "get", url, **kwargs)

    @staticmethod
    def post(url, **kwargs):
        current_budget().remaining()
        return _request(_backend(), "post", url, **kwargs)


requests = _Transport()


def get_json(url, *, params=None, headers=None):
    response = requests.get(url, params=params, headers={**HEADERS, **(headers or {})}, timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()


def post_json(url, *, payload=None, headers=None):
    response = requests.post(url, json=payload or {}, headers={**HEADERS, "Content-Type": "application/json", **(headers or {})}, timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()


def post_form(url, *, data=None, headers=None):
    response = requests.post(url, data=data or {}, headers={**HEADERS, "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8", **(headers or {})}, timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()
