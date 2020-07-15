from copy import deepcopy
from random import choice,random
from time import time

class Contagion(object):

    def __init__(self,init_perc = 0.1,test_r = 0.1,pop = 10,n = 0):
        """initial perc: initial percentage of
           population affected
           pop: Total population of people
           test_r = capacity to test people

           people are tested, hospitalized or isolated
           else they go to work and infect others
           TODO: Don't go to work when on lockdown
           TODO: Create state econ reward, on shop and work output
        """

        self.test_r = test_r

        self.n = n

        #pop number of persons
        self.persons = ['p'+str(i) for i in range(pop)]

        #init_perc % of persons initially ill
        self.ill = [int(random() < init_perc) for i in range(pop)]

        #record self isolation of persons in case of no beds
        self.isolated = [0 for i in range(pop)]

        #record hospitalized persons
        self.hospitalized = [0 for i in range(pop)]

        #record where people shop
        self.shops = ['shop1' for i in range(int(pop/2))]
        self.shops += ['shop2' for i in range(int(pop/2),pop)]

        #record where people work, everybody works
        self.works = ['work1' for i in range(int(pop/2))]
        self.works += ['work2' for i in range(int(pop/2),pop)]

        #two tracks to work that persons take
        #each track has a residential complex with houses containing half the population
        #each track has a shop that makes 1$ per person that travels
        #each person working contributes $1 to GDP
        self.tracks = {'t1': {'res1': ['h'+str(i) for i in range(int(pop/2))],
                              'shop1': 1,
                              'work1': 1},
                       't2': {'res2': ['h'+str(i) for i in range(int(pop/2),pop)],
                              'shop2': 1,
                              'work2': 1}}

        self.locked = {}
        
        #each person assigned randomly to 1 of 10 houses,
        #that they live in
        self.houses = [choice(range(0,pop)) for i in range(pop)]

        #record if hospitalized or in isolation or immune
        self.out = [0 for i in range(pop)]
        
        #one hospitals with max capacity 3
        self.hospitals = {'hos0' : [False for i in range(3)]}

        locs = list(self.tracks.keys())
        for track in self.tracks:
            locs += list(self.tracks[track].keys())
            for est in self.tracks[track]:
                if "res" in est:
                    locs += self.tracks[track][est]

        #set locked to 0 for all locations
        for loc in locs:
            self.locked[loc] = 0
        
        self.hospitalize_and_transmit(self.test_r)
        self.create_KG(dot = False)


    def hospitalize_and_transmit(self,testing_rate):
        """some persons who are sick are identified.
           those identified are hospitalized,
           others infect those they contact
        """

        n_persons = len(self.persons)

        #hospitalize ill persons or isolate
        for i in range(n_persons):
            if random() < testing_rate:
                if self.ill[i]:
                    no_beds = True
                    for hospital in self.hospitals:
                        if False in self.hospitals[hospital]:
                            no_beds = False
                            bed = self.hospitals[hospital].index(False)
                            self.hospitals[hospital][bed] = i
                            self.hospitalized[i] = 1
                            self.out[i] = 1
                            break
                    if no_beds:
                        self.isolated[i] = 1
                        self.out[i] = 1
                        
        #those missed in testing will spread contagion in their house
        for i in range(n_persons):
            if self.ill[i]:
                house = self.houses[i]
                track = 't1'
                if i in range(int(n_persons/2),int(n_persons)):
                    track = 't2'
                if self.out[i] or self.locked['h'+str(house)] or self.locked[track]:
                    continue
                else:
                    for j in range(n_persons):
                        if i == j:
                            continue
                        else:
                            house_j = self.houses[j]
                            track_j = 't1'
                            if j in range(int(n_persons/2),int(n_persons)):
                                track_j = 't2'
                            if self.out[j] or self.ill[j] or self.locked['h'+str(house_j)] or self.locked[track_j]:
                                continue
                            if house == house_j:
                                self.ill[j] = 1

        #those missed in testing will spread contagion at shopping
        for i in range(n_persons):
            if self.ill[i]:
                shop = self.shops[i]
                track = 't1'
                if i in range(int(n_persons/2),int(n_persons)):
                    track = 't2'
                if self.out[i] or self.locked[shop] or self.locked[track]:
                    continue
                else:
                    for j in range(n_persons):
                        if i == j:
                            continue
                        else:
                            shop_j = self.shops[j]
                            track_j = 't1'
                            if j in range(int(n_persons/2),int(n_persons)):
                                track_j = 't2'
                            if self.out[j] or self.ill[j] or self.locked[shop_j] or self.locked[track_j]:
                                continue
                            if shop == shop_j:
                                self.ill[j] = 1
                                
        #those missed in testing will spread contagion at work
        for i in range(n_persons):
            if self.ill[i]:
                work = self.works[i]
                track = 't1'
                if i in range(int(n_persons/2),int(n_persons)):
                    track = 't2'
                if self.out[i] or self.locked[work] or self.locked[track]:
                    continue
                else:
                    for j in range(n_persons):
                        if i == j:
                            continue
                        else:
                            work_j = self.works[j]
                            track_j = 't1'
                            if j in range(int(n_persons/2),int(n_persons)):
                                track_j = 't2'
                            if self.out[j] or self.ill[j] or self.locked[work_j] or self.locked[track_j]:
                                continue
                            if work == work_j:
                                self.ill[j] = 1

        #release a third of patients from hospital
        for hospital in self.hospitals:
            n_hospitalized = len(self.hospitals[hospital])
            for i in range(n_hospitalized):
                person = self.hospitals[hospital][i]
                if not person:
                    continue
                else:
                    if random() < 0.3:
                        self.hospitals[hospital][i] = False
                        self.hospitalized[person] = 0
                        #self.out still 1 as person recovered,
                        #and assumed immune
                        

    def create_KG(self,dot = False):
        """creates Knowledge Graph
        """

        self.KG = []
        
        #establishments on same track (use combinations later)
        facts = ["same_track(res1,shop1)",
                 "same_track(shop1,work1)",
                 "same_track(res1,work1)",
                 "same_track(res2,shop2)",
                 "same_track(shop2,work2)",
                 "same_track(res2,work2)"]

        n_persons = len(self.persons)
        
        for i in range(n_persons):

            #person in house
            facts.append("stays_in(per"+str(i+1)+",house"+str(self.houses[i]+1)+")")

            #person is ill
            '''never observe who is ill
            if self.ill[i]:
                facts.append("ill(s"+str(self.n)+",p"+str(i)+")")
            '''
        for track in self.tracks:
            if not self.locked[track]:

                #track is open
                facts.append("open(track"+track.split('t')[1]+")")
            for est in self.tracks[track]:
                if 'res' in est:
                    if not self.locked[est]:

                        #establishment (residence) is open
                        facts.append("open("+est+")")

                    #establishment (residence) on particular track
                    facts.append("on("+est+",track"+track.split('t')[1]+")")
                    for house in self.tracks[track][est]:
                        if not self.locked[house]:

                            #house is open
                            facts.append("open(house"+str(int(house.split('h')[1])+1)+")")

                        #house is in this establishment (residence)
                        facts.append("part_of(house"+str(int(house.split('h')[1])+1)+","+est+")")
                elif 'shop' in est:
                    if not self.locked[est]:

                        #establishment (shop) is open
                        facts.append("open("+est+")")

                    #establishment (shop) on particular track
                    facts.append("on("+est+",track"+track.split('t')[1]+")")
                elif 'work' in est:
                    if not self.locked[est]:

                        #establishment (work) is open
                        facts.append("open("+est+")")

                    #establishment (work) on particular track
                    facts.append("on("+est+",track"+track.split('t')[1]+")")


        for i in range(n_persons):
            if self.hospitalized[i]:
                facts.append("hospitalized(per"+str(i+1)+")")

        for i in range(n_persons):
            if self.isolated[i]:
                facts.append("quarantined(per"+str(i+1)+")")

        self.KG = facts

        #write to dot file if illustration required
        if dot:

            with open('KG'+str(self.n)+'.dot','a') as fp:
                fp.write("digraph G {" + "\n")
                fp.write("rankdir = LR"+"\n")

            lines_to_add = []
            for fact in self.KG:
                if len(fact.split('(')[1].split(',')) != 2:
                    attr = fact.split('(')[0]
                    if attr not in lines_to_add:
                        lines_to_add.append(attr)
                    obj = fact.split('(')[1][:-1]
                    if obj+"[shape=box]" not in lines_to_add:
                        lines_to_add.append(obj+"[shape=box]")
                    lines_to_add.append(obj+"->"+attr)
                    continue
                rel = fact.split('(')[0]
                obj = fact.split('(')[1].split(',')[0]
                subj = fact.split('(')[1].split(',')[1][:-1]
                if obj+"[shape=box]" not in lines_to_add:
                    lines_to_add.append(obj+"[shape=box]")
                if subj+"[shape=box]" not in lines_to_add:
                    lines_to_add.append(obj+"[shape=box]")
            
                lines_to_add.append(obj+"->"+subj+"[label="+rel+"]")

            with open('KG'+str(self.n)+'.dot','a') as fp:
                for line in lines_to_add:
                    fp.write(line+"\n")
                fp.write("}")
                            
    def __repr__(self):
        """call to print or str
           returns this
        """

        out = "State number: "+str(self.n)+"\n"

        for fact in self.KG:
            out += fact + "\n"

        return out
           
    def facts(self):
        """returns predicate rep
           of state of the virtual city
           persons ill
           persons in house
           houses in particular residence are open
           if tracks are open
           if establishments (res, shops or work) on tracks, are open
           load at hospitals
        """

        #establishments on same track (use combinations later)
        facts = ["same(s"+str(self.n)+",res1,shop1)",
                 "same(s"+str(self.n)+",shop1,work1)",
                 "same(s"+str(self.n)+",res1,work1)",
                 "same(s"+str(self.n)+",res2,shop2)",
                 "same(s"+str(self.n)+",shop2,work2)",
                 "same(s"+str(self.n)+",res2,work2)"]

        n_persons = len(self.persons)
        
        for i in range(n_persons):

            #person in house
            facts.append("pin(s"+str(self.n)+",p"+str(i)+",h"+str(self.houses[i])+")")

            #person is ill
            '''never observe who is ill
            if self.ill[i]:
                facts.append("ill(s"+str(self.n)+",p"+str(i)+")")
            '''
        for track in self.tracks:
            if not self.locked[track]:

                #track is open
                facts.append("topen(s"+str(self.n)+","+track+")")
            for est in self.tracks[track]:
                if 'res' in est:
                    if not self.locked[est]:

                        #establishment (residence) is open
                        facts.append("ropen(s"+str(self.n)+","+est+")")

                    #establishment (residence) on particular track
                    facts.append("ron(s"+str(self.n)+","+est+","+track+")")
                    for house in self.tracks[track][est]:
                        if not self.locked[house]:

                            #house is open
                            facts.append("hopen(s"+str(self.n)+","+house+")")

                        #house is in this establishment (residence)
                        facts.append("hin(s"+str(self.n)+","+house+","+est+")")
                elif 'shop' in est:
                    if not self.locked[est]:

                        #establishment (shop) is open
                        facts.append("sopen(s"+str(self.n)+","+est+")")

                    #establishment (shop) on particular track
                    facts.append("son(s"+str(self.n)+","+est+","+track+")")
                elif 'work' in est:
                    if not self.locked[est]:

                        #establishment (work) is open
                        facts.append("wopen(s"+str(self.n)+","+est+")")

                    #establishment (work) on particular track
                    facts.append("won(s"+str(self.n)+","+est+","+track+")")

        for i in range(n_persons):
            if self.hospitalized[i]:
                
                #person is hospitalized
                facts.append("ph(s"+str(self.n)+",p"+str(i)+")")

        for i in range(n_persons):
            if self.isolated[i]:

                #person is quarantined
                facts.append("q(s"+str(self.n)+",p"+str(i)+")")

        return facts

    def random(self):
        """returns random valid action
           action can be lockdown shops,
           work, residences, houses,
           entire track or incr tests
           lock : [0,<loc>]
           unlock: [1, <loc>]
           incr test: [2]
           noop: [3]
        """

        action = [choice([0,1,2,3])]
        
        locs = list(self.tracks.keys())
        for track in self.tracks:
            locs += list(self.tracks[track].keys())
            for est in self.tracks[track]:
                if "res" in est:
                    locs += self.tracks[track][est]
                    
        if action[0] == 0:
            return (action + [choice(locs)])

        elif action[0] == 1:
            return (action + [choice(locs)])

        elif action[0] == 2 or action[0] == 3:
            return action

    def action_pred(self,action):
        """returns predicate form of action
        """

        if action[0] == 0:
            return "lockdown(s"+str(self.n)+","+action[1]+")"

        elif action[0] == 1:
            return "unlock(s"+str(self.n)+","+action[1]+")"

        elif action[0] == 2:
            return "incr_test(s"+str(self.n)+")"

        elif action[0] == 3:
            return "noop(s"+str(self.n)+")"

    def act(self,action):
        """[0,<loc>]: locksdown location
           [1,<loc>]: unlocks location
           [2]: increases test rate by 10%
           [3]: Noop
        """

        next_state = deepcopy(self)
        next_state.n = self.n + 1

        if action[0] == 0:

            if next_state.locked[action[1]]:
                #invalid action
                return False

            loc = action[1]
            next_state.locked[loc] = 1

        elif action[0] == 1:

            if not next_state.locked[action[1]]:
                #invalid action
                return False

            loc = action[1]
            next_state.locked[loc] = 0

        elif action[0] == 2:
            if next_state.test_r >= 0.9:
                #invalid action
                return False

            next_state.test_r += 0.1

        next_state.hospitalize_and_transmit(self.test_r)
        next_state.create_KG(dot = True)
        
        return next_state

#===============TEST FUNCTION============
'''
s0 = Contagion()
action = s0.random()
print (action)
print (s0.action_pred(action))
s1 = s0.act(action)
'''
