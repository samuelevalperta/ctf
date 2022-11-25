 # Readdle

 ## Description
 > 4 bytes di shellcode... possibile?
 nc readdle.challs.olicyber.it 10018

 ## Solution
In this challenge we have no attachments, it will be slightly more difficult to find a solution.

Connecting to the service we observe that we are asked for a **shellcode** which will then be executed.

Typically a shellcode is much longer than 4 bytes so we have to find a way to increase the size of our input.
Unfortunately, having no source code or binary file, we have to go by trial and error and hope for some luck.

We can imagine that our input is asked through a `read()` with limited input size of `0x4`, let's try to solve the challenge by following this path.

This is an example of how the `main` function of our program could be
```c
unsigned char shellcode[4];

// Ask for a shellcode
printf("Enter your shellcode (max 4 bytes):\n");
read(0, shellcode, 4);

// Exec the shellcode
((void (*)(void))shellcode)(); 
```

The *read* is a *System Call* and from this [documentation](https://chromium.googlesource.com/chromiumos/docs/+/master/constants/syscalls.md#x86_64-64_bit) we can better understand how it is performed.

|Num|Name|%rax|arg0(%rdi)|arg1(%rsi)|arg2(%rdx)|
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
|0|read|0x00|unsigned int fd|char *buf|size_t count|

Now we are able to understand that right after the request for our input the registers will have the following values
 # Readdle

 ## Description
 > 4 bytes di shellcode... possibile?
 nc readdle.challs.olicyber.it 10018

 ## Solution
In this challenge we have no attachments, it will be slightly more difficult to find a solution.

Connecting to the service we observe that we are asked for a **shellcode** which will then be executed.

Typically a shellcode is much longer than 4 bytes so we have to find a way to increase the size of our input.
Unfortunately, having no source code or binary file, we have to go by trial and error and hope for some luck.

We can imagine that our input is asked through a `read()` with limited input size of `0x4`, let's try to solve the challenge by following this path.

This is an example of how the `main` function of our program could be
```c
unsigned char shellcode[4];

// Ask for a shellcode
printf("Enter your shellcode (max 4 bytes):\n");
read(0, shellcode, 4);

// Exec the shellcode
((void (*)(void))shellcode)(); 
```

The *read* is a *System Call* and from this [documentation](https://chromium.googlesource.com/chromiumos/docs/+/master/constants/syscalls.md#x86_64-64_bit) we can better understand how it is performed.

|Num|Name|%rax|arg0(%rdi)|arg1(%rsi)|arg2(%rdx)|
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
|0|read|0x00|unsigned int fd|char *buf|size_t count|

Now we are able to understand that right after the request for our input the registers will have the following values

## Flag
`flag{e4sy_r34d_ftw_br0}`
