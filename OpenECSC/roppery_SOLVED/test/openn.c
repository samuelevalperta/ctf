#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

int main(){
  int fd = open("flag.txt", O_RDONLY);
  printf("%d\n", fd);
}