# 岗位数据

[岗位JD.md](岗位JD.md) 是可直接打开官方详情的正式索引。[official-jds.json](official-jds.json) 是正式库；[bytedance-jds.json](bytedance-jds.json) 是字节跳动的同一正式库分片，不是另一套数据库。正式岗位保留官方职位 ID、原文、地点、类别、资格依据和 GPT 的工程职责判断。

[source-observations.json](source-observations.json) 保存非当前观察；[historical-jds.json](historical-jds.json) 保存未重新取得的历史材料，均不计入当前正式岗位数量。

自动运行只需要四个中间文件：

- `automation/scan-state.json`：官方职位的身份与正文指纹，用于下次比较，防止重复抓取和错误删除。
- `automation/review-queue.json`：尚未交给 GPT 作最终判断的新增或变化职位。
- `automation/audit-batch.json`：从队列取出的下一批完整 JD，供 GPT 定时任务读取。
- `automation/audit-decisions.json`：GPT 写回本批纳入、排除或确认下线的结论；GitHub Actions 验证后立即入库并清空收件箱。

**只有两项业务动作：GitHub 采集，GPT 筛选后入库。** 中间 JSON 只是两者交换数据，不代表额外人工审批。只要 JD 未变，不重复审计。网络失败、列表页误抓和不完整详情不会覆盖已有完整正式 JD。
