#include <iostream>
#include <fstream>
using namespace std;
int result[] = {1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1};

class LFSR{
public:
    unsigned long long state, tap, size;

    LFSR(unsigned long long state, unsigned long long tap, uint size):
        state{state},tap{tap},size{size}{}
    
    int getbit(){
        int f = __builtin_popcountll(state & tap) & 1;
        int ret = state & 1;
        state >>= 1;
        state |= f << (size-1);
        return ret;
    }

    void backward(){
        int o = (state >> ( size - 1 )) & 1;
        state <<= 1;
        state &= (1 << size) -1;
        if ((__builtin_popcountll((state | 1) & tap) & 1) == 0)
            state |= 1;
    }
};

int main(){
    ifstream infile("thefile.txt");
    unsigned long long origin_states[3],taps[3],sizes[3] = {27,23,25};
    infile>>origin_states[0]>>origin_states[1]>>origin_states[2];
    taps[0] = (1 << 26) | (1 << 16) | (1 << 13) | 1;
    taps[1] = (1 << 22) | (1 << 7) | (1 << 5) | 1;
    taps[2] = (1 << 24) | (1 << 19) | (1 << 17) | 1;
    LFSR lfsr0 = LFSR(origin_states[0], taps[0], sizes[0]);
    LFSR lfsr1 = LFSR(origin_states[1], taps[1], sizes[1]);
    LFSR lfsr2 = LFSR(origin_states[2], taps[2], sizes[2]);

    char flag[30]={0};
    for (int i=0;i<29;i++){
        for (int j=0;j<8;j++){
            int x0,x1,x2,o;
            x0 = lfsr0.getbit();
            x1 = lfsr1.getbit();
            x2 = lfsr2.getbit();

            o = x0 ? x1:x2;
            flag[i] |= (result[i*8+j] ^ o) << (7-j);
        } 
    }
    cout << flag;
}