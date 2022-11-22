# Software 19 - Pwntools 3

## Description
> Pwntools permette anche di interagire con binari locali. Si può utilizzare la funzione process(), che ritorna un oggetto come remote().
Spesso conviene avere uno script che permette di scegliere se lanciare il binario locale o se connettersi al server remoto. Il seguente snippet di codice può tornare utile in questi casi:
La funzione ELF permette di caricare dei binari ELF e di ottenere diverse informazioni. Per esempio exe.sym ritorna un dizionario di elementi simbolo : indirizzo.
Per esempio exe.sym.main o exe.sym['main'] ritorna l'indirizzo della funzione main all'interno del binario.
Il binario di questa challenge ti chiederà l'indirizzo di alcune funzioni presenti al suo interno. Ti verrà anche fornito il binario che gira sul server remoto.
Puoi collegarti al servizio remoto con il comando:
nc software-19.challs.olicyber.it 13002

## Solution
`exploit.py`

## Flag
`flag{e353daccc34b6fbd}`


