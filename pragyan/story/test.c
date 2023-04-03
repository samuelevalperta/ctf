#include "stdio.h"
#include "time.h"

void main(){
  srand(time(0x0) / 0x3c);
  long int value = rand() % 1000;
  printf("%ld", value);
}
