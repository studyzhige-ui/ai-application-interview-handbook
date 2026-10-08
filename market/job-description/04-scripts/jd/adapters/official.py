"""Configured first-party adapters reused for their request/response contracts.

Filtering, deduplication, persistent state, and rendering belong to other modules.
"""
from __future__ import annotations
import json
import re
import time
from typing import Any, Callable
from urllib.parse import urljoin, urlparse, parse_qs
from ..model import Job, txt
from ..matching import likely_target_title
from ..freshness import cache_is_fresh
from ..paths import XIAOMI_NODE_CACHE, BYTEDANCE_NODE_CACHE
from .http import requests, HEADERS, TIMEOUT, get_json, post_json, post_form


def fetch_xiaomi(src: dict) -> list[Job]:
    """Read Xiaomi campus jobs fetched by the official Node ATSX adapter.

    Xiaomi's official ATSX endpoint is first-party but its WAF currently treats
    Python requests differently from browser/Node fetch on GitHub runners.
    The collection interface therefore runs adapters/xiaomi.mjs first.
    """
    cache = XIAOMI_NODE_CACHE
    if not cache.exists():
        raise RuntimeError("Xiaomi official Node adapter output missing")
    payload = json.loads(cache.read_text(encoding="utf-8"))
    if not cache_is_fresh(payload) or payload.get("complete") is not True:
        raise RuntimeError("Official Node adapter output is stale or incomplete")
    if len(payload.get("jobs") or []) < int(payload.get("total") or 0):
        raise RuntimeError("Official Node adapter output does not cover advertised total")
    out: list[Job] = []
    for j in payload.get("jobs") or []:
        out.append(Job(
            src["company"], txt(j.get("title")), txt(j.get("job_id")),
            txt(j.get("location")), txt(j.get("category")), txt(j.get("department")),
            txt(j.get("description")), txt(j.get("requirements")),
            txt(j.get("official_url")), txt(j.get("official_api")),
            txt(j.get("cycle_evidence")),
        ))
    return out


def fetch_bytedance(src: dict) -> list[Job]:
    cache = BYTEDANCE_NODE_CACHE
    if not cache.exists():
        raise RuntimeError("ByteDance official Node adapter output missing")
    payload = json.loads(cache.read_text(encoding="utf-8"))
    if not cache_is_fresh(payload) or payload.get("complete") is not True:
        raise RuntimeError("Official Node adapter output is stale or incomplete")
    if len(payload.get("jobs") or []) < int(payload.get("total") or 0):
        raise RuntimeError("Official Node adapter output does not cover advertised total")
    out: list[Job] = []
    for j in payload.get("jobs") or []:
        out.append(Job(
            src["company"], txt(j.get("title")), txt(j.get("job_id")),
            txt(j.get("location")), txt(j.get("category")), txt(j.get("department")),
            txt(j.get("description")), txt(j.get("requirements")),
            txt(j.get("official_url")), txt(j.get("official_api")),
            txt(j.get("cycle_evidence")),
        ))
    return out


def fetch_kuaishou(src: dict) -> list[Job]:
    """Enumerate Kuaishou's official 2027 project; list API already returns full JD."""
    base = "https://campus.kuaishou.cn"
    list_api = base + "/recruit/campus/e/api/v1/open/positions/simple"
    project = str(src.get("project_code") or "20271779425607")
    headers = {
        **HEADERS,
        "Referer": src["portal"],
        "Content-Type": "application/json",
    }
    out: list[Job] = []
    page = 1
    while page <= 20:
        payload = {
            "recruitSubProjectCodes": [project],
            "pageSize": 500,
            "pageNum": page,
            "positionNatureCode": "fulltime",
        }
        r = requests.post(list_api, json=payload, headers=headers, timeout=TIMEOUT)
        r.raise_for_status()
        body = r.json()
        if body.get("code") not in (None, 0):
            raise RuntimeError(f"Kuaishou API code={body.get('code')} message={body.get('message')}")
        result = body.get("result") or {}
        rows = result.get("list") or []
        if not rows:
            break
        for j in rows:
            jid = txt(j.get("id"))
            code = txt(j.get("code"))
            locations = j.get("workLocationDicts") or []
            city = " / ".join(
                txt(x.get("name")) for x in locations if isinstance(x, dict) and x.get("name")
            )
            out.append(Job(
                src["company"],
                txt(j.get("name")),
                jid,
                city,
                "2027校招正式",
                txt(j.get("departmentName") or j.get("positionCategoryName")),
                txt(j.get("description")),
                txt(j.get("positionDemand")),
                f"{base}/recruit/campus/e/#/campus/job-info/{jid}?code={code}&recruitSubProjectCodes={project}",
                list_api,
                f"快手官方2027项目 {project}",
            ))
        pages = int(result.get("pages") or 0)
        total = int(result.get("total") or 0)
        if (pages and page >= pages) or (total and page * 500 >= total) or len(rows) < 500:
            break
        page += 1
    return out


def fetch_baidu(src: dict) -> list[Job]:
    out = []
    page = 1
    while page <= 30:
        data = post_form(
            src["api"],
            data={"recruitType": "GRADUATE", "pageSize": 20, "curPage": page, "projectType": "", "keyWord": ""},
            headers={"Referer": "https://talent.baidu.com/jobs/list?projectType=1"},
        )
        d = data.get("data") or {}
        rows = d.get("list") or []
        if not rows:
            break
        for j in rows:
            pid = txt(j.get("jobId") or j.get("postId"))
            out.append(Job(
                src["company"], txt(j.get("name")), pid,
                txt(j.get("workPlace")), "校招", txt(j.get("serviceType")),
                txt(j.get("workContent")), txt(j.get("serviceCondition")),
                f"https://talent.baidu.com/jobs/detail/GRADUATE/{pid}", src["api"],
                "百度当前校园招聘=2027届",
            ))
        total = int(d.get("total") or 0)
        if page * 20 >= total:
            break
        page += 1
    return out


def fetch_netease(src: dict) -> list[Job]:
    out = []
    page = 1
    while page <= 30:
        data = post_json(src["api"], payload={"currentPage": page, "pageSize": 100},
                         headers={"Origin": "https://hr.163.com"})
        d = data.get("data") or {}
        rows = d.get("list") or []
        if not rows:
            break
        for j in rows:
            jid = txt(j.get("id"))
            out.append(Job(
                src["company"], txt(j.get("name")), jid,
                txt(j.get("workPlaceName")), txt(j.get("recruitTypeName")), txt(j.get("deptName")),
                txt(j.get("requirement")), "学历: " + txt(j.get("educationName")),
                f"https://hr.163.com/position/detail.html?id={jid}", src["api"],
                txt(j.get("recruitTypeName")),
            ))
        pages = int(d.get("pages") or 0)
        if pages and page >= pages:
            break
        page += 1
    return out


def fetch_tencent_campus(src: dict) -> list[Job]:
    api = "https://join.qq.com/api/v1/position/searchPosition"
    detail_api = "https://join.qq.com/api/v1/jobDetails/getJobDetailsByPostId"
    headers = {**HEADERS, "Content-Type": "application/json", "Referer": "https://join.qq.com/post.html"}
    out, seen = [], set()
    page = 1
    while page <= 50:
        body = {
            "keyword": "", "pageIndex": page, "pageSize": 50,
            "recruitType": "40003", "bgIds": [], "productIds": [],
            "categoryIds": [], "workLocations": [], "timestamp": "",
        }
        r = requests.post(api, json=body, headers=headers, timeout=TIMEOUT)
        r.raise_for_status()
        d = (r.json().get("data") or {})
        rows = d.get("positionList") or []
        if not rows:
            break
        for row in rows:
            pid = txt(row.get("postId") or row.get("id"))
            if not pid or pid in seen:
                continue
            seen.add(pid)
            project = txt(row.get("recruitLabelName") or row.get("projectName") or "校招")
            if "实习" in project:
                continue
            title = txt(row.get("positionTitle"))
            if not likely_target_title(title):
                continue
            try:
                detail = get_json(
                    detail_api,
                    params={"timestamp": int(time.time() * 1000), "postId": pid},
                    headers={"Referer": "https://join.qq.com/post.html"},
                )
                dd = detail.get("data") or {}
            except Exception:
                dd = {}
            desc = txt(dd.get("desc") or dd.get("topicDetail") or dd.get("introduction"))
            req = txt(dd.get("request") or dd.get("topicRequirement"))
            out.append(Job(
                src["company"], title, pid,
                txt(row.get("workCities")), project, txt(row.get("bgs")),
                desc, req,
                f"https://join.qq.com/post_detail.html?postId={pid}", api,
                project or "腾讯官方校园招聘",
            ))
        if page * 50 >= int(d.get("count") or 0):
            break
        page += 1
    return out


