deadbeef = [0xde,0xad,0xbe,0xef]
section = [0xde,0xad,0xbe,0xef]

for i in range(4):
    print(hex(section[i]^deadbeef[i]))    
