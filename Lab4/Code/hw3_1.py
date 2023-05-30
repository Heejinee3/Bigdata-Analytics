import sys
from pyspark import SparkConf, SparkContext

beta = 0.9
n = 1000
v = [1.0/n for _ in range(n)]
w = [1.0/n for _ in range(n)]

def line_to_srcdest(l):
    p = l.split()
    k = int(p[0])-1
    v = int(p[1])-1
    return (k, v)

def modify_srcdest(sd):
    v = 1.0/len(sd[1])
    return (sd[0],(v, sd[1]))

def srcdest_to_destsrc(sd):
    l = []
    t = (sd[0], sd[1][0])
    for x in sd[1][1]:
        l.append((x, t))
    return l

def calc(ds):
    sum = 0.0
    for t in ds[1]:
        sum = sum + t[1] * v[t[0]]
    result = beta * sum + (1.0 - beta) * w[ds[0]]
    return (ds[0], result)

conf = SparkConf()
sc = SparkContext(conf=conf)
lines = sc.textFile(sys.argv[1])
srcdest = lines.map(line_to_srcdest) ### Make (source,dest)
srcdest = srcdest.distinct() ### Drop duplication
srcdest = srcdest.groupByKey() ### Make (source,[dest1,dest2,...,destn])  
srcdest = srcdest.map(modify_srcdest) ### Make (source,(1/n,[dest1,...,destn]))
destsrc = srcdest.flatMap(srcdest_to_destsrc) ### Make (dest1,(source,1/n)),...,(destn,(source,1/n))
destsrc = destsrc.groupByKey() ### Make (dest,[(source1,1/n1),...,(sourcem,1/nm)]

for i in range(50):
    result = destsrc.map(calc) ### Calculate PageRank using Taxation: result is (dest, new_v)
    result = result.collect() ### Make list
    v = [(1.0 - beta) / n for _ in range(n)] ### One row can be 0 (that is not appeared in destsrc). 
                                             ### In that case, new v is probability to teleport random page (taxation)
    for x in result:
        v[x[0]] = x[1] ### set new v

sorted_v = [(i, v[i]) for i in range(n)]
sorted_v.sort(key = (lambda t: t[1]), reverse = True) ### Sort v to find highest PageRank
for i in range(10):
    print("%d\t%.5f" %(sorted_v[i][0]+1, sorted_v[i][1]))