def fetch_meituan_campus(src: dict) -> list[Job]:
    api = "https://zhaopin.meituan.com/api/official/job/getJobList"
    headers = {
        **HEADERS, "Content-Type": "application/json",
        "Referer": "https://zhaopin.meituan.com/web/campus",
        "Origin": "https://zhaopin.meituan.com",
        "X-Requested-With": "XMLHttpRequest",
    }
    out, seen = [], set()
    for page in range(1, 30):
        body = {
            "page": {"pageNo": page, "pageSize": 100},
            "jobShareType": "1", "keywords": "", "cityList": [],
            "department": [], "jfJgList": [],
            "jobType": [{"code": "1", "subCode": []}],
            "typeCode": [], "specialCode": [],
        }
        r = requests.post(api, json=body, headers=headers, timeout=TIMEOUT)
        r.raise_for_status()
        d = r.json().get("data") or {}
        rows = d.get("list") or []
        if not rows:
            break
        for j in rows:
            if str(j.get("jobType") or "") not in ("", "1"):
                continue
            jid = txt(j.get("jobUnionId"))
            if not jid or jid in seen:
                continue
            seen.add(jid)
            city = " / ".join(
                txt(x.get("name")) for x in (j.get("cityList") or [])
                if isinstance(x, dict) and x.get("name")
            )
            out.append(Job(
                src["company"], txt(j.get("name")), jid, city,
                "校招正式", txt(j.get("departmentName") or j.get("jobCategoryName")),
                txt(j.get("jobDuty") or j.get("desc")), txt(j.get("jobRequirement")),
                f"https://zhaopin.meituan.com/web/position/detail?jobUnionId={jid}&highlightType=campus",
                api, "美团官方当前校园招聘正式岗（届别需主库复核）",
            ))
        p = d.get("page") or {}
        if page >= int(p.get("totalPage") or page):
            break
    return out


def fetch_jd_campus(src: dict) -> list[Job]:
    api = "https://campus.jd.com/api/wx/position/page"
    headers = {**HEADERS, "Content-Type": "application/json", "Referer": "https://campus.jd.com/"}
    out = []
    for recruit_type in ("present", "talent"):
        page, seen = 0, set()
        while page < 30:
            payload = {
                "pageSize": 50, "pageIndex": page,
                "parameter": {
                    "positionName": "", "planIdList": [], "jobDirectionCodeList": [],
                    "workCityCodeList": [], "positionDeptList": [],
                },
            }
            r = requests.post(f"{api}?type={recruit_type}", json=payload, headers=headers, timeout=TIMEOUT)
            r.raise_for_status()
            d = r.json().get("body") or {}
            rows = d.get("items") or []
            if not rows:
                break
            for j in rows:
                pid = txt(j.get("publishId") or j.get("reqId"))
                key = f"{recruit_type}:{pid}"
                if not pid or key in seen:
                    continue
                seen.add(key)
                cities = []
                for req in j.get("requirementVoList") or []:
                    city = txt(req.get("workCity"))
                    if city and city not in cities:
                        cities.append(city)
                out.append(Job(
                    src["company"], txt(j.get("positionName")), key,
                    " / ".join(cities), "校招正式", txt(j.get("positionDept")),
                    txt(j.get("workContent")), txt(j.get("qualification")),
                    f"https://campus.jd.com/#/details?type={recruit_type}&id={pid}",
                    api, f"京东官方校园招聘 {recruit_type}（届别需主库复核）",
                ))
            total = int(d.get("totalNumber") or 0)
            page += 1
            if page * 50 >= total:
                break
    return out


def fetch_pdd_campus(src: dict) -> list[Job]:
    root = "https://careers.pddglobalhr.com/api/careers/api/recruit/position"
    list_api, detail_api = root + "/list", root + "/detail"
    headers = {
        **HEADERS, "Content-Type": "application/json;charset=UTF-8",
        "Referer": "https://careers.pddglobalhr.com/campus/grad",
    }
    session = requests.Session()
    session.headers.update(headers)
    rows, page = [], 1
    while page <= 30:
        r = session.post(list_api, json={"page": page, "pageSize": 100, "t": None}, timeout=TIMEOUT)
        r.raise_for_status()
        body = r.json()
        if not body.get("success"):
            raise RuntimeError(body.get("errorMsg") or "PDD official API success=false")
        d = body.get("result") or {}
        got = d.get("list") or []
        if not got:
            break
        rows.extend(got)
        if len(rows) >= int(d.get("total") or len(rows)):
            break
        page += 1

    out = []
    for row in rows:
        pid = txt(row.get("id"))
        if not pid:
            continue
        try:
            r = session.post(detail_api, json={"id": pid, "t": None}, timeout=TIMEOUT)
            r.raise_for_status()
            body = r.json()
            detail = (body.get("result") or {}) if body.get("success") else {}
        except Exception:
            detail = {}
        year = txt(detail.get("graduationYear") or row.get("graduationYear"))
        recruit_type = txt(detail.get("recruitTypeName") or row.get("recruitTypeName"))
        out.append(Job(
            src["company"], txt(row.get("name")), pid,
            txt(detail.get("workLocationName") or row.get("workLocationName") or row.get("workLocation")),
            "校招正式" + (f" {year}届" if year else ""), txt(row.get("departmentName")),
            txt(detail.get("jobDuty") or row.get("jobDuty")),
            txt(detail.get("serveRequirement") or row.get("serveRequirement")),
            txt(detail.get("shareUrl")) or f"https://careers.pddglobalhr.com/campus/grad/detail?positionId={pid}",
            list_api, f"拼多多官方校招 {year + '届' if year else '届别待复核'} {recruit_type}",
        ))
    return out


def fetch_oppo_campus(src: dict) -> list[Job]:
    api = "https://careers.oppo.com/openapi/position/pageNew"
    headers = {
        **HEADERS, "Content-Type": "application/json", "Tenant-Id": "1000",
        "Referer": "https://careers.oppo.com/university/oppo/recruitment/post",
    }
    out, page = [], 1
    while page <= 20:
        payload = {
            "pageNum": page, "pageSize": 100, "positionName": "",
            "projectList": [], "positionTypeList": [], "workCityCodeList": [],
        }
        r = requests.post(api, json=payload, headers=headers, timeout=TIMEOUT)
        r.raise_for_status()
        d = r.json().get("data") or {}
        rows = d.get("records") or []
        if not rows:
            break
        for j in rows:
            jid = txt(j.get("idProjPosition") or j.get("idRecruitPosition"))
            project = txt(j.get("projectName"))
            out.append(Job(
                src["company"], txt(j.get("positionName") or j.get("projectPositionName")), jid,
                txt(j.get("workCityName")), txt(j.get("positionTypeName") or "校招"),
                project, txt(j.get("positionDesc")), txt(j.get("positionRequire")),
                f"https://careers.oppo.com/university/oppo/campus/post/{jid}",
                api, project or "OPPO官方校园招聘（届别待复核）",
            ))
        total = int(d.get("total") or len(rows))
        if page * 100 >= total:
            break
        page += 1
    return out


