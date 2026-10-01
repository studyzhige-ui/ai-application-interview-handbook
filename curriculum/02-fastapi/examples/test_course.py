"""Run examples extracted from the teaching source, not independently rewritten fixtures."""
from pathlib import Path
from types import ModuleType
from importlib.metadata import version
import ast
import asyncio
import contextlib
import hashlib
import itertools
import json
import re
import socket
import subprocess
import sys
import threading
import time

import httpx
import pytest
from fastapi.testclient import TestClient

DOCS = Path(__file__).resolve().parents[1] / "docs"
EXAMPLES = {}
for path in sorted(DOCS.glob("*.md")):
    for code in re.findall(r"```python\n(.*?)\n```", path.read_text(encoding="utf-8"), re.S):
        marker = re.match(r"# example: ([a-z_]+)\n", code)
        if marker:
            name = marker.group(1)
            if name in EXAMPLES:
                raise RuntimeError(f"Duplicate example: {name}")
            EXAMPLES[name] = (code, str(path))

COUNTER = itertools.count()

def load(name):
    code, source = EXAMPLES[name]
    module_name = f"_course_{name}_{next(COUNTER)}"
    module = ModuleType(module_name)
    module.__file__ = source
    sys.modules[module_name] = module
    try:
        exec(compile(code, source + "#" + name, "exec"), module.__dict__)
    except BaseException:
        sys.modules.pop(module_name, None)
        raise
    return module


def require_target():
    if version("fastapi") != "0.141.1":
        pytest.skip("Requires target FastAPI 0.141.1; NOT verified in compatibility runtime")


@pytest.mark.parametrize("name", sorted(EXAMPLES))
def test_marked_example_syntax(name):
    ast.parse(EXAMPLES[name][0])


def test_chapter_learning_sections():
    pages = sorted(DOCS.glob("*.md"))
    assert len(pages) == 16
    for page in pages:
        text = page.read_text(encoding="utf-8")
        for heading in ["## 本章小结", "## 🎯 面试怎么回答", "## ⚠️ 易错点", "## 本章自测", "## 知识回看与权威资料"]:
            assert heading in text, (page, heading)
        assert text.count("<details>") == text.count("</details>")
        assert not re.search(r"<details[^>]*\bopen\b", text)
        assert len(text.split("## 1.")[0]) > 140


def test_first_app_and_openapi():
    module = load("hello_app")
    with TestClient(module.app) as client:
        assert client.get("/hello").json() == {"message": "你好，接口已经工作了"}
        assert client.get("/").status_code == 404
        assert "/hello" in client.get("/openapi.json").json()["paths"]
        assert client.get("/docs").status_code == 200


def test_hello_exercise_fails_then_passes():
    module = load("hello_app")
    with TestClient(module.app) as client:
        assert client.get("/health").status_code == 404
    @module.app.get("/health")
    def health():
        return {"ok": True}
    old = sys.modules.get("main")
    sys.modules["main"] = module
    try:
        test = load("hello_test")
        for name, fn in vars(test).items():
            if name.startswith("test_"):
                fn()
    finally:
        if old is None:
            sys.modules.pop("main", None)
        else:
            sys.modules["main"] = old


@pytest.mark.parametrize("path,status,count", [
    ("/notes",200,2),("/notes?limit=1",200,1),("/notes?limit=3",200,3),
    ("/notes?limit=0",422,None),("/notes?limit=4",422,None),("/notes?limit=x",422,None),
    ("/notes/99",404,None),("/notes/no",422,None),
])
def test_query_contract(path,status,count):
    module = load("notes_query")
    with TestClient(module.app) as client:
        response=client.get(path)
        assert response.status_code == status
        if count is not None:
            assert len(response.json()) == count


def test_five_input_locations():
    module=load("notes_input")
    with TestClient(module.app, cookies={"theme":"dark"}) as client:
        r=client.post("/notes/7/preview?uppercase=true",json={"text":"hello"},headers={"X-Request-ID":"req-7"})
    assert r.status_code==200
    data=r.json()
    assert 7 in data.values() and "HELLO" in data.values() and "req-7" in data.values() and "dark" in data.values()


def test_router_is_registered():
    router=load("notes_router")
    previous=sys.modules.get("notes_api")
    sys.modules["notes_api"]=router
    try:
        module=load("router_main")
        with TestClient(module.app) as client:
            assert client.get("/notes/count").json()=={"count":3}
    finally:
        if previous is None: sys.modules.pop("notes_api",None)
        else: sys.modules["notes_api"]=previous


