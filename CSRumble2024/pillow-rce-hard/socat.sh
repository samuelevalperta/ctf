#!/bin/sh

socat TCP-LISTEN:4143,reuseaddr,fork,su=chall EXEC:./chall.py,stderr
