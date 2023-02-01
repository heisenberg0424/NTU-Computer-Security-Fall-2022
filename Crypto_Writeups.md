# Crypto writeups

Done: Yes
Due date: October 21, 2022
Subject: 計算機安全

# Hw1 Writeups

## LSB

查看 server 端的 source code 可以知道和課堂上的例子差不多，只是從 mod 2 變為 mod 3

要注意在最後換算 long 的時候要改成 3 進制運算  

```jsx
# ref https://ce-automne.github.io/2020/02/16/RSA-LSB-Oracle攻击原理分析/
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
```

## Xor_revenge

原本以為和 lab 一樣要分兩部分暴力破解，但發現 get_bit ouput  前會空轉 36 次，導致原始 state 無法被輕易猜出，經過 **r10942074** 提示才知道能利用 XOR 特性可以找出 state。實際作法如下：

- 首先對 1,2,4,8,16,…….. 共 64 個 init state 輸出長為 n 的 output
- 利用類似 Gaussion elimination 的技巧把所有 output 化簡如下
    
    state0      [ 1, 0, 0, 0, ……..]
    
    state1       [ 0, 1, 0, 0, ……..]
    
    state2      [ 0, 0, 1, 0, ……..]
    
    …
    
    state64    [0, 0, 0, 0, …….1]
    