@pytest.mark.parametrize("body,status", [
    ({"text":" hi ","repeat":2},200),({"text":"hi","repeat":"2"},200),
    ({"text":"hi","repeat":0},422),({"text":"hi","repeat":4},422),
    ({"text":"   "},422),({},422),({"text":"hi","repeet":2},422),
])
def test_input_and_output_contract(body,status):
    m=load("contract_app")
    with TestClient(m.app) as c:
        r=c.post("/preview",json=body)
    assert r.status_code==status
    if status==200:
        assert set(r.json())=={"result"}
        assert r.json()["result"]=="hihi"


def test_strict_json_content_type_target_only():
    require_target()
    m=load("contract_app")
    with TestClient(m.app) as c:
        assert c.post("/preview",content='{"text":"hi"}').status_code==422
        assert c.post("/preview",json={"text":"hi"}).status_code==200


def test_pydantic_roundtrip(capsys):
    load("pydantic_roundtrip")
    assert "2" in capsys.readouterr().out


def test_domain_error_mapping():
    m=load("domain_error_app")
    with TestClient(m.app) as c:
        assert c.get("/notes/1").status_code==200
        r=c.get("/notes/2")
        assert r.status_code==404
        assert r.json()["error"]["code"]=="NOTE_NOT_FOUND"


def test_dependency_reuse_and_input():
    m=load("dependency_app")
    with TestClient(m.app) as c:
        for path in ["/notes","/tasks"]:
            assert c.get(path+"?limit=3").json()["limit"]==3
            assert c.get(path+"?limit=0").status_code==422


def test_dependency_cache_is_request_local():
    m=load("dependency_cache")
    with TestClient(m.app) as c:
        for _ in range(2):
            assert list(c.get("/cached").json().values())==[1,1]
        assert list(c.get("/uncached").json().values())==[1,2]


def test_middleware_order():
    m=load("middleware_order")
    with TestClient(m.app) as c:
        r=c.get("/order")
    assert r.headers["x-order"]=="B.before,A.before,handler,A.after,B.after"


def test_resource_scope_and_close():
    m=load("resource_app")
    with TestClient(m.app) as c:
        assert c.get("/use").json()["open_during_handler"] is True
        assert m.app.state.events==["acquire","handler","release"]
    m=load("resource_scope")
    with TestClient(m.app) as c:
        assert "True" in c.get("/request-scope").text
        assert "False" in c.get("/function-scope").text


def test_resource_cleanup_when_handler_raises():
    m=load("resource_app")
    from fastapi import Depends
    @m.app.get("/fail")
    async def fail(resource=Depends(m.get_resource)):
        raise RuntimeError("controlled failure")
    with TestClient(m.app,raise_server_exceptions=False) as c:
        assert c.get("/fail").status_code==500
    assert m.app.state.events==["acquire","release"]


def test_lifespan_resource_closed():
    m=load("lifespan_app")
    with TestClient(m.app) as c:
        assert c.get("/catalog").status_code==200
        catalog=m.app.state.catalog
        assert catalog.closed is False
    assert catalog.closed is True


def test_execution_thread_boundary():
    m=load("execution_app")
    with TestClient(m.app) as c:
        r=c.get("/offload")
        assert r.status_code==200
        assert r.json()["loop_thread"] != r.json()["worker_thread"]
        assert c.get("/sync-wait").status_code==200
        assert c.get("/async-wait").status_code==200


def test_batch_capacity():
    m=load("bounded_app")
    with TestClient(m.app) as c:
        r=c.get("/batch?size=8")
        assert r.status_code==200
        data=r.json()
        assert data["peak"]<=2
        assert data["results"]==[i*2 for i in range(8)]
        assert c.get("/batch?size=9").status_code==422
        assert m.app.state.active==0


def test_raw_stream_content():
    m=load("raw_stream_app")
    with TestClient(m.app) as c:
        r=c.get("/stream")
    assert r.text.splitlines()==["开始整理","找到两条材料","整理完成"]


@pytest.mark.parametrize("fail,expected",[(False,["start","delta","end"]),(True,["start","delta","error","end"])])
def test_native_sse_contract(fail,expected):
    require_target()
    m=load("native_sse_app")
    with TestClient(m.app) as c:
        r=c.get("/events",params={"fail":str(fail).lower()})
    assert r.headers["content-type"].startswith("text/event-stream")
    events=re.findall(r"^event: (.+)$",r.text.replace("\r\n","\n"),re.M)
    assert events==expected
    assert ("failed" if fail else "succeeded") in r.text


