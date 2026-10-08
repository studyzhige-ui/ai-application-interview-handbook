"""Title-first role scope and eligibility; pure, independently testable rules."""
from __future__ import annotations
import re
from .model import Job
TARGET_TITLE_HINT_RE = re.compile(
    r"(?:agent|智能体|rag|harness|runtime|coding|"
    r"ai\s*(?:应用|全栈|开发|研发|工程|平台|infra|devops|builder|软件|系统|技术|后端|前端)|"
    r"大模型(?:应用|开发|研发|工程|平台)|fde)",
    re.I,
)


def likely_target_title(title: str) -> bool:
    return bool(TARGET_TITLE_HINT_RE.search(title or ""))

def training_heavy(job: Job, signals: list[str]) -> bool:
    title = job.title.lower()
    if any(k in title for k in ["算法", "研究员", "research scientist", "scientist"]):
        return True
    body = " ".join([job.description, job.requirements]).lower()
    hits = {s.lower() for s in signals if s.lower() in body}
    # Protect explicit Agent systems/infra roles that mention training only as
    # surrounding context; generic R&D roles dominated by 2+ training signals
    # are outside this engineering JD library.
    protected = any(k in title for k in ["agent", "智能体", "harness", "runtime", "infra", "ai应用", "ai 应用", "大模型应用", "coding"])
    return (not protected) and len(hits) >= 2

def is_hard_excluded(job: Job, excludes: list[str]) -> bool:
    title = job.title.lower()
    return any(k.lower() in title for k in excludes)


def campusish(job: Job) -> bool:
    s = " ".join([
        job.category, job.cycle_evidence, job.title,
        job.description, job.requirements,
    ]).lower()
    return any(k in s for k in [
        "校招", "校园", "应届", "毕业生", "毕业", "2027",
        "graduate", "campus", "new grad", "new-grad", "new graduate",
        "fresh grad", "fresh graduate", "graduates welcome",
        "new graduates welcome", "应届生优先", "欢迎应届",
    ])


class RoleMatcher:
    def __init__(self, cfg: dict):
        self.keywords = [x.lower() for x in cfg.get("strong_agent_keywords", cfg["agent_keywords"])]
        self.excludes = [x.lower() for x in cfg["hard_exclude_title_keywords"]]
        self.engineering_signals = [x.lower() for x in cfg.get("engineering_title_signals", [])]
        self.body_agent_signals = [x.lower() for x in cfg.get("body_agent_signals", [])]
        self.training_signals = [x.lower() for x in cfg.get("training_heavy_signals", [])]
        self.strict_title_allowlist = {x.lower() for x in cfg.get("strict_title_allowlist", [])}

    def strict_role_title(self, job: Job) -> bool:
        title_lines = (job.title or "").splitlines()
        if not title_lines:
            return False
        title = title_lines[0].strip().lower()
        if not title:
            return False
        body = " ".join([job.category, job.department, job.description, job.requirements]).lower()

        if title in self.strict_title_allowlist:
            return True

        # Formal library requires the job itself to be an engineering role whose
        # title explicitly names the Agent / AI-application system being built.
        explicit = (
            any(k in title for k in self.keywords)
            and any(s in title for s in self.engineering_signals)
        )
        if explicit:
            return True

        # AI-qualified FDE titles are explicit AI engineering roles. Generic FDE
        # titles still require first-party JD evidence of Agent/RAG/application work.
        body_hits = {k for k in self.body_agent_signals if k in body}
        if "fde" in title and any(k in title for k in ("ai", "大模型", "智能体", "agent")):
            return True
        if "fde" in title and len(body_hits) >= 2:
            return True
        if any(k in title for k in ("大模型研发工程师", "大模型开发工程师")) and any(
            k in body for k in ("agent", "智能体", "rag", "function calling", "工具调用")
        ):
            return True
        return False

    def target_matches(self, jobs: list[Job], src: dict) -> list[Job]:
        # Official recruiting policy:
        # - campus board: the live board itself is the time gate;
        # - mixed official Careers/ATS board: the JD must explicitly allow new grads.
        # Role scope is intentionally title-first so generic software jobs that merely
        # mention "using AI tools" in boilerplate never enter the formal library.
        explicit_campus_board = bool(src.get("current_campus_board"))
        campus_formal_pool = bool(src.get("campus_formal_pool"))
        matches = [
            j for j in jobs
            if (explicit_campus_board or campusish(j))
            and self.strict_role_title(j)
            and (
                not training_heavy(j, self.training_signals)
                or j.title.splitlines()[0].strip().lower() in self.strict_title_allowlist
            )
            and not is_hard_excluded(j, self.excludes)
            and "实习" not in j.title.lower()
            and "intern" not in j.title.lower()
            and (
                campus_formal_pool
                or (
                    "实习" not in j.category.lower()
                    and "intern" not in j.category.lower()
                )
            )
        ]
        seen = set()
        uniq: list[Job] = []
        for j in matches:
            key = (j.company, j.job_id or j.title, j.location)
            if key in seen:
                continue
            seen.add(key)
            uniq.append(j)
        return uniq
