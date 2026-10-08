# 2026-10-08 两平台登录与9条候选复核

两平台均已实际验证云端登录、站内搜索与原帖读取。9条全部做了所需核验：2条准入S402–S403，7条不满足正式收录条件而排除本批，未尝试/待核验均0。证据不足不等于虚假，独立流程未证不等于重复。

## 更正

- 小红书300017：上轮导航时把相邻帖子的链接参数误配到6a990afd；不是已经证明的平台整体封锁。此次从作者主页直接获取对应原始href后全文正常。 撤销平台持续受限结论，修正访问日志；不复用或手工拼接相邻帖参数。
- 牛客上一轮完整正文计数：yzxcxy的上轮存档HTML是通用页面壳，不足以支持live_full_html。原报5条完整应更正为4条已证实完整。此次原帖明确删除，但不推断删除发生时间。 原报告保留为历史快照并加更正；不把壳页或搜索摘要计为完整原帖。
- 浪潮旧质量hold：旧判据把不确定的两条记录当作整场不收录理由，忽视了6个明确连续技术问题和真人现场。 按既有政策重新独立审核通过；不确定记录仍保留且不进确定题频，不放宽准入。

## 逐条判定

### Zxsoul｜浪潮智能体开发面经

- 结论：admit，S402
- 原帖：https://www.nowcoder.com/feed/main/detail/a8854ce3fa4b45cb8d73ec92c798a63b
- 已完成：Live full original body；One comment: emoji only, no substantive supplement；Author profile: all 15 posts and the no-more-content end marker；Formal raw key, author, title and distinctive wording dedup
- 理由：The source independently meets HUMAN-A without reconstructing ambiguous questions: specific company/Agent role; actual interviewer composition (HR, team member, manager); 20-minute interview; personal reactions and talent-pool outcome; six unambiguous technical prompts forming a RAG project follow-up chain. The policy says usually at least 5–8 informative prompts, not that every original record must be a complete question. The two uncertain records do not invalidate the six usable prompts.

### yzxcxy｜快手3.25日常一面

- 结论：exclude_deleted_original
- 原帖：https://www.nowcoder.com/feed/main/detail/58eb5c0382964b3cb7b28e5d505b3743
- 已完成：Live original navigation；Ordinary page reload；Known author profile
- 理由：The logged-in original explicitly says 来晚一步，该内容已经被删除了o(T_T)o on both navigation and reload. The author profile says 这个牛友还没发布过内容. There is no live body/comment thread left to verify role. Exclude under Verifiable rather than carrying an unattempted hold.

### upc｜字节全栈一面

- 结论：exclude_role_unsubstantiated
- 原帖：https://www.nowcoder.com/feed/main/detail/a01aeac81ad342d88252f899c47f2dc4
- 已完成：Live full original；All 11 comments, including initially collapsed 2 replies；Author profile and related hiring-history titles
- 理由：Body and first-person authenticity are now verified. The author says the department is 中国交易与广告 in a direct reply, but neither body nor comments establish that the full-stack position's core work is AI Service/RAG/Agent. The RAG interview block and personal Agent practice do not establish the job's responsibilities; the author's own question contrasts full-stack and Agent career paths. Exclude because required role evidence is absent, not because the body is inaccessible.

### night_code｜小厂Agent开发面经分享攒人品版

- 结论：exclude_insufficient_first_person_scene
- 原帖：https://www.nowcoder.com/feed/main/detail/24909dbd84b24f23ba18d2e6c8d528b3
- 已完成：Live full original 14 prompts；Sole comment；Complete profile of 6 posts, reaching no-more-content
- 理由：The original has detailed RAG prompts, but only the generic preface 继续来分享下之前的面经 and no identifiable company, interview date/round/duration, candidate reaction/result or direct author account of the live interaction. The sole comment requests an answer and has no author reply. Other profile posts do not identify this particular interview. Thus the candidate-first-person real-scene gate is unsubstantiated; do not infer a genuine source from a plausible question chain.

