# 官方岗位业务执行

唯一业务入口是 [jd.py](jd.py)。调用它即可完成离线检查、显式联网采集、快照审计或工作流发布，不再依赖根目录 tools 中的岗位脚本。

## 职责边界

- jd/adapters：仅处理官方 API、浏览器、ATS 请求与响应；保留当前公司配置实际使用的适配器和必要辅助函数，移除未被现行配置调用的旧接口
- jd/model.py 与 jd/matching.py：统一岗位结构、资格和工程岗位范围
- jd/collection.py：公司级并行采集、完整性判定与失败回退
- jd/freshness.py：时间、来源提交和运行 ID 的缓存一致性
- jd/normalize.py：Role Family 归组、每个 Requisition 完整正文、人工种子与未完成采集的事实保留
- jd/state.py：公司持久化岗位状态；只有完整枚举可以清零或更新核验日期
- jd/evidence.py：覆盖当前快照前保存原始字节，防止最新结果取代历史一手事实
- jd/render.py 与 jd/audit.py：完整 JSON / Markdown 呈现及覆盖审计；业务审计不会发起网络请求
- jd/pipeline.py：读取明确输入并串接各步骤；损坏的持久化文件直接失败，不能被空状态覆盖
- jd/publication.py：Windows / Linux 共用的输出发布；整个岗位业务树或工作流发生变化，正在运行的旧结果即作废；不强制推送
- tests：不连接真实网站的回归测试

## 操作约束

现有工作流的每周二、五 UTC 01:00 调度、手动触发、private 仓库 Windows self-hosted / public 仓库 Ubuntu 分流保持。并发组与取消旧运行策略保持。依赖安装、网络访问和发布在 workflow 的相应步骤执行，离线 check 不需要 requests 或 Playwright。

浏览器和 ATS 的输出必须证明完整分页，不能因为发现了岗位、搜索框不可用或请求成功而宣称完整。缓存过期、来自另一来源提交或另一运行时被忽略。可选加速器失败后允许使用可靠的官方替代途径；审计失败不会进入发布步骤。

本轮只进行了离线验证，未重新抓取外部网站，也未验证远端 runner 或真实站点当日可用性。
