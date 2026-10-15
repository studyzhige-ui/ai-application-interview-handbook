# JD 自动采集与离线校验

岗位库现在使用 GitHub Actions 维护官方来源的**增量采集层**，不再依赖 Dot、ChatGPT Pro 或额外付费模型 API。采集和语义审核分开：代码负责发现官方职位池变化、保存原文证据、维护身份/正文指纹和待审队列；`official-jds.json` 仍只保存完成完整 JD 语义审核后确认与 AI Agent / AI 应用开发相关的岗位。

## 1. 自动流程

`.github/workflows/sync-official-2027-agent-jobs.yml` 每周二、周五 `01:00 UTC` 自动执行，也支持手动触发。69 个已登记公司/品牌入口按固定规则分为 16 个 shard 并行扫描，使用 GitHub-hosted Ubuntu，不依赖本地 self-hosted runner。

每个来源都有独立的页数、岗位数和墙钟时间上限。本轮默认上限为每来源 200 页、10000 个岗位/详情、900 秒。来源失败不会中断其余来源；原始 JSON/HTML、请求记录和逐来源结果作为 GitHub Actions artifact 保留 14 天。

扫描结束后只更新三个操作文件：

- `../01-data/automation/scan-state.json`：上一次已观察到的官方职位身份与正文指纹基线。
- `../01-data/automation/review-queue.json`：累计待审的新增、正文变化和“完整扫描中可能消失”事件。
- `../02-analysis/automation-status.md`：最近一次运行的来源状态和事件汇总。

首次成功观察某个来源时只建立基线，不把该公司已有的几百或几千个岗位全部误报为“新增”。之后只有新身份、已知身份正文/字段指纹变化，或一次明确完整的扫描中身份消失才生成事件。非完整扫描、403、登录要求、超时、WAF 和适配器失败都不会触发删除判断，旧基线继续保留。

待审队列中的 `triage` 只是排序提示：Agent、LLM/RAG、评测和工程词会提高优先级，但**任何关键词都不直接决定岗位是否进入正式库**。所有检测到的变化都会保留，最终仍按完整职责和任职要求判断。

自动工作流只提交上述操作状态，不直接改写 `official-jds.json`、`bytedance-jds.json`、`source-observations.json`、`岗位JD.md` 或课程分析。这样一次错误抓取不会污染正式岗位库。

## 2. 本地离线检查

从仓库根目录运行：

```sh
python -B market/job-description/04-scripts/jd.py
python -B market/job-description/04-scripts/jd.py sources
python -B market/job-description/04-scripts/jd.py check
```

无参数只显示可用入口；`sources` 列出 69 个登记来源；`check` 完全离线，校验正式岗位库、来源登记、自动化状态结构、测试、Node 语法和浏览器 fixture。检查需要 Python 3.12+ 和 Node 22+。

## 3. 手动采集单个或少量来源

安装网络采集依赖：

```sh
python -m pip install -r market/job-description/04-scripts/requirements.txt
npm install --no-save playwright@1.55.0
npx playwright install chromium
```

然后显式给出来源和边界：

```sh
python -B market/job-description/04-scripts/jd.py collect \
  --enable-code-collection \
  --source-id official-004 \
  --max-pages 5 \
  --max-jobs 100 \
  --timeout-seconds 300 \
  --output-dir /tmp/jd-manual-unique-run
```

`collect` 永远写入新的输出目录，不覆盖正式快照，不执行语义分类，也不提交 Git。可重复 `--source-id` 采集少量登记来源。所有边界按单来源计算，失败和截断均保存为非完整状态。

`.github/workflows/discover-official-2027-portals.yml` 现在是同一能力的手动 GitHub 诊断入口：输入一个 `source_id` 即可在 GitHub-hosted runner 上复现采集并下载 artifact。它不定时运行，也不发布数据。

## 4. 自动化内部命令

定时 workflow 使用：

```sh
python -B market/job-description/04-scripts/jd.py scan \
  --shard-index 0 --shard-count 16 \
  --max-pages 200 --max-jobs 10000 --timeout-seconds 900 \
  --output-dir /tmp/jd-scan/shard-0

python -B market/job-description/04-scripts/jd.py reconcile \
  --input-dir /tmp/jd-scans \
  --state-file market/job-description/01-data/automation/scan-state.json \
  --queue-file market/job-description/01-data/automation/review-queue.json \
  --report-file market/job-description/02-analysis/automation-status.md
```

