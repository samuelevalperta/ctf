# privateclub

## Description
> Solo chi ha il badge potrà entrare nel mio club privato :)
nc privateclub.challs.olicyber.it 10015

## Solution
Secondo la logica del programma se la variabile local_14 contiene un valore diverso da 0x10 il viene eseguito `/bin/sh`, possiamo sovrascrivere il valore di quella variabile grazie ad un overflow al momento della richiesta del nostro nome.
Una volta aver sovrascritto la variabile otterremo la shell e potremo cattuare la flag con `cat flag.txt`.

## Flag
`flag{b4d_sc4nf}`