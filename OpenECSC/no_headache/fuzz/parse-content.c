#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
  unsigned long j, k;
  long i, v9, idx_from_start, idx, idx_, v2;
  char *key, *v8, *set_start;

  char *new_obj_content = malloc(0x1000);
  char *content = malloc(0x1000);

  v8 = new_obj_content;
  v9 = 0LL;

  // Handle input like program does
  if (!fgets(new_obj_content, 4096, stdin))
    exit(1);
  char *v1 = strchr(new_obj_content, 10);
  if (v1)
    *v1 = 0;

  // Start parsing
  while (1) {
    set_start = v8;
    for (i = 0LL; v8[i] != '=' && v8[i] != ';' && v8[i];
         ++i) // increment i till ; = \0 are found
      ;
    if (!v8[i]) // if we found nullbyte break out
      break;
    if (v8[i] == ';') {
      v8 += i + 1; // if we have a ; move v8 after it
    } else {       // if i is =
      v8 += i + 1; // move v8 after the =
      for (j = 0LL; v8[j] != ';' && v8[j];
           ++j) // increment j till ; or \0 are found
        ;
      if (v9) { // add \0 to the end of the set
        v2 = v9++;
        new_obj_content[v2] = 0;
      }
      while (*set_start !=
             '=') // until we found an = from the beginning of this set
      {
        key = set_start++;
        idx = v9++;
        new_obj_content[idx] = *key;
      }
      idx_ = v9++;
      new_obj_content[idx_] = 0; // add \0 at end of the key, instead of =
      for (k = 0LL; k < j; ++k) {
        idx_from_start = v9++;
        // content[set_end - set_start + value_idx]
        new_obj_content[idx_from_start] = content[v8 - new_obj_content + k];
      }
      if (v8[j]) // move v8 after the set
        v8 += j + 1;
    }
  }
  new_obj_content[v9] = 0;
}
