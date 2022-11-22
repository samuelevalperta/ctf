# Software 10 - Dynamic 3

## Description
> Questo binario chiama la funzione access(FLAG). Tuttavia, come spesso accade, i binari eseguono molte chiamate ad altre funzioni, è quindi utile riuscire a filtrarle in qualche modo. 
Il comando ltrace fornisce l'opzione -e che permette di filtrare le funzioni chiamate.

## Solution
```ltrace -e 'access' ./sw-10```

## Flag
`flag{0f32826c}`