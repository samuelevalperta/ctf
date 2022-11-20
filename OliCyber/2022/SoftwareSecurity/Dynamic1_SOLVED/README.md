# Software 08 - Dynamic 1

## Description
> Le prossime challenge introducono il concetto dell'analisi dinamica. 
Prova a risolvere le challenge della serie Dynamic senza l'utilizzo di tool di analisi statica come Ghidra. 
Questo binario esegue la chiamata a funzione open(FLAG). Trova la flag provando con il comando ltrace, un tool che permette di tracciare le chiamate a funzione eseguite da un file binario. 
Puoi installare ad esempio su Ubuntu con apt install ltrace.

## Solution
```sh
ltrace sw-08
```
  
## Flag
`flag{e25b8bdf}`