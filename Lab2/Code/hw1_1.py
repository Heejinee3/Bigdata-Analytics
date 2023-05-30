import sys
from pyspark import SparkConf, SparkContext
#import time

def find_common_friends(l):
    me_and_friends = l.split('\t')
    friends = me_and_friends[1]
    friends = friends.split(",")
    friends.sort()
    
    key_list = []
    for i in range(len(friends)-1):
        for j in range(i+1, len(friends)):
            key_list.append(((friends[i], friends[j]), 1))
    
    return key_list

def find_friends(l):
    me_and_friends = l.split('\t')
    me = me_and_friends[0]
    friends = me_and_friends[1]
    friends = friends.split(",")
    
    key_list = []
    for i in range(len(friends)):
        if me <= friends[i]:
            key_list.append(((me, friends[i]), 1))
    
    return key_list

#start_time = time.time()

conf = SparkConf()
sc = SparkContext(conf = conf)
lines = sc.textFile(sys.argv[1])
common_friends1 = lines.flatMap(find_common_friends)
friends = lines.flatMap(find_friends)
common_friends2= common_friends1.subtractByKey(friends)
count = common_friends2.reduceByKey(lambda x, y: x + y)
sorted_count = count.sortBy(lambda c: (-c[1],c[0][0],c[0][1]))
result = sorted_count.take(10)

#time_spent = time.time() - start_time

for i in range(10):
    if len(result) > i:
        print(result[i][0][0],'\t',result[i][0][1],'\t',result[i][1])

#print('It took ', time_spent, 'seconds.')

