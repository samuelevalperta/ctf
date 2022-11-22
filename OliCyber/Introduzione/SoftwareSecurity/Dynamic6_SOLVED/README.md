# Software 13 - Dynamic 6

## Description
> Con gdb è possibile stampare il risultato di espressioni utilizzando il comando print, abbreviabile con p.
La sua sintassi è print/f expr o print expr, dove:
print è il comando
f è il formato con il quale stampare il risultato dell'espressione:
x per l'esadecimale
f per i float
d per i numeri interi con segno
u per i numeri interi unsigned
...
expr può essere un registro, come ad esempio $rax, ma può anche essere un espressione aritmetica come $rax+0x100.
Questo programma salva la flag all'interno del registro $rax e poi esegue int 3.
Apri il programma con gdb e al breakpoint leggi $rax utilizzando il comando p.
Per ottenere la flag stampa il registro come numero intero SIGNED e inserisci il risultato dentro a flag{} (senza il segno +/-).

## Solution
```gdb ./sw-13``` and then ```p/d $rax```

## Flag
`flag{415710747049308268}`