def fetch_lenovo(src: dict) -> list[Job]:
    api = "https://talent.lenovo.com.cn/gateway/jobBase/list"
    headers = {
        **HEADERS, "Referer": "https://talent.lenovo.com.cn/position",
        "portal-type": "PC",
    }
    out, page = [], 1
    while page <= 30:
        data = get_json(api, params={"pageNum": page, "pageSize": 50}, headers=headers)
        d = data.get("result") or {}
        rows = d.get("rows") or []
        if not rows:
            break
        for j in rows:
            jid = txt(j.get("id"))
            out.append(Job(
                src["company"], txt(j.get("jobName")), jid, txt(j.get("workPlace")),
                txt(j.get("recruitType") or j.get("jobType") or "校招待复核"),
                txt(j.get("jobCategory")), txt(j.get("cont") or j.get("jobDesc")),
                txt(j.get("requirement")),
                f"https://talent.lenovo.com.cn/position/detail?id={jid}",
                api, "联想官方招聘（2027归属需复核）",
            ))
        if page * 50 >= int(d.get("total") or 0):
            break
        page += 1
    return out


def fetch_sf(src: dict) -> list[Job]:
    api = "https://campus.sf-express.com/api/web/position/query"
    out, page = [], 1
    while page <= 20:
        data = get_json(api, params={"pageNum": page, "pageSize": 50}, headers={"Referer": "https://campus.sf-express.com/positionList"})
        rows = data.get("list") or []
        if not rows:
            break
        for j in rows:
            jid = txt(j.get("id"))
            out.append(Job(
                src["company"], txt(j.get("positionName")), jid,
                txt(j.get("demandCity")), "校招", txt(j.get("positionTypeName") or j.get("orgSourceName")),
                txt(j.get("postDuty")), txt(j.get("jobRequirement")),
                f"https://campus.sf-express.com/#/postDetail/{jid}",
                api, "顺丰官方校园招聘（届别待复核）",
            ))
        if page * 50 >= int(data.get("total") or 0):
            break
        page += 1
    return out


def fetch_alibaba_campus(src: dict) -> list[Job]:
    origin = "https://campus-talent.alibaba.com"
    batch_id = int(src.get("batch_id") or 100000540002)
    page_url = f"{origin}/campus/position?batchId={batch_id}"
    session = requests.Session()
    session.headers.update({**HEADERS, "Referer": page_url, "Content-Type": "application/json"})
    warm = session.get(page_url, timeout=TIMEOUT)
    warm.raise_for_status()
    csrf = session.cookies.get("XSRF-TOKEN")
    if not csrf:
        raise RuntimeError("Alibaba campus XSRF-TOKEN missing")
    out, page = [], 1
    while page <= 30:
        payload = {
            "batchId": batch_id, "pageIndex": page, "pageSize": 50,
            "channel": "campus_group_official_site", "language": "zh",
        }
        r = session.post(f"{origin}/position/search?_csrf={csrf}", json=payload, timeout=TIMEOUT)
        r.raise_for_status()
        content = r.json().get("content") or {}
        rows = content.get("datas") or []
        if not rows:
            break
        for j in rows:
            jid = txt(j.get("id"))
            out.append(Job(
                src["company"], txt(j.get("name")), jid,
                " / ".join(txt(x) for x in (j.get("workLocations") or [])),
                "校招", txt(j.get("departmentName") or j.get("categoryName")),
                txt(j.get("description")), txt(j.get("requirement")),
                f"{origin}/campus/position-detail?positionId={jid}",
                f"{origin}/position/search",
                f"阿里官方校园招聘 batchId={batch_id}（2027归属需复核）",
            ))
        total = int(content.get("totalCount") or content.get("total") or 0)
        if page * 50 >= total:
            break
        page += 1
    return out


def _strip_html(value: Any) -> str:
    s = txt(value)
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    s = re.sub(r"</(?:p|div|li|h[1-6]|tr|td|th|ul|ol|section)>", "\n", s, flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)
    return (
        s.replace("&nbsp;", " ").replace("&amp;", "&")
        .replace("&lt;", "<").replace("&gt;", ">")
        .replace("&quot;", '"').replace("&#39;", "'")
        .strip()
    )


def fetch_xiaohongshu_2027(src: dict) -> list[Job]:
    api = "https://job.xiaohongshu.com/websiterecruit/position/pageQueryPosition"
    detail_api = "https://job.xiaohongshu.com/websiterecruit/position/queryPositionDetail"
    headers = {**HEADERS, "Origin": "https://job.xiaohongshu.com", "Referer": "https://job.xiaohongshu.com/campus"}
    out: list[Job] = []
    page = 1
    while page <= 30:
        data = post_json(
            api,
            payload={
                "positionName": "", "pageNum": page, "pageSize": 100,
                "recruitType": "campus", "jobProjects": ["red_star_27"],
            },
            headers=headers,
        )
        d = data.get("data") or {}
        rows = d.get("list") or []
        if not rows:
            break
        for row in rows:
            pid = txt(row.get("positionId"))
            list_title = txt(row.get("positionName"))
            if not likely_target_title(list_title):
                continue
            detail = {}
            if pid:
                try:
                    detail_payload = get_json(detail_api, params={"positionId": pid}, headers=headers)
                    detail = detail_payload.get("data") or {}
                except Exception:
                    detail = {}
            title = txt(detail.get("positionName") or list_title)
            out.append(Job(
                src["company"], title, pid,
                txt(detail.get("workplace") or row.get("workplace")),
                "2027校园招聘", txt(detail.get("positionType") or row.get("jobType")),
                txt(detail.get("duty") or row.get("duty")),
                txt(detail.get("qualification") or row.get("qualification")),
                f"https://job.xiaohongshu.com/campus/position/{pid}" if pid else src["portal"],
                api,
                "小红书2027校园招聘 / red_star_27",
            ))
        total_pages = int(d.get("totalPage") or 0)
        if total_pages and page >= total_pages:
            break
        if len(rows) < 100:
            break
        page += 1
    return out


def fetch_bilibili_2027(src: dict) -> list[Job]:
    root = "https://jobs.bilibili.com"
    token_url = root + "/api/auth/v1/csrf/token"
    list_api = root + "/api/campus/position/positionList"
    base_headers = {
        **HEADERS,
        "Content-Type": "application/json",
        "X-AppKey": "ops.ehr-api.auth",
        "X-UserType": "2",
        "Referer": root + "/campus/positions",
    }
    token_payload = get_json(token_url, headers=base_headers)
    token = txt(token_payload.get("data"))
    if not token:
        raise RuntimeError("Bilibili official CSRF token missing")
    headers = {**base_headers, "X-CSRF": token, "Cookie": f"X-CSRF={token}"}
    out: list[Job] = []
    page = 1
    while page <= 50:
        data = post_json(
            list_api,
            payload={
                "pageSize": 100, "pageNum": page, "positionName": "",
                "postCode": [], "postCodeList": [], "workLocationList": [],
                "workTypeList": [3], "positionTypeList": [],
                "deptCodeList": [], "recruitType": 1,
                "practiceTypes": [], "onlyHotRecruit": 0,
            },
            headers=headers,
        )
        if data.get("code") != 0:
            raise RuntimeError(f"Bilibili code={data.get('code')}: {data.get('message')}")
        d = data.get("data") or {}
        rows = d.get("list") or []
        if not rows:
            break
        for j in rows:
            jid = txt(j.get("id"))
            jd = txt(j.get("positionDescription"))
            out.append(Job(
                src["company"], txt(j.get("positionName")), jid,
                txt(j.get("workLocation")), txt(j.get("positionTypeName") or "校招全职"),
                txt(j.get("postCodeName")), jd, "",
                f"{root}/campus/positions/{jid}" if jid else src["portal"],
                list_api,
                "哔哩哔哩官方校园招聘全职项目" + (" / 2027" if "2027" in jd else ""),
            ))
        total = int(d.get("total") or 0)
        if page * 100 >= total or len(rows) < 100:
            break
        page += 1
    return out


