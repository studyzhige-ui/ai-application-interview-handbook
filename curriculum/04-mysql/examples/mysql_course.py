"""Read named SQL from the course; never connect or execute implicitly."""
from pathlib import Path
import re

MODULE = Path(__file__).resolve().parent.parent

def examples():
    found = {}
    paths = [*sorted((MODULE / "docs").glob("*.md")), MODULE / "examples" / "experiments.md"]
    for path in paths:
        text = path.read_text(encoding="utf-8")
        pattern = r"(?:<!-- mysql-example: ([a-z0-9_]+) -->\s*)?```sql\n(.*?)\n```"
        for match in re.finditer(pattern, text, re.S):
            code = match.group(2)
            inline = re.search(r"^-- example: ([a-z0-9_]+)\s*$", code, re.M)
            name = match.group(1) or (inline.group(1) if inline else None)
            if name:
                if name in found:
                    raise ValueError(f"Duplicate SQL example: {name}")
                found[name] = {"code": code, "file": str(path.relative_to(MODULE))}
    return found

def split_sql(text):
    """Split this course's SQL: quotes and comments supported; no DELIMITER/procedures.

    This is a statement splitter, NOT syntax or semantic validation of SQL.
    """
    statements, buf = [], []
    i, quote = 0, None
    while i < len(text):
        c = text[i]
        if quote:
            buf.append(c)
            if c == "\\" and i + 1 < len(text):
                i += 1
                buf.append(text[i])
            elif c == quote:
                if i + 1 < len(text) and text[i + 1] == quote:
                    i += 1
                    buf.append(text[i])
                else:
                    quote = None
        elif c in ("'", '"', '`'):
            quote = c
            buf.append(c)
        elif text.startswith('--', i) and (i + 2 == len(text) or text[i + 2].isspace()):
            end = text.find('\n', i)
            if end < 0:
                break
            i = end
            buf.append('\n')
        elif c == '#':
            end = text.find('\n', i)
            if end < 0:
                break
            i = end
            buf.append('\n')
        elif text.startswith('/*', i):
            end = text.find('*/', i + 2)
            if end < 0:
                raise ValueError('Unclosed block comment')
            i = end + 1
            buf.append(' ')
        elif c == ';':
            statement = ''.join(buf).strip()
            if statement:
                statements.append(statement)
            buf = []
        else:
            buf.append(c)
        i += 1
    if quote:
        raise ValueError('Unclosed SQL quote')
    tail = ''.join(buf).strip()
    if tail:
        statements.append(tail)
    return statements

def execute(connection, sql):
    results = []
    with connection.cursor() as cursor:
        for statement in split_sql(sql):
            cursor.execute(statement)
            if cursor.description:
                results.append(cursor.fetchall())
    return results
