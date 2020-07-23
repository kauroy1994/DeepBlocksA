from PhiMap import PhiMap
from sklearn.neural_network import MLPRegressor as DN

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

class NN():

    def __init__(self):
        """constructor
        """

        self.clf = DN()

    def train(self,X,Y):
        """train function
        """

        self.clf.fit(X,Y)

    def test(self,x):

        print (self.clf.predict(x))
        

#====== TESTCODE ==============
'''
clf = NN()
clf.train([[1],[2]],[2,4])
clf.test([[3]])
'''
