import numpy as np
import sys

U_idx = 600
U_idx = U_idx - 1
num_sim = 10
movie_rng = 1000
top_movie_num = 5

### Get data ###

data_arr = []
f = open(sys.argv[1], 'r')
lines = f.readlines()
for line in lines:
    line = line.split(",")[0:3]
    data_arr.append(line)
data_arr = np.array(data_arr, dtype = np.float64)
f.close()

### Make utility matrix ###

size = np.max(data_arr[:,0:2], axis = 0).astype(int)
util_mtx = np.full(size, -5.0)

for data in data_arr:
    util_mtx[int(data[0]-1), int(data[1]-1)] = data[2]
    
### Normalize utiliry matrix ###

mean_arr = []

for i in range(size[0]):
    tmp_arr = []
    for j in util_mtx[i]:
        if j != -5:
            tmp_arr.append(j)
    if len(tmp_arr):
        mean = np.mean(tmp_arr)
    else:
        mean = 0.0
    mean_arr.append(mean)
    for j in range(size[1]):
        rating = util_mtx[i, j]
        if rating != -5:
            util_mtx[i, j] = rating - mean
            
mean_arr = np.array(mean_arr)            

### Get top similar users ###

cos_sim = []

tmp_arr = []
for i in range(size[1]):
    if util_mtx[U_idx, i] != -5: 
        tmp_arr.append(util_mtx[U_idx, i])
den1 = np.linalg.norm(tmp_arr)

for i in range(size[0]):
    dot = 0.0 
    tmp_arr = []
    
    for j in range(size[1]):
        if util_mtx[i, j] != -5 and util_mtx[U_idx, j] != -5:
            dot = dot + util_mtx[i, j] * util_mtx[U_idx, j]
            
    for j in range(size[1]):
        if util_mtx[i, j] != -5:
            tmp_arr.append(util_mtx[i, j])
    den2 = np.linalg.norm(tmp_arr)

    cos_sim.append(dot/(den1 + 1e-15)/(den2 + 1e-15))

top_sim_usr = np.argpartition(cos_sim, -1*(num_sim+1))[-1*(num_sim+1):]
top_sim_usr = np.setdiff1d(top_sim_usr,[U_idx])

### Get top movies ###

U_1to1000 = np.zeros(movie_rng, dtype = tuple)
calc_U_arr = util_mtx[top_sim_usr,0:movie_rng]
calc_U_arr = calc_U_arr + mean_arr[top_sim_usr].reshape(1,-1).T

for i in range(movie_rng):
    s = 0.0
    d = 0.0
    for j in range(num_sim):
        if calc_U_arr[j, i] > 0:
            s = s + calc_U_arr[j, i]
            d = d + 1.0
    if d == 0:
        U_1to1000[i] = (i+1, 0)
    else:
        U_1to1000[i] = (i+1, -1.0*s/d)
        
dtype = [('movieID', int), ('rating', float)]
U_1to1000 = np.array(U_1to1000, dtype=dtype)      
U_1to1000 = np.sort(U_1to1000, order=['rating', 'movieID'])

for i in range(top_movie_num):
    print("%d\t%f" %(U_1to1000[i][0], -1.0 * U_1to1000[i][1])) 

### Get top similar movies ###

cos_sim = np.zeros((movie_rng, size[1]))
top_sim_movie = np.zeros((movie_rng, num_sim))

den = []
for i in range(size[1]):
    tmp_arr = []
    for j in range(size[0]):
        if util_mtx[j, i] != -5: 
            tmp_arr.append(util_mtx[j, i])  
    den_tmp = np.linalg.norm(tmp_arr)
    den.append(den_tmp)

for k in range(movie_rng):
    for i in range(size[1]):
        dot = 0.0 
        for j in range(size[0]):
            if util_mtx[j, k] != -5 and util_mtx[j, i] != -5: 
                dot = dot + util_mtx[j, k] * util_mtx[j, i]

        cos_sim[k, i] = dot/(den[k] + 1e-15)/(den[i] + 1e-15)

for i in range(movie_rng):
    tmp_arr = np.argpartition(cos_sim[i], -1*(num_sim+1))[-1*(num_sim+1):]
    tmp_arr = np.setdiff1d(tmp_arr,[i])
    top_sim_movie[i] = tmp_arr
top_sim_movie = top_sim_movie.astype(int)
    
### Get top movies ###

U_1to1000 = np.zeros(movie_rng, dtype = tuple)
calc_U_arr = util_mtx[U_idx]
calc_U_arr = calc_U_arr + mean_arr[U_idx]

for i in range(movie_rng):
    tmp_arr = calc_U_arr[top_sim_movie[i]]
    s = 0.0
    d = 0.0
    for j in range(num_sim):
        if tmp_arr[j] > 0:
            s = s + tmp_arr[j]
            d = d + 1.0
    if d == 0:
        U_1to1000[i] = (i+1, 0)
    else:
        U_1to1000[i] = (i+1, -1*s/d)
        
dtype = [('movieID', int), ('rating', float)]
U_1to1000 = np.array(U_1to1000, dtype=dtype)      
U_1to1000 = np.sort(U_1to1000, order=['rating', 'movieID'])

for i in range(top_movie_num):
    print("%d\t%f" %(U_1to1000[i][0], -1 * U_1to1000[i][1])) 

         



