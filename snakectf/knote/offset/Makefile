obj-m = offset_module.o
KVERSION = $(shell uname -r)
dir = /home/samuele/ctf/snakectf/knote/offset
all:
	make -C /lib/modules/$(KVERSION)/build M=$(dir) modules
clean:
	make -C /lib/modules/$(KVERSION)/build M=$(dir) clean
