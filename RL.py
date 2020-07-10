from Blocks import Simulator
from ML import RelLinReg

class MCTS(object):

    @staticmethod
    def run():
        """Monte Carlo Tree Search
        """

        bk = Simulator.bk
        model = RelLinReg()
        episode = Simulator.backward_episode()
        print (episode)

class AVI(object):

    @staticmethod
    def approx_value(model,state):
        """returns approximate value
           of state from function approximator
        """

        return 5
    
    @staticmethod
    def run(iters = 2, goal_value = 5, discount = 1):
        """Approximate value iteration
        """

        bk = Simulator.bk
        model = RelLinReg()
        #n = 0
        for i in range(iters):
            facts = []
            examples = {}
            target = 'v'
            episode = Simulator.backward_episode()
            reverse_episode = episode[::-1]
            goal = reverse_episode[0][0]
            facts += goal.facts()
            if i == 0:
                examples['v(s'+str(goal.n)+')'] = goal_value
            else:
                examples['v(s'+str(goal.n)+')'] = AVI.approx_value(model,goal)
            n_items = len(reverse_episode)
            for j in range(n_items):
                if j == 0:
                    continue
                facts += reverse_episode[j][0].facts()
                if i == 0:
                    v_next = examples['v(s'+str(reverse_episode[j-1][0].n)+')']
                    examples['v(s'+str(reverse_episode[j][0].n)+')'] = -1 + (discount * v_next)
                else:
                    v_next = AVI.approx_value(model,reverse_episode[j-1][0])
                    examples['v(s'+str(reverse_episode[j][0].n)+')'] = -1 + (discount * v_next)
                
            model.learn(facts,examples,bk,'v')

MCTS.run()
        
        
        

    
