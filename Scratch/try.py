from Math import Matrix
from random import random
from copy import deepcopy

class neuron(object):
    """implements ANN node
    """

    def __init__(self,params,layer = 0,act = False):
        """constructor
        """

        self.params = params
        self.layer = layer
        self.act = act
        self.out = 0.0 #inactive default
        self.delta = 0.0 #inactive gradient
        self.bias_delta = 0.0 #inactive gradient

    def __repr__(self):
        """call to print or type cast
           outputs this
        """

        return str(self.out)

class DN(object):
    """implements ANN for regression
    """

    def __init__(self,specs = []):
        """initializes DN params
           based on specification file
        """
            
        self.layers = [] #ANN layers
        self.specs = specs
        specs = self.specs

        n = len(specs)
        for i in range(n):
            m = specs[i][0]
            act = specs[i][1]
            self.layers.append([])
            for j in range(m):
                params = False
                if i != 0:
                    pn = specs[i-1][0]
                    params = Matrix([[0.0 for l in range(1)] for k in range(pn+1)])
                self.layers[i].append(neuron(params,layer = i,act = act))
                
    def __getitem__(self,layer):
        """gets layer neurons
        """

        return [item.out for item in self.layers[layer]]

    def __setitem__(self,layer,inputs):
        """set value from matrix
        """

        n = len(self.layers[layer])
        for i in range(n):
            self.layers[layer][i].out = inputs[i]

    def feed_forward(self,x_i):
        """performs forward pass
           through ANN with x_i
           input and params
        """

        n = len(self.specs)
        for i in range(n):
            if i == 0:
                self[i] = x_i
            else:
                ips = self[i-1] + [1] #bias
                for neu in self.layers[i]: #can parallelize
                    i_m = Matrix([[ip] for ip in ips])
                    out = neu.params.T()*i_m
                    neu.out = out.array[0][0]

    def back_prop(self,y_i,e_grad,r=0.01):
        """chain rule backpropogation step
           from output backward to input
        """

        n = len(self.specs)
        rev = range(1,n)[::-1]
        for i in rev: #compute deltas
            for neu in self.layers[i]: #can parallelize
                if i == n-1:
                    o_m = Matrix([[neu.out]])
                    delta = o_m.grad(a=neu.act) * e_grad
                    neu.delta = delta.array[0][0]
                    bias_delta = Matrix([[1]]).grad(a=neu.act) * e_grad
                    neu.bias_delta = bias_delta.array[0][0]
                else:
                    o_m = Matrix([[neu.out]])
                    neu_index = self.layers[i].index(neu)
                    delta = Matrix([[0.0]])
                    bias_delta = Matrix([[0.0]])
                    bias_w_index = len(self.layers[i+1])-1 
                    for neu2 in self.layers[i+1]: #can parallelize
                        w = Matrix([neu2.params.array[neu_index]])
                        bias_w = Matrix([neu2.params.array[bias_w_index]])
                        neu2_delta = Matrix([[neu2.delta]])
                        delta += w * neu2_delta
                        bias_delta += bias_w * neu2_delta
                    delta = o_m.grad(a=neu.act)*delta
                    bias_delta = Matrix([[1]]).grad(a=neu.act)*bias_delta
                    neu.delta = delta.array[0][0]
                    neu.bias_delta = bias_delta.array[0][0]

        for i in range(1,n): #compute gradients
            ips = self[i-1] + [1] #bias
            for neu in self.layers[i]:
                m = neu.params.dim()[0]
                for j in range(m-1):
                    param = neu.params.array[j][0]
                    grad = ips[j] * neu.delta
                    param -= r * grad
                bias_grad = 1 * neu.delta
                neu.params.array[m-1][0] -= r * bias_grad

    def train(self,X,Y,iters=200):
        """trains DN using GD
           iters: max iters to train
        """

        N = len(X)
        n = len(self.layers)

        for it in range(iters):
            e_grad = Matrix([[0.0]])
            state = deepcopy(self)
            for i in range(N):
                x_i = X[i]
                y_i = Y[i]
                self.feed_forward(x_i)
                e_grad += Matrix([self[n-1]]) - Matrix([y_i])
            e_grad.array[0][0] /= N
            self.back_prop(y_i,e_grad,r=0.01)

#======== TESTCODE ===============
DN_layers = [(1,False),
            (1,'lin')]
clf = DN(specs = DN_layers) #construct network first
X,Y = [],[]
for i in range(100):
    x1 = random()
    x2 = random()
    X.append([x1,x2])
    Y.append([x1+x2])
clf.train(X,Y)
x = random()
y = random()
print (x,y)
clf.feed_forward([x,y])
print (clf[len(clf.layers)-1])
print (clf.layers[1][0].params)
