# Software 09 - Dynamic 2

## Description
> Questo binario è identico a quello di Dynamic 1, compilato però questa volta staticamente. 
Non è quindi più possibile utilizzare il comando ltrace, in quanto funziona solamente con binari linkati dinamicamente. 
Prova ad usare il comando strace, un tool che permette di fare il trace delle syscalls eseguite da un binario. 
Su Ubuntu: apt install strace

## Solution
```sh
stracei ./sw-09
```
  
## Flag
`flag{01b81d48}`