def fetch_huawei_2027(src: dict) -> list[Job]:
    portal_root = "https://career.huawei.com/reccampportal"
    pub = portal_root + "/services/portal/portalpub"
    user_api = portal_root + "/services/portal/portaluser"
    page_url = portal_root + "/portal5/campus-recruitment.html"
    session = requests.Session()
    session.headers.update({**HEADERS, "Referer": page_url})
    try:
        session.get(portal_root + "/", timeout=TIMEOUT)
    except Exception:
        pass

    out: list[Job] = []
    page = 1
    while page <= 50:
        params = {
            "jobType": "0", "jobTypes": "2", "language": "zh_CN",
            "reqTime": int(time.time() * 1000),
            "orderBy": "ISS_STARTDATE_DESC_AND_IS_HOT_JOB",
        }
        url = f"{pub}/getJob/newHr/page/50/{page}"
        r = session.get(url, params=params, timeout=TIMEOUT)
        r.raise_for_status()
        payload = r.json()
        rows = payload.get("result") or []
        if not rows:
            break
        for row in rows:
            jid = txt(row.get("jobId"))
            ds = txt(row.get("dataSource") or "1")
            list_title = txt(row.get("jobname"))
            if not likely_target_title(list_title):
                continue
            detail = {}
            if jid:
                try:
                    dr = session.get(
                        f"{pub}/getJobDetail/newHr",
                        params={"jobId": jid, "dataSource": ds, "language": "zh_CN"},
                        timeout=TIMEOUT,
                    )
                    dr.raise_for_status()
                    detail = dr.json() or {}
                except Exception:
                    detail = {}
            desc = txt(detail.get("mainBusiness") or row.get("mainBusiness"))
            req = txt(detail.get("jobRequire") or row.get("jobRequire"))
            req_id = txt(detail.get("jobRequirementId") or row.get("jobRequirementId"))
            if req_id and (not desc or "详见岗位意向" in desc or not req or "详见岗位意向" in req):
                try:
                    ir = session.get(
                        f"{user_api}/findIntentListByJobRequirementId/newHr/zh_CN/{req_id}/null",
                        params={"dataSource": ds, "jobId": jid},
                        timeout=TIMEOUT,
                    )
                    ir.raise_for_status()
                    intents = ir.json() or []
                    if isinstance(intents, list) and intents:
                        desc = "\n\n".join(
                            f"【{txt(i.get('positionIntention'))}】\n{_strip_html(i.get('jobResponsibilities'))}"
                            for i in intents
                        )
                        req = "\n\n".join(
                            f"【{txt(i.get('positionIntention'))}】\n{_strip_html(i.get('jobDemand'))}"
                            for i in intents
                        )
                except Exception:
                    pass
            out.append(Job(
                src["company"], txt(detail.get("jobname") or list_title), jid,
                txt(detail.get("jobArea") or row.get("jobArea") or row.get("jobAddress")),
                "2027应届生", txt(detail.get("jobFamilyName") or row.get("jobFamilyName")),
                _strip_html(desc), _strip_html(req),
                f"{page_url.replace('campus-recruitment.html','campus-recruitment-detail.html')}?jobId={jid}&dataSource={ds}",
                f"{pub}/getJob/newHr/page/50/{{page}}",
                "华为2027届应届生招聘",
            ))
        pvo = payload.get("pageVO") or {}
        total_pages = int(pvo.get("totalPages") or 0)
        if total_pages and page >= total_pages:
            break
        if len(rows) < 50:
            break
        page += 1
    return out


def fetch_ant_2027(src: dict) -> list[Job]:
    api = "https://hrcareersweb.antgroup.com/api/campus/position/search"
    headers = {
        **HEADERS, "Content-Type": "application/json",
        "Origin": "https://talent.antgroup.com",
        "Referer": "https://talent.antgroup.com/campus-list",
    }
    out: list[Job] = []
    page = 1
    while page <= 80:
        data = post_json(
            api,
            payload={"key": "", "pageIndex": page, "pageSize": 49, "language": "zh"},
            headers=headers,
        )
        if data.get("success") is not True:
            raise RuntimeError(data.get("errorMsg") or f"Ant success={data.get('success')}")
        rows = data.get("content") or []
        if not rows:
            break
        for j in rows:
            jid = txt(j.get("id") or j.get("code"))
            graduation = txt(j.get("graduationTime"))
            out.append(Job(
                src["company"], txt(j.get("name")), jid,
                txt(j.get("workLocations")), txt(j.get("positionType") or "校招"),
                txt(j.get("department") or j.get("project") or j.get("categoryName")),
                _strip_html(j.get("description")), _strip_html(j.get("requirement")),
                f"https://talent.antgroup.com/campus-position?positionId={jid}" if jid else src["portal"],
                api,
                "蚂蚁集团官方校园招聘" + (f" / {graduation}" if graduation else ""),
            ))
        total = int(data.get("totalCount") or 0)
        if page * 49 >= total or len(rows) < 49:
            break
        page += 1
    return out


def _beisen_fetch_all(
    *,
    company: str,
    root: str,
    portal_id: str,
    categories: list[str] | None,
    cycle_evidence: str,
    source_url: str,
) -> list[Job]:
    api = root.rstrip("/") + "/api/Jobad/GetJobAdPageList"
    headers = {
        **HEADERS,
        "Content-Type": "application/json",
        "Origin": root.rstrip("/"),
        "Referer": source_url,
        "x-requested-with": "xmlhttprequest",
        "langtype": "zh_CN",
    }
    out: list[Job] = []
    page = 0
    while page < 50:
        body: dict[str, Any] = {
            "PageIndex": page, "PageSize": 100, "KeyWords": "",
            "SpecialType": 0, "PortalId": portal_id,
            "DisplayFields": ["Category", "Kind", "LocId", "Org", "HeadCount", "PostDate", "Salary"],
        }
        if categories:
            body["Category"] = categories
        data = post_json(api, payload=body, headers=headers)
        if data.get("Code") != 200:
            raise RuntimeError(data.get("Message") or f"Beisen code={data.get('Code')}")
        rows = data.get("Data") or []
        if not rows:
            break
        for j in rows:
            jid = txt(j.get("JobAdId") or j.get("Id"))
            out.append(Job(
                company, txt(j.get("JobAdName")), jid,
                txt(j.get("LocNames")), txt(j.get("Category") or "校园招聘"),
                txt(j.get("Org")), _strip_html(j.get("Duty")), _strip_html(j.get("Require")),
                f"{root.rstrip('/')}/campus/detail?jobAdId={jid}" if jid else source_url,
                api, cycle_evidence,
            ))
        total = int(data.get("Count") or data.get("Total") or 0)
        page += 1
        if page * 100 >= total or len(rows) < 100:
            break
    return out


def fetch_vivo_2027(src: dict) -> list[Job]:
    return _beisen_fetch_all(
        company=src["company"], root="https://hr-campus.vivo.com",
        portal_id="903cbcbf-4898-46e1-817c-da522a9752b1",
        categories=["2"], cycle_evidence="vivo官方校园招聘（2027届别由职位/项目正文复核）",
        source_url="https://hr-campus.vivo.com/campus/jobs",
    )


