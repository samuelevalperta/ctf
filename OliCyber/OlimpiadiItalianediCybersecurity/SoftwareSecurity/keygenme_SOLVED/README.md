# keygenme
## Description
> Registrare il nostro prodotto è facilissimo, basta inserire ID e chiave!
nc keygenme.challs.olicyber.it 10017

## Solution
Analyzing the binary with [Ghidra](https://github.com/NationalSecurityAgency/ghidra'), with little effort we can understand that the service generates a random *user id* and after printing it, it asks us to enter the *serial key*.

This *serial_key* is calculated through a static algorithm starting from the *user id*.
Being that our *user id* is shown to us we can replicate the algorithm (that's what `exploit.c` does) and calculate the correct *serial key* starting from the *user id* given by the service.

Done that, after sending the *serial key* we found to the service, the flag will be printed.

## Flag
`flag{3z_l1c3n53_4_3v3ry0n3}`