### dejavu06｜小厂agent面试

- 结论：exclude_insufficient_scene_and_role
- 原帖：https://www.nowcoder.com/feed/main/detail/db1ccb5e509a42d29d14216122b61419
- 已完成：Live full categorized original question list；All 7 original comments, no author replies；Author profile and comment index; nearby dated hiring timeline visible
- 理由：The post contains categories of Java/backend questions and an AI section, but does not provide this interview's candidate reactions, actual dialogue, date/round/result, company identity or actual role duties. All 7 comments are reader reactions rather than author clarification. The profile shows the author has personal hiring experience and also writes tutorials/mock interview material; neither proves that this particular categorized list is a verifiable single real interview. A nearby timeline starts application on May 28, later than this May 25 post, so it cannot silently supply the missing chronology.

### Real｜8.31 字节TikTok Shop AI Agent一面

- 结论：exclude_independent_flow_unsubstantiated
- 原帖：https://www.xiaohongshu.com/explore/6a9641060000000028002c36
- 已完成：原帖全文与全部39条评论及折叠回复；作者公开主页；秋招round1结束原帖；9.14剪映一面全文、20条评论及折叠回复
- 理由：本人/岗位/题目可信，但同作者字节S330剪映流程与本场的独立投递、明确结束重启或转组关系仍未披露。9/8手头无面试仅是个人阶段总结，不证明TikTok流程已正式结束或另起招聘流程。排除本批新增，不断言同场重复，不捏造独立性。

### OSAKO｜AI应用开发一天四面面经

- 结论：exclude_flow_and_role_unsubstantiated
- 原帖：https://www.xiaohongshu.com/explore/6a5f950e00000000060121ce
- 已完成：4/4正文原图已读；置顶第四场二面评论图已展开阅读；31条评论及折叠回复；作者公开主页及近期招聘记录标题
- 理由：候选人真实复盘，但前三场未给可区分雇主/独立投递边界及具体招聘职责；游戏部分作者明确是项目经历，不能当雇主业务。第四场本人说明实际为金融交易后端、Agent由另一部门负责，二面图标题亦为交易后端开发二面。四场不合成一个假流程，不按图片数拆4个来源；整体不满足本批正式收录条件。

### AI起点｜金山软件AI全栈一面

- 结论：exclude_answer_packaging
- 原帖：https://www.xiaohongshu.com/explore/6a9f8102000000000b00d883
- 已完成：8/8原图全文；全部2条评论；作者公开主页定位与置顶/学员反馈标题
- 理由：8图中1图题单、7图逐题标准答案解析；正文仅话题标签，无本场日期/轮次结果/本人互动。主页明确面经、视频及学习路线整理。属于答案化整理材料，不因技术内容具体升级为真人候选人原始场次；不指控作者伪造。

### MeGuMin｜东成集团算法工程师一面（Agent应用方向）

- 结论：admit，S403
- 原帖：https://www.xiaohongshu.com/explore/6a990afd000000002b01d810
- 已完成：从作者主页实时原始href进入；正文、封面与全部2条评论；作者明确回复东成机电；401流程全历史去重与独立审核
- 理由：原帖实际可正常读取。封面一面、作者回复公司、本人Agent平台连续追问及招聘方明确客服/海外售后/企业Code Agent业务，满足本人真实性和应用工程职责。原8/9思路非追加实问；原11重复保留。

## 归档与范围

本次2条追加同日Batch38，正式分支403流程/38批，下一S404；PR49累计新增4流程。保留旧来源所有字节、原题次序与不确定性。两条共24条序列项，其中17条为可计技术问法/主题，不称24道独立技术题。东成原5为本人贡献确认，浪潮LRO推断、HashMap残缺和demo确认等均不贡献技术频率。

market派生按原脚本重建。root interview的10个自动证据块仍因范围未获授权而未同步，完整检查仍有已知失败；没有为清零待核而修改准入政策或验证器。