def fetch_beisen_direct(src: dict) -> list[Job]:
    """Enumerate a company-proven Beisen/Zhiye campus tenant via the public first-party API."""
    parsed = urlparse(src.get("search_url") or src.get("portal") or "")
    root = f"{parsed.scheme}://{parsed.netloc}"
    if not parsed.netloc or not parsed.netloc.endswith("zhiye.com"):
        raise RuntimeError("beisen_direct requires a zhiye.com official ATS search_url")
    cond_api = root + "/api/Jobad/GetJobAdSearchConditions"
    headers = {
        **HEADERS, "Content-Type": "application/json", "Origin": root,
        "Referer": src.get("search_url") or src.get("portal") or root,
        "x-requested-with": "xmlhttprequest", "langtype": "zh_CN",
    }
    categories: list[str] = []
    try:
        conditions = post_json(cond_api, payload={"displayFilters": ["Category"]}, headers=headers)
        if conditions.get("Code") == 200:
            for axis in conditions.get("Data") or []:
                if txt(axis.get("Value")) != "Category":
                    continue
                for item in axis.get("Data") or []:
                    label = txt(item.get("Text"))
                    cid = txt(item.get("StrValue") or item.get("Value"))
                    if cid and not re.search(r"社会|社招|实习", label):
                        categories.append(cid)
    except Exception:
        categories = []
    return _beisen_fetch_all(
        company=src["company"], root=root, portal_id=txt(src.get("beisen_portal_id")),
        categories=categories or None,
        cycle_evidence=txt(src.get("beisen_cycle_evidence")) or "官方校园招聘",
        source_url=src.get("search_url") or src.get("portal") or root,
    )


def fetch_iflytek_2027(src: dict) -> list[Job]:
    root = "https://iflytek.zhiye.com"
    cond_api = root + "/api/Jobad/GetJobAdSearchConditions"
    headers = {
        **HEADERS, "Content-Type": "application/json", "Origin": root,
        "Referer": root + "/jobs", "x-requested-with": "xmlhttprequest", "langtype": "zh_CN",
    }
    categories: list[str] = []
    try:
        conditions = post_json(cond_api, payload={"displayFilters": ["Category"]}, headers=headers)
        if conditions.get("Code") == 200:
            for axis in conditions.get("Data") or []:
                if txt(axis.get("Value")) != "Category":
                    continue
                for item in axis.get("Data") or []:
                    label = txt(item.get("Text"))
                    cid = txt(item.get("StrValue") or item.get("Value"))
                    if cid and not re.search(r"社会|社招|实习", label):
                        categories.append(cid)
    except Exception:
        pass
    if not categories:
        categories = ["4", "5", "6"]
    return _beisen_fetch_all(
        company=src["company"], root=root, portal_id="", categories=categories,
        cycle_evidence="科大讯飞官方校园招聘（2027届别由职位/项目正文复核）",
        source_url=root + "/jobs",
    )


def fetch_ctrip_2027(src: dict) -> list[Job]:
    api = "https://careers.ctrip.com/api/hrrecruit/getJobAd"
    headers = {
        **HEADERS, "Content-Type": "application/json",
        "Origin": "https://careers.ctrip.com", "Referer": "https://careers.ctrip.com/#/campus",
    }
    data = post_json(api, payload={"condition": {"pageIndex": 1, "pageSize": 100, "category": "2"}}, headers=headers)
    if txt(data.get("retCode")) != "201":
        raise RuntimeError(data.get("retMessage") or f"Ctrip retCode={data.get('retCode')}")
    d = data.get("retValue") or {}
    out: list[Job] = []
    for j in d.get("recruitJobAdList") or []:
        jid = txt(j.get("id") or j.get("jobId"))
        mj = txt(j.get("fromId"))
        out.append(Job(
            src["company"], txt(j.get("jobTitle")), jid,
            txt(j.get("cityName")), "2027届应届校招",
            txt(j.get("buName") or j.get("jobFamilyGroupName")),
            _strip_html(j.get("duty")), _strip_html(j.get("requirements")),
            f"https://careers.ctrip.com/campus#/experienced/job-detail/{mj}" if mj else "https://careers.ctrip.com/#/campus",
            api, "携程集团2027届应届校招生",
        ))
    return out


def fetch_honor_2027(src: dict) -> list[Job]:
    host = "https://career.honor.com"
    su = "SU60eea919bef57c1023f6fe78"
    list_api = f"{host}/wecruit/positionInfo/listPosition/{su}"
    detail_api = f"{host}/wecruit/positionInfo/listPositionDetail/{su}"
    headers = {
        **HEADERS, "Content-Type": "application/x-www-form-urlencoded",
        "Origin": host, "Referer": f"{host}/{su}/pb/school.html",
        "X-Requested-With": "XMLHttpRequest",
    }
    out: list[Job] = []
    page = 1
    while page <= 100:
        params = {"iSaJAx": "isAjax", "request_locale": "zh_CN", "t": int(time.time() * 1000)}
        # Official Wecruit list endpoint is form-urlencoded with query params.
        rr = requests.post(
            list_api,
            params=params,
            data={"isFrompb": "true", "recruitType": 1, "pageSize": 100, "currentPage": page},
            headers=headers, timeout=TIMEOUT,
        )
        rr.raise_for_status()
        data = rr.json()
        if txt(data.get("state")) != "200":
            raise RuntimeError(data.get("msg") or f"Honor state={data.get('state')}")
        pf = ((data.get("data") or {}).get("pageForm") or {})
        rows = pf.get("pageData") or []
        if not rows:
            break
        for row in rows:
            pid = txt(row.get("postId"))
            list_title = txt(row.get("postName"))
            if not likely_target_title(list_title):
                continue
            detail: dict[str, Any] = {}
            if pid:
                try:
                    dr = requests.post(
                        detail_api,
                        params={"iSaJAx": "isAjax", "request_locale": "zh_CN", "t": int(time.time() * 1000)},
                        data={"postId": pid, "recruitType": 1},
                        headers=headers | {"Referer": f"{host}/{su}/pb/posDetail.html"},
                        timeout=TIMEOUT,
                    )
                    dr.raise_for_status()
                    dp = dr.json()
                    if txt(dp.get("state")) == "200":
                        detail = dp.get("data") or {}
                except Exception:
                    detail = {}
            out.append(Job(
                src["company"], txt(detail.get("postName") or list_title), pid,
                txt(detail.get("workPlaceStr") or row.get("workPlaceStr")),
                "荣耀2027校招", txt(detail.get("orgName") or row.get("department") or row.get("postTypeName")),
                _strip_html(detail.get("workContent") or row.get("description") or row.get("duty")),
                _strip_html(detail.get("serviceCondition") or row.get("require") or row.get("requirement")),
                f"{host}/{su}/pb/school.html#/postDetail?postId={pid}" if pid else src["portal"],
                list_api, "荣耀2027校招",
            ))
        total_pages = int(pf.get("totalPage") or 0)
        if total_pages and page >= total_pages:
            break
        if len(rows) < 100:
            break
        page += 1
    return out


