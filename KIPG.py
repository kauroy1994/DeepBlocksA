from Contagion import Simulator
from ML import RepLearn
from tqdm import tqdm

class KIPG(object):
    """Knowledge Infused Policy
       Gradients
    """

    @staticmethod
    def learn_count_features(bk,iters = 2):
        """learns count features
           from random policy episodes
        """

        actions = list(bk.keys())
        features = {}
        n_actions = len(actions)
        print ("Learning count features ..")
        for i in tqdm(range(n_actions)):
            n = 0
            for j in range(iters):
                facts = []
                examples = {}
                episode = False
                while True:
                    if not episode:
                        episode = Simulator.generate_episode(s_number = n)
                    else:
                        break
                n_sa_pairs = len(episode)
                for k in range(n_sa_pairs):
                    facts += episode[k][0].facts()
                    if episode[k][1].split('(')[0] == actions[i]:
                        examples[episode[k][1]] = 0
            n = 2*len(examples)-1
            features[actions[i]] = RepLearn.generate_features(facts,
                                                              examples,
                                                              bk[actions[i]],
                                                              actions[i])
        return features
        

    @staticmethod
    def run(iters = 2,discount = 1.0):
        """comment pending
        """

        bk = Simulator.bk
        features = KIPG.learn_count_features(bk)
        print (features)
        exit()

KIPG.run()
