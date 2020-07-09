from PhiMap import PhiMap

class RelLinReg(object):
    """performs linear regression with
       relational features
    """

    def __init__(self,regularizer = "l2",excite = False):
        """initializes hyper parameters,
           regularizer can be "l1/l2/hybrid,
           excitation for inhomogenous process
        """

        self.regularizer = regularizer
        self.excite = excite

    def features(self,facts,examples,bk,target):
        """generates relational features
        """
        
        PhiMap.learn(facts,bk,target,examples = examples)
        PhiMap.remove_redundant(facts,list(examples.keys()),[])
        return PhiMap.clause_list
        

    def learn(self,facts,examples,bk,target):
        """generates relational features,
           trains the parameters of model
        """

        features = self.features(facts,examples,bk,target)
        
           

        
