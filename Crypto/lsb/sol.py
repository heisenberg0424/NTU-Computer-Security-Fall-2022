# ref https://ce-automne.github.io/2020/02/16/RSA-LSB-Oracle%E6%94%BB%E5%87%BB%E5%8E%9F%E7%90%86%E5%88%86%E6%9E%90/
from Crypto.Util.number import long_to_bytes, bytes_to_long
from pwn import *
from tqdm import tqdm

server = remote('edu-ctf.zoolab.org', 10102)
n = int( server.readline() )
e = int( server.readline() )
enc = int( server.readline() )

def send2server(s):
    server.sendline(s)
    r = server.recvline().strip()
    return int(r)

sub = 0
bits_3 = []
for i in tqdm(range(n.bit_length())):
    c1 = enc * pow(3,e*i*-1,n)
    c1 %= n 
    c1 = str(c1)
    result = send2server(c1)
    result = (result - sub) % 3
    bits_3.append(result)
    sub = (sub * pow(3, -1, n) + pow(3, -1, n) * result) % n

flag = 0
print('Calculateing FLAG.....')
for i,j in enumerate(bits_3):
    flag += pow(3,i) * j

print(long_to_bytes(flag))