def test_native_jsonl_contract():
    require_target()
    m=load("native_jsonl_app")
    with TestClient(m.app) as c:
        r=c.get("/notes/stream")
    assert r.headers["content-type"].startswith("application/jsonl")
    assert [json.loads(line) for line in r.text.splitlines() if line]==[
        {"id":1,"text":"第一条"},{"id":2,"text":"第二条"}]


def test_websocket_echo_and_cleanup():
    m=load("websocket_app")
    with TestClient(m.app) as c:
        with c.websocket_connect("/ws") as ws:
            ws.send_text("你好")
            assert ws.receive_text()=="收到：你好"
            ws.send_text("stop")
            assert ws.receive_text()=="已结束"
    assert m.app.state.connections==0


def test_websocket_invalid_then_valid():
    m=load("websocket_protocol_app")
    with TestClient(m.app) as c:
        with c.websocket_connect("/ws") as ws:
            for bad in ["not-json",'{"type":"delete","request_id":"m1"}',"{}"]:
                ws.send_text(bad)
                assert ws.receive_json()["code"]=="INVALID_MESSAGE"
            ws.send_json({"type":"ping","request_id":"m1"})
            assert ws.receive_json()=={"type":"pong","request_id":"m1"}


@pytest.mark.parametrize("token,note,status",[(None,1,401),("wrong",1,401),("demo-alice",1,200),("demo-alice",2,404),("demo-bob",2,200)])
def test_tenant_access(token,note,status):
    m=load("auth_app")
    headers={"X-Tenant-ID":"team-b"}
    if token: headers["Authorization"]="Bearer "+token
    with TestClient(m.app) as c:
        r=c.get(f"/notes/{note}",headers=headers)
    assert r.status_code==status
    if status==200: assert "token" not in r.text


def test_cors_preflight():
    m=load("cors_app")
    with TestClient(m.app) as c:
        r=c.options("/hello",headers={"Origin":"http://localhost:5173","Access-Control-Request-Method":"GET","Access-Control-Request-Headers":"Authorization"})
        assert r.status_code==200
        assert r.headers["access-control-allow-origin"]=="http://localhost:5173"
        assert c.options("/hello",headers={"Origin":"https://untrusted.example","Access-Control-Request-Method":"GET"}).status_code==400
        assert c.get("/hello").status_code==200  # CORS did not add authentication.


@pytest.mark.parametrize("text,status",[("你好",200),("timeout",504),("busy",502),("broken",502),("",422)])
def test_external_adapter(text,status):
    m=load("external_app")
    with TestClient(m.app) as c:
        client=m.app.state.provider
        r=c.post("/ask",json={"text":text})
        assert r.status_code==status
    assert client.is_closed


@pytest.mark.parametrize("content,status",[(b"abc",200),(b"",200),(b"a"*(1024*1024+1),413)])
def test_upload_result(content,status):
    m=load("upload_app")
    with TestClient(m.app) as c:
        r=c.post("/files/check",files={"file":("sample.txt",content,"text/plain")})
    assert r.status_code==status
    if status==200:
        assert r.json()=={"bytes":len(content),"sha256":hashlib.sha256(content).hexdigest()}


def test_background_order():
    m=load("background_app")
    with TestClient(m.app) as c:
        assert c.post("/seen").json()=={"accepted":True}
    assert m.app.state.events==["handler","background:note"]


def test_timeout_cleanup():
    m=load("timeout_app")
    with TestClient(m.app) as c:
        assert c.get("/slow").status_code==504
    assert m.app.state.events==["started","cleaned"]


def test_cancel_and_taskgroup_semantics():
    assert not issubclass(asyncio.CancelledError, Exception)
    assert asyncio.run(load("cancellation_demo").main())==["cancelled","cleaned","observed"]
    assert asyncio.run(load("taskgroup_demo").main())==["slow cleaned","failure observed"]


def test_documented_pytest_files(tmp_path):
    # This runs the actual tests printed in chapter13, with their documented filenames.
    for target,name in [("main.py","tested_app"),("test_main.py","basic_api_tests"),("test_override.py","override_tests"),
                        ("websocket_app.py","websocket_app"),("test_ws.py","websocket_tests")]:
        (tmp_path/target).write_text(EXAMPLES[name][0], encoding="utf-8")
    r=subprocess.run([sys.executable,"-m","pytest","-q"],cwd=tmp_path,capture_output=True,text=True,timeout=30)
    assert r.returncode==0, r.stdout+r.stderr
    assert "6 passed" in r.stdout


