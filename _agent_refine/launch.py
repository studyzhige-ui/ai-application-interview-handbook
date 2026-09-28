"""Apply bounded transport repairs; never change main or bypass validation."""
from pathlib import Path
p = Path(__file__).with_name('apply.py')
text = p.read_text(encoding='utf-8')
# The previous interrupted upload omitted the final top-level array bracket.
# Repair only that known transport envelope; the normal JSON parser and 56-entry
# assertion still validate the resulting data. No repair logic enters the course.
needle = "answers = json.loads(read('_agent_refine/interview.json'))"
replacement = "answers = json.loads(read('_agent_refine/interview.json') + '\\n]')"
assert text.count(needle) == 1
text = text.replace(needle, replacement)
# Section anchors precede their headings in the original. Map them by the
# explicit section number rather than the preceding text segment.
old = "    grouped = {}\n    for alias, target in sorted(assignments.items()):"
new = '''    for old_num, old_title, _ in numbered_sections(old[n]):
        alias = 'section-' + str(old_num)
        if alias not in anchors(old[n]) or alias in present:
            continue
        if '面试怎么' in old_title: destination = 'interview'
        elif '易错' in old_title: destination = 'pitfalls'
        elif '自测' in old_title: destination = 'self-test'
        elif re.search(r'HUMAN-A|产品实现|源码证据|官方资料', old_title): destination = 'references'
        elif old_num <= len(DEST[n]): destination = 'core-' + str(DEST[n][old_num-1])
        else: destination = 'references'
        assignments[alias] = destination if destination in present else 'references'
    grouped = {}
    for alias, target in sorted(assignments.items()):'''
assert old in text
text = text.replace(old, new)
# Teaching targets are the mechanism sections, not a generic first paragraph.
needle = "    targets = [paths[n-1] + '#core-1' for n in target_chapters]"
replacement = '''    routes = {
        1:[(2,1),(2,2)], 2:[(1,2)], 3:[(3,1),(3,3)], 4:[(3,5)],
        5:[(8,2)], 6:[(8,4),(8,5)], 7:[(8,3)], 8:[(9,3),(9,2)],
        9:[(10,2)], 10:[(10,4)], 11:[(9,6)], 12:[(9,7)], 13:[(9,4)],
        14:[(11,4)], 15:[(11,2),(11,5)], 16:[(11,5)], 17:[(12,6)],
        18:[(6,1),(4,2)], 19:[(5,1),(5,6)], 20:[(6,3),(6,5)],
        21:[(5,4),(5,5)], 22:[(4,2),(4,3)], 23:[(16,1),(16,4)],
        24:[(17,1)], 25:[(17,2)], 26:[(7,3),(7,4)], 27:[(13,1),(13,4)],
        28:[(14,1),(14,3),(14,4)], 29:[(13,2),(13,3)],
        30:[(19,1),(19,2)], 31:[(19,3),(19,4)], 32:[(18,2),(18,3)],
        33:[(21,2)], 34:[(21,2)], 35:[(21,3),(21,4)],
        36:[(22,3),(22,5)], 37:[(22,1)], 38:[(18,4),(18,5)],
        39:[(23,1),(23,2)], 40:[(23,7)], 41:[(21,6)],
        42:[(3,6),(8,3)], 43:[(20,1),(20,3)], 44:[(15,1),(15,2)],
        45:[(18,1),(18,6)], 46:[(19,5)], 47:[(24,5),(24,6)], 48:[(22,1),(22,6)]}
    key = int(cid.split('-')[1])
    if key not in routes: raise ValueError('canonical target requires review: '+cid)
    targets = [paths[ch-1] + '#core-' + str(sec) for ch,sec in routes[key]]'''
assert needle in text
text = text.replace(needle, replacement)
text = text.replace("assert not git('status', '--porcelain').strip(), 'checkout must begin clean'", "assert not git('status', '--porcelain').strip(), 'checkout must begin clean: ' + git('status','--porcelain')")
exec(compile(text, str(p), 'exec'), {'__name__':'__main__', '__file__':str(p)})
