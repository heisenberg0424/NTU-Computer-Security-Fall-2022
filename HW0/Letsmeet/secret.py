from output import *
import time
import numpy as np
key4 = pow(4668,65537,p)
print('key4: ',key4)
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


#xortable01 = np.zeros((998,998), dtype=np.float64)
xortable01 = [[0] * 998 for i in range(998)]
i=-1
for key0 in keytable0:
    i+=1
    j=-1
    for key1 in keytable1:
        j+=1
        xortable01[i][j] = key0^key1
print("xortable01 created")

#xortable23 = np.zeros((998,998), dtype=np.float64)
xortable23 = [[0] * 998 for i in range(998)]

i=-1
for key2 in keytable2:
    i+=1
    j=-1
    for key3 in keytable3:
        j+=1
        xortable23[i][j] = key2^key3
print("xortable23 created")


hint = hint ^ key4
for key0 in range(998):
    start = time.time()
    for key1 in range(998):
        #tmp = hint^xortable01[key0][key1]
        for key2 in range(998):
            for key3 in range(998):
                pass
    end = time.time()
    print("執行時間：%f 秒" % (end - start))
                    



