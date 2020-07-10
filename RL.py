from Blocks import Simulator
from ML import RelLinReg

class MCTS(object):

    @staticmethod
    def run(iters = 2,discount = 0.99):
        """Monte Carlo Tree Search
        """

        bk = Simulator.bk
        targets = list(bk.keys())
        models = {}
        for target in targets:
            print ("target:",target)
            model = RelLinReg()
            n = 0
            for i in range(iters):
                facts = []
                examples = {}
                episode = False
                while True:
                    if not episode:
                        episode = Simulator.backward_episode(s_number = n)
                    else:
                        break
                n_items = len(episode)
                for j in range(n_items):
                    facts += episode[j][0].facts()
                    sum_reward = 0
                    counter = 1
                    for k in range(j+1,n_items):
                        sum_reward += (discount**counter)*1 #or -1
                        counter += 1
                    if episode[j][1].split('(')[0] == target:
                        examples[episode[j][1]] = sum_reward
            n = 2*len(examples) - 1
            model.learn(facts,examples,bk[target],target)
            models[target] = model

MCTS.run()
        
        
        

    
