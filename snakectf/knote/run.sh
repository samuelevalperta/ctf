#!/bin/sh

set -e
cd tmp
gcc -o exploit ../exploit.c -static

rm initramfs.cpio
find . -print0 | cpio -o --format=newc --null --owner=root > initramfs.cpio
cd ..;

qemu-system-x86_64 \
	-m 128M \
	-s \
	-nographic \
	-kernel "./bzImage" \
	-append "console=ttyS0 quiet loglevel=3 oops=panic panic=-1 pti=on" \
	-monitor /dev/null \
	-initrd "./tmp/initramfs.cpio" \
	-cpu qemu64,+smep,+smap,+rdrand \
	-no-reboot