`scan` 负责传输；`reconcile` 负责机械 diff。两者都不做岗位语义纳入判断。

## 5. 69 个入口和特殊来源

来源登记仍在 `../03-strategy/official-2027-campus-sources.json`。当前适配器包括公司专用官方 API、Moka、飞书招聘、北森/Zhiye、Ashby、浏览器动态页以及小米、字节等专用实现。官网改版后，某个适配器可能变成 `BLOCKED` / `PARTIAL` / `INCOMPLETE`；这代表需要维护采集契约，不代表该公司没有岗位。

金山办公/WPS（`official-018`）当前公开 `jobs/v2` 接口已验证可以匿名读取校园职位池，自动任务不再依赖运行时 source parameter 或仓库 Secret。适配器仍保留“显式私密参数模式”的隔离与脱敏测试，用于未来官网若重新要求该参数时安全恢复，但默认自动采集不会读取或保存这类参数。

BOSS直聘/看准科技（`official-065`）仍保留明确的安全验证边界；如果固定官方入口无法可靠提取职位，记录为受限，不通过绕过 WAF、登录或验证码来制造“完整扫描”。

## 6. 发布安全

自动 workflow 在采集结束后先运行完整 `jd.py check` 和 `git diff --check`。只有工作流启动时的 `main` SHA 仍然是远端最新 `main` 时，才提交三个生成状态文件；若期间人工提交改变了 `main`，本次 raw artifacts 保留，但跳过写回，下一轮从新 `main` 重新扫描。这样不会用旧扫描覆盖人工更新。


## 7. ChatGPT 定时语义审计

仓库通过 `01-data/automation/audit-batch.json` 向 ChatGPT 定时任务暴露一个有界小批次，而不是让模型每轮搬运整个多 MB 的 `review-queue.json`。模型必须逐条阅读批次中的完整职责与任职要求，只输出 `include`、`exclude`，以及针对已确认消失事件的 `remove` 决策。即使缺失完整 JD、招聘类型不明确或抓到了列表筛选项，也必须说明证据缺口并判定为不予入库（`exclude`），不再输出无限期的 `needs_review`。

ChatGPT 只写 `01-data/automation/audit-decisions.json`。随后 `.github/workflows/apply-jd-semantic-audit.yml` 机械应用结果：更新队列审核状态；对通过审核的岗位写入正式 `official-jds.json`（字节跳动写入其哈希固定分片）；对不再符合范围或已确认消失的正式岗位执行移除；重新生成 `岗位JD.md`；最后运行完整 `jd.py check` 与 `git diff --check` 后才提交。

批次按高、中、低 triage 顺序消费，但 triage 仍只负责排序，不能代替完整 JD 语义判断。已经审核且事件指纹未变化的岗位不会重复进入批次；正文发生变化时会生成新的事件并重新审核。

## 8. 终审准入与证据缺口

审核输出必须是 **`include` / `exclude`**（确认岗位已下线时可用 `remove`），不再接受新的 `needs_review`。只有取得完整官方 JD、核验具体校招/实习资格、并确认职责中有可交付的 AI 应用/Agent/LLM/RAG/AI 平台或测试评测工具工程工作，才允许 `include`。

拿不到完整 JD、抓取内容实际上只是地区/职位类别、无法确认属于当前校招/实习批次，均作出明确的 **`exclude` 入库决定**，在 `decision_reason` 里注明“完整 JD 缺失”“非具体职位”“非目标招聘批次”等具体缺口，而不是伪称该岗位技术上不相关。拒绝的审计事件保留历史记录，若官方发布实质改变的完整 JD，扫描会产生新的事件，允许重新进行一次独立语义判断；同一旧事件不能无限重复审核。

历史复核的逐项结论见 [63 条专项终审台账](../02-analysis/needs-review-followup-2026-10-15.md)。此前 `needs_review` 的历史记录仍完整保留审计轨迹，但已由受控复核批次全部终审清零。
