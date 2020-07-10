from PhiMap import PhiMap

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

class RelLinReg(object):
    """performs linear regression with
       relational features
    """

    def __init__(self,features,regularizer = "l2",excite = False):
        """initializes hyper parameters,
           regularizer can be "l1/l2/hybrid,
           excitation for inhomogenous process
        """

        self.features = features
        self.regularizer = regularizer
        self.excite = excite
        self.features = None

    def learn(self,features,facts,examples,bk,target):
        """generates relational features,
           trains the parameters of model
        """

        pass
        
           

        
