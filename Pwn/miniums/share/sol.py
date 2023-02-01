from pwn import *

context.arch = 'amd64'
context.terminal = ['tmux','splitw','-h']
ip = 'edu-ctf.zoolab.org'
port = 10011
local = False