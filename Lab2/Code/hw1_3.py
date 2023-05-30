import sys
import re
import numpy as np
#import time

def is_prime(n):
    for i in range(2, n):
        if n % i == 0:
            return False   
    return True 

file_path = sys.argv[1]
E = set()
candidate = set()
band = 6
row = 20
n = band * row
num_news = 0
ids = []

#start_time = time.time()

#### Get shingles.
with open(file_path, 'r') as f:
    for line in f:
        num_news = num_news + 1 
        news_id = line.split()[0]
        ids.append(news_id)
        news = line.lstrip(news_id)
        news = news.lstrip()
        news = news.lower()
        news = re.sub('[^a-z ]',"",news)
        news = re.sub('\s+'," ",news)
        for i in range(len(news)-3+1):
            E.add(news[i:i+3])

#### Find out if news contains shingles.
E = list(E)
C = [[] for i in range(len(E))] 

with open(file_path, 'r') as f:
    for line in f:
        for i in range(len(E)):
            C[i].append(E[i] in line)
                           
#### Get hash function values.           
p = len(C)
while not is_prime(p):
    p = p + 1
a = np.random.randint(p, size = n).tolist()
b = np.random.randint(p, size = n).tolist()

H = [[] * n for i in range(len(C))] 
for i in range(len(C)):
    for j in range(n):
        H[i].append((a[j]*i+b[j])%p)
     
#### Make signature matrix
S = [[float('inf') for i in range(num_news)] for j in range(n)]
for i in range(len(C)):
    for j in range(num_news):
        if C[i][j] == True:
            for k in range(n):
                if S[k][j] > H[i][k]:
                    S[k][j] = H[i][k]
                             
#### Get candidates.
S = np.array(S)
for i in range(band):
    for j in range(num_news-1):
        for k in range(j+1,num_news):
            sig1 = S[i*row:(i+1)*row,j]
            sig2 = S[i*row:(i+1)*row,k]
            if np.array_equal(sig1, sig2):
                candidate.add((j, k))

#### Calculate similarity
candidate = list(candidate)
C = np.array(C)
for i in range(len(candidate)):
    set1 = C[:,candidate[i][0]]
    set2 = C[:,candidate[i][1]]
    set1_and_set2 = np.logical_and(set1, set2)
    set1_num = sum(set1)
    set2_num = sum(set2)
    and_num = sum(set1_and_set2)
    sim = float(and_num) / float(set1_num + set2_num - and_num)
    if sim >= 0.9:
        print("%s\t%s"%(ids[candidate[i][0]], ids[candidate[i][1]]))

#elapsed_time = time.time() - start_time
#print('It took %d seconds'%elapsed_time)

