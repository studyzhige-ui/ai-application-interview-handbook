# 岗位需求与官方 JD

保留第一方岗位正文、官方链接、职位 ID、原时间戳与既有公司状态。岗位含义、资格、关联与选择由模型理解；代码仅保留少量保全、链接、计数工具，以及目前关闭的有界手动采集能力。

## 已存材料

- [人工岗位资料](01-data/curated-official-jds.md)
- [原岗位快照 Markdown](01-data/official-2027-agent-jobs.generated.md)与[JSON](01-data/official-2027-agent-jobs.generated.json)
- [原公司岗位状态](01-data/official-company-role-index.md)与[人工第一方线索](01-data/official-first-party-role-seeds.json)
- [登记公司与官方来源](03-strategy/official-2027-campus-sources.json)
- [保存与采集边界](03-strategy/collection-policy.md)

这些是此前采集留下的快照。文件名中的 `generated` 不表示本次重新生成。原正文、URL、ID、状态与时间戳原字节保留；它们可能受旧采集器的筛选范围影响，不能代表整个岗位市场或官网全部职位，也不是新的模型复核结论。旧文件中的“当前”“完整”“0 个目标岗位”和 Role Family 数量均属于当时保存的记录，不据此认定今天的岗位情况。

尚未进行新的模型分析或官网重采集；不伪造分析产物或更新时间。

## 工具

```sh
python -B market/job-description/04-scripts/jd.py check
python -B market/job-description/04-scripts/jd.py sources
```

两条命令均离线只读。代码采集默认关闭，工作流没有定时或 push 自动启动，不会自动发布。以后需要采集时，必须手动指定启用开关、登记来源 ID、页数、岗位数、超时和全新输出目录，详见[操作说明](04-scripts/README.md)。
