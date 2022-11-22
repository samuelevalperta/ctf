# Software 16 - Dynamic 9

## Description
> Usando gdb è anche possibile cambiare il contenuto della memoria.
Il comando da utilizzare in questo caso è set {type}address = value, dove type indica il tipo della variabile all'indirizzo address. Per esempio set {int}0x650000 = 0x42.
Per trovare l'indirizzo di una variabile globale si può utilizzare il comando print insieme a &. Ad esempio p &var.
Il binario di questa challenge dichiara la variabile globale tochange. Nel main viene eseguita una chiamata a sleep(2), dopodichè il binario esegue delle operazioni aritmetiche sulla flag, controlla se il valore di tochange è stato cambiato correttamente, e in tal caso stampa la flag.
Usa gdb per aprire il binario, e metti un breakpoint sulla chiamata a sleep. Una volta raggiunto il breakpoint, cambia il contenuto della variabile tochange con il valore richiesto.

## Solution
We use `break sleep` to set a break before the function call, then we can retrive the address where `tochange` variable is located with `p &tochange`.
Now that we know the address of the variable we can assing the value that the program ask to be set with `set {unsigned long *}0x404038 = 0xdeadc0debadc0ffe`.

## Flag
`flag{1980000802282532}`


