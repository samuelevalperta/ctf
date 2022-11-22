# Software 17 - Pwntools 1

## Description
> Solitamente quando si affrontano delle challenge di tipo pwn è frequente interagire con un programma eseguito in remoto su un server.
Per facilitare la scrittura delle soluzione è possibile utilizzare pwntools, una libreria per python che offre diverse funzionalità, quali ad esempio:
Tubes: Wrapper I/O per connessioni remote o per binari locali
Packing: Conversioni tra numeri e bytes in little/big endian
ELFs: Caricare e analizzare ELF direttamente da python
Assembly: Assemblare codice on-the-fly
GDB Debug: Debuggare programmi con gdb
pwntools ci permette quindi di scrivere script in python che interagiscono con un servizio in locale o in remoto.
Per installare pwntools su Ubuntu è possibile eseguire i seguenti comandi da linea di comando:
$ apt install python3 python3-pip python3-dev
$ pip3 install pwntools
In questa challenge ti viene chiesto di connetterti ad un server remoto e di risolvere alcune semplici espressioni aritmetiche.
Tra gli attachments trovi un file python script.py che utilizza la libreria pwntools e alcuni esempi di interazione con un server remoto.
Puoi collegarti al servizio remoto con il comando:
nc software-17.challs.olicyber.it 13000

## Solution
`exploit.py`

## Flag
`flag{15af56f2f4295e9d38}`