def fetch_feishu_direct(src: dict) -> list[Job]:
    """Enumerate a company-proven Feishu Recruiting tenant directly.

    Feishu's public job search is anonymous. Portal scope is selected by the
    official portal-channel / website-path header; optional subject/project and
    recruitment filters come only from the company's official career URL.
    """
    host = txt(src.get("feishu_host"))
    channel = txt(src.get("feishu_channel"))
    if not host:
        host = urlparse(src["portal"]).hostname or ""
    if not channel:
        path = urlparse(src["portal"]).path.strip("/")
        channel = path.split("/")[0] if path else ""
    if not host:
        raise RuntimeError("Feishu host missing")

    api = f"https://{host}/api/v1/search/job/posts"
    apply_prefix = txt(src.get("feishu_apply_prefix")) or f"https://{host}/{channel}/position"
    headers = {
        **HEADERS,
        "Content-Type": "application/json",
        "portal-channel": channel,
        "portal-platform": "pc",
        "website-path": channel,
        "Origin": f"https://{host}",
        "Referer": src["portal"],
    }
    subject_ids = [str(x) for x in (src.get("feishu_subject_ids") or [])]
    recruitment_ids = [str(x) for x in (src.get("feishu_recruitment_ids") or [])]
    out: list[Job] = []
    offset = 0
    total = None
    for _ in range(100):
        body: dict[str, Any] = {
            "keyword": "", "limit": 100, "offset": offset,
            "portal_type": 3, "portal_entrance": 1, "language": "zh",
            "job_category_id_list": [], "location_code_list": [],
        }
        if subject_ids:
            body["subject_id_list"] = subject_ids
        if recruitment_ids:
            body["recruitment_id_list"] = recruitment_ids
        data = post_json(api, payload=body, headers=headers)
        if data.get("code") != 0:
            raise RuntimeError(f"Feishu {host}/{channel} code={data.get('code')}: {data.get('message')}")
        d = data.get("data") or {}
        rows = d.get("job_post_list") or []
        if total is None:
            total = int(d.get("count") or 0)
        if not rows:
            break
        for j in rows:
            jid = txt(j.get("id"))
            cities = " / ".join(
                txt(x.get("name")) for x in (j.get("city_list") or [])
                if isinstance(x, dict) and x.get("name")
            ) or txt((j.get("city_info") or {}).get("name"))
            category = txt((j.get("recruit_type") or {}).get("name"))
            department = txt((j.get("job_category") or {}).get("name")) or txt((j.get("job_function") or {}).get("name"))
            subjects = []
            raw_subjects = j.get("job_subject_list") or ([j.get("job_subject")] if j.get("job_subject") else [])
            for s in raw_subjects:
                if not isinstance(s, dict):
                    continue
                name = s.get("name")
                if isinstance(name, dict):
                    name = name.get("zh_cn") or name.get("i18n") or name.get("en_us")
                if name:
                    subjects.append(txt(name))
            cycle = " / ".join(subjects + ([category] if category else []))
            out.append(Job(
                src["company"], txt(j.get("title")), jid, cities, category, department,
                txt(j.get("description")), txt(j.get("requirement")),
                f"{apply_prefix.rstrip('/')}/{jid}/detail" if jid else src["portal"],
                api, cycle,
            ))
        offset += len(rows)
        if len(rows) < 100 or (total is not None and offset >= total):
            break
    return out


def fetch_mihoyo_campus(src: dict) -> list[Job]:
    """Enumerate miHoYo's complete current formal campus pool via its first-party ATS."""
    list_api = "https://ats.openout.mihoyo.com/ats-portal/v1/job/list"
    detail_api = "https://ats.openout.mihoyo.com/ats-portal/v1/job/info"
    headers = {
        **HEADERS, "Content-Type": "application/json",
        "Origin": "https://jobs.mihoyo.com",
        "Referer": "https://jobs.mihoyo.com/#/campus/position",
    }
    rows: list[dict[str, Any]] = []
    page = 1
    page_size = 100
    total = None
    while page <= 100:
        payload = {
            "pageNo": page, "pageSize": page_size,
            "channelDetailIds": [1], "hireType": 1,
        }
        data = post_json(list_api, payload=payload, headers=headers)
        d = data.get("data") or {}
        got = d.get("list") or d.get("records") or d.get("items") or []
        if not got:
            break
        rows.extend(x for x in got if isinstance(x, dict))
        try:
            total = int(d.get("total") or d.get("totalCount") or 0)
        except Exception:
            total = 0
        if len(got) < page_size or (total and len(rows) >= total):
            break
        page += 1

    out: list[Job] = []
    for row in rows:
        jid = txt(row.get("id") or row.get("jobId"))
        title = txt(row.get("title") or row.get("jobTitle") or row.get("positionName"))
        cities = " / ".join(
            txt(x.get("addressDetail") or x.get("name"))
            for x in (row.get("addressDetailList") or row.get("addressList") or [])
            if isinstance(x, dict) and (x.get("addressDetail") or x.get("name"))
        )
        desc = txt(row.get("description") or row.get("jobDescription") or row.get("jobSummary"))
        req = txt(row.get("jobRequire") or row.get("requirement") or row.get("jobRequirement"))
        detail: dict[str, Any] = {}
        if jid and likely_target_title(title):
            try:
                dd = post_json(
                    detail_api,
                    payload={"id": jid, "channelDetailIds": [1], "hireType": 1},
                    headers=headers,
                )
                detail = dd.get("data") or {}
            except Exception:
                detail = {}
        if detail:
            desc = txt(
                detail.get("description") or detail.get("jobDescription") or
                detail.get("responsibility") or detail.get("jobResponsibility") or desc
            )
            req = txt(
                detail.get("jobRequire") or detail.get("requirement") or
                detail.get("jobRequirement") or detail.get("qualification") or req
            )
        out.append(Job(
            src["company"], title, jid, cities,
            txt(row.get("jobNature") or row.get("projectName") or "2027校园招聘正式岗"),
            txt(row.get("competencyType") or row.get("jobCategory")),
            _strip_html(desc), _strip_html(req),
            f"https://jobs.mihoyo.com/#/campus/position/{jid}" if jid else src["portal"],
            list_api,
            "米哈游官方校园招聘 / 校招渠道 channelDetailIds=1 / 正式岗 hireType=1",
        ))
    return out


def fetch_byd_campus(src: dict) -> list[Job]:
    """Enumerate BYD's complete 2027 formal campus list with retry/bounded pages."""
    root = "https://job.byd.com"
    list_api = root + "/portal/api/portal-api/schoolPortal/queryPositionList"
    detail_api = root + "/portal/api/portal-api/schoolPortal/queryPosition"
    headers = {
        **HEADERS, "Content-Type": "application/json",
        "Origin": root, "Referer": src.get("search_url") or src.get("portal") or root,
    }
    session = requests.Session()
    session.headers.update(headers)
    try:
        session.get(root + "/", timeout=20)
    except Exception:
        pass

    def post_retry(payload: dict) -> Any:
        last: Exception | None = None
        for attempt in range(4):
            try:
                r = session.post(list_api, json=payload, timeout=35)
                r.raise_for_status()
                return r.json()
            except Exception as exc:
                last = exc
                if attempt < 3:
                    time.sleep(1.2 * (attempt + 1))
        raise last or RuntimeError("BYD list request failed")

    rows: list[dict[str, Any]] = []
    page = 1
    page_size = 30
    while page <= 200:
        payload = {
            "topicCode": "", "batch": "2027", "campusNature": "008501",
            "abroad": "", "degree": "", "jobType": [], "researchDirection": [],
            "workPlace": [], "keywords": "", "pageSize": page_size, "pageIndex": page,
        }
        data = post_retry(payload)
        got = data.get("data") if isinstance(data, dict) else None
        if not isinstance(got, list):
            raise RuntimeError("BYD list response data is not a list")
        if not got:
            break
        rows.extend(x for x in got if isinstance(x, dict))
        if len(got) < page_size:
            break
        page += 1

    out: list[Job] = []
    for row in rows:
        outer_id = txt(row.get("id"))
        outer_title = txt(row.get("jobName") or row.get("positionName") or row.get("title"))
        detail_outer: dict[str, Any] = {}
        inner_rows: list[dict[str, Any]] = []
        if outer_id and likely_target_title(outer_title):
            for attempt in range(2):
                try:
                    rr = session.get(
                        detail_api,
                        params={"id": outer_id, "abroad": "", "degree": ""},
                        headers={"Referer": src.get("search_url") or root},
                        timeout=20,
                    )
                    rr.raise_for_status()
                    detail_payload = rr.json()
                    detail_outer = detail_payload.get("data") or {}
                    raw_inner = detail_outer.get("positionInfoList") or []
                    inner_rows = [x for x in raw_inner if isinstance(x, dict)]
                    break
                except Exception:
                    if attempt == 0:
                        time.sleep(0.8)
        if inner_rows:
            for inner in inner_rows:
                inner_id = txt(inner.get("id"))
                title = txt(inner.get("jobName") or inner.get("positionName") or outer_title)
                out.append(Job(
                    src["company"], title, f"{outer_id}:{inner_id}" if inner_id else outer_id,
                    txt(inner.get("workPlace") or detail_outer.get("workPlace") or row.get("workPlace")),
                    "比亚迪2027校园招聘正式岗",
                    txt(inner.get("jobType") or detail_outer.get("jobType") or row.get("jobType")),
                    _strip_html(inner.get("jobDuty") or inner.get("description")),
                    _strip_html(inner.get("jobRequirements") or inner.get("requirement")),
                    f"{detail_api}?id={outer_id}&abroad=&degree=",
                    list_api,
                    "比亚迪2027届校园招聘 / campusNature=008501 / 全职",
                ))
        else:
            out.append(Job(
                src["company"], outer_title, outer_id,
                txt(row.get("workPlace")), "比亚迪2027校园招聘正式岗",
                txt(row.get("jobType")),
                _strip_html(row.get("jobDuty") or row.get("description")),
                _strip_html(row.get("jobRequirements") or row.get("requirement")),
                f"{detail_api}?id={outer_id}&abroad=&degree=" if outer_id else src["portal"],
                list_api,
                "比亚迪2027届校园招聘 / campusNature=008501 / 全职",
            ))
    return out


