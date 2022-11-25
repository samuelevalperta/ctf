#include "stdio.h"
#include "stdlib.h"
#include <unistd.h>
// #include <sys/mman.h>

void init()
{
  setbuf(stdout,(char *)0x0);
  setbuf(stdin,(char *)0x0);
}

int main ()
{
    init();
        
    // void *shellcode = mmap(NULL, 128, PROT_EXEC | PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    char shellcode[4];

    printf("Enter your shellcode (max 4 bytes):\n");
    
    read(0, shellcode, 4);
    
    // Exec the shellcode
    ((void (*)(void))shellcode)();
       
    return 0;
}
