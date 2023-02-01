#include <iostream>
#include <vector>
#include <fstream>
#define LEN(a) (sizeof(a)/sizeof(a[0]))
using namespace std;

int result[] = {1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1};
int result_len = LEN(result);
int flag_len = result_len - 200;
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

double cal_cor(int a[], int b[]){
    int cnt =0;
    const int total = 200;
    for (int i=0;i<total; i++){
        if (a[i] == b[i])
            cnt++;
    }
    return (double)cnt/total;
}

vector<unsigned long long> get_state(unsigned long long tap, uint size){
    int output[result_len];
    vector<unsigned long long> vec;
    for (unsigned long long state = 0; state < 1ll << size; state++){
        LFSR lfsr = LFSR(state,tap,size);
        for (int i=0;i<result_len;i++)
            output[i] = lfsr.getbit();
        double cor = cal_cor(&output[flag_len], &result[flag_len]);
        if (cor >= 0.7){
            vec.push_back(state);
            cout<<"Caught cor: "<<cor<<endl;
        }
            
    }
    return vec;
}

int main(){
    cout<<"key_len :"<<result_len<<endl;
    cout<<"flag_len:"<<flag_len<<endl;

    unsigned char flag[(LEN(result)-200)/8 +1] = {0};
    int output[result_len];
    unsigned long long origin_states[3],taps[3],sizes[3] = {27,23,25};
    vector<vector<unsigned long long>> states;
    taps[0] = (1 << 26) | (1 << 16) | (1 << 13) | 1;
    taps[1] = (1 << 22) | (1 << 7) | (1 << 5) | 1;
    taps[2] = (1 << 24) | (1 << 19) | (1 << 17) | 1;

    for (int i=1;i<3;i++)
        states.push_back(get_state(taps[i], sizes[i]));
    cout<<"Done get state 1&2 "<<endl;
    for (unsigned long long state1 : states[0]){
        for (unsigned long long state2 : states[1]){
            for (unsigned long long state0 = 0; state0 < (1ll << sizes[0]); state0++){
                LFSR lfsr0 = LFSR(state0, taps[0], sizes[0]);
                LFSR lfsr1 = LFSR(state1, taps[1], sizes[1]);
                LFSR lfsr2 = LFSR(state2, taps[2], sizes[2]);
                int x0, x1, x2;
                for (int i=0;i<result_len;i++){
                    x0 = lfsr0.getbit();
                    x1 = lfsr1.getbit();
                    x2 = lfsr2.getbit();
                    output[i] = x0 ? x1 : x2;
                }
                double cor = cal_cor(&output[flag_len], &result[flag_len]);
                if (cor >= 1){
                    cout<<"Found 100% match"<<endl;
                    origin_states[0] = state0;
                    origin_states[1] = state1;
                    origin_states[2] = state2;
                    ofstream f("thefile.txt");
                    f<<state0<<endl;
                    f<<state1<<endl;
                    f<<state2<<endl;
                    f.close()
                    return 0;
                }
            }
        }
    }
}