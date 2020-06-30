from copy import deepcopy

class Simulator(object):

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

    def act(self,action):
        """[1,i,j]: stacks block from i to j
           [0,i]: puts down block from i on table
        """

        next_state = deepcopy(self)
        next_state.n = self.n + 1
        
        if action[0] == 1:

            i_stack = next_state.state[action[1]]
            j_stack = next_state.state[action[2]]
            
            if not i_stack:
                #invalid action
                return False
            
            top = i_stack[0]
            next_state.state[action[1]] = i_stack[1:]
            next_state.state[action[2]] = [top] + j_stack

        elif action[0] == 0:

            i_stack = next_state.state[action[1]]

            if (not i_stack) or (len(i_stack) == 1):
                #invalid action
                return False

            top = i_stack[0]
            next_state.state[action[1]] = i_stack[1:]
            next_state.state.append([top])

        return next_state

#============= TESTING CODE ====================
'''

s0 = Simulator([['a','b'],['c','d','e']],[['a','b','c','d','e']])
s1 = s0.act([0,1])
s2 = s1.act([1,0,1])
print (s0)
print ('-'*40)
print (s1)
print ('-'*40)
print (s2)

'''               