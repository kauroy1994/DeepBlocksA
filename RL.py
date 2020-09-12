from Blocks import Simulator
from ML import RepLearn,DN
from tqdm import tqdm

class MCS(object):

    @staticmethod
    def learn_representation(bk,iters = 2):
        """learns representation from
           episode data
        """

        targets = list(bk.keys())
        features = {}
        n_targets = len(targets)
        '''
        print ("Generating relational features ..")
        for i in tqdm(range(n_targets)):
            n = 0
            for j in range(iters):
                facts = []
                examples = {}
                episode = False
                while True:
                    if not episode:
                        episode = Simulator.backward_episode(s_number = n)
                    else:
                        break
                n_items = len(episode)
                for k in range(n_items):
                    facts += episode[k][0].facts()
                    if episode[k][1].split('(')[0] == targets[i]:
                        examples[episode[k][1]] = 0
            n = 2 * len(examples ) - 1
            features[targets[i]] = RepLearn.generate_features(facts,
                                                              examples,
                                                              bk[targets[i]],
                                                              targets[i])
        '''

        #for now hard code the learned features to check rest of the algorithmic framework
        for i in tqdm(range(n_targets)):
            if targets[i] == 'lockshop':
                features[targets[i]] = ['lockshop(S,A):-same(S,R,A),pin(S,P,H),hin(S,H,R)',
                                        'lockshop(S,A):-same(S,A,W),pin(S,P,H),hin(S,H,R),same(S,R,W)'
                                        'lockshop(S,A):-sopen(S,A)',
                                        'lockshop(S,A):-ph(S,P)',
                                        'lockshop(S,A):-q(S,P)',
                                        'lockshop(S,A):-ropen(S,R)',
                                        'lockshop(S,A):-wopen(S,W)',
                                        'lockshop(S,A):-hopen(S,H)']
            elif targets[i] == 'lockwork':
                features[targets[i]] = ['lockwork(S,W):-same(S,R,W),pin(S,P,H),hin(S,H,R)',
                                        'lockwork(S,W):-same(S,A,W),pin(S,P,H),hin(S,H,R),same(S,R,A)',
                                        'lockwork(S,W):-wopen(S,W)',
                                        'lockwork(S,W):-ph(S,P)',
                                        'lockwork(S,W):-q(S,P)',
                                        'lockwork(S,W):-ropen(S,R)',
                                        'lockwork(S,W):-sopen(S,A)',
                                        'lockwork(S,W):-hopen(S,H)']
            elif targets[i] == 'lockhouse':
                features[targets[i]] = ['lockhouse(S,H):-same(S,R,A),pin(S,P,H),hin(S,H,R)',
                                        'lockhouse(S,H):-same(S,A,W),pin(S,P,H),hin(S,H,R),same(S,R,W)',
                                        'lockhouse(S,H):-sopen(S,A)',
                                        'lockhouse(S,H):-ph(S,P)',
                                        'lockhouse(S,H):-q(S,P)',
                                        'lockhouse(S,H):-ropen(S,R)',
                                        'lockhouse(S,H):-wopen(S,W)',
                                        'lockhouse(S,H):-hopen(S,H)']
            elif targets[i] == 'unlockshop':
                features[targets[i]] = ['unlockshop(S,A):-same(S,R,A),pin(S,P,H),hin(S,H,R)',
                                        'unlockshop(S,A):-same(S,A,W),pin(S,P,H),hin(S,H,R),same(S,R,W)'
                                        'unlockshop(S,A):-sopen(S,A)',
                                        'unlockshop(S,A):-ph(S,P)',
                                        'unlockshop(S,A):-q(S,P)',
                                        'unlockshop(S,A):-ropen(S,R)',
                                        'unlockshop(S,A):-wopen(S,W)',
                                        'unlockshop(S,A):-hopen(S,H)']
            elif targets[i] == 'unlockwork':
                features[targets[i]] = ['unlockwork(S,W):-same(S,R,W),pin(S,P,H),hin(S,H,R)',
                                        'unlockwork(S,W):-same(S,A,W),pin(S,P,H),hin(S,H,R),same(S,R,A)',
                                        'unlockwork(S,W):-wopen(S,W)',
                                        'unlockwork(S,W):-ph(S,P)',
                                        'unlockwork(S,W):-q(S,P)',
                                        'unlockwork(S,W):-ropen(S,R)',
                                        'unlockwork(S,W):-sopen(S,A)',
                                        'unlockwork(S,W):-hopen(S,H)']
            elif targets[i] == 'unlockhouse':
                features[targets[i]] = ['unlockhouse(S,H):-same(S,R,A),pin(S,P,H),hin(S,H,R)',
                                        'unlockhouse(S,H):-same(S,A,W),pin(S,P,H),hin(S,H,R),same(S,R,W)',
                                        'unlockhouse(S,H):-sopen(S,A)',
                                        'unlockhouse(S,H):-ph(S,P)',
                                        'unlockhouse(S,H):-q(S,P)',
                                        'unlockhouse(S,H):-ropen(S,R)',
                                        'unlockhouse(S,H):-wopen(S,W)',
                                        'unlockhouse(S,H):-hopen(S,H)']
        return features
        

    @staticmethod
    def run(iters = 2,discount = 0.99):
        """Monte Carlo Tree Search
        """

        bk = Simulator.bk
        features = MCS.learn_representation(bk)
        print (features)
        exit()
        targets = list(bk.keys())
        models = {}
        for target in targets:
            print ("target:",target)
            model = DN(features[target])
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
            n = 2 * len(examples) - 1
            model.learn(facts,examples,bk[target],target)
            models[target] = model

MCS.run()
        
        
        

    
