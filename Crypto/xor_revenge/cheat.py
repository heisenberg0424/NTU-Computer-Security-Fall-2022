import random

output = [1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0]
non_flag_output = output[-70:]
flag_len = (len(output) - 70)
print(f'flag len: {flag_len}')

class generator:
    def __init__(self, state):
        self.state = state
    
    def getbit(self):
        self.state <<= 1
        if self.state & (1 << 64):
            self.state ^= 0x1da785fc480000001
            return 1
        return 0

    def backward(self):
        # test if bit 1 is 1
        if self.state & 1:
            self.state ^= 0x1da785fc480000001
        self.state >>= 1

# bits: the output out a given state
bits = []

# the states we give by ourselves
states = []

# given 64 different states to generate 64 output series with length 64 for every state
search_len = 64
for i in range(64):
    # 64 different states: (1 << i)
    gen = generator((1 << i))
    
    # generate the output series by using the state we assign
    out = []
    for j in range(search_len):
        for __ in range(36):
            gen.getbit()
        out.append(gen.getbit())
    bits.append(out)
    states.append((1 << i))

# then use gaussian deletion to find the state that can generate the output series with only one "1" at an assigned position
for i in range(search_len):
    # find the first row of the matrix with the given position being "1"
    swap_idx = 0
    for j in range(i, search_len):
        if bits[j][i] == 1:
            swap_idx = j
            break

    # swap the index we find with the given position
    bits[i], bits[swap_idx] = bits[swap_idx], bits[i]
    states[i], states[swap_idx] = states[swap_idx], states[i]

    # xor every bit after the given position
    for j in range(search_len):
        if j != i and bits[j][i] == 1:
            for k in range(i, search_len):
                bits[j][k] ^= bits[i][k]
            states[j] ^= states[i]

# according to the first 64 bits of non_flag_output, caculate the state
state = 0
for i in range(search_len):
    if non_flag_output[i] == 1:
        state ^= states[i]

# start from the state we just found, to test if this state is the true state that can generate all the outputs of non_flag_out
gen = generator(state)
out = []
for _ in range(70):
    for __ in range(36):
        gen.getbit()
    out.append(gen.getbit())
print(f'find state: {out == non_flag_output}')

# update the state backward to the initial state
gen = generator(state)
for i in range(flag_len):
    for _ in range(37):
        gen.backward()
state = gen.state
print(f'init state: {state}')

# turn the bit back to ascii code
flag = ""
for i in range(flag_len // 8):
    word = 0
    for j in range(8):
        for __ in range(36):
            gen.getbit()
        word |= (gen.getbit() ^ output[i*8+j]) << (7 - j)
    flag += chr(word)

print(flag)

