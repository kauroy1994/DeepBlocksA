from PhiMap import PhiMap
from Math import Matrix
from random import random

class RepLearn(object):
    """learns relational
       representations from data
    """

    @staticmethod
    def generate_features(facts,examples,bk,target):
        """generates relational features
        """

        PhiMap.learn(facts,bk,target,examples = examples)
        PhiMap.remove_redundant(facts,list(examples.keys()),[])
        return PhiMap.clause_list

class DN(object):
    """implements ANN for regression
    """

    def __init__(self,features = [],layers = [100],reg = False,act = 'sigmoid'):
        """initialize hyper parameters,
           regularizer: l1/l2
        """

        self.features = features
        self.layers = layers
        self.network = []
        self.delta = []
        self.Ws = []
        self.act = act
        self.reg = reg

    def feed_forward(self,x_i):
        """network forward pass
        """

        n_params = len(self.params)

        for i in range(n_params-1):
            self.network.append([[0] for n in range(self.params[i])])
        self.network.append([[0] for i in range(self.params[-1])])
        
        self.network[0] = Matrix([[x] for x in x_i])

        #compute node values
        for i in range(1,n_params):
            self.network[i] = self.Ws[i-1].T()*self.network[i-1]
            if i != n_params-1:
                if self.act == 'sigmoid':
                    self.network[i] = self.network[i].sigmoid()
                elif self.act == 'relu':
                    self.network[i] = self.network[i].relu()
            else:
                self.network[i] = self.network[i]

    def compute_deltas(self,y_i,error_grad):
        """computes deltas for backprop
        """

        n_params = len(self.params)
        
        for i in range(n_params-1):
            self.delta.append([[0] for n in range(self.params[i])])
        self.delta.append([[0] for i in range(self.params[-1])])

        #compute deltas
        backward_range = range(1,n_params-1)[::-1]
        self.delta[n_params-1] = (self.network[n_params-1].grad(a='lin') * error_grad)        
        for i in backward_range:
            self.delta[i] = (self.network[i].grad(a=self.act)) @ (self.Ws[i] * self.delta[i+1])


    def back_prop(self,y_i,e_grad,r=0.01):
        """propagates chain rule grads
           through network structure
           o/p layer to i/p
        """

        n_params = len(self.params)
        self.compute_deltas(y_i,e_grad)

        #compute gradients        
        for i in range(1,n_params):
            n,m = self.Ws[i-1].dim()[0],self.Ws[i-1].dim()[1]
            lr = Matrix([[r for j in range(m)] for i in range(n)])
            rm = Matrix([[1 for j in range(m)] for i in range(n)])
            if self.reg == 'l2':
                rm = Matrix([[2 for j in range(m)] for i in range(n)]) @ self.Ws[i-1]
            grad = self.network[i-1] * self.delta[i].T()
            if self.reg:
                grad += rm
            self.Ws[i-1] -= lr @ grad

    def learn(facts,examples,bk,target):
        """to be completed ..
        """
        
        pass

    def fit(self,X,Y,iters=100,lr = 0.01):
        """leanrs DN with optimization
           from data
        """

        N = len(X)
        
        self.params = [len(X[0])+1] + self.layers + [1] #one label, add ones for bias
        params = self.params
        n_params = len(params)
        
        for i in range(n_params-1):
            self.Ws.append(Matrix([[1.0 for k in range(params[i+1])] for j in range(params[i])]))
            
        for it in range(iters):
            e_grad = Matrix([[0.0]]) 
            for i in range(N):
                x_i = X[i]+[1] #bias
                y_i = Y[i]
                self.feed_forward(x_i)
                #e_grad = (self.network[n_params-1] - Matrix([y_i])), for SGD
                #self.back_prop(y_i,e_grad,r=lr)
                e_grad += (self.network[n_params-1] - Matrix([y_i]))
            e_grad.array[0][0] /= N
            self.back_prop(y_i,e_grad,r=lr)

    def predict(self,X):
        """predicts on points in X
        """

        N = len(X)
        predictions = []
        for i in range(N):
            x_i = X[i] + [1] #bias
            self.feed_forward(x_i)
            predictions.append(self.network[len(self.params)-1])

        return predictions

#====== TESTCODE ==============
'''
clf = DN(layers=[])#,reg='l1')
X,Y = [[1],[3]],[[2],[5]]
clf.fit(X,Y,iters=100,lr = 0.01)
predictions = clf.predict(X)
print ([float(m.array[0][0]) for m in predictions])
'''