def test_full_body_measurement():
    m=load("observed_app")
    with TestClient(m.app) as c:
        assert c.get("/stream").text=="first\nsecond\n"
    item=m.records[-1]
    assert item["status"]==200
    assert item["body_end_s"] - item["headers_s"]>=0.02
    assert item["app_end_s"]>=item["body_end_s"]


def test_health_lifecycle():
    m=load("health_app")
    with TestClient(m.app) as c:
        assert c.get("/live").json()=={"alive":True}
        assert c.get("/ready").json()=={"ready":True}
        m.app.state.ready=False
        assert c.get("/ready").status_code==503
    assert m.app.state.ready is False and not m.app.state.catalog


def test_integrated_contract():
    m=load("integrated_app")
    a={"Authorization":"Bearer demo-alice"}; b={"Authorization":"Bearer demo-bob"}
    with TestClient(m.app) as c:
        assert c.post("/tasks",json={"text":"任务"}).status_code==401
        assert c.post("/tasks",json={"text":" "},headers=a).status_code==422
        r=c.post("/ask",json={"text":"问题"},headers=a)
        assert r.status_code==200 and len(r.json()["citations"])==1
        one=c.post("/tasks",json={"text":"任务"},headers=a)
        assert one.status_code==202
        task_id=one.json()["task_id"]
        assert c.get(f"/tasks/{task_id}",headers=a).json()["status"]=="queued"
        assert c.get(f"/tasks/{task_id}",headers=b).status_code==404
        for _ in range(2):
            assert c.post(f"/tasks/{task_id}/cancel",headers=a).json()=={"task_id":task_id,"status":"cancelled"}
        two=c.post("/tasks",json={"text":"任务"},headers=a)
        assert two.json()["task_id"] != task_id  # Explicitly not idempotent creation.


def test_real_local_socket_incremental_stream(tmp_path):
    # Actual Uvicorn socket, not TestClient. Still NOT a production proxy test.
    (tmp_path/"main.py").write_text(EXAMPLES["raw_stream_app"][0], encoding="utf-8")
    with socket.socket() as s:
        s.bind(("127.0.0.1",0)); port=s.getsockname()[1]
    with (tmp_path/"server.log").open("w+", encoding="utf-8") as log:
        process=subprocess.Popen([sys.executable,"-m","uvicorn","main:app","--host","127.0.0.1","--port",str(port),"--log-level","warning"],cwd=tmp_path,stdout=log,stderr=log)
        try:
            base=f"http://127.0.0.1:{port}"
            with httpx.Client(timeout=5,trust_env=False) as client:
                deadline=time.monotonic()+10
                while True:
                    if process.poll() is not None:
                        log.seek(0); pytest.fail(log.read())
                    try:
                        client.get(base+"/openapi.json"); break
                    except httpx.ConnectError:
                        if time.monotonic()>deadline: raise
                        time.sleep(.05)
                arrivals=[]; texts=[]
                with client.stream("GET",base+"/stream") as r:
                    for line in r.iter_lines():
                        arrivals.append(time.monotonic()); texts.append(line)
                assert texts==["开始整理","找到两条材料","整理完成"]
                assert arrivals[-1]-arrivals[0]>.15
        finally:
            process.terminate()
            try: process.wait(timeout=5)
            except subprocess.TimeoutExpired: process.kill();process.wait()


def test_async_transport_does_not_start_lifespan():
    m=load("health_app")
    async def check():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=m.app),base_url="http://test") as client:
            return await client.get("/ready")
    assert asyncio.run(check()).status_code==503


def test_response_contract_failure_is_server_error():
    m=load("contract_app")
    @m.app.get("/invalid-output",response_model=m.PreviewOutput)
    def invalid_output():
        return {"unrelated":True}
    with TestClient(m.app,raise_server_exceptions=False) as c:
        assert c.get("/invalid-output").status_code==500


def test_bad_body_does_not_call_external_adapter():
    m=load("external_app")
    original=m.fake_provider
    calls=[]
    def counted(request):
        calls.append(str(request.url))
        return original(request)
    m.fake_provider=counted
    with TestClient(m.app) as c:
        assert c.post("/ask",json={"text":""}).status_code==422
    assert calls==[]


@pytest.mark.parametrize("payload,status,result", [
    ({"text": "hello"}, 200, "HELLO"),
    ({}, 422, None),
    ({"text": ["hello"]}, 422, None),
])
def test_simple_body_before_combined_parameters(payload, status, result):
    module = load("note_body_app")
    with TestClient(module.app) as client:
        response = client.post("/notes/preview", json=payload)
    assert response.status_code == status
    if status == 200:
        assert response.json() == {"text": result}


