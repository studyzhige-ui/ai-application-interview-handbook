# 岗位库：GitHub 采集 → GPT 筛选入库

## 1. GitHub 自动采集

[采集工作流](../../../.github/workflows/sync-official-2027-agent-jobs.yml) 每周二、周五 01:00 UTC 运行，69 个官方入口分 16 个 shard。原始抓取证据保留为 Actions artifact（14 天）；扫描程序只维护官方身份基线、待筛选队列与下一批完整 JD。

GitHub 自动采集不会根据标题或关键词决定入库，也不会因为一次采集失败删除职位。入口受阻会保留失败状态。扫描完成后将最新批次写入 `01-data/automation/audit-batch.json`，供 GPT 读取。

## 2. GPT 筛选后入库

ChatGPT 定时任务读取 `../01-data/automation/audit-batch.json`，逐条审查完整职责、任职要求及校招/实习资格。符合目标岗位的写 `include`，不符合或关键官方证据缺失的写 `exclude`，对确认消失且已在库中的岗位写 `remove`。不能输出 `needs_review`。

GPT **只写** `../01-data/automation/audit-decisions.json`；[入库工作流](../../../.github/workflows/apply-jd-semantic-audit.yml) 将结果一次性用于正式库、岗位索引和数据校验，消费完便清空决策文件，并准备下一批。中间队列中的已处理事件会删除，不再长期积压。无待处理职位时不修改正式库。

## 常用命令

```sh
python -B market/job-description/04-scripts/jd.py sources
python -B market/job-description/04-scripts/jd.py check
```

离线校验需要 Python 3.12 和 Node 22。手动验证单个官方来源：

```sh
python -m pip install -r market/job-description/04-scripts/requirements.txt
npm install --no-save playwright@1.55.0
npx playwright install chromium
python -B market/job-description/04-scripts/jd.py collect \
  --enable-code-collection --source-id official-001 \
  --max-pages 5 --max-jobs 100 --timeout-seconds 300 \
  --output-dir /tmp/jd-one-scan
```

手动采集只输出证据，不改正式库。GitHub Actions 的定时扫描入口、GPT 决策入口及输入输出协议共同组成完整自动维护流程。
