# Software 11 - Dynamic 5

## Description
> Questo programma esegue 3 istruzioni mov, e poi esegue una int 3.
int 3 è un istruzione che viene utilizzata dai debugger per mettere i breakpoint e fermare l'esecuzione del programma.
Uno dei più famosi debugger, per ambienti linux, è gdb di cui puoi trovare una introduzione nel modulo di Software Security 2. Per installare gdb su Ubuntu: apt install gdb
Apri con gdb il binario (gdb ./chall).
Con il comando run il programma verrà eseguito dal debugger.
Ad ogni momento puoi premere CTRL-C per mettere in pausa l'esecuzione del programma, per poi utilizzare continue per riprenderne l'esecuzione.
Con il comando info registers puoi stampare lo stato dei registri della cpu.
Aspetta l'esecuzione della int 3 e poi leggi il contenuto dei registri con info registers, concatena il valore dei primi tre registri in esadecimale e inseriscilo dentro flag{} (senza il 0x prima dei valori).
Come per il resto delle challenge Dynamic, prova a risolverle senza l'utilizzo di tool di analisi statica come Ghidra.

## Solution
`gdb ./sw-12` and then `info registers`

## Flag
`flag{15af56f2f4295e9d38}`


