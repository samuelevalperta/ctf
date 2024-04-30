# Define variables
NASM = nasm
LD = ld
OBJCOPY = objcopy

# Default filename (shellcode.asm)
FILENAME ?= shellcode.asm

# Default target
all: shellcode.bin

# Rule to assemble assembly code into object file
shellcode.o: $(FILENAME)
	$(NASM) -f elf64 $(FILENAME) -o shellcode.o

# Rule to link object file into executable shellcode
shellcode: shellcode.o
	$(LD) shellcode.o -o shellcode

# Rule to extract binary text section from executable into shellcode.bin
shellcode.bin: shellcode
	$(OBJCOPY) -O binary -j .text shellcode shellcode.bin

# Clean rule to remove generated files
clean:
	rm -f shellcode.o shellcode shellcode.bin

.PHONY: all clean

