# Intagram Generator

## Description
> Ho trovato questo servizio che genera frasi per Instagram! Ad un certo punto però mi ha stampato delle frasi che non avrebbe dovuto mostrarmi...
Puoi collegarti al servizio remoto con:
nc intagram.challs.olicyber.it 10101

## Solution
The program save some Strings in the stack, one of which is the flag, and then ask us which String we want to read. We can read the flag sending  `-3` as index.

## Flag
`flag{w41t_th4ts_1ll3gal_c0m3_h41_f4tt0}`