- 利用化簡出的 table 湊出能輸出 output 的 state
- 驗證是否為正確的 state ( 經測試 n 為 30,40,50 都可能找到錯誤的 state，所以最後 n 設 64

找到正確 state 後 reverse 回到輸出 output 的 state 即可逆 xor 找到 flag :

**FLAG{Y0u_c4N_nO7_Bru73_f0RCe_tH15_TiM3!!!}**

```python
output = [1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0]
notflag = output[-70:]

def listxor(a,b):
    x = []
    for i in range(len(a)):
        x.append(a[i]^b[i])
    return x

class crypto:
    def __init__(self,state):
        self.state = state
    
    def getbit(self):
        self.state <<= 1
        if self.state & (1 << 64):
            self.state ^= 0x1da785fc480000001
            return 1
        return 0
    
    def backward(self):
        if self.state & 1 :
            self.state ^= 0x1da785fc480000001
        self.state >>= 1

state = []
out = []
tmp = []

for i in range(64):
    gen = crypto(1 << i)
    state.append(1 << i)
    tmp.clear()
    for j in range(64):
        for _ in range(36):
            gen.getbit()
        tmp.append(gen.getbit())
    out.append(tmp[:])

for i in range(64):
    # print("Epoch: ",i)
    # for t in out:
    #     print(t) 
    for j in range(i,64):
        if out[j][i] == 1:
            out[i]  ,out[j]   = out[j]  ,out[i]
            state[i],state[j] = state[j],state[i]
            break
    for j in range(64):
        if j==i:
            continue
        if out[j][i] == 1:
            out[j] = listxor(out[j],out[i])
            state[j] ^= state[i]

target_state = state[0]
for i in range(1,64):
    if notflag[i] == 1:
        target_state ^= state[i]

gen = crypto(target_state)

flag_len = 406-70
for i in range(flag_len*37):
    gen.backward()

myoutput = []
for j in range(406):
    for _ in range(36):
        gen.getbit()
    myoutput.append(gen.getbit())

# print(myoutput[-70:])
# print(notflag)
tmp = 0
power = 7
for i in range(flag_len):
    tmp += (myoutput[i] ^ output[i]) * pow(2,power)
    power-=1
    if(power==-1):
        print(tmp.to_bytes(1,'big').decode(),end='')
        tmp = 0
        power = 7
```

## AES

這題我照著簡報中 Analytics Workflow 解題，由於題目已經附上 power trace 紀錄檔所以我們把 json 中資料整理一下就可以從 Step 2 開始

- 首先處理 Plaintexts 的第一個 byte，把所有 Plaintext 的第一個 byte 分別和 0x00, 0x01 …, 0xFF做 XOR 運算，得到一個 D x 256 的結果
- 再來把剛才的結果對照 Sbox 內的值取 Hamming Weight 更新表格
- 最後利用每個 Plaintext 的 Hamming Weight 對每個 trace 做 Correlation 的運算，得到 256 x trace 的 table
- 找出 correlation 最高的值就是 key
- 重複以上步驟得到 16 個 key

```python
import json
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

sbox =[ 0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
	    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
	    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
	    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
		0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
		0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
		0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
		0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
		0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
		0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
		0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
		0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
		0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
		0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
		0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
		0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]

def hamming(input):
    binary = format(input,'b')
    return binary.count('1')

with open('stm32f0_aes.json','r') as f:
    output = json.load(f)

key_len = 16
texts =  len(output)
traces = len(output[0]['pm'])
pm = []
pt = []
ans = ''
for i in range(texts):
    pm.append(output[i]['pm'])
    pt.append(output[i]['pt'])

pm = np.array(pm)
pt = np.array(pt)

for i in range(key_len):
    table = np.zeros((texts,256),dtype=np.int32)
    
    for idx in range(texts):
        for key in range(256):
            table[idx][key] = hamming( sbox[ pt[idx][i] ^ key ] )
    
    coe_matrix = np.zeros((256,traces),dtype=np.single)
    for k in tqdm(range(256),leave=False):
        for t in range(traces):
            coe_matrix[k,t] = np.corrcoef(table[:,k],pm[:,t])[0][1]
    flag = np.argmax( np.abs(coe_matrix))//traces
    ans+=chr(flag)

print("### FLAG ###")
print(ans)
```

**FLAG{** **18MbH9oEnbXHyHTR }**

## Node

這題也是照著 ppt 41 頁解，先檢查這題是不是 singular，確定是以後把 $\phi$ ( P(x,y) ) 寫出來，把 x,y 跟 output 帶入可得 dP 跟 P ， 用 discrete_log 可以找到 flag

```python
from Crypto.Util.number import long_to_bytes
from sage.all import *

output_x = 98015495932907076864096258407988962007376328849899810250322002325625359735922937686533359455570369291999900476297694445557845368802830788062976760815467239661283157094425185337540578842851843497177780602415322706226426265515846633379203744588829488176045794602858847864402137150751961826536524265308139934971 
output_y = 87166136054299272658534592982430361675520319206099499992529237663935246617561944716447831162561604277568397630920048376392806047558420891922813475124718967889074322061747341780368922425396061468851460185861964432392408561769588468524187868171386564578362923777824279396698093857550091931091983893092436864205
p = 143934749405770267808039109533241671783161568136679499142376907171125336784176335731782823029409453622696871327278373730914810500964540833790836471525295291332255885782612535793955727295077649715977839675098393245636668277194569964284391085500147264756136769461365057766454689540925417898489465044267493955801
a = -3
b = 2
x, y = 101806057140780850544714530443644783825785167075147195900696966628348944447492085252540090679241301721340985975519224144331425477628386574016040358648752353263802400527250163297781189749285392087154377684890287451078937692380556192126971669069015673662635561425735593795743852141232711066181542250670387203333, 21070877061047140448223994337863615306499412743288524847405886929295212764999318872250771845966630538832460153205159221566590942573559588219757767072634072564645999959084653451405037079311490089767010764955418929624276491280034578150363584012913337588035080509421139229710578342261017441353044437092977119013

alpha = 1
beta = -2

def phi(x,y):
    up = y + Mod(alpha-beta,p).sqrt() * (x - alpha)
    down = y - Mod(alpha-beta,p).sqrt() * (x - alpha)
    up = Mod(up,p)
    down = Mod(down,p)
    return up * inverse_mod(down,p)

dp = phi(output_x,output_y)
p = phi(x,y)

print("### FLAG ###")
print(long_to_bytes(discrete_log(dp,p)))
```