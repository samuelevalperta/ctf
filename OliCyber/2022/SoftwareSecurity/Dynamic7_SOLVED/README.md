# Software 14 - Dynamic 7

## Description
> Con gdb è possibile ancora ispezionare il contenuto della memoria.
La sintassi del comando per ispezionare la memoria é x/nfu addr, dove:
x -> Examine (esamina)
n -> Numero intero che specifica quanti elementi stampare (opzionale, di default 1)
f -> Formato con il quale stampare la memoria, per esempio: (opzionale, di default x)
- s per le stringhe
- i per il disassembly
- x per l'esadecimale
- f per i float
- d per i numeri interi con segno
...
u -> La dimensione di ogni elemento da stampare, per esempio: (opzionale, di default w):
- b Bytes
- h Halfwords (2 bytes)
- w Words (4 bytes)
- g Giant words (8 bytes)
addr può essere sia un indirizzo di memoria, come 0x5000000, sia un registro che contiene un indirizzo, come $rax.
Insieme ad addr si possono specificare delle operazioni aritmetiche, ad esempio $rax+8.
Questo programma salva la flag in una variabile unsigned int (4 byte) sullo stack e poi esegue int 3.
Apri il programma con gdb e al breakpoint leggi la variabile utilizzando il comando x, la variabile sullo stack si troverà a $rbp-4.
Per ottenere la flag stampa la variabile come un float e inserisci SOLO la parte intera dentro a flag{}.

## Solution
```gdb ./sw-14``` then ```x/f $rbp-4```

## Flag
`flag{31337}`


