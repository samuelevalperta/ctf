# van_halen

## Description
> Mai sentito i Van Halen? Potrebbero tornarti utili!

## Solution
After running the executable under `radare2` we can disaply all the debugging symbols with the command `f`.
Here we notice a function called `funzione_totalmente_anonima_non_mi_lanciare`, we can call it using `gdb` with  `call (void *)funzione_totalmente_anonima_non_mi_lanciare`.
## Solution 2
Another way to solve this is to reverse the function and replicate it with the same data (`exploit.py` make this).

## Flag
`flag{g0_4h3ad_4nd_jump}`