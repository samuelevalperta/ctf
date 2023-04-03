#include "stdio.h"

void main(uint param_1,int param_2)

{
  uint uVar1;
  ulonglong uVar2;
  longlong lVar3;
  char cVar4;
  undefined4 uVar5;
  uint uVar6;
  longlong lVar7;
  longlong lVar8;
  uint local_2c;
  int local_28;
  
  lVar8 = CONCAT44(param_2,param_1);
  if (param_2 == 0 && (uint)(0x4fff < param_1) <= (uint)-param_2) {
    uVar5 = 0;
  }
  else {
    lVar3 = 0;
    local_2c = 1;
    local_28 = 0;
    do {
      if (lVar8 == 0) {
        return 0;
      }
      lVar7 = __umoddi3(lVar8,10,0);
      lVar3 = lVar7 * CONCAT44(local_28,local_2c) + lVar3;
      uVar1 = (uint)((ulonglong)lVar3 >> 0x20);
      lVar7 = __udivdi3(lVar8,10,0);
      uVar6 = (uint)((ulonglong)lVar7 >> 0x20);
      lVar8 = __udivdi3(lVar8,10,0);
      uVar2 = (ulonglong)local_2c;
      local_2c = (uint)(uVar2 * 10);
      local_28 = local_28 * 10 + (int)(uVar2 * 10 >> 0x20);
    } while (((uVar6 <= uVar1 && (uint)((uint)lVar3 < (uint)lVar7) <= uVar1 - uVar6) ||
             ((lVar7 + lVar3) * (lVar7 + lVar3) != CONCAT44(param_2,param_1))) ||
            (cVar4 = check_(lVar3), cVar4 == '\0'));
    uVar5 = 1;
  }
  return uVar5;
