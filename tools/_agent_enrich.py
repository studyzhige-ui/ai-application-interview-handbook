from pathlib import Path
import re, subprocess
ROOT=Path(__file__).resolve().parents[1]
BEFORE='2fbd42e65940b961e6c2edb17bc87940feb028ff'
inter=ROOT/'agent/interview/README.md'; text=inter.read_text()
for n in range(1,17):
    heading=f'### {n:02}｜'; anchor=f'<a id="chapter-{n:02}"></a>'
    assert text.count(heading)==1
    if anchor not in text:
        text=text.replace(heading,anchor+'\n\n'+heading,1)
if '## 快速定位' not in text:
    nav='## 快速定位\n\n'+' · '.join(f'[{n:02}](#chapter-{n:02})' for n in range(1,17))+'\n\n编号与正式16章一致，按薄弱机制查找，不必一次刷完所有题。\n\n'
    text=text.replace('## 按16章展开的64道训练题',nav+'## 按16章展开的64道训练题',1)
inter.write_text(text.rstrip()+'\n')
for p in sorted((ROOT/'agent/docs').glob('*.md')):
    n=int(p.name[:2]); text=p.read_text()
    target=f'../interview/README.md#chapter-{n:02}'
    if target not in text:
        text=text.replace('## 回到主线',f'[本章面试练习与具体追问]({target}) · [综合复习](../review/README.md)\n\n## 回到主线',1)
    p.write_text(text.rstrip()+'\n')
# Store detailed migration evidence once, not duplicated across two audits.
mark='## 2026-09-16｜Agent 分层增强：吸收 main 的机制与训练优势'
p=ROOT/'roadmap/final-quality-audit.md'; t=p.read_text()
anchor='<a id="agent-enrichment-20260916"></a>'
if anchor not in t:
    t=t.replace(mark,anchor+'\n\n'+mark,1)
t=t.replace('当前Agent已按任务→四层→治理重构为16章，全仓库正文177篇。本次结构、链接、计数与研究证据不变性检查记录见本文末尾；不将历史PASS伪装为一次新的逐项技术复审。','当前Agent为任务→四层→治理的16章增强版，全仓库177篇；机制迁移、教学示例、细粒度训练和检查范围见文末。历史全仓库PASS不等于新版本逐句技术复审。')
p.write_text(t.rstrip()+'\n')
p=ROOT/'roadmap/content-depth-audit.md'; t=p.read_text()
assert mark in t
t=t[:t.index(mark)]+'''## 2026-09-16｜Agent 分层增强复核

保留16章任务驱动与四层主线，吸收main的23章机制细节和细粒度训练。前两章新增同一个通用文件报告的契约/控制权推导；16章均补阅读提示、情景自测与对应面试练习链接；长章分段阅读，不另建平行教材。

面试页保留main的56个练习能力范围，并增加8个系统推导题；86个易错辨析和速查同页组织。64道练习不等于真人Canonical；44道ACTIVE Canonical及研究证据保持不变。最小Loop教学例实际执行5种场景通过，但不替代真实模型/工具和生产可靠性测试。

逐章迁移表、具体差异处理、检查结果与限制只维护在[Agent增强质量记录](final-quality-audit.md#agent-enrichment-20260916)。结构检查不按字数冒充语义质量证明。
'''
p.write_text(t.rstrip()+'\n')
result=subprocess.run(['python','tools/validate_agent_curriculum.py'],cwd=ROOT,text=True,capture_output=True,check=True)
print(result.stdout)
# Verify the explicitly authored deterministic example, not arbitrary code blocks.
loop=next((ROOT/'agent/docs').glob('04-*.md')).read_text()
code=re.search(r'<!-- runnable: report-loop -->\s*```python\n(.*?)\n```',loop,re.S).group(1)
run=subprocess.run(['python','-I','-c',code],capture_output=True,text=True,timeout=10,check=True)
assert '5 cases passed' in run.stdout
print(run.stdout)
protected=['research/interviews','research/questions','research/analysis','research/agent-sources']
changed=subprocess.check_output(['git','diff','--name-only','-z',BEFORE,'--',*protected],cwd=ROOT).decode().rstrip('\0').split('\0')
assert all(x in ['', 'research/questions/progress.md'] for x in changed),changed
p=ROOT/'roadmap/final-quality-audit.md'; t=p.read_text()
marker='### 本轮增强最终检查输出'
if marker in t: t=t[:t.index(marker)]
t+='\n\n'+marker+'\n\n```text\n'+result.stdout.strip()+'\n'+run.stdout.strip()+'\nResearch content diff: only progress.md changed; questions/sources/analysis/source-index unchanged.\n```\n\n上述输出来自本分支实际checkout的检查；文件链接检查与显式锚点检查不等于对所有外部站点可用性或所有Markdown渲染器的验证。\n'
p.write_text(t.rstrip()+'\n')
subprocess.run(['git','diff','--check'],cwd=ROOT,check=True)
