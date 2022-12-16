# Terminator

## Description
> Ho appena incontrato Terminator, non pensavo fosse così gentile!<br>
Puoi collegarti al servizio remoto con:<br>
nc terminator.challs.olicyber.it 10307

## Solution
I used [Cutter]("https://github.com/rizinorg/cutter") to analize this program and this is what I found out.

The program reads an input of 0x38 bytes and saves it in a 56(0x38) long char array named **buf**, then save the value `0xa` to the address  `*buf+inputLen`.


Being the stack frame like this
|address (higher to lower)|value|
|---|---|
|rbp-0x44|inputLen|
|rbp-0x40|*buf|
|rbp-0x10|*buf+48|
|...|...|
|rbp-0x8|stack canary|
|rbp|saved base pointer|

If we send 56 characters, `0xa` will be saved in `*buf+56`, which is no longer a value of **buf** (because it ends at `*buf+55`) but is the *less significant byte* of **stack canary**.

Usually the *less significant byte* of the **stack canary** is set to `0x0` so as to avoid it being leaked (the function that is supposed to leak it would stop at that `0x0`) but in this case we managed to replace it with `0xa`, so the `printf()` that returns our input will continue to print from the stack until another *null byte* is found, leaking the **stack canary** first and then also the **saved base pointer**.<br>

But what do we do with the **stack canary** now?<br>
We observe that the program now asks us for another input using a read of 0x48 and saving it in the same buffer used before of length 56, this obviusly allow us to perform a buffer overflow attack and knowing the **canary** is essential to our goal.

Usually the goal of a buffer overflow is to overwrite the **return address** in such a way as to direct the execution of the program to our liking. In this case, however, it is not possible, since the **return address** is located 0x48 bytes below (actually above being that stack grows downwards) and we can write exactly 0x48 bytes, so we stop at exactly the byte before where the return address is stored.
<br>
On the stack, before the **return address**, is stored the **saved base pointer** of the previous stack frame, and luckly, there's a tecnique called *stack pivoting* wich allows us to redirect the program flow by editing the value of the **saved base pointer**.


### Stack Pivoting
- This is the stack while we are in the `welcome()` function
```bash
00:0000│ rsp 0x7ffee1f1b080 ◂— 0x0
01:0008│     0x7ffee1f1b088 ◂— 0x38194fa013
02:0010│     0x7ffee1f1b090 ◂— 0x4141414141414141 ('AAAAAAAA')
... ↓        6 skipped
09:0048│     0x7ffee1f1b0c8 ◂— 0x4242424242424242 ('BBBBBBBB')
0a:0050│ rbp 0x7ffee1f1b0d0 ◂— 0x4343434343434343 ('CCCCCCCC')
0b:0058│     0x7ffee1f1b0d8 —▸ 0x4011c7 (main+101)
0c:0060│     0x7ffee1f1b0e0 —▸ 0x7ffee1f1b1e0
0d:0068│     0x7ffee1f1b0e8 —▸ 0x402004 ◂— 'Welcome!!!\n'
0e:0070│     0x7ffee1f1b0f0 ◂— 0x0
0f:0078│     0x7ffee1f1b0f8 —▸ 0x7f661948d0b3 (__libc_start_main+243)
```

- **leave** (`mov rsp, rbp` and `pop rbp`) from `welcome()`
```bash
00:0000│ rsp 0x7ffee1f1b0d8 —▸ 0x4011c7 (main+101)
01:0008│     0x7ffee1f1b0e0 —▸ 0x7ffee1f1b1e0 ◂— 0x1
02:0010│     0x7ffee1f1b0e8 —▸ 0x402004 ◂— 'Welcome!!!\n'
03:0018│     0x7ffee1f1b0f0 ◂— 0x0
04:0020│     0x7ffee1f1b0f8 —▸ 0x7f661948d0b3 (__libc_start_main+243)
... ↓        
..:....│ rbp 0x4343434343434343 ◂— 0xdeadbeef
```

- **ret** (`pop rip`)
```bash
00:0000│ rsp 0x7ffee1f1b0e0 —▸ 0x7ffee1f1b1e0 ◂— 0x1
01:0008│     0x7ffee1f1b0e8 —▸ 0x402004 ◂— 'Welcome!!!\n'
02:0010│     0x7ffee1f1b0f0 ◂— 0x0
03:0018│     0x7ffee1f1b0f8 —▸ 0x7f661948d0b3 (__libc_start_main+243)
... ↓        
..:....│ rbp 0x4343434343434343 ◂— 0xdeadbeef

rip 0x4011c7 (main+101)
```
- 0x4011c7 contains `mov rax, 0` so this is executed and the `rip` is incremented to 0x4011cc
- **leave** (`mov rsp, rbp` and `pop rbp`) from `main()`
```bash
00:0000│     0x4343434343434343 ◂— 0xdeadbeef
01:0008│ rsp 0x434343434343434b ◂— 0xcafebabe
... ↓
..:....│ rbp 0xdeadbeef

rip 0x4011cd
```

- **ret** (`pop rip`)
```bash
00:0000│     0x434343434343434b ◂— 0xcafebabe
01:0008│ rsp 0x4343434343434353
... ↓
..:....│ rbp 0xdeadbeef

rip 0xcafebabe
```

We managed to give `rip` the value contained in the address (incremented by 0x8) pointed by the  **saved base pointer** in the `welcome()` frame, which we can arbitrary change due to the stack overflow.
Here's a less abstractive view of the sentence just written (the values used down here have no connection with the ones used above, they just look similar):

```bash
sbp 0x4141414141414141 ◂— 0x4242424242424242
    0x424242424242424b ◂— 0x4343434343434343
rip 0x4343434343434343
```

The goal is to assign to `rip` a value sent by us (so saved on the stack) and this is possible thanks to the **base pointer** leak that we obtained earlier.<br>
We know that our input (saved in `welcome()` frame) is stored at an address slightly lower than the leak we obtained (`rbp` of `main()` frame). We can refine the search using `pwn cyclic`.

### ROP
Now that we can assign a value to `rip` at our discretion we can exploit using a ROP chain.
We use the ROP chain to dynamically get the address of `puts` (stored in the GOT) in the libc and, knowing the version, we find the library base. We repeat the execution of `main()` but this time our ROP chain will execute `system("/bin/sh")`.


## Flag
`flag{d0Nt_F0rg37_y0uR_5tr1nG_T3rM1n470R}`