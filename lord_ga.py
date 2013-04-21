import random
from village import Village

class Lord_GA:

    def __init__(self):
        """
        Initialize first batch of values
        """
        self.init_P = []
        example_row = self.random_vals()
        for x in range(6):
            #self.init_P.append(example_row)
            self.init_P.append(self.random_vals())


    def run(self, max_runs=10, max_fitness=1000, num_villages=100):
        """
        GA repeatedly creates a village, runs it with values, then judges its
        performance and modifies values.
        Runs in groups of 10 villages.
        """
        max_years = 100
        run = 1
        total_results = []
        P = self.init_P
        while run <= max_runs:
            results = []
            # for each set of rates, run one village
            for rates in P:
                vill = Village(rates)
                fitness = vill.run_village(max_years)
                # append single result to results
                results.append((fitness, rates))
                vill = None
            # append set of 10 results to main set of results
            total_results.append(results)

            # now modify rates
            P = self.tournament_select(P, results, True)
            P = self.mutate(P)
            P = self.one_point_crossover(P)

            run += 1

        return total_results


    def run_once(self, max_years=20):
        #rates = self.random_vals()
        rates = [0.5, 0.2, 0, 0.1]
        vill = Village(rates)
        fitness = vill.run_village(max_years)
        print fitness, rates



    def random_vals(self):
        f_rate = round(random.uniform(0, 1), 2)
        c_rate = round(random.uniform(0, 1), 2)
        g_rate = round(random.uniform(0, 1), 2)
        baby_rate = round(random.uniform(0,1), 2)
        return [f_rate, c_rate, g_rate, baby_rate]


    def tournament_select(self, P, results, elitism=False):
        """
        Take random pairs, and add the winner
        """
        # get actual fitness values for each trial. They're first elem in tuple.
        fitnesses = [run[0] for run in results]
        #max_fit_index = fitnesses.index(max(fitnesses))
        indexes = range(len(P))
        #new_P = [P[max_fit_index]]
        new_P = []
        for x in range(len(P)):
        	# grab two random row indexes
            index1, index2 = random.sample(indexes, 2)
            row1 = P[index1]
            row2 = P[index2]
            fit1 = fitnesses[index1]
            fit2 = fitnesses[index2]
            if fit1 > fit2:
            	new_P.append(row1)
            else:
            	new_P.append(row2)
        return new_P


    def roulette_select(self, P, results):
        """
        Take random pairs, and add the winner
        """
        # get actual fitness values for each trial. They're first elem in tuple.
        #fitnesses = [run[0] for run in results]
        #indexes = range(len(P))
        #new_P = []
        #for x in range(len(P)):
            ## grab two random row indexes
            #index1, index2 = random.sample(indexes, 2)
            #row1 = P[index1]
            #row2 = P[index2]
            #fit1 = fitnesses[index1]
            #fit2 = fitnesses[index2]
            #if fit1 > fit2:
                #new_P.append(row1)
            #else:
                #new_P.append(row2)
        #return new_P



    def mutate(self, P):
        """
        mutate randomly selected elements by creating random new values for
        rates
        """
        # first grab random rows from P
        rows = random.sample(P, random.randint(1, len(P))) 
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
        for pair in range(len(P)/2):
        	index_a = indexes.pop()
        	index_b = indexes.pop()
        	row_a = P[index_a]
        	row_b = P[index_b]
        	a_vals = [row_a[2], row_a[3]]
        	row_a[2] = row_b[2]
        	row_a[3] = row_b[3]
        	row_b[2] = a_vals[0]
        	row_b[3] = a_vals[1]
        	new_P.append(row_a)
        	new_P.append(row_b)

        return new_P


if __name__ == "__main__":
    ga = Lord_GA()
    total_results = ga.run()
    for results in total_results:
        for result in results:
            print result
        print "\n"

