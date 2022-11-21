# Software 11 - Dynamic 4

## Description
> Questo binario è simile al precedente, con la differenza che il binario esegue una fork() e il processo figlio esegue open(FLAG). 
Il comando strace permette di tracciare le syscall eseguite dai processi figli con l'opzione -f.

## Solution
```strace -f ./sw-11```

## Flag
`flag{5a11b5a6}`