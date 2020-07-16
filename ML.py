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

    def __init__(self,features = [],layers = [100],regularizer = "l2"):
        """initialize hyper parameters,
           regularizer: l1/l2
        """

        self.features = features
        self.layers = layers
        self.network = []
        self.delta = []
        self.Ws = []

    def feed_forward(self,x_i,y_i):
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
            self.network[i] = self.network[i].sigmoid()

        for i in range(n_params-1):
            self.delta.append([[0] for n in range(self.params[i])])
        self.delta.append([[0] for i in range(self.params[-1])])

        #compute deltas
        backward_range = range(n_params-1)[::-1]
        error = (self.network[n_params-1] - Matrix([y_i]))**2
        self.delta[n_params-1] = (self.network[n_params-1].grad()*error)
        
        for i in backward_range:
            self.delta[i] = (self.network[i].grad()) @ (self.Ws[i] * self.delta[i+1])

        
    def learn(facts,examples,bk,target):
        """to be completed ..
        """
        
        pass

    def fit(self,X,Y):
        """leanrs DN with optimization
           from data
        """

        N = len(X)
        
        self.params = [len(X[0])+1] + self.layers + [1] #one label, add ones for bias
        params = self.params
        n_params = len(params)
        
        for i in range(n_params-1):
            self.Ws.append(Matrix([[random() for k in range(params[i+1])] for j in range(params[i])]))

        for i in range(N):
            x_i = X[i]+[1] #bias
            y_i = Y[i]
            self.feed_forward(x_i,y_i)

#====== TESTCODE =============
'''
clf = DN()
X,Y = [[1,2],[1,3]],[[5],[7]]
clf.fit(X,Y)
'''

        