def fetch_ashby_official(src: dict) -> list[Job]:
    """Enumerate an official Ashby hosted board through its anonymous GraphQL API."""
    board = txt(src.get("ashby_board_name"))
    if not board:
        path = urlparse(src.get("portal") or "").path.strip("/")
        board = path.split("/")[0] if path else ""
    if not board:
        raise RuntimeError("Ashby board name missing")

    api = "https://jobs.ashbyhq.com/api/non-user-graphql?op=ApiJobBoardWithTeams"
    query = """
    query ApiJobBoardWithTeams($organizationHostedJobsPageName: String!) {
      jobBoard: jobBoardWithTeams(organizationHostedJobsPageName: $organizationHostedJobsPageName) {
        teams { id name externalName parentTeamId }
        jobPostings {
          id title teamId locationId locationName workplaceType employmentType
          secondaryLocations { locationId locationName }
        }
      }
    }
    """
    payload = post_json(
        api,
        payload={
            "operationName": "ApiJobBoardWithTeams",
            "variables": {"organizationHostedJobsPageName": board},
            "query": query,
        },
        headers={"Referer": f"https://jobs.ashbyhq.com/{board}"},
    )
    job_board = (payload.get("data") or {}).get("jobBoard") or {}
    rows = job_board.get("jobPostings") or []
    if not isinstance(rows, list):
        raise RuntimeError("Ashby public board returned no jobPostings list")

    team_names = {
        txt(t.get("id")): txt(t.get("externalName") or t.get("name"))
        for t in (job_board.get("teams") or []) if isinstance(t, dict)
    }
    out: list[Job] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        jid = txt(row.get("id"))
        title = txt(row.get("title"))
        # The board list is the exhaustive source of truth. For target-like
        # postings, the public detail page supplies eligibility/JD text and is
        # already the first-party evidence URL retained by the persistent index.
        description = ""
        if jid and likely_target_title(title):
            try:
                rr = requests.get(
                    f"https://jobs.ashbyhq.com/{board}/{jid}",
                    headers={**HEADERS, "Referer": f"https://jobs.ashbyhq.com/{board}"},
                    timeout=TIMEOUT,
                )
                if rr.ok:
                    description = _strip_html(rr.text)
            except Exception:
                pass
        out.append(Job(
            src["company"], title, jid, txt(row.get("locationName")),
            txt(row.get("employmentType") or "当前官方招聘"),
            team_names.get(txt(row.get("teamId")), ""),
            description, "",
            f"https://jobs.ashbyhq.com/{board}/{jid}" if jid else src.get("portal") or "",
            api,
            "Ashby 当前公开职位池；目标岗位正文用于核验 new-grad / graduate eligibility",
        ))
    return out


def fetch_hikvision_campus(src: dict) -> list[Job]:
    """Enumerate Hikvision's current graduate pool through its first-party campus API."""
    root = "https://mcampus.hikvision.com"
    batch_api = root + "/api/userfacade/crsBatch/findBatchAll"
    list_api = root + "/api/search/crsPositionSearch/getPositionByQuery"
    headers = {
        **HEADERS,
        "Referer": root + "/#/position?activeTab=0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": root,
    }
    batch_id = txt(src.get("hikvision_batch_id"))
    batch_data: Any = {}
    if not batch_id:
        batch_data = get_json(batch_api, params={"jobNature": "应届生"}, headers=headers)
    def walk_batches(v: Any) -> list[dict[str, Any]]:
        found: list[dict[str, Any]] = []
        if isinstance(v, dict):
            if any(k in v for k in ("batchId", "id")) and any(
                "2027" in txt(v.get(k)) for k in ("batchName", "name", "title", "batchDesc")
            ):
                found.append(v)
            for x in v.values():
                found.extend(walk_batches(x))
        elif isinstance(v, list):
            for x in v:
                found.extend(walk_batches(x))
        return found
    batches = walk_batches(batch_data) if not batch_id else []
    if not batch_id and batches:
        first_batch = batches[0]
        batch_id = txt(first_batch.get("batchId") or first_batch.get("id"))
    if not batch_id:
        # Current official browser discovery exposed this endpoint; if the API
        # omits the year label, fall back to the first active batch object.
        def first_id(v: Any) -> str:
            if isinstance(v, dict):
                for k in ("batchId", "id"):
                    if v.get(k):
                        return txt(v.get(k))
                for x in v.values():
                    got = first_id(x)
                    if got:
                        return got
            elif isinstance(v, list):
                for x in v:
                    got = first_id(x)
                    if got:
                        return got
            return ""
        batch_id = first_id(batch_data)
    if not batch_id:
        raise RuntimeError("Hikvision current graduate batchId missing")

    def rows_from(payload: Any) -> tuple[list[dict[str, Any]], int]:
        if not isinstance(payload, (dict, list)):
            return [], 0
        candidates: list[list[dict[str, Any]]] = []
        totals: list[int] = []
        def walk(v: Any) -> None:
            if isinstance(v, dict):
                for k in ("total", "count", "totalCount"):
                    try:
                        if v.get(k) is not None:
                            totals.append(int(v.get(k)))
                    except Exception:
                        pass
                for x in v.values():
                    walk(x)
            elif isinstance(v, list):
                ds = [x for x in v if isinstance(x, dict)]
                if ds and any(
                    any(key in x for key in ("positionName", "postName", "jobName", "positionId", "postAdSn"))
                    for x in ds
                ):
                    candidates.append(ds)
                for x in v:
                    walk(x)
        walk(payload)
        rows = max(candidates, key=len) if candidates else []
        return rows, max(totals) if totals else 0

    out: list[Job] = []
    seen: set[str] = set()
    page = 1
    while page <= 100:
        form = {
            "pageNum": page, "pageSize": 100, "keyWord": "",
            "jobNature": "应届生", "batchId": batch_id,
            "postAdSnList": "", "workPlaces": "", "adNeedDept": "", "interviewMethodList": "",
        }
        data = post_form(list_api, data=form, headers=headers)
        rows, total = rows_from(data)
        if not rows:
            exhausted = True
            break
        for j in rows:
            jid = txt(j.get("positionId") or j.get("postAdSn") or j.get("id"))
            key = jid or (txt(j.get("positionName") or j.get("postName") or j.get("jobName")) + "|" + txt(j.get("workPlace")))
            if key in seen:
                continue
            seen.add(key)
            title = txt(j.get("positionName") or j.get("postName") or j.get("jobName") or j.get("name"))
            out.append(Job(
                src["company"], title, jid,
                txt(j.get("workPlace") or j.get("workPlaces") or j.get("location")),
                "【2027校园招聘】应届生", txt(j.get("departmentName") or j.get("adNeedDept") or j.get("department")),
                _strip_html(j.get("description") or j.get("positionDescription") or j.get("duty")),
                _strip_html(j.get("requirement") or j.get("jobRequirement") or j.get("qualification")),
                src.get("search_url") or root + "/#/position?activeTab=0",
                list_api,
                "海康威视官方 2027 校园招聘 / 应届生",
            ))
        if len(rows) < 100 or (total and page * 100 >= total):
            break
        page += 1
    return out


