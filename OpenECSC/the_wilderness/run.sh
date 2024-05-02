#!/bin/sh

echo "[+] starting challenge..."
./sde-external-9.33.0-2024-01-07-lin/sde64 -no-follow-child -cet -cet_output_file /dev/null -debug -- ./build/the_wilderness
echo "[+] challenge stopped"
