# Software 01 - Architetture

## Description
> In questa serie di challenge verranno introdotte le basi necessarie ad affrontare le challenge che rientrano nelle categorie di reverse engineering e pwn (altrimenti dette binary). 
Nelle sfide di reverse vi verrà richiesto di analizzare un programma, comprenderne il funzionamento e trovare la flag che nasconde al suo interno. 
Nelle sfide di pwn l'obiettivo sarà invece di sfruttare dei bug presenti in un programma per alterare la logica di esecuzione del programma stesso mentre viene eseguito su un server remoto. 
Per poter affrontare queste sfide bisogna prima di tutto essere familiari con i file binari che su Linux prendono nome di ELF. 
Nelle seguenti challenge (e nella maggior parte delle challenge di tipo binary, se non meglio specificato) vi verrà fornito un file ELF per ambiente Linux, dovrete analizzarlo e trovare la flag al suo interno. 
Nella prima challenge viene richiesto di trovare l'architettura del file ELF. 
Il formato della flag è flag{architettura}.

## Solution
```sh
file sw-01
```
  
## Flag
`flag{aarch64}`