import random

class Lord_GA:

    def __init__(self):
        """
        Initialize first batch of values
        """
        self.P = []
        for x in range(10):
        	self.P.append(self.random_vals())


    def run(self, max_fitness=1000, num_villages=100):
        """
        GA repeatedly creates a village, runs it with values, then judges its
        performance and modifies values.
        Runs in groups of 10 villages.
        """
        pass


    def random_vals(self):
        f_rate = random.uniform(0, 1)
        c_rate = random.uniform(f_rate, 1)
        g_rate = 1
        baby_rate = random.uniform(0,1)
        return [f_rate, c_rate, g_rate, baby_rate]


    def mutate(self, P):
        """
        mutate randomly selected elements by creating random new values for
        rates
        """
        # first grab random rows from P
        rows = random.sample(P, random.uniform(1, len(P))) 
        for row in rows:
        	row = self.random_vals()
        return P
        
    def one_point_crossover(self, P):
        """
        evolves P by randomly grabbing pairs of rows and crossing them
        """
        # first create list of indexes that we'll use to grab rows
        indexes = range(len(P))
        random.shuffle(indexes)

        # now grab pair of random rows and crossover. Repeat until no more.
        new_P = []
        while P:
        	row_a = P.pop(indexes.pop())
        	row_b = P.pop(indexes.pop())
        	a_vals = [a[2], a[3]]
        	row_a[2] = row_b[2]
        	row_a[3] = row_b[3]
        	row_b[2] = a_vals[0]
        	row_b[3] = a_vals[1]
        	new_P.append(row_a)
        	new_P.append(row_b)

        return new_P

