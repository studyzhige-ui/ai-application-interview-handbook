# JD 保全与手动采集

代码采集目前关闭。岗位含义、资格判断、归类和选择交给模型；代码只保留原文、来源链接、ID、计数和传输状态。旧的标题/正文关键词过滤、Role Family 合并、摘要改写、公司状态自动更新与自动发布入口已移除。

## 默认离线

从仓库根目录运行：

```sh
python -B market/job-description/04-scripts/jd.py
python -B market/job-description/04-scripts/jd.py sources
python -B market/job-description/04-scripts/jd.py check
```

无参数只说明采集关闭；`sources` 列出已登记来源 ID；`check` 只读校验已存文件的 SHA-256、大小、来源数与链接结构，并运行离线模拟测试和 Node 语法检查。它不联网、不更新快照、不刷新时间、不生成分析。检查需要 Python 3.12+ 和 Node 22+，不需要 requests、Playwright 或 Chromium。

## 以后手动启用

确实需要代码采集时，先安装依赖：

```sh
python -m pip install -r market/job-description/04-scripts/requirements.txt
npm install --no-save playwright@1.55.0
npx playwright install chromium
```

仅浏览器来源需要 Playwright/Chromium；直接 API 来源按实际适配器使用 Python requests 或 Node 内置 fetch。依赖不会在导入或检查时自动安装。

从 `sources` 输出中选择确切 ID，再显式指定全部边界，例如：

```sh
python -B market/job-description/04-scripts/jd.py collect \
  --enable-code-collection \
  --source-id official-004 \
  --max-pages 2 --max-jobs 20 --timeout-seconds 90 \
  --output-dir /tmp/jd-manual-unique-run
```

- 必须提供启用开关、至少一个已登记来源 ID、正数页数、岗位数、超时和新的输出目录。缺项、未知 ID、重复 ID、已存在的输出目录都会拒绝执行。
- 可重复 `--source-id` 指定少量来源。边界按每个来源分别计算；不会默认抓全部公司，也不会扩展为全站抓取。
- `max-pages` 限制列表分页。Python 保留既有有限重试；Node 的列表重试也占页数。`max-jobs` 限制提取记录与详情获取，列表响应本身可能包含更多原始记录，这些原文仍完整保存。
- Python 进程受单来源超时硬限制；Node 在同一期限中止请求后，另有最多 2 秒的退出与保存时间。超时、失败和截断保留为未完成状态，不能解释为无岗位或无目标岗位。
- 仅使用登记的公司官方列表/API/ATS 请求契约与该列表的结构化详情链接；不按标题或正文内容决定是否抓详情。
- 输出到新目录，保留收到的 JSON/HTML 原始响应（Python 为 `.body` 文件；Node 为 base64 原文与 SHA-256）、提取字段、请求/失败记录。Python 会逐步落盘原始响应和岗位，即使被超时终止也保留已收到的部分。
- 结果未经过模型复核，不生成岗位结论，不替换原快照，不更新公司岗位状态，不提交或推送。

适配器仍依赖官网实际请求契约，可能因官网变化、签名或访问限制失败。本次仅用离线 fixture/mock 验证，没有重新抓取官网，也没有据此宣称适配器当前线上可用。

## WPS 来源的手动运行参数

金山办公/WPS（`official-018`）不再保存来源访问参数，也不是开箱可采集的来源。缺少操作者提供的运行时参数时，该来源会在任何网络请求之前明确阻止采集；其他已登记来源不受影响。

日后确需手动启用此来源，由操作者自行确认参数用途，并通过本次进程的环境变量 `JD_MOKA_SOURCE_PARAMETER_OFFICIAL_018` 配置。仍须同时提供启用开关、来源 ID、页数/岗位数/超时和新输出位置。工具不生成参数、不从旧文件或 Git 历史寻找参数，也不接受登记表中的旧值作为回退。不要把值写进仓库、命令行参数、日志或共享配置。

运行时参数只发送到固定的 WPS 官方 Moka 列表接口与租户。请求记录、错误信息、岗位输出和响应存档会去除参数回显；涉及参数的存档明确标记已脱敏。私有来源无法安全检查或未完整收到的响应体不存档，以避免保留部分参数。其他来源继续使用原有原始响应保全方式；已有 JD 快照没有改写。

## 工作流

两个岗位 workflow 只允许手动执行离线检查/来源列表，仍保留 private 仓库 Windows self-hosted、public 仓库 Ubuntu 的原有路由；设置 PYTHONUTF8=1，checkout 不持久化凭据。没有 schedule、push 启动、网络采集、内容写权限或自动发布。日后启用采集使用上面的有界命令，不能只恢复旧的定时同步流程。
