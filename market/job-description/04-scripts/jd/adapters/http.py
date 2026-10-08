"""Shared HTTP transport. Offline contracts never require requests or make a request."""
from __future__ import annotations
import re
from typing import Any
from urllib.parse import urljoin
try:
    import requests
except ModuleNotFoundError:
    class _MissingRequests:
        def __getattr__(self, name):
            raise RuntimeError("Live collection requires the requests dependency; install requirements.txt")
    requests = _MissingRequests()
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36"
HEADERS = {
    "User-Agent": UA,
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}
TIMEOUT = 12

def discover_api_candidates(portal: str) -> list[str]:
    """Best-effort discovery of current API paths from an official JS recruitment portal.

    This is diagnostic only. A discovered endpoint is never treated as a JD until
    a company adapter explicitly understands its request/response contract.
    """
    base = portal.split("#", 1)[0]
    try:
        r = requests.get(base, headers=HEADERS, timeout=TIMEOUT)
        r.raise_for_status()
    except Exception:
        return []

    bodies = [r.text]
    scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', r.text, flags=re.I)
    for src in scripts[:16]:
        try:
            js = requests.get(urljoin(base, src), headers=HEADERS, timeout=TIMEOUT)
            if js.ok:
                bodies.append(js.text[:5_000_000])
        except Exception:
            continue

    candidates: set[str] = set()
    patterns = [
        r'https?://[^"\'\s]{1,240}',
        r'["\']([^"\']{0,80}(?:/api/|api/|/recruit/)[^"\']{0,180})["\']',
    ]
    for body in bodies:
        for pattern in patterns:
            for m in re.finditer(pattern, body, flags=re.I):
                raw = m.group(1) if m.lastindex else m.group(0)
                raw = raw.replace("\\/", "/")
                low = raw.lower()
                if any(k in low for k in ("job", "position", "recruit", "opportun")):
                    candidates.add(raw[:260])
    return sorted(candidates)[:30]


def get_json(url: str, *, params=None, headers=None) -> Any:
    h = dict(HEADERS)
    if headers:
        h.update(headers)
    r = requests.get(url, params=params, headers=h, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()


def post_json(url: str, *, payload=None, headers=None) -> Any:
    h = dict(HEADERS)
    h["Content-Type"] = "application/json"
    if headers:
        h.update(headers)
    r = requests.post(url, json=payload or {}, headers=h, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()


def post_form(url: str, *, data=None, headers=None) -> Any:
    h = dict(HEADERS)
    h["Content-Type"] = "application/x-www-form-urlencoded;charset=UTF-8"
    if headers:
        h.update(headers)
    r = requests.post(url, data=data or {}, headers=h, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()
