# 全仓外围导航同步｜2026-09-27

## 基线与职责

LLM Foundation 精修已通过 PR #30 合并到 `fe288e14b14930ebed4164f7fff90dec8207facf`。外围同步从这一基线开始；发布前又纳入 `e36d24ecd32f5827ae538dfa1f11b566186f891a` 中并行提交的 Vector DB 精修，并重新生成索引。

本次检查全部 61 份 README，以及知识地图、学习路线、术语表和新增资源索引，共 65 个外围页面。当前课程为 10 个模块、175 篇正式正文；Products 为四组、16 篇专题正文，Coding 为9篇正文，References 有8个实际资料目录。后三类不并入 Curriculum 章节数。

## 已同步内容

根目录、知识地图和模块入口统一推荐学习顺序：Python、FastAPI、MySQL、Redis、Backend、Vector DB、LLM Foundation、RAG、Agent、System Design。目录数字仍是稳定路径标识，不按学习顺序重命名。

知识地图更新模块职责与内部主线，保留旧标题的锚点别名；学习路线的181篇改为175篇；References 补齐 MySQL、Redis。产品总入口从各模块读取固定快照，并明确 Claude Code 私有学习镜像的访问与发行版本边界。项目及审计入口补齐尚未列出的专项记录，包括新合并的 Vector DB 修订。

累计同步16个外围文件或生成索引，具体清单见同名 JSON 的 `all_synchronized_pages`。正确的 README 保留，不为增加修改量重写。历史审查原文、Market、冻结 Canonical、题目归属与来源计数保持原样；课程正文、产品专题、练习和实验实现也没有被此次外围同步修改。

## 统一来源与防漂移

`tools/sync_outer_navigation.py` 从学习顺序配置、模块 README 和实际章节生成 `guide/navigation-index.json` 与阅读索引，并同步外围页。默认只预览；`--apply` 才写入允许范围，`--check` 检查漂移。重复执行不产生新改动。

旧的仓库语义检查把 MySQL、Redis 的目录序号、英文计数标签和质量图标写死。本轮改为按 `guide/learning-order.json` 验证全部十个模块的标题顺序和实际章节数，保留原有冻结证据与章节完整性校验。

新增 `.github/workflows/validate-navigation.yml` 仅有读取权限，在 PR 和 main 上检查导航漂移及回归测试。用于本次同步的临时写入工作流与初始清点文件不进入最终 main。

## 实际验证

完整工作树使用 Python 3.12.3 运行：外围同步回归14项、原学习顺序回归6项、LLM标准库数值测试36项，均通过。全仓结构/链接检查和语义检查通过。

外围检查覆盖1,127个本地链接，缺失目标、无法解析的锚点和冲突标记均为0；再次运行没有待同步改动。与最新 main 对比，课程正文、产品专题、Market及冻结 Canonical 的差异为0。机器记录保存在 `outer-navigation-sync-2026-09-27.json`，区分最后一轮变动与累计同步清单。

## 验证边界

这些结果证明的是本次导航、结构、保留范围和数值测试，不是全模块的初学者阅读验收。本次不运行真实模型、数据库集成、GPU训练或生产实验，也未重做浏览器/手机实机渲染；不把历史 PASS 改写成当前验证。最终发布状态以 PR 合并及 main 回读为准。
