import sys
from pyspark import SparkConf, SparkContext

k = int(sys.argv[2])
init_pts = []

def line_to_point(l):
    p = l.split()
    for i in range(len(p)):
        p[i] = float(p[i])
    return p

def cal_dist(p1, p2):
    minus_p = []
    for i in range(len(p1)):
        minus_p.append((p1[i] - p2[i])**2)
        dist = (sum(minus_p))**(1/2)
    return dist

def cluster(p):
    min_dist = float("inf")
    for i in range(len(init_pts)):
        dist = cal_dist(p, init_pts[i])
        if dist < min_dist:
            min_dist = dist
            cluster_idx = i
    return (cluster_idx, p)

def cal_diam(pts):
    diam = 0
    for p1 in pts:
        for p2 in pts:
            length = cal_dist(p1, p2)
            if length > diam:
                diam = length
    return diam

conf = SparkConf()
sc = SparkContext(conf = conf)
lines = sc.textFile(sys.argv[1])
pts_rdd = lines.map(lambda l: line_to_point(l))
pts = pts_rdd.collect()

for i in range(k):
    max_dist = -1
    for j in range(len(pts)):
        min_dist = float("inf")
        for m in range(len(init_pts)):
            dist = cal_dist(pts[j], init_pts[m])
            if dist < min_dist:
                min_dist = dist
        if min_dist > max_dist:
            max_dist = min_dist
            add_idx = j
    init_pts.append(pts[add_idx])
    pts.pop(add_idx)

cluster_pts = pts_rdd.map(lambda p: cluster(p))
cluster_pts = cluster_pts.groupByKey()
diams = cluster_pts.map(lambda cpts: cal_diam(cpts[1]))
n = diams.count()
s = diams.reduce(lambda a, b: a + b)
avrg_diam = s/n

print(avrg_diam)
