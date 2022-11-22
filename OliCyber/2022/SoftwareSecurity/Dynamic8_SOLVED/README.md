# Software 15 - Dynamic 8

## Description
> Nelle challenge precedenti è stata inserita volutamente un'istruzione int 3 in modo che il debugger si fermasse da solo.
Ora dovrai inserire manualmente un breakpoint, come si è soliti fare durante l'utilizzo di un debugger.
Con gdb è possibile inserire breakpoint utilizzando l'istruzione break, abbreviata b.
I due casi più frequenti sono break *addresse break function.
Il primo crea un breakpoint che viene azionato quando il programma esegue l'istruzione che si trova all'indirizzo address.
Mentre il secondo permette di mettere un breakpoint direttamente su una funzione.
Possiamo specificare address come offset rispetto ad una funzione, per esempio b *main+10 mette un breakpoint sull'istruzione che si trova 10 byte dopo l'inizio della funzione main.
Questa sintassi risulta utile quando combinata con l'istruzione disassemble function_name, che permette di disassemblare il contenuto di una funzione mostrando gli offset delle varie istruzioni rispetto all'indirizzo della funzione.
Qu esto programma crea una variable unsigned long sullo stack, e dopo averla inizializzata esegue diverse operazioni aritmetiche.
La flag è il valore in esadecimale, inserito dentro alle parentesi di flag{} senza gli zeri in eccesso e senza 0x, della variable sullo stack nel momento dell'invocazione della funzione puts che si trova nel main.
Utilizzando il comand break metti un breakpoint sulla chiamata alla puts() nella funzione main, e con il comando x stampa il contenuto della variabile in esadecimale. La variabile si trova a $rbp-0x8.

## Solution
We open the file with `gdb`, we set a breakpoint with `break puts` and, after running the program,  we print the value of the unsigned long variable using `x/gx $rbp-0x8`.

## Flag
`flag{2823a0c041}`


