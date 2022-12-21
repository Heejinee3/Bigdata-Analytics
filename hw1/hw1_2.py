import sys
#import time

#start_time = time.time()

file_path = sys.argv[1]
support = 200
C1 = {}
num_fre_items = 0

#### First Pass : Count items
with open(file_path, 'r') as f:
    for line in f:
       basket = line.split()
       for i in basket:
           C1[i] = C1.get(i, 0) + 1

#### Beween First Pass and Second Pass: Select frequent items          
num_fre_items = 0
for key, value in C1.items():
    if value < support:
        C1[key] = -1
    else:
        C1[key] = num_fre_items
        num_fre_items = num_fre_items + 1

C2 = [0 for i in range(int(num_fre_items*(num_fre_items - 1.0) / 2.0))]
temp = [False for i in range(num_fre_items)]

#### Second Pass: Count frequent item pairs
with open(file_path, 'r') as f:
    for line in f:
        basket = line.split()
        
        for i in basket:
            if C1[i] != -1:
                temp[C1[i]] = True

        for i in range(num_fre_items - 1):
            for j in range(i + 1, num_fre_items):
                if temp[i] == True and temp[j] == True:
                    index = int(i*(num_fre_items-i/2.0-1.0/2.0)+j-i-1.0)
                    C2[index] = C2[index] + 1
        temp = [False for i in range(num_fre_items)]

#### After Second Pass: Adjust frequent items dictionary to list
temp = []
for key, value in C1.items():
    if value == -1:
        temp.append(key)
for key in temp:
    del C1[key]
C1 = sorted(C1.items(), key = lambda item: item[1])
for i in range(len(C1)):
    C1[i] = C1[i][0]

#### After Second Pass: Make frequent item pairs list
k = 0
for i in range(len(C1) - 1):
    for j in range(i+1, len(C1)):
        if C2[k] < support:
            del C2[k]
        else:
            C2[k] = (C1[i], C1[j], C2[k])
            k = k + 1
C2 = sorted(C2, key = lambda item: item[2], reverse = True)

#elapsed_time = time.time() - start_time

print(num_fre_items)
print(len(C2))
for i in range(10):
    if i < len(C2):
        print('%s\t%s\t%d'%(C2[i][0],C2[i][1],C2[i][2]))

#print("It took %d seconds"%(elapsed_time))
