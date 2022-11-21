# Software 07 - Stack 1 

## Description
> Questo programma salva la flag sullo stack, tramite delle istruzioni mov, e poi esce. 
Spesso conviene guardare anche il codice disassemblato e non solo il decompilato

## Solution
We can run the program under gdb and set a breakpoint to the functin `main`, then we can use `x/20i $pc` to display the next 20 assembly instruction.
We see a lot of `mov` each one pushing an ASCII value on the stak, if we copy all of them and convert into thei ASCII value we get the flag.

We could also have set a breakpoint at `*main+200` and then analyze the stack with `stack` to see the flag.
  
## Flag
`flag{aarch64}`