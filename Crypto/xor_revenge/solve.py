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
     