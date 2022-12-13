# Terminator

## Description
> Ho appena incontrato Terminator, non pensavo fosse così gentile!<br>
Puoi collegarti al servizio remoto con:<br>
nc terminator.challs.olicyber.it 10307

## Solution
I used [Cutter]('https://github.com/rizinorg/cutter') to analize this program and this is what I found out.

The program reads an input of 0x38 bytes and saves it in a 56(0x38) long char array named **buf**, then save the value `0xa` to the address  `*buf+inputLen`.


Being the stack frame like this
|address (higher to lower)|value|
|---|---|
|rbp|saved base pointer|
|rbp-0x8|stack canary|
|rbp-0x10|*buf+48|
|...|...|
|rbp-0x40|*buf|
|rbp-0x44|inputLen|

If we send 56 characters, `0xa` will be saved in `*buf+56`, which is no longer a value of **buf** (because it ends at `*buf+55`) but is the *less significant byte* of **stack canary**.

Usually the *less significant byte* of the **stack canary** is set to `0x0` so as to avoid it being leaked (the function that is supposed to leak it would stop at that `0x0`) but in this case we managed to replace it with `0xa`, so the `printf()` that returns our input will continue to print from the stack until another *null byte* is found, leaking the **stack canary** first and then also the **saved base pointer**.<br>

But what do we do with the **stack canary** now?<br>
We observe that the program now asks us for another input using a read of 0x48 and saving it in the same buffer used before of length 56, this obviusly allow us to perform a buffer overflow attack and knowing the **canary** is essential to our goal.

Usually the goal of a buffer overflow is to overwrite the **return address** in such a way as to direct the execution of the program to our liking. In this case, however, it is not possible, since the **return address** is located 0x48 bytes below (actually above being that stack grows downwards) and we can write exactly 0x48 bytes, so we stop at exactly the byte before where the return address is stored.
<br>
On the stack, before the **return address**, is stored the **saved base pointer** of the previous stack frame, and luckly, there's a tecnique called *stack pivoting* wich allows us to redirect the program flow by editing the value of the **saved base pointer**.

To well undestand how *stack pivoting* works we can assume that the stack of this executable at the moment of the second `read()` would looks like this
|address (higher to lower)|value|





## Flag
`flag{d0Nt_F0rg37_y0uR_5tr1nG_T3rM1n470R}`