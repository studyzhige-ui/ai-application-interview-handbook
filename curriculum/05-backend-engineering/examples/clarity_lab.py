"""精修章节的可观察逻辑模型，不连接 Redis、OAuth 服务或负载均衡器。

VersionedReadModel 以顺序调用表达已经成立的权威提交与不可变版本规则。
它不实现分布式事务、权限服务、数据库复制或并发故障切换。
"""
from __future__ import annotations

import base64
from bisect import bisect_left
from dataclasses import dataclass
import hashlib
import re
from typing import Mapping


class SourceUnavailable(RuntimeError):
    """不能取得本次读取所需的权威依据。"""


@dataclass(frozen=True)
class Revision:
    tenant: str
    doc_id: str
    version: int


class VersionedReadModel:
    """单线程时序模型：版本查询每次访问权威 heads，不缓存当前指针。"""

    def __init__(self) -> None:
        self.heads: dict[tuple[str, str], tuple[int, bool]] = {}
        self.bodies: dict[Revision, str] = {}
        self.cache: dict[Revision, tuple[Revision, str]] = {}
        self.head_available = True
        self.body_available = True
        self.cache_available = True

    def publish(self, key: Revision, content: str | None) -> None:
        """一次调用代表数据库已原子提交；None 表示本修订是删除墓碑。"""
        old = self.heads.get((key.tenant, key.doc_id))
        if not key.tenant or not key.doc_id or key.version <= 0:
            raise ValueError("版本身份无效")
        if old is not None and key.version <= old[0]:
            raise ValueError("修订号必须递增，不可复用")
        if content is not None:
            self.bodies[key] = content
        self.heads[key.tenant, key.doc_id] = (key.version, content is None)

    def select_revision(self, tenant: str, doc_id: str) -> Revision:
        if not self.head_available:
            raise SourceUnavailable("权威版本不可确认，不返回任意旧缓存")
        version, deleted = self.heads[tenant, doc_id]
        if deleted:
            raise KeyError("文档已删除")
        return Revision(tenant, doc_id, version)

    def fill(self, expected: Revision, actual: Revision, content: str) -> None:
        if expected != actual:
            raise ValueError("不能把旧版本内容标成所选新版本")
        previous = self.cache.get(expected)
        if previous is not None and previous != (actual, content):
            raise ValueError("同一版本的已发布内容不可改写")
        if self.cache_available:
            self.cache[expected] = (actual, content)

    def read_selected(self, selected: Revision) -> tuple[int, str]:
        """读取已选版本；不声称在返回瞬间重新检查最新版本或权限。"""
        cached = self.cache.get(selected) if self.cache_available else None
        if cached is not None:
            actual, content = cached
            if actual != selected:
                raise ValueError("缓存身份不符")
            return selected.version, content
        if not self.body_available:
            raise SourceUnavailable("所选版本正文不可用")
        content = self.bodies[selected]  # 缺失则失败，不回退到别的版本
        self.fill(selected, selected, content)
        return selected.version, content

    def read_current(self, tenant: str, doc_id: str) -> tuple[int, str]:
        selected = self.select_revision(tenant, doc_id)
        return self.read_selected(selected)


def s256_challenge(verifier: str) -> str:
    """RFC 7636 的单项变换；不实现授权码绑定、OAuth 回调或令牌端点。"""
    if not re.fullmatch(r"[A-Za-z0-9._~-]{43,128}", verifier):
        raise ValueError("verifier 格式不符合 RFC 7636")
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def ring_owner(position: int, nodes: Mapping[str, int], size: int = 100) -> str:
    """按人为给定的位置顺时针选择，不包含真实哈希、虚拟节点或数据迁移。"""
    if size <= 0 or not 0 <= position < size or not nodes:
        raise ValueError("环或键位置无效")
    ordered = sorted((p, name) for name, p in nodes.items())
    points = [p for p, _ in ordered]
    if len(set(points)) != len(points) or any(not 0 <= p < size for p in points):
        raise ValueError("节点位置必须在环内且不重复")
    index = bisect_left(points, position) % len(points)
    return ordered[index][1]


def main() -> None:
    store = VersionedReadModel()
    v7, v8 = Revision("team-a", "doc-42", 7), Revision("team-a", "doc-42", 8)
    store.publish(v7, "旧正文")
    old_reader = store.select_revision("team-a", "doc-42")
    store.publish(v8, "新正文")
    store.read_selected(v8)
    store.cache.clear()
    store.fill(old_reader, v7, "旧正文")
    print("迟到回填后的新读取:", store.read_current("team-a", "doc-42"))
    before = {"A": 20, "B": 60, "C": 90}
    after = {**before, "D": 50}
    print("键 40 的去向:", ring_owner(40, before), "->", ring_owner(40, after))
    print("键 95 的去向:", ring_owner(95, before), "->", ring_owner(95, after))


if __name__ == "__main__":
    main()
