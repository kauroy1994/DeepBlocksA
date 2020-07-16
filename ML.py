from PhiMap import PhiMap
from Math import Matrix

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
       and classification
    """

    def __init__(self,features = [],layers = [100],regularizer = "l2"):
        """initialize hyper parameters,
           regularizer: l1/l2
        """

        self.features = features
        self.layers = layers
        self.Ws = []

    def learn(facts,examples,bk,target):

        pass

    def fit(self):
        """leanrs DN with optimization
           from data
        """

        X,Y = [[1,2],[1,3]],[[5,7]]
        params = [len(X)] + self.layers + [len(Y)]
        n_params = len(params)
        for i in range(n_params-1):
            self.Ws.append(Matrix([[0 for k in range(params[i+1])] for j in range(params[i])]))


#====== TESTCODE =============
'''
clf = DN()
clf.fit()
for W in clf.Ws:
    print (W.dim())
'''
           

        
