# Software 18 - Pwntools 2

## Description
> In questa challenge vedrai come utilizzare le funzioni di packing e unpacking the pwntools offre.
Queste sono utili durante lo sviluppo di exploit in quando ti permettono di convertire per esempio indirizzi di memoria in forma numerica nella loro rappresentazione in bytes in little o big endian.
Pwntools offre dei wrapper per la libreria struct di python (che offre struct.pack).
p64(num, endianness="little", ...) Esegue il packing di un integer a 64 bit
p64(num, endianness="little", ...) Esegue il packing di un integer a 32 bit
u64(data, endianness="little", ...) Esegue l'unpacking di integer a 64 bit
u32(data, endianness="little", ...) Esegue l'unpacking di integer a 32 bit
Per esempio:
p64(0x401020) -> b"\x20\x10\x40\x00\x00\x00\x00\x00"
u32(b"\x00\x50\x40\x00") -> 0x405000
Puoi trovare maggiorni informazioni nella documentazione relativa
Il binario di questa challenge ti chiederà di eseguire delle operazioni di conversione utilizzando le funzioni di packing di pwntools.
Puoi collegarti al servizio remoto con il comando:
nc software-18.challs.olicyber.it 13001
## Solution
`exploit.py`

## Flag
`flag{ab2dde2a2b764d65}`


