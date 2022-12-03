# supermegaiperencryption

## Description
> Supermegaiper-Buongiornissimo!
Per proteggere le nostre supermegaipersegrete conversazioni abbiamo messo al lavoro i nostri matematici supermegaiperbravi che hanno reali
Per essere più sicuri che non riuscirai a rompere la nostra supermegaipercriptazione, abbiamo dirittura fatto più livelli di supermegaiper
Facci sapere se riuscirai a rompere la nostra supermegaiperbella creazione, ma non supermegaipercrediamo ;) SIUUUUUUUUM!
Puoi collegarti al servizio remoto con:
nc supermegaiperencryption.challs.olicyber.it 10803

## Solution
This is a reverse engineering challenge, we need to analyze the binary using our preferred decompiler to understand its operation.

After some work we realize that the program encrypts the flag through 3 functions called **lvl1**, **lvl2** and **lvl3** and then print the result.

### lvl1
```c
int lvl1(long flag_str,int len)

{
  char flag[i];
  int i;
  
  for (i = 0; i < len; i = i + 1) {
    flag[i] = *(char *)(flag_str + i);
    if (flag[i] < 'd') {
      flag[i] = flag[i] + -0x14;
    }
    else if ('c' < flag[i]) {
      flag[i] = flag[i] + 'd';
    }
    *(char *)(i + flag_str) = flag[i];
  }
  return len;
}
```
For each character of the flag this operation subtracts `0x14` from its ASCII value if the character is `a`, `b` or `c`, otherwise increases it by `0x64`.

###lvl2
```c
 void lvl2(char *flag_str,int len)

{
  size_t digits_of_ascii_value;
  size_t 1;
  long in_FS_OFFSET;
  int offset;
  int index;
  char ascii_value [8];
  char digits_of_(digits_of_ascii_value) [8];
  char enc_flag [520];
  
  canary = *(long *)(in_FS_OFFSET + 0x28);
  offset = 0;
  for (index = 0; index < len; index = index + 1) {
    sprintf(ascii_value,"%d",(ulong)((int)flag_str[index] & 0xff));
    digits_of_ascii_value = strlen(ascii_value);
    sprintf(digits_of_(digits_of_ascii_value),"%d",digits_of_ascii_value & 0xffffffff);
    1 = strlen(digits_of_(digits_of_ascii_value));
    strcpy(enc_flag + offset,digits_of_(digits_of_ascii_value));
    offset = offset + (int)1;
    strcpy(enc_flag + offset,ascii_value);
    offset = offset + (int)digits_of_ascii_value;
  }
  strcpy(flag_str,enc_flag);
  strlen(flag_str);
  return;
```

I named a variable `1` because of this: being the ASCII

