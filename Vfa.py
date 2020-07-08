from Blocks import Simulator

class AVI(object):

    @staticmethod
    def approx_value(state):
        """returns approximate value
           of state from function approximator
        """

        return 5
    
    @staticmethod
    def run(iters = 2, goal_value = 5, discount = 1):
        """Approximate value iteration
        """

        #n = 0
        for i in range(iters):
            facts = []
            examples = {}
            target = 'v'
            episode = Simulator.backward_episode() #s_number = n)
            reverse_episode = episode[::-1]
            goal = reverse_episode[0][0]
            facts += goal.facts()
            if i == 0:
                examples['v(s'+str(goal.n)+')'] = goal_value
            else:
                examples['v(s'+str(goal.n)+')'] = AVI.approx_value(goal)
            n_items = len(reverse_episode)
            for j in range(n_items):
                if j == 0:
                    continue
                if i == 0:
                    v_next = examples['v(s'+str(reverse_episode[j-1][0].n)+')']
                    examples['v(s'+str(reverse_episode[j][0].n)+')'] = -1 + (discount * v_next)
                else:
                    v_next = AVI.approx_value(reverse_episode[j-1][0])
                    examples['v(s'+str(reverse_episode[j][0].n)+')'] = -1 + (discount * v_next)
                
            #n = len(examples) + len(episode) - 1
            print (examples)
            #print (n)

AVI.run()
        
        
        

    
