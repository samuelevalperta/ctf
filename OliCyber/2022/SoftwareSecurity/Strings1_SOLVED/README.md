# Strings 1

## Description
Le prossime tre challenge sono strutturate in maniera simile ad alcune challenge di reverse engineering che si possono incontrare durante le competizioni. 
Questi programmi chiedono in input la flag, o una stringa in generale, e ne verificano la correttezza. 
Un tool utile che permette di trovare tutte le stringhe contenute in un file è strings.

## Solution
```sh
strings sw-04 | grep flag
```

## Flag
`flag{0cca06f6}`