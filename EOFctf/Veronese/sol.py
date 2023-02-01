import requests

url = "http://edu-ctf.zoolab.org:10020/" + "to_image"
file_data = open("a.txt", "rb")

#r = requests.post(url, files={"code": file_data})

#print(r.text)

url = "http://edu-ctf.zoolab.org:10020/" + "exec"
img_data = open("img.webp", "rb")

r = requests.post(url, files={"code": file_data,"img": img_data})

print(r.text)