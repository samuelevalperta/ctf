# Generatore Numeri (poco) Casuali

## Description
> Un mio collega ha di recente creato un generatore di numeri casuali da poterci accedere in qualsiasi momento esponendolo su internet... A me è sembrata una pessima idea, puoi dimostrargli il perchè?
Puoi collegarti al servizio remoto con:
nc gpc.challs.olicyber.it 10104

## Solution
In this challenge we have access to the source code so first of all we take a look at it.
The program generate a random value, which define the lenght of an array, then the address where this array is stored is printed to us and being the array the only local variable on this frame it corresponds to the value of the **rsp**.
Using `checksec` we notice that the program was compiled with no stack protection (canary) and no NX flag enabled, which allows us to execute things on the stack.