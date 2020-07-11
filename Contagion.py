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

        self.n = n

        #pop number of persons
        self.persons = ['p'+str(i) for i in range(pop)]

        #init_perc % of persons initially ill
        self.ill = [int(random() < init_perc) for i in range(pop)]

        #record self isolation of persons in case of no beds
        self.isolated = [0 for i in range(pop)]

        #record hospitalized persons
        self.hospitalized = [0 for i in range(pop)]

        #record immune persons
        self.immune = [0 for i in range(pop)]

        #two tracks to work that persons take
        #each track has a residential complex with 5 houses
        #each track has a shop that makes 1$ per person that travels
        #each person working contributes $1 to GDP
        self.tracks = {'t1': {'res1': ['h'+str(i) for i in range(5)],
                              'shop1': 1,
                              'work1': 1},
                       't2': {'res2': ['h'+str(i) for i in range(5,10)],
                              'shop2': 1,
                              'work2': 1}}

        self.locked = {}
        
        #each person assigned randomly to 1 of 10 houses,
        #that they live in
        self.houses = [choice(range(0,10)) for i in range(pop)]

        #record if hospitalized or in isolation
        self.out = [0 for i in range(pop)]
        
        #one hospitals with max capacity 3
        self.hospitals = {'hos0' : [False for i in range(3)]}
        self.hospitalize_and_transmit(test_r)


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
                        
        #those missed in testing will spread contagion
        for i in range(n_persons):
            if self.ill[i]:
                house = self.houses[i]
                if self.out[i]:
                    continue
                else:
                    for j in range(n_persons):
                        if i == j:
                            continue
                        else:
                            house_j = self.houses[j]
                            if self.out[j] or self.ill[j]:
                                continue
                            if house == house_j:
                                self.ill[j] = 1
                    
           
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
            if self.ill[i]:
                facts.append("ill(s"+str(self.n)+",p"+str(i)+")")
        for track in self.tracks:
            if track not in self.locked:

                #track is open
                facts.append("topen(s"+str(self.n)+","+track+")")
            for est in track:
                if 'res' in est:
                    if est not in self.locked:

                        #establishment (residence) is open
                        facts.append("ropen(s"+str(self.n)+","+est+")")

                    #establishment (residence) on particular track
                    facts.append("ron(s"+str(self.n)+","+est+","+track+")")
                    for house in track[est]:
                        if house not in self.locked:

                            #house is open
                            facts.append("hopen(s"+str(self.n)+","+house+")")

                        #house is in this establishment (residence)
                        facts.append("hin(s"+str(self.n)+","+house+","+est+")")
                elif 'shop' in est:
                    if est not in self.locked:

                        #establishment (shop) is open
                        facts.append("sopen(s"+str(self.n)+","+est+")")

                    #establishment (shop) on particular track
                    facts.append("son(s"+str(self.n)+","+est+","+track+")")
                elif 'work' in est:
                    if est not in self.locked:

                        #establishment (work) is open
                        facts.append("wopen(s"+str(self.n)+","+est+")")

                    #establishment (work) on particular track
                    facts.append("won(s"+str(self.n)+","+est+","+track+")")

        for hospital in self.hospitals:
            for person in self.hospitals[hospital]:
                if not person:
                    continue
                else:

                    #person is hospitalized
                    facts.append("ph(s"+str(self.n)+",p"+str(person)+")")

        return facts


#===============TEST FUNCTION============
'''
city = Contagion()            
'''
        
