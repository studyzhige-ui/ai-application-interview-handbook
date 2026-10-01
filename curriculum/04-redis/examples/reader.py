"""Read Redis teaching fixtures from the Markdown source of truth.

This module performs no Redis I/O. Metadata is an executable expectation, not
proof that the command has already been run.
"""
from __future__ import annotations
import json
import re
import shlex
from dataclasses import dataclass
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1]
DOCS = MODULE / 'docs'
VERSION = '8.10.2'

def source_paths():
    return [*sorted(DOCS.glob('*.md')), MODULE / 'examples/labs.md']

@dataclass(frozen=True)
class Lab:
    name: str
    source: Path
    commands: tuple[tuple[str, ...], ...]
    expected: tuple


def labs() -> list[Lab]:
    pattern = re.compile(r'<!-- redis-lab: ([\w-]+) -->\s*```redis\n(.*?)\n```\s*<!-- redis-expect: (.*?) -->', re.S)
    result = []
    for path in source_paths():
        for match in pattern.finditer(path.read_text(encoding='utf-8')):
            commands = tuple(tuple(shlex.split(line)) for line in match[2].splitlines() if line.strip())
            expected = tuple(json.loads(match[3]))
            if len(commands) != len(expected):
                raise ValueError(f'{path.name}: command/reply count mismatch')
            result.append(Lab(match[1], path, commands, expected))
    if not result or len({r.name for r in result}) != len(result):
        raise ValueError('missing or duplicate Redis lab identifiers')
    return result


def scripts() -> dict[str, str]:
    result = {}
    pattern = re.compile(r'<!-- lua-lab: ([\w-]+) -->\s*```lua\n(.*?)\n```', re.S)
    for path in source_paths():
        for match in pattern.finditer(path.read_text(encoding='utf-8')):
            if match[1] in result:
                raise ValueError('duplicate Lua script: '+match[1])
            result[match[1]] = match[2]+'\n'
    return result


def export(destination: Path) -> dict:
    """Write disposable copies. Never rewrite existing files without matching bytes."""
    items = {f'{x.name}.redis': '\n'.join(shlex.join(c) for c in x.commands)+'\n' for x in labs()}
    items.update({name+'.lua': code for name, code in scripts().items()})
    destination.mkdir(parents=True, exist_ok=True)
    for name, content in items.items():
        p = destination / name
        if p.exists() and p.read_bytes() != content.encode('utf-8'):
            raise ValueError(f'Refusing to overwrite a different file: {p}')
    for name, content in items.items():
        (destination/name).write_bytes(content.encode('utf-8'))
    return {'files': len(items), 'destination': str(destination)}


class RedisReplyError:
    def __init__(self, message: str):
        self.message = message
    def __repr__(self):
        return f'RedisReplyError({self.message!r})'


def assert_reply(actual, expected):
    """Match RESP2 replies, preserving errors inside transaction result arrays."""
    if isinstance(expected, dict):
        if 'error' in expected:
            assert isinstance(actual, RedisReplyError) and expected['error'] in actual.message, (actual,expected)
        elif 'between' in expected:
            lo,hi=expected['between']
            assert isinstance(actual,int) and lo <= actual <= hi,(actual,expected)
        elif 'set' in expected:
            assert isinstance(actual,list) and sorted(actual)==sorted(expected['set']),(actual,expected)
        elif 'pairs' in expected:
            assert isinstance(actual,list) and len(actual)%2==0,(actual,expected)
            assert len(actual)==2*len(expected['pairs']),(actual,expected)
            assert dict(zip(actual[::2],actual[1::2]))==expected['pairs'],(actual,expected)
        else:
            raise ValueError('Unknown reply matcher: '+repr(expected))
    elif isinstance(expected,list):
        assert isinstance(actual,list) and len(actual)==len(expected),(actual,expected)
        for a,e in zip(actual,expected):assert_reply(a,e)
    else:
        assert actual==expected and (not isinstance(expected,int) or type(actual) is int),(actual,expected)
