# more privte club

## Description
> Entrare nel mio club non sarà così facile questa volta. ):
> nc moreprivateclub.challs.olicyber.it 10016

## Solution
Analyzing the file with [Ghidra](https://GitHub.com/NationalSecurityAgency/Ghidra) we easily notice an error in the implementation of the `scanf()` function when we are asked to enter the name.
In fact, our input will be saved in a *char array* of size *35* but there’s no type of length check so nothing prevents us from entering more than the *35* characters being reserved for it.

This is how the stack will look after the call to `scanf()` :
||
|:---:|
| return address|
| saved base pointer|
| input+32|
| input+24|
| input+16|
| input+8|
|input|

By sending an input longer than 35 we will first overwrite the **saved base pointer** and then the **return address** (where the address from which the program will continue its execution after the `scanf()` is saved).

Observing the disassembled code we notice that immediately after the `scanf()` the **return address** saved in the stack will point to `0x000011fb` so the program will performs these operations

```bash
000011fb 	0f b6 45 d0     MOVZX      EAX,byte ptr [RBP + local_38]
000011ff	84 c0			TEST       AL,AL
00001201	74 40       	JZ         LAB_00001243
```

which will make our program always jump to the instruction at `0x00001243`, which will print the message *"Non hai il badge, mi displace."* and then exit.
If we keep looking at the disassembled code we find, at address `0x00001235`, a call to the *libc* `system()` function with `/bin/sh` as argument.

At this point we know our goal: write `0x1235` where the **return address** is saved.

To know the exact offset from the start of our input to the place where **return address** is saved we can use the *cyclic* [Pwntools](https://github.com/gallopsled/pwntools) function as following
```bash
gdb ./moreprivateclub
r < <(pwn cyclic 100)	# use the output of cyclic 100 as input
```
our program will segfault at
```
ret    <0x6161706161616f61>
```
and we can get the offset with
```bash
pwn cyclic -l 0x61616f61	# because of the endianness we pick the last 8 bytes
```
which is `0x37`.

Our exploit will have to send `0x37` garbage values and then `0x1235` formatted as *x86_64 little endian* address.

## Flag
`flag{r3t2wh3r31w4nt}`
