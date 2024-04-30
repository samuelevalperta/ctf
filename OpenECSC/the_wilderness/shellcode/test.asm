section .data
    array1 dd 1.0, 2.0, 3.0, 4.0         ; First array of single-precision floats
    array2 dd 5.0, 6.0, 7.0, 8.0         ; Second array of single-precision floats
    result dd 0.0, 0.0, 0.0, 0.0         ; Array to store the result

section .text
    global _start

_start:
    ; Load arrays into ZMM registers
    vmovaps zmm0, [array1]               ; Load array1 into ZMM0
    vmovaps zmm1, [array2]               ; Load array2 into ZMM1

    ; Perform vectorized addition
    vaddps zmm2, zmm0, zmm1              ; ZMM2 = ZMM0 + ZMM1

    ; Store the result back to memory
    vmovaps [result], zmm2               ; Store ZMM2 into result

    ; Exit the program
    mov eax, 60                          ; Syscall number for exit
    xor edi, edi                         ; Exit status (0)
    syscall                              ; Invoke syscall to exit

