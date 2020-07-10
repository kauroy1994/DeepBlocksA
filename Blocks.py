from copy import deepcopy
from random import choice

class Blocks(object):

    def __init__(self,start,goal,n = 0):
        """start: list of block stacks
           goal: desired list of block stacks
        """

        self.start = deepcopy(start)
        self.state = start
        self.n = n
        self.goal = deepcopy(goal)

    def facts(self):
        """returns predicate rep
           of block stacks
        """

        facts = []

        if not self.state:
            return facts

        for stack in self.state:
            n_blocks = len(stack)
            if not n_blocks:
                continue
            facts.append("clear(s"+str(self.n)+","+str(stack[0])+")")
            for i in range(n_blocks-1):
                facts.append("on(s"+str(self.n)+","+str(stack[i])+","+str(stack[i+1])+")")
            facts.append("table(s"+str(self.n)+","+str(stack[n_blocks-1])+")")

        return facts

    def vector_rep(self):
        """returns vector representation
           for traditional machine learning
           block can be on table
           block can also be clear
           block can be on other blocks
           so dim(vector) = n_blocks + 2
        """

        vector = {}
        blocks = {}
        block_c = 2

        for stack in self.state:
            for block in stack:
                if block not in blocks:
                    blocks[block] = block_c
                    block_c += 1

        for block in blocks:
            block_vector = [0 for i in range(len(blocks) + 2)]
            for stack in self.state:
                if block == stack[0]: #clear
                    block_vector[1] = 1
                if block == stack[len(stack) - 1]: #table
                    block_vector[0] = 1
                elif block in stack: #on other blocks
                    on_block = stack[stack.index(block) + 1]
                    block_vector[blocks[on_block]] = 1
            vector[block] = block_vector

        return vector
            

    def __repr__(self):
        """call to print returns this
        """

        out = "state number: "+str(self.n)+"\n" 

        if not self.state:
            return out + "empty state\n"

        out += "state facts:\n"

        for stack in self.state:
            n_blocks = len(stack)
            if not n_blocks:
                continue
            out += "clear("+str(stack[0])+")"+"\n"
            for i in range(n_blocks-1):
                out += "on("+str(stack[i])+","+str(stack[i+1])+")"+"\n"
            out += "table("+str(stack[n_blocks-1])+")"+"\n"

        return out

    def random(self):
        """returns random valid action
        """

        random_action = [choice([0,1,2])] #stack/putdown/no-op
        
        if random_action[0] == 1: #stack
            stacks = range(len(self.state))
            random_action += [choice(stacks)] #from
            random_action += [choice(stacks)] #to
        
        elif random_action[0] == 0: #putdown
            stacks = range(len(self.state))
            random_action += [choice(stacks)] #from


        return random_action

    def action_pred(self,action):
        """returns predicate form of action
        """

        if action[0] == 1:
            block_i = self.state[action[1]][0]
            block_j = self.state[action[2]][0]
            return "stack(s"+str(self.n)+","+block_i+","+block_j+")"

        elif action[0] == 0:
            block = self.state[action[1]][0]
            return "unstack(s"+str(self.n)+","+block+")"

        elif action[0] == 2:
            return "noop(s"+str(self.n)+")"
            
            
    def act(self,action):
        """[1,i,j]: stacks block from i to j
           [0,i]: puts down block from i on table
        """

        next_state = deepcopy(self)
        next_state.n = self.n + 1
        
        if action[0] == 1:

            if action[1] > len(next_state.state)-1:
                #invalid action
                return False

            i_stack = next_state.state[action[1]]

            if action[2] > len(next_state.state)-1:
                #invalid action
                return False
            
            j_stack = next_state.state[action[2]]

            
            if not i_stack:
                #invalid action
                return False

            if i_stack == j_stack:
                #invalid action
                return False
            
            top = i_stack[0]
            next_state.state[action[1]] = i_stack[1:]
            next_state.state[action[2]] = [top] + j_stack
            next_state.state = [item for item in next_state.state if item]

        elif action[0] == 0:

            if action[1] > len(next_state.state)-1:
                #invalid action
                return False

            i_stack = next_state.state[action[1]]

            if (not i_stack) or (len(i_stack) == 1):
                #invalid action
                return False

            top = i_stack[0]
            next_state.state[action[1]] = i_stack[1:]
            next_state.state.append([top])

        return next_state


class Simulator(object):
    """to simulate the world
    """

    bk = ['on(+state,+block,-block)',
          'on(+state,-block,+block)',
          'clear(+state,+block)',
          'table(+state,+block)',
          'stack(+state,+block,+block)',
          'unstack(+state,+block)',
          'noop(+state)']

    @staticmethod
    def policy(s_prev,s):
        """finds policy that leads
           from s_prev -> s
        """

        while True:
            action = s_prev.random()
            if not s_prev.act(action):
                continue
            else:
                s_next = s_prev.act(action)
                if str(s_next).split(':')[2] != str(s).split(':')[2]:
                    continue
                else:
                    return action

    @staticmethod
    def backward_episode(times = 5,goal = [['a','b','c']],s_number = 0):
        """generates trajectories by
           random permutations from
           goal state
        """
        
        s = Blocks(goal,[],n = s_number)
        episode = [[s]]
        for i in range(times):
            while True:
                action = s.random()
                if not s.act(action):
                    continue
                else:
                    s_prev = deepcopy(s)
                    s = s.act(action)
                    forward_action = Simulator.policy(s,s_prev)
                    forward_action_pred = s.action_pred(forward_action)
                    episode = [[deepcopy(s),deepcopy(forward_action_pred)]] + episode
                    break
        return (episode)
            
        

#============= TESTING CODE ====================

'''
episode = Simulator.backward_episode()
for item in episode[:-1]:
    print (item[0],item[1])
print (episode[-1][0])
'''






