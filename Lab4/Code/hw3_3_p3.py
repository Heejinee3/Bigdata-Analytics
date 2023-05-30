import sys
import numpy as np

k = 10
N = 6000 
num_features = 122
C = 1.0
step = 0.4
accuracy = np.zeros(10)

### Define x data ###
x = []
with open(sys.argv[1]) as f:
    for line in f.readlines():
        feature = line.split(",")
        for i in range(len(feature)):
            feature[i] = float(feature[i])
        x.append(feature)
x = np.array(x, dtype = float)

### Define y data ###
y = []
with open(sys.argv[2]) as f:
    for line in f.readlines():
        y.append(float(line))
y = np.array(y, dtype = float)

for i in range(k):

    ### Define test data
    indexing = np.full(N, False)
    indexing[N/k*i: N/k*(i+1)] = True
    x_test = x[indexing, :]
    y_test = y[indexing]
    
    ### Define train data
    indexing = ~indexing
    x_train = x[indexing, :]
    y_train = y[indexing]
   
    ### Initialize w, b
    w = np.zeros(num_features, dtype = float) 
    b = 1.0 
    
    ### Update
    for j in range(100):
        result = y_train * (np.sum(x_train * w, axis = 1) + b)
        dw = w + C * np.sum(np.float32(result < 1.0) * (-1.0) * y_train * x_train.T, axis = 1)
        db = C * np.sum(np.float32(result < 1.0) * (-1.0) * y_train * b)

        w = w - step * dw
        b = b - step * db

    ### Calculate accuracy
    result_test = y_test * (np.sum(x_test * w, axis = 1) + b)
    well_classified = result_test > 0
    #print(well_classified)
    accuracy[i] = float(sum(well_classified)) / float(len(well_classified))

print(np.mean(accuracy))
print(C)
print(step)