def _decode_js_string(value: str) -> str:
    try:
        return json.loads(f'"{value}"')
    except json.JSONDecodeError:
        return value


def fetch_meitu_campus_html(src: dict) -> list[Job]:
    """Enumerate Meitu's server-rendered campus filter page page-by-page."""
    session = requests.Session()
    session.headers.update(HEADERS)
    pattern = re.compile(
        r'jobId\\":\\"(?P<job_id>[^\\"]+)\\"'
        r',\\"title\\":\\"(?P<title>.*?)\\"'
        r',\\"departmentName\\":\\"(?P<department>.*?)\\"'
        r',\\"locations\\":\\"(?P<locations>.*?)\\"'
        r',\\"publishedAt\\":\\"(?P<published_at>.*?)\\"'
        r',\\"modeName\\":\\"(?P<mode_name>.*?)\\"'
        r',\\"siteId\\":\\"(?P<site_id>[^\\"]+)\\"',
        flags=re.S,
    )
    out: list[Job] = []
    seen: set[str] = set()
    for page in range(1, 101):
        url = f"https://hr.meitu.com/?page={page}&recruitmentType=campus"
        r = session.get(url, timeout=30)
        r.raise_for_status()
        items = [m.groupdict() for m in pattern.finditer(r.text)]
        if page == 1 and not items:
            text_body = _strip_html(r.text)
            if re.search(r"(暂无职位|没有职位|0\\s*个职位|0\\s*jobs?)", text_body, re.I):
                return []
            raise RuntimeError("Meitu campus HTML contained no parseable job records")
        for item in items:
            jid = _decode_js_string(item["job_id"])
            if not jid or jid in seen:
                continue
            seen.add(jid)
            title = _decode_js_string(item["title"])
            out.append(Job(
                src["company"], title, jid,
                _decode_js_string(item["locations"]).replace(" / ", " / "),
                "美图官方校园招聘",
                _decode_js_string(item["department"]),
                title, "",
                f"https://hr.meitu.com/?page=1&keyword={requests.utils.quote(title)}&recruitmentType=campus",
                url,
                _decode_js_string(item["mode_name"]) or "美图官方校园招聘",
            ))
        if len(items) < 10:
            break
    return out


def _find_position_rows_and_total(payload: Any) -> tuple[list[dict[str, Any]], int | None]:
    candidates: list[list[dict[str, Any]]] = []
    totals: list[int] = []
    def walk(v: Any) -> None:
        if isinstance(v, dict):
            for k in ("total", "totalCount", "count", "recordsTotal"):
                try:
                    if v.get(k) is not None:
                        totals.append(int(v.get(k)))
                except Exception:
                    pass
            for x in v.values():
                walk(x)
        elif isinstance(v, list):
            ds = [x for x in v if isinstance(x, dict)]
            if ds and any(
                any(k in x for k in ("positionName", "jobName", "postName", "title", "positionId", "jobId"))
                for x in ds
            ):
                candidates.append(ds)
            for x in v:
                walk(x)
    walk(payload)
    rows = max(candidates, key=len) if candidates else []
    return rows, (max(totals) if totals else None)


def fetch_midea_campus_api(src: dict) -> list[Job]:
    """Enumerate Midea's current school project through the official position API."""
    root = "https://newpower.midea.com"
    api = root + "/backend/school/position/common/position/list"
    project_rule_id = txt(src.get("midea_project_rule_id"))
    if not project_rule_id:
        raise RuntimeError("Midea project_rule_id missing")
    session = requests.Session()
    session.headers.update({
        **HEADERS, "Content-Type": "application/json",
        "Origin": root, "Referer": root + "/schoolOut/post",
    })
    out: list[Job] = []
    seen: set[str] = set()
    page_size = 20
    covered = 0
    total = None
    exhausted = False
    for page in range(1, 101):
        body = {
            "keyword": None, "superiorIds": [], "recruitCategoryIds": [],
            "workPlaceCodes": [], "projectRuleId": project_rule_id,
            "pageIndex": page, "pageSize": page_size,
        }
        r = session.post(api, json=body, timeout=30)
        r.raise_for_status()
        payload = r.json()
        rows, page_total = _find_position_rows_and_total(payload)
        if page_total is not None:
            total = max(total or 0, page_total)
        if page == 1 and not rows:
            if total == 0:
                return []
            raise RuntimeError("Midea position response contained no recognizable list/zero total")
        if not rows:
            exhausted = True
            break
        for j in rows:
            jid = txt(j.get("positionId") or j.get("jobId") or j.get("id"))
            title = txt(j.get("positionName") or j.get("jobName") or j.get("postName") or j.get("title"))
            key = jid or title
            if not key or key in seen:
                continue
            seen.add(key)
            out.append(Job(
                src["company"], title, jid,
                txt(j.get("workPlace") or j.get("workPlaceName") or j.get("location")),
                "美的官方校园招聘",
                txt(j.get("departmentName") or j.get("categoryName") or j.get("jobType")),
                _strip_html(j.get("description") or j.get("jobDuty") or j.get("responsibility")),
                _strip_html(j.get("requirement") or j.get("jobRequirement") or j.get("qualification")),
                src.get("search_url") or root + "/schoolOut/post",
                api,
                "美的集团当前官方校园招聘",
            ))
        covered += len(rows)
        if (total is not None and len(out) >= total) or len(rows) < page_size:
            exhausted = True
            break
    if (total is not None and len(out) < total) or not exhausted:
        raise RuntimeError(f"Midea list incomplete: unique={len(out)}, advertised={total}")
    return out


FETCHERS: dict[str, Callable[[dict], list[Job]]] = {
    "alibaba_campus_api": fetch_alibaba_campus,
    "ant_2027_api": fetch_ant_2027,
    "ashby_official": fetch_ashby_official,
    "baidu_api": fetch_baidu,
    "beisen_direct": fetch_beisen_direct,
    "bilibili_api": fetch_bilibili_2027,
    "byd_campus_api": fetch_byd_campus,
    "bytedance_api": fetch_bytedance,
    "ctrip_2027_api": fetch_ctrip_2027,
    "feishu_direct": fetch_feishu_direct,
    "hikvision_campus_api": fetch_hikvision_campus,
    "honor_2027_api": fetch_honor_2027,
    "huawei_api": fetch_huawei_2027,
    "iflytek_2027_api": fetch_iflytek_2027,
    "jd_campus_api": fetch_jd_campus,
    "kuaishou_api": fetch_kuaishou,
    "lenovo_api": fetch_lenovo,
    "meitu_campus_html": fetch_meitu_campus_html,
    "meituan_campus_api": fetch_meituan_campus,
    "midea_campus_api": fetch_midea_campus_api,
    "mihoyo_campus_api": fetch_mihoyo_campus,
    "netease_api": fetch_netease,
    "oppo_campus_api": fetch_oppo_campus,
    "pdd_campus_api": fetch_pdd_campus,
    "sf_campus_api": fetch_sf,
    "tencent_campus_api": fetch_tencent_campus,
    "vivo_2027_api": fetch_vivo_2027,
    "xiaohongshu_2027_api": fetch_xiaohongshu_2027,
    "xiaomi_api": fetch_xiaomi,
}
