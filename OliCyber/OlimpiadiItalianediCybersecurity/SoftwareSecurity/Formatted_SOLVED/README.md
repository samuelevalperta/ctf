# Formatted

## Description
> C'è questo binario, mi hanno detto che è vulnerabile, però non riesco a leggere la flag. Mi puoi aiutare?
Puoi collegarti al servizio remoto con:
nc formatted.challs.olicyber.it 10305

## Solution

We can exploit this little program with a format string, sending the following payload.
```python
payload = b'A'*4  + b'%7$n' + p64(0x40404c)
```
Because *%n* will write the size of our input if we don't write something before it the value `0` will be written and our goal is to write anything different from 0 into the global variable *flag*.
We need to this 4 of this to guarantee the right alignment of the stack.
`printf(%7$n)` will write in position 7, which refers to the 8th argument.
We are working on amd-64 so the first 6 arguments are passed from registers and from the 7th onwards from the stack.
So if we try to access the 7th argument we are accessing the 8 bytes at the top of the stack (the first 8 bytes of our input, which are the last thing being pushed).
We want to write into `0x40404c` (which is the address of the global variable) so we write this into the second 8 bytes of the stack and refer to it with %8 in the printf call.

# Flag
`flag{So_y0U_kn0w_F0rm4t_StR1ng5}`
