"""Minimal RESP2 client for an owned local teaching server, not a production driver.

No retries, no credentials, no connection pooling or arbitrary server URLs.
Errors are values so EXEC can return both successful and failed subcommands.
"""
from __future__ import annotations
import socket
from reader import RedisReplyError

MAX_FRAME = 16 * 1024 * 1024


def encode(args):
    values=[v if isinstance(v,bytes) else str(v).encode('utf-8') for v in args]
    return b'*'+str(len(values)).encode()+b'\r\n'+b''.join(b'$'+str(len(v)).encode()+b'\r\n'+v+b'\r\n' for v in values)


def read_reply(stream, depth=0):
    if depth>32:raise ValueError('RESP nesting too deep')
    header=stream.readline(MAX_FRAME+1)
    if not header or len(header)>MAX_FRAME or not header.endswith(b'\r\n'):
        raise ConnectionError('Incomplete or oversized RESP header')
    kind,value=header[:1],header[1:-2]
    if kind==b'+':return value.decode('utf-8')
    if kind==b'-':return RedisReplyError(value.decode('utf-8'))
    if kind==b':':return int(value)
    if kind in (b'$',b'*'):
        size=int(value)
        if size==-1:return None
        if size<0 or size>MAX_FRAME:raise ValueError('Invalid RESP size')
        if kind==b'$':
            data=stream.read(size+2)
            if len(data)!=size+2 or data[-2:]!=b'\r\n':raise ConnectionError('Truncated bulk reply')
            return data[:-2].decode('utf-8')
        if size>100000:raise ValueError('Teaching reply array too large')
        return [read_reply(stream,depth+1) for _ in range(size)]
    raise ValueError('Expected RESP2 reply')


class Client:
    def __init__(self,port,timeout=3):
        if not isinstance(port,int) or not 1<=port<=65535:raise ValueError('Invalid local port')
        self.socket=socket.create_connection(('127.0.0.1',port),timeout=timeout)
        self.socket.settimeout(timeout)
        self.stream=self.socket.makefile('rb')
    def execute(self,*args):
        self.socket.sendall(encode(args))
        return self.receive()
    def receive(self):return read_reply(self.stream)
    def pipeline(self,commands):
        commands=list(commands)
        self.socket.sendall(b''.join(encode(c) for c in commands))
        return [self.receive() for _ in commands]
    def close(self):
        self.stream.close();self.socket.close()
    def __enter__(self):return self
    def __exit__(self,*unused):self.close()
