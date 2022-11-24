
# Formatted

## Description
> C'è questo binario, mi hanno detto che è vulnerabile, però non riesco a leggere la flag. Mi puoi aiutare?
Puoi collegarti al servizio remoto con:
nc formatted.challs.olicyber.it 10305

## Solution

First of all we need to know that the program will print the flag before exiting only if the value of the global variable `flag` is different from `0x0`, so  that's our goal.

Analyzing more in depth the binary we can understand that the operation is as follows:
- we are asked for the name as input
- our input is returned as output using `printf()`.

This use of the `printf()` function allows us to use a [format string attack](https://axcheron.github.io/exploit-101-format-strings), the name of the challenge confirms that this is the right way.

After reading the above article it won't be too hard to get to this solution
```python
payload = b'A'*4  + b'%7$n' + p64(0x40404c)
```
but let's explain better.

We need to remember that our payload will be passed as argument of the `printf()` function so our program will execute something like this
```c
printf(AAAA%7$n\x4c\x40\x40\x00)
``` 


But why this payload?
- **%n** is a format which will write the *size* of our input into the address pointed by **%n**.

Being it the first format specifier read by `printf()` it will point to the second argument, which following the [amd64 calling convention](https://courses.cs.washington.edu/courses/cse378/10au/sections/Section1_recap.pdf) is stored into `$rsi`.

```c
// Example 1, %s reference to $rsi and %p to $rdx
printf("%s,%p",$rsi,$rdx)

// Example 2, %s reference to $rdx and %p to $rsi
printf("%2$s,%1$s", $rsi, $rdx)
```

So we need to make the **%n** point to the address of our `flag` variable which is `0x40404c` (obtained with [Ghidra](https://github.com/NationalSecurityAgency/ghidra)) but we can't change the value of `$rsi` in any way, we can only write things to the stack as our input is saved there.

From the 7th argument upwards, following the amd64 calling convention, the argument of a function call will be taken from the stack, so `%6$n` will write to the address saved in the first 8 bytes of the stack.
At the top of the stack there's our input, more precisely `0x6e243625` (that correspond to ASCII `%6$n`) which is obviously not a valid address.
But we solve this using `%7$p` to make the **%n** point to the second address of the stack, which we can arbitrary write(remember that our input is the last thing pushed on the stack).

- `AAAA` will make the **%n** write 4(so different from `0x0`) and also will pad our input so the address we send will be placed in the seconds 8 bytes of the stack.

If we place a `break printf` and look at the stack the moment right after the function call it will be:
```
pwndbg> x/4x $rsp
0x7ffcbcdbb460: 0x41414141      0x6e243725      0x0040404c      0x00000000
```

With this payload we achieve to write `4` at the address of the global `flag` so the service will print out the flag.

## Flag
`flag{So_y0U_kn0w_F0rm4t_StR1ng5}`

