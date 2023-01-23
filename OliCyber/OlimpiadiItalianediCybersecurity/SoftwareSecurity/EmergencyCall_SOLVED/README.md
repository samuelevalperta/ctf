# Emergency Call

## Description
> Questa non è un esercitazione! Ripeto. Questa non è un esercitazione!!! Hai una sola chiamata di emergenza, quindi usala bene.
Puoi collegarti al servizio remoto con:
nc emergency.challs.olicyber.it 10306

## Solution
Thanks to Ghidra we can easily notice an out of bounds write in the request of the emergency. We are asked for the input trought a **read_syscall** with maximum size of $128$ and it will be saved in a **char array** of length $32$.

That's the output of the `checksec` command
```bash
RELRO:    No RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      No PIE (0x400000)
```
Having **No PIE** means that the base of our binary will always be the same in every execution, so we exactly know the address of every assembly operation, even on the remote service.<br>

Let's better analyze the program locally by sending this payload as second input
```python
payload = b'A'*32 + b'B'*8 + b'C'*8 + b'D'*16
```
This is how the stack looks right after we send our payload
|register|address|value|ascii
|-|-|-|-|
|rsp|0xfe158|0x4010e0
|rsi|0xfe160|input_hex (0x4141414141414141)|AAAAAAAA
||0xfe168|input + 8|AAAAAAAA|
||0xfe170|input + 16|AAAAAAAA
||0xfe178|input + 24|AAAAAAAA
|rbp|0xfe180|input + 32 (0x4242424242424242)|BBBBBBBB
|ret_addr|0xfe188|input + 40 (0x4343434343434343)|CCCCCCCC
||0xfe190|input + 48 (0x4444444444444444)|DDDDDDDD
||0xfe198|input + 56 (0x4444444444444444)|DDDDDDDD

<br>**RIP** now points to $\mathrm{0x401031}$ which contains `RET` instruction.
This `RET` instruction execute `POP RIP`.

Now `RIP` points to $\mathrm{0x4010E0}$ which is `RETURN 0`, executing this will do as following:
- `MOV RAX, 0` , the stack does not get affected
- `MOV RSP, RBP` which delete the last frame

|register|address|value|ascii
|-|-|-|-|
|rsp,rbp|0xfe180|input + 32 (0x4242424242424242)|BBBBBBBB
|ret_addr|0xfe188|input + 40 (0x4343434343434343)|CCCCCCCC
||0xfe190|input + 48 (0x4444444444444444)|DDDDDDDD
||0xfe198|input + 56 (0x4444444444444444)|DDDDDDDD

<br>

- `POP RBP` which pop from the stack to **RBP** and move  **RSP** to the next address

|register|address|value|ascii
|-|-|-|-|
|rsp (ret_addr)|0xfe188|input + 40 (0x4343434343434343)|CCCCCCCC
||0xfe190|input + 48 (0x4444444444444444)|DDDDDDDD
||0xfe198|input + 56 (0x4444444444444444)|DDDDDDDD
|rbp|0x4242424242424242|

<br>

- and `RET` which is basically a `POP RIP`

|register|address|value|ascii
|-|-|-|-|
|rsp|0xfe190|input + 48 (0x4444444444444444)|DDDDDDDD
||0xfe198|input + 56 (0x4444444444444444)|DDDDDDDD
|rbp|0x4242424242424242|


<br>

**RIP** = $\mathrm{0x4343434343434343}$.

At this point, knowing that we have control over the return address, we can adapt the payload to our needs.
We can exploit this using ROP due to the fact that the program was compiled without PIE.
<br>
Our goal is to make an ***execve_syscall*** to $/bin/sh$, by looking at [x86-64 syscall table](https://chromium.googlesource.com/chromiumos/docs/+/master/constants/syscalls.md#x86_64-64_bit) we know that the register should be as following:
|register|arg|value
|-|-|-|
|RAX|syscall number|0x3b|
|RDI|const char *filename|"/bin/sh"|
|RSI|const char *const *argv|0x0
|RDX|const char *const *envp|0x0

We can start searching for gadgets using
```bash
ROPgadget --binary=emergency-call | grep rax
```
We can use `XOR RAX, RDI; RET` to assign the correct value to **RAX**.
We know that **RAX** is equal to $\mathrm{0x0}$ because of the `RETURN 0` operation, so **RDI** must be $\mathrm{0x3B}$ before we reach the `XOR` instruction.

We can use `POP RDI; RET` gadget to achieve this and then do the operation.

The next step is to assign to **RDI** the address of a ***char array*** containing $/bin/sh$, there's no string in the program which contains this but we can send $/bin/sh$ as first input and then use its location.

Now we still need to set **RSI** and **RDX** to $\mathrm{0x0}$ and we can get this with this two gadgets:  `POP RSI; RET` and `POP RDX; RET`.

## Flag
```c
flag{Th3_b35T_em3Rg3nCy_C4ll_1s_Sy5c411!}
```
