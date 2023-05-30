import sys

def EdgeIndex(a, b):
    index = int(a * (NumPage - (a - 1.0) / 2.0)+ b - a)
    return index

# Define priority between node u and node v (Lecture Note p.68) 
def SmallerThan(a, b):
    result = False
    if NodeDegree[a] < NodeDegree[b]:
        result = True
    elif (NodeDegree[a] == NodeDegree[b]) and (a < b):
        result = True

    return result

Triagle = []

### Step 0-1. Make EdgePair (in Lecture Note p.60) ###
# The page number is original number - 1 (ex. 1 -> 0)
EdgePair = set()

with open(sys.argv[1]) as f:
    for line in f.readlines():
        pages = line.split()
        page1 = int(pages[0]) - 1
        page2 = int(pages[1]) - 1
        if page1 < page2: 
            EdgePair.add((page1, page2))
        else:
            EdgePair.add((page2, page1))

### Step 0-2. Make EdgeIndexSingle (in Lecture Note p.60) ###
# First, define number of pages to initialize EdgeIndexSingle 
NumPage = 0

for edge in EdgePair:
    if NumPage < edge[0]:
        NumPage = edge[0]
    if NumPage < edge[1]:
        NumPage = edge[1]

NumPage = NumPage + 1

# Second, make EdgeIndexSingle
EdgeIndexSingle = [[] for _ in range(NumPage)]

for edge in EdgePair:
    EdgeIndexSingle[edge[0]].append(edge[1])
    EdgeIndexSingle[edge[1]].append(edge[0])

### Step 0-3. Make NodeDegree (in Lecture Note p.60) ###
NodeDegree = [0 for _ in range(NumPage)]

for i in range(NumPage):
    NodeDegree[i] = len(EdgeIndexSingle[i])

### Step 1-1. Make HeavyHitter (in Lecture Note p.61) ###
HeavyHitter = []
RootNumEdge = len(EdgePair)**0.5

for i in range(NumPage):
    if NodeDegree[i] >= RootNumEdge:
        HeavyHitter.append(i)

### Step 1-2. Count HeavyHitter Triagles (in Lecture Note p.63) ###
temp = len(HeavyHitter)
for i in range(0, temp-2):
    for j in range(i+1, temp-1):
        for k in range(j+1, temp):
            if HeavyHitter[j] in EdgeIndexSingle[HeavyHitter[i]]:
                if HeavyHitter[k] in EdgeIndexSingle[HeavyHitter[i]]:
                    if HeavyHitter[k] in EdgeIndexSingle[HeavyHitter[j]]:
                        Triagle.append((HeavyHitter[i],HeavyHitter[j],HeavyHitter[k]))

### Step 2. Count Other Triagles (in Lecure Note p.69) ###
for edge in EdgePair:
    if SmallerThan(edge[0], edge[1]):
        a = edge[0]
        b = edge[1]
    else:
        a = edge[1]
        b = edge[0]

    # Check whether it is heavy hitter
    if NodeDegree[a] >= RootNumEdge:
        continue
    
    # Find Triagle (B ~ D in Step 2)
    for c in EdgeIndexSingle[a]:    
        if not SmallerThan(b, c):
            continue
    
        if b not in EdgeIndexSingle[c]:
            continue
        
        if not SmallerThan(a, c):
            continue
        
        Triagle.append((a,b,c))

print(len(Triagle))

