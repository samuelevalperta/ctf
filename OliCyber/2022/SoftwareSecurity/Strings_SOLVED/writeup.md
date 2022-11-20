# Software 02 - Strings 2

## Description
> Il programma di questa challenge è molto simile al precedente. Questa volta però il comando strings non ti aiuterà. 
Quasi sempre per risolvere queste challenge abbiamo bisogno di utilizzare tool più sofisticati, come i disassembler e i decompiler, quali ad esempio Ghidra. Ne esistono molti altri come IDA, radare2, Hopper ecc. 
Prova con Ghidra (o il tuo decompiler di fiducia) e analizza il contenuto della funzione main.

## Solution
Doing `r2 -c 'iz' sw-05` in bash it's the same as opening `sw-05` file with `radare2` and then execute the `iz` command which print the Strings in data section.
One of this Strings is the flag.
  
## Flag
`flag{81750e63}`