# Software 03 - Sezioni

## Description
> Gli ELF sono composti da diverse sezioni, per esempio il codice eseguibile risiede nella sezione .text, le variabili globali non inizializzate risiedono nella sezione .bss, e così via. Può quindi tornare utile saper elencare le sezioni presenti in un file ELF. 
In particolare questo ELF ha una sezione misteriosa, cosa contiene? 
Un tool utile per analizzare gli object files è objdump, l'opzione -h ti permette di elencare le sezioni di un ELF.

## Solution
Doing `objdump -h sw-03` we find out that our file has a `.super-secret-section` section.
We can display the section details with `readelf -t .super-secret-section sw-03` and get the flag.

## Flag
`flag{d03lvn4i}`