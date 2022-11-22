# GuessTheNumber

## Description
> Ho sviluppato un nuovo gioco, puoi aiutarmi a testarlo?
Puoi collegarti al servizio remoto con:
nc gtn.challs.olicyber.it 10022

## Solution
After generating a random number the game ask us to enter our name and try to guess the number it generated.
When we enter the name we can arbitrary change the value of the number generetad by the program thanks to a buffer overflow.
Sendig lot of 'A' the value of the number will be set to `0x41414141`, this is equal to decimal `1094795585` so now this is the number we have to "guess".

## Flag
`flag{4lw4y5_r34d_w4rn1ng5_>:[}`