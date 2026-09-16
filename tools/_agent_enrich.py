from pathlib import Path
import re, subprocess
ROOT=Path(__file__).resolve().parents[1]
BEFORE='2fbd42e65940b961e6c2edb17bc87940feb028ff'
review=ROOT/'agent/review/README.md'; t=review.read_text()
visual='''## 机制局部图｜放大同一张四层图，不是另一套架构

吸收main原Review的七种机制图，按新版职责重新组织。先自行画，再展开对照；不把Memory当作权威事实，不把安全链路再命名为一套“架构四层”。

<details>
<summary>局部图1｜运行层怎样把候选决策变成闭环（04章）</summary>

```text
目标/约束 → Context → 模型候选
                      ├─ 行动 → 校验/授权 → 工具执行 → 观察/状态 → 继续
                      ├─ 缺输入/批准 → 暂停并持久化
                      └─ 完成候选 → 独立验收 → 交付或返回缺口
```

达到预算只是有原因的停止，不是成功。回到[04执行控制](../docs/04-AgentLoopAndControl.md)。

</details>

<details>
<summary>局部图2｜信息从哪里来，什么是事实、什么是投影（05–07章）</summary>

```text
任务契约/可信策略 + Runtime状态/回执 + 外部权威事实
                         ↓ 受控选择与版本核验
历史记录 + 相关Memory + 检索证据 + Tool结果/Artifact引用
                         ↓ 去重、预算、适配
                     当前模型Context
```

Memory可能有错，History记录的是过去，Context是本轮视图；三者都不能自动覆盖权威事实和当前授权。回到[05上下文](../docs/05-ContextEngineering.md)、[06记忆](../docs/06-MemoryLifecycle.md)、[07状态](../docs/07-StateAndRecovery.md)。

</details>

<details>
<summary>局部图3｜长任务在什么窗口会重复动作（07、11章）</summary>

```text
建立逻辑操作身份/保存意图
→ 校验授权与前置条件 → 提交外部动作
→ 取得回执 → 保存结果/检查点 → 继续

中途崩溃 → 读取恢复状态 → 核对未知操作
          → 已成功则补状态；安全可重放才重试；不可核对则UNKNOWN/人工
```

这是恢复协议示意，不是跨系统原子事务或exactly-once保证。回到[07恢复](../docs/07-StateAndRecovery.md)、[11副作用](../docs/11-ToolExecutionAndEffects.md)。

</details>

<details>
<summary>局部图4｜能力怎样被发现而不被过度暴露（09–12章）</summary>

```text
L2当前需求/预算
→ L3完整能力目录 → 权限/环境/任务筛选
→ 候选发现 → 按需加载完整契约 → 版本解析与调用
→ L4真实资源返回 → 结果校验 → L2后续决策
```

Tool是动作接口，MCP是连接协议，Skill是知识/资源包，Hook是生命周期点；目录收录或模型可见都不等于实际授权。回到[10发现](../docs/10-ToolContractAndDiscovery.md)、[12扩展](../docs/12-KnowledgeAndCapabilityAccess.md)。

</details>

<details>
<summary>局部图5｜多Agent怎样分工与收口（08章）</summary>

```text
父级任务契约/总预算
 ├─ 子A：范围/资源/截止时间 → 证据/产物/状态
 └─ 子B：范围/资源/截止时间 → 证据/产物/状态
                         ↓
           冲突核对 + 汇聚 + 最终验收
```

共享写入还需所有权、隔离或版本协调；子任务成功不能覆盖整体未完成，委派也不能放大权限。回到[08协作](../docs/08-MultiAgentCoordination.md)。

</details>

<details>
<summary>局部图6｜安全约束落在哪些执行点（13–14章）</summary>

```text
L1可信身份与明确确认范围
→ L2维护契约/审批状态，区分指令与不可信资料
→ L3每次调用校验参数、权限、版本与凭证范围
→ L4资源授权及适用的文件/网络/进程隔离
→ 输出/Artifact/Trace访问与外传控制
```

这是一条横跨既有四层的责任链，不是“安全四层”新架构。事后过滤不能撤销已发生的副作用。回到[13环境](../docs/13-ResourcesAndEnvironments.md)、[14安全](../docs/14-IdentityPermissionsAndSafety.md)。

</details>

<details>
<summary>局部图7｜生产部署与质量闭环（15–16章）</summary>

```text
任务入口 → Run服务/调度 → Harness Worker
                         ├─ 模型适配 → 模型服务
                         ├─ Tool接入 → 外部系统/执行环境
                         └─ 状态/产物接口 → 持久存储
各阶段事件/证据 → Trace定位 → 固定回归用例 → 修改/评测 → 受控发布/回滚
```

逻辑角色可以同进程实现；拆分要有规模、隔离或故障证据。图里的框不意味着全部都必须立即部署。回到[15观测评测](../docs/15-ObservabilityAndEvaluation.md)、[16生产演进](../docs/16-ProductionArchitectureAndEvolution.md)。

</details>

'''
if '## 机制局部图｜' not in t:
    t=t.replace('## 2. 逐章闭卷检查',visual+'## 2. 逐章闭卷检查',1)
review.write_text(t.rstrip()+'\n')
p=ROOT/'agent/README.md'; t=p.read_text().replace('Review提供16章回忆检查与6个综合失败推演','Review提供7张折叠机制局部图、16章回忆检查与6个综合失败推演'); p.write_text(t.rstrip()+'\n')
result=subprocess.run(['python','tools/validate_agent_curriculum.py'],cwd=ROOT,capture_output=True,text=True,check=True)
print(result.stdout)
loop=next((ROOT/'agent/docs').glob('04-*.md')).read_text()
code=re.search(r'<!-- runnable: report-loop -->\s*```python\n(.*?)\n```',loop,re.S).group(1)
run=subprocess.run(['python','-I','-c',code],capture_output=True,text=True,timeout=10,check=True)
assert '5 cases passed' in run.stdout
assert len(re.findall(r'<summary>局部图\d',review.read_text()))==7
changed=subprocess.check_output(['git','diff','--name-only','-z',BEFORE,'--','research/interviews','research/questions','research/analysis','research/agent-sources'],cwd=ROOT).decode().rstrip('\0').split('\0')
assert all(x in ['', 'research/questions/progress.md'] for x in changed),changed
p=ROOT/'roadmap/final-quality-audit.md'; t=p.read_text(); marker='### 本轮增强最终检查输出'
if marker in t: t=t[:t.index(marker)]
t+='\n\n'+marker+'\n\n```text\n'+result.stdout.strip()+'\n'+run.stdout.strip()+'\nReview local diagrams: 7, default collapsed; 16 chapter checks and 6 scenario drills retained.\nResearch content diff: only progress.md changed; questions/sources/analysis/source-index unchanged.\n```\n\n上述输出来自本分支实际checkout的检查；文件链接与显式锚点检查不等于所有外部站点可用性或所有Markdown渲染器的验证。main原Review的七种机制图已按新四层责任重绘，不恢复含混的Memory即事实、另一套安全层级或固定部署组件清单。\n'
p.write_text(t.rstrip()+'\n')
subprocess.run(['git','diff','--check'],cwd=ROOT,check=True)
print(run.stdout.strip())
