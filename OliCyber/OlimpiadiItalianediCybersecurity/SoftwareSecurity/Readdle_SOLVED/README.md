# Readdle

## Description
> 4 bytes di shellcode... possibile?
nc readdle.challs.olicyber.it 10018

## Solution
In this challenge we have no attachments, it will be slightly more difficult to find a solution.

Connecting to the service we observe that we are asked for a **shellcode** of size equals to 4 bytes which will then be executed.

Typically a shellcode is much longer than 4 bytes so we have to find a way to increase the size of our input, unfortunately, having no source code or binary file, we have to go by trial and error and hope for some luck.

Just for clarity, I wrote the following code as an example of how the program that the service runs could look like
```c
unsigned char shellcode[4];

// Ask for a shellcode
printf("Enter your shellcode (max 4 bytes):\n");
read(0, shellcode, 4);

// Exec the shellcode
((void (*)(void))shellcode)(); 
```
*This code will save the shellcode into the stack, so we need to compile using `-z execstack` and `--fno-stack-protector` option to make our input executable, otherwise it will segfault.*

Anyway whichever function of any library is used to recive our input it will most likely come down using a ***read*** *System Call*, from this [documentation](https://chromium.googlesource.com/chromiumos/docs/+/master/constants/syscalls.md#x86_64-64_bit) we can better understand how it is performed.

|Num|Name|%RAX|arg0 (%RDI)|arg1 (%RSI)|arg2 (%RDX)|
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
|0|read|0x00|unsigned int fd|char *buf|size_t count|

So at the precise moment in which we are asked for the input, the registers will be in this state
```bash
$rax = 0x0             # syscall number
$rdi = 0               # which is stdin 
$rdx = 0x4             # max length
$rsi = *shellcode      # will be pointing to the addres where our input will be stored
```
We need to know that as soon as we send our shellcode the program will continue his execution moving the `$pc` to our shellcode, this means that no register (excluded `$pc`) will be touched so they are in the same status as they were before the *Syscall*.
This means they are ready to be used to perform another reading operation of `0x4` bytes from `stdin` to the address pointed by `shellcode`, and this can be achieved by sending the *Syscall* opcode (`0x0f05`) as input.

We haven't won yet, because even if we manage to read another 4 bytes they will be saved at the address of  `shellcode`, an address that has now been surpassed by the `$pc`, since it was moved to our `shellcode` after the read an then it performed the Syscall we send, so now it's ready to execute the next operation and it's pointing to `shellcode+0x2`.

Now we can send another shell code but it will be executed from the third byte (`shell code+0x2`) and considering that we can send no more then 4 bytes we can execute only the third and the fourth bytes.

But what if we manage to change the *count* of our read before we send the Syscall opcode, we could be able to read a bigger shell code and even if the program would start executing it from the second byte we could send `NOP` operation till we reach the `$pc` pointing address and then write the a real and "unlimited" shell code.

My solution to increment the value of *count*, which we remember is taken from `$RDX`, is to `push $RSP` (which contains the address of the top of the stack, which if interpreted as *number* will be a really big one) and then `pop $RDX`. With this trick we are able to assign to `$RDX` (that corresponds to the *count* argument of the *read Syscall*) a value similar to `0x7fffffffe058`.

The opcode of `push $RSP` and `pop $RDX` are respectively `0x54` and `0x5a` and the "final" payload is 
```python
payload = "\x54\x5a\x0f\x05"
```
at this point we can send a **shell code** shorter than `0x7fffffffe058` bytes that will be executed starting from the 4th, [Pwntools](https://github.com/Gallopsled/pwntools) comes to help now...
```python
shellcode = b"\x90"*4 + asm(shellcraft.sh())
``` 

## Flag
`flag{e4sy_r34d_ftw_br0}`