@pytest.mark.parametrize("start,end,allowed", [
    (2, 5, True), (2, 2, True), (5, 2, False), (0, 5, False), ("x", 5, False),
])
def test_cross_field_page_range(start, end, allowed):
    from pydantic import ValidationError
    model = load("page_range_model").PageRange
    if allowed:
        result = model(start_page=start, end_page=end)
        assert (result.start_page, result.end_page) == (start, end)
    else:
        with pytest.raises(ValidationError):
            model(start_page=start, end_page=end)


def test_cross_field_model_at_http_boundary():
    from fastapi import FastAPI
    model = load("page_range_model").PageRange
    app = FastAPI()
    calls = []

    @app.post("/pages")
    def pages(body: model):
        calls.append((body.start_page, body.end_page))
        return {"start": body.start_page, "end": body.end_page}

    with TestClient(app) as client:
        assert client.post("/pages", json={"start_page": 5, "end_page": 2}).status_code == 422
        assert calls == []  # Rejection occurs before the handler's normal work.
        reply = client.post("/pages", json={"start_page": 2, "end_page": 5})
        assert reply.status_code == 200 and reply.json() == {"start": 2, "end": 5}
    assert calls == [(2, 5)]


def test_required_nullable_four_combinations():
    from pydantic import create_model, ValidationError
    # These four declarations are the chapter 03 table's four independent contracts.
    cases = [(str, ..., False, False), (str | None, ..., False, True),
             (str, "匿名", True, False), (str | None, None, True, True)]
    for field_type, default, allow_missing, allow_null in cases:
        model = create_model("Presence", name=(field_type, default))
        for body, allowed in [({}, allow_missing), ({"name": None}, allow_null),
                              ({"name": "A"}, True)]:
            if allowed:
                model.model_validate(body)
            else:
                with pytest.raises(ValidationError):
                    model.model_validate(body)


def test_nested_alias_and_independent_default_lists():
    from pydantic import ValidationError
    m = load("nested_contract")
    one = m.Notebook.model_validate({"ownerId": "u1"})
    two = m.Notebook.model_validate({"ownerId": "u2"})
    one.notes.append(m.Note(text="A"))
    assert two.notes == []
    assert one.model_dump(by_alias=True) == {"ownerId": "u1", "notes": [{"text": "A"}]}
    with pytest.raises(ValidationError) as error:
        m.Notebook.model_validate({"ownerId": "u1", "notes": [{}]})
    assert error.value.errors()[0]["loc"] == ("notes", 0, "text")
    with pytest.raises(ValidationError):
        m.Notebook.model_validate({"ownerId": "u1", "notes": None})


def test_patch_missing_and_explicit_null():
    m = load("patch_contract")
    assert m.missing.description is m.clear.description is None
    assert m.missing.model_dump(exclude_unset=True) == {}
    assert m.clear.model_dump(exclude_unset=True) == {"description": None}
    assert {**m.stored, **m.missing.model_dump(exclude_unset=True)} == {"description": "原说明"}
    assert {**m.stored, **m.clear.model_dump(exclude_unset=True)} == {"description": None}


def test_datetime_decimal_json_representation():
    from decimal import Decimal
    m = load("serialization_contract")
    assert isinstance(m.quote.model_dump()["amount"], Decimal)
    assert m.quote.model_dump(mode="json") == {"created_at": "2026-01-01T00:00:00Z", "amount": "1.20"}


def test_response_paths_headers_cookie_deletion():
    m = load("response_paths")
    with TestClient(m.app) as client:
        response = client.get("/model")
        assert response.json() == {"text": "第一条"}
        assert response.headers["x-format"] == "public-note"
        assert client.cookies["theme"] == "light"
        assert "httponly" in response.headers["set-cookie"].lower()
        assert client.get("/direct").json() == {"text": "第一条"}
        cleared = client.delete("/theme")
        assert cleared.status_code == 204 and cleared.content == b""
        assert "theme" not in client.cookies


def test_documented_async_lifespan_test(tmp_path):
    (tmp_path / "lifespan_app.py").write_text(EXAMPLES["lifespan_app"][0], encoding="utf-8")
    (tmp_path / "test_lifespan.py").write_text(EXAMPLES["async_lifespan_test"][0], encoding="utf-8")
    result = subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=tmp_path,
                            capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "1 passed" in result.stdout
