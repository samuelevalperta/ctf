#include "stdlib.h"
#include "stdio.h"
#include <unistd.h>

int main (int argc, char *argv[])
{
    char test[20];
    read(0, test, 4);
    // scanf("%s", test);
    return 0;

}
