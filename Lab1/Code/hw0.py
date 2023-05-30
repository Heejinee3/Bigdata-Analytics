import re
import sys
from pyspark import SparkConf, SparkContext

alphabet = 'abcdefghijklmnopqrstuvwxyz'
j = 0

conf = SparkConf()
sc = SparkContext(conf=conf)
lines = sc.textFile(sys.argv[1])
words = lines.flatMap(lambda l: re.split(r'[^\w]+', l))
words1 = words.map(lambda w: w.lower())
words2 = words1.distinct()
pairs = words2.map(lambda w: (w[0], 1) if len(w) != 0 else ('', 1))
pairs1 = pairs.filter(lambda p: True if p[0].isalpha() else False)
counts = sorted(pairs1.countByKey().items())

for i in range(26):
    if (j < len(counts)) and (counts[j][0] == alphabet[i]):
        print('%s\t%d' %(counts[j][0],counts[j][1]))
        j = j + 1
    else:
        print('%s\t0' %(alphabet[i]))
