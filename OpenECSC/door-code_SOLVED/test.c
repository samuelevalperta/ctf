#include <stdio.h>

int main() {
  long array[4];

  while(1){
    memset(&array, 0, 32);  
    scanf("%99lx", array);
  }
}
