import numpy as np
import sys

def sigmoid(x):

    z = np.exp(-x)
    sig = 1.0 / (1.0 + z)


    return sig

class Fully_Connected_Layer:
    def __init__(self, learning_rate):
        self.InputDim = 784
        self.HiddenDim = 128
        self.OutputDim = 10
        self.learning_rate = learning_rate
        
        '''Weight Initialization'''
        self.W1 = np.random.randn(self.InputDim, self.HiddenDim)
        self.b1 = np.zeros(self.HiddenDim)
        self.W2 = np.random.randn(self.HiddenDim, self.OutputDim)
        self.b2 = np.zeros(self.OutputDim)
        
        self.Input2 = None # for using in backward process
        
    def Forward(self, Input):
        '''Implement forward propagation'''
        Output1 = np.matmul(Input, self.W1) + self.b1
        self.Input2 = sigmoid(Output1)
        Output2 = np.matmul(self.Input2, self.W2) + self.b2
        Output = sigmoid(Output2)
        
        return Output
    
    def Backward(self, Input, Label, Output):
        '''Implement backward propagation'''
        dOutput = (Output - Label)/float(Label.shape[0])*2.0
        dOutput2 = (1.0 - Output) * Output * dOutput
        dW2 = np.matmul(self.Input2.T, dOutput2)
        db2 = np.sum(dOutput2, axis = 0)
        dInput2 = np.matmul(dOutput2, self.W2.T)
        dOutput1 = (1.0 - self.Input2) * self.Input2 * dInput2
        dW1 = np.matmul(Input.T, dOutput1)
        db1 = np.sum(dOutput1, axis = 0)
        
        '''Update parameters using gradient descent'''
        self.W1 = self.W1 - self.learning_rate * dW1
        self.b1 = self.b1 - self.learning_rate * db1
        self.W2 = self.W2 - self.learning_rate * dW2
        self.b2 = self.b2 - self.learning_rate * db2
    
    def Train(self, Input, Label_onehot):
        Output = self.Forward(Input)
        self.Backward(Input, Label_onehot, Output)

    def GetAccuracy(self, Input, Label):
        Output_onehot = self.Forward(Input)
        Output = np.argmax(Output_onehot, axis = 1) # Get predict
        Correct = Label == Output # Compare predict and label

        accuracy = float(sum(Correct)) / float(len(Correct)) # Get accuracy
        
        return accuracy
        

'''Process data'''
'''Use train_data(N1 * 784), train_label_onehot(N1 * 10), train_label(N1)
   test_data(N2 * 784), test_label_onehot(N2 * 10), test_label(N2).
   N1 is the number of train data,
   N2 is the number of test data'''

# Get data
f1 = open(sys.argv[1],"r")
f2 = open(sys.argv[2],"r")

train_data = f1.readlines()
test_data = f2.readlines()

f1.close()
f2.close()

# Process train_data
for i in range(len(train_data)):
    train_data[i] = train_data[i].strip()
    train_data[i] = train_data[i].split(",")

# Process test data    
for i in range(len(test_data)):
    test_data[i] = test_data[i].strip()
    test_data[i] = test_data[i].split(",")
    
# Divide train_data to train_data and train_label   
train_data = np.array(train_data, dtype = np.float32)
train_label = (train_data[:,-1]).astype(np.int32)
train_data = train_data[:,:-1]

# Get train_label_onehot
train_label_onehot = np.zeros((train_label.shape[0],10))
for i in range(len(train_label)):
    j = train_label[i]
    train_label_onehot[i,j] = 1

# Divide test_data to test_data and test_label
test_data = np.array(test_data, dtype = np.float32)
test_label = ((test_data[:,-1])).astype(np.int32)
test_data = (test_data[:,:-1])

# Get test_label_onehot
test_label_onehot = np.zeros((test_label.shape[0],10))
for i in range(len(test_label)):
    j = test_label[i]
    test_label_onehot[i,j] = 1

'''Decide hyper parameter'''
np.random.seed(0) # for same result
iteration = 10000
learning_rate = 1.0

'''Construct a fully-connected network'''        
Network = Fully_Connected_Layer(learning_rate)

'''Train the network for the number of iterations'''
for i in range(iteration):
    Network.Train(train_data, train_label_onehot)

'''Implement function to measure the accuracy'''
acc_train = Network.GetAccuracy(train_data, train_label)
acc_test = Network.GetAccuracy(test_data, test_label)

'''Print'''
print(acc_train)
print(acc_test)
print(iteration)
print(learning_rate)
    
