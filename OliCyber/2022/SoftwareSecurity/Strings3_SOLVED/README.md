# Software 06 - Strings 3

## Description
> Le prossime tre challenge sono strutturate in maniera simile ad alcune challenge di reverse engineering che si possono incontrare durante le competizioni. 
Questi programmi chiedono in input la flag, o una stringa in generale, e ne verificano la correttezza. 
Un tool utile che permette di trovare tutte le stringhe contenute in un file è strings.

## Solution
If we analize the file with Ghidra we notice that the flag is stored after being xored with a key.
This key is saved in the program so we can get it and xor every char with the corrispective in the flag.

## Flag
`flag{d21fe035}`