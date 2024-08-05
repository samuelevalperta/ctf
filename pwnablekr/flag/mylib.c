#include <stdio.h>

void exit(int exit_code) { return; }

char *strncpy(char dst, const char *restrict src, unsigned long dsize) {
  printf("%s\n", src);
}
