# privateclub

## Description
> Solo chi ha il badge potrà entrare nel mio club privato :)
nc privateclub.challs.olicyber.it 10015

## Solution
Quando ci viene chiesto il nome, se mandiamo più di 32 caratteri andremo a sovrascrivere la variabile local_14.
Se local_14 non contiene 0x10 il programma esegue `/bin/sh`,stampiano la flag con `cat flag.txt`.

## Flag
`flag{b4d_sc4nf}`