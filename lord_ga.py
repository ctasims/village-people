import random
from village import Village
import datetime

class Lord_GA:

    def __init__(self, villages_per_gen):
        """
        Initialize first batch of values
        """
        self.init_P = []
        for x in range(villages_per_gen):
            self.init_P.append(self.random_vals())


    def run(self, villages_per_gen=100, num_families=10, max_gens=10,
            max_fitness=1000, elitism=False):
        """
        GA repeatedly creates a village, runs it with values, then judges its
        performance and modifies values.
        Runs in groups of 10 villages.
        """
        gen = 1
        total_results = []
        P = self.init_P
        printing = False
        while gen <= max_gens:
            results = []
            vill = None
            fitness = None
            print gen
            # for each set of rates, run one village
            for rates in P:
                vill = Village(rates, num_families)
                fitness, count_villagers, count_fams = vill.run_village(max_fitness, printing)
                # append single result to results
                results.append([fitness] + rates + [count_villagers, count_fams])
                vill = None
            # append set of 10 results to main set of results
            total_results.append(results)
            #for result in results:
                #print result
            #print '\n'

            # now modify rates
            #elitism = True
            P = self.tournament_select(P, results, elitism)
            P = self.mutate(P)
            P = self.one_point_crossover(P)

            # BASE: replace P with random vals
            #P = []
            #for x in range(villages_per_gen):
                #P.append(self.random_vals())

            gen += 1

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
        indexes = range(len(P))

        if elitism:
            max_fit_index = fitnesses.index(max(fitnesses))
            new_P = [P[max_fit_index]]
            iterations = len(P)-1
        else:
            new_P = []
            iterations = len(P)

        for x in range(iterations):
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
        pass
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
        new_P = []
        mutate_chance = 0.1
        for x in range(len(P)):
            if random.random() < mutate_chance:
                row = self.random_vals()
                new_P.append(row)
            else:
            	new_P.append(P[x])
        return new_P
        
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
    import time
    import csv
    import os
    # short analysis

    #### BASE RUNS ####
    villages_per_gen = 50
    num_families = 10
    max_gens = 50
    max_fitness = 1000
    elitism = False

    # long analysis
    #villages_per_gen = 100
    #num_families = 10
    #max_gens = 200
    #max_fitness = 1000
    #elitism = True

    ga = Lord_GA(villages_per_gen)

    total_results = ga.run(
            villages_per_gen, num_families, max_gens,
            max_fitness, elitism)

    timestr = time.strftime("%Y%m%d-%H%M%S")
    result_dir = os.path.join(os.path.dirname(os.path.os.path.realpath(__file__)), 'results')
    result_file = os.path.join(result_dir, timestr) + '.csv'
    summary_file = os.path.join(result_dir, timestr) + '_summary.csv'
    with open(result_file, 'wb') as file1:
        outs = csv.writer(file1)
        run = 1
        max_fit_list = []
        avg_fit_list = []
        max_f_rate_list = []
        max_c_rate_list = []
        max_g_rate_list = []
        max_b_rate_list = []
        max_count_villagers = []
        max_count_families = []
        for results in total_results:
            for row in results:
                outs.writerow(row)
            fitnesses = [row[0] for row in results]
            #f_rates = [row[1] for row in results]
            #c_rates = [row[2] for row in results]
            #g_rates = [row[3] for row in results]
            #b_rates = [row[4] for row in results]
            max_fit = max(fitnesses)

            # get rates from the gen with max fitness
            max_fit_indx = fitnesses.index(max_fit)
            max_f_rate = results[max_fit_indx][1]
            max_c_rate = results[max_fit_indx][2]
            max_g_rate = results[max_fit_indx][3]
            max_b_rate = results[max_fit_indx][4]
            max_count_villager = results[max_fit_indx][5]
            max_count_family = results[max_fit_indx][6]

            avg_fit = round(sum(filter(None, fitnesses)) * 1.0 / len(fitnesses))
            max_fit_list.append(max_fit)
            max_f_rate_list.append(max_f_rate)
            max_c_rate_list.append(max_c_rate)
            max_g_rate_list.append(max_g_rate)
            max_b_rate_list.append(max_b_rate)
            max_count_villagers.append(max_count_villager)
            max_count_families.append(max_count_family)

            avg_fit_list.append(avg_fit)

            summary = ['max fit', max_fit, '', 'avg fit', avg_fit]
            outs.writerow(summary)
            outs.writerow('')
            outs.writerow(['NEW RUN', run])
            run += 1

    # Save max fitnesses to summary file
    with open(summary_file, 'wb') as file2:
        outs2 = csv.writer(file2)
        for i in range(len(max_fit_list)):
            # generation, max fit, avg fit, f rate, c rate, g rate, birth rate, # vgs, # fams
            outs2.writerow([
                '', i, max_fit_list[i], avg_fit_list[i],
                '', max_f_rate_list[i], max_c_rate_list[i],
                    max_g_rate_list[i], max_b_rate_list[i],
                '', max_count_villagers[i], max_count_families[i]])

    print 'max: {0}'.format(max(max_fit_list))
    # average
    avg = sum(avg_fit_list) / len(avg_fit_list)
    print 'average: {0}'.format(avg)
    print 'max villagers: {0}, families: {1}'.format(max(max_count_villagers), max(max_count_families))

