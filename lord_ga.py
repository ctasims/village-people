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
            self.init_P.append(self.generate_genome())


    def run(self, villages_per_gen=100, num_families=10, max_gens=10,
            max_fitness=1000, elitism=False, use_ga=False):
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
            for prof_designations in P:
                vill = Village(num_families, prof_designations)
                fitness, count_villagers, count_fams = vill.run_village(max_fitness, printing)
                # append single result to results
                results.append((fitness, prof_designations, count_villagers, count_fams))
                vill = None
            # append set of 10 results to main set of results
            total_results.append(results)

            # now modify rates
            #elitism = True

            if elitism:
                fitnesses = [run[0] for run in results]
                indexes = range(len(P))
                max_fit_index = fitnesses.index(max(fitnesses))
                P[0] = P[max_fit_index]
                #P[1] = P[max_fit_index]

            if use_ga:
                P = self.tournament_select(P, results, elitism)
                P = self.mutate(P, elitism)
                P = self.alternate_crossover(P, elitism)
                #P = self.three_point_crossover(P)

            else:
                # BASE: replace P with random vals
                P = []
                for x in range(villages_per_gen):
                    P.append(self.generate_genome())

            gen += 1

        return total_results


    def run_once(self, max_years=20):
        #rates = self.generate_genome()
        rates = [0.5, 0.2, 0, 0.1]
        vill = Village(rates)
        fitness = vill.run_village(max_years)
        print fitness, rates



    def generate_genome(self):
        f = 'farmer'
        c = 'crafter'
        g = 'guard'
        prof_designations = []
        for x in range(4000):
            prof_designations.append(random.choice([c, f, g]))
        return prof_designations


    def tournament_select(self, P, results, elitism):
        """
        Take random pairs, and add the winner
        """
        # get actual fitness values for each trial. They're first elem in tuple.
        fitnesses = [run[0] for run in results]
        indexes = range(len(P))

        if elitism:
            new_P = [P[0], P[1]]
            iterations = len(P)-2
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



    def mutate(self, P, elitism):
        """
        mutate randomly selected elements by creating random new values for
        rates
        """
        mutate_chance = 0.1
        if elitism:
        	indexes = range(2, len(P))
        	new_P = [P[0], P[1]]
        else:
        	indexes = range(len(P))
        	new_P = []

        for x in indexes:
            if random.random() < mutate_chance:
                row = self.generate_genome()
                new_P.append(row)
            else:
            	new_P.append(P[x])
        return new_P
        
    def alternate_crossover(self, P, elitism):
        """
        evolves P by randomly grabbing pairs of rows and crossing them.
        If elitism, the first two rows are the elites so skip them.
        """
        if elitism:
            elite_row1 = P[0][:]
            elite_row2 = P[1][:]
        # first create list of indexes that we'll use to grab rows
        indexes = range(len(P))
        new_P = []
        random.shuffle(indexes)

        # now grab pair of random rows and crossover. Repeat until no more.
        halfway = len(P[0]) / 2
        q1 = halfway / 2
        q3 = halfway + q1
        for iteration in range(len(P) / 2):
            index_a = indexes.pop()
            index_b = indexes.pop()
            row_a = P[index_a]
            row_b = P[index_b]
            new_row_a = []
            new_row_b = []
            for i in range(len(row_a)):
                if i % 2 == 0:
                    new_row_a.append(row_a[i])
                    new_row_b.append(row_b[i])
                else:
                    new_row_a.append(row_b[i])
                    new_row_b.append(row_a[i])
            new_P.append(new_row_a)
            new_P.append(new_row_b)

        if elitism:
        	new_P[0] = elite_row1
        	new_P[1] = elite_row2
        return new_P



    def three_point_crossover(self, P):
        """
        evolves P by randomly grabbing pairs of rows and crossing them
        """
        if elitism:
            elite_row1 = P[0][:]
            elite_row2 = P[1][:]

        # first create list of indexes that we'll use to grab rows
        indexes = range(len(P))
        random.shuffle(indexes)

        # now grab pair of random rows and crossover. Repeat until no more.
        new_P = []
        halfway = len(P[0]) / 2
        q1 = halfway / 2
        q3 = halfway + q1
        for pair in range(len(P)/2):
            index_a = indexes.pop()
            index_b = indexes.pop()
            row_a = P[index_a]
            row_b = P[index_b]
            new_row_a = row_a[:q1] + row_b[q1:halfway] + row_a[halfway:q3] + row_b[q3:]
            new_row_b = row_b[:q1] + row_a[q1:halfway] + row_b[halfway:q3] + row_a[q3:]
            new_P.append(new_row_a)
            new_P.append(new_row_b)

        if elitism:
        	new_P[0] = elite_row1
        	new_P[1] = elite_row2
        return new_P


if __name__ == "__main__":
    import time
    import csv
    import os
    # short analysis

    #### BASE RUNS ####
    villages_per_gen = 40
    num_families = 10
    max_gens = 100
    max_fitness = 500
    use_ga = True
    elitism = True

    ga = Lord_GA(villages_per_gen)

    total_results = ga.run(
            villages_per_gen, num_families, max_gens,
            max_fitness, elitism, use_ga)

    timestr = time.strftime("%Y%m%d-%H%M%S")
    result_dir = os.path.join(os.path.dirname(os.path.os.path.realpath(__file__)), 'results')
    result_file = os.path.join(result_dir, timestr) + '.csv'
    summary_file = os.path.join(result_dir, timestr) + '_summary.csv'
    with open(result_file, 'wb') as file1:
        outs = csv.writer(file1)
        run = 1
        max_fit_list = []
        avg_fit_list = []
        max_profs_list = []
        max_count_villagers = []
        max_count_families = []
        for results in total_results:
            for row in results:
                outs.writerow(row)
            fitnesses = [row[0] for row in results]
            max_fit = max(fitnesses)
            avg_fit = round(sum(filter(None, fitnesses)) * 1.0 / len(fitnesses))

            # get rates from the gen with max fitness
            max_fit_indx = fitnesses.index(max_fit)
            max_profs = results[max_fit_indx][1]
            max_count_villager = results[max_fit_indx][2]
            max_count_family = results[max_fit_indx][3]

            max_fit_list.append(max_fit)
            max_profs_list.append(max_profs)
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
        outs2.writerow(['', 'gen', 'max fit', 'avg fit', 'max villagers', 'max families'])
        for i in range(len(max_fit_list)):
            # generation, max fit, avg fit, f rate, c rate, g rate, birth rate, # vgs, # fams
            outs2.writerow([
                '', i, max_fit_list[i], avg_fit_list[i],
                max_count_villagers[i], max_count_families[i]])
        outs2.writerow([''])
        for desigs in max_profs_list:
        	outs2.writerow([''] + desigs)

    print 'max: {0}'.format(max(max_fit_list))
    print max_fit_list
    # average
    avg = sum(avg_fit_list) / len(avg_fit_list)
    print 'average: {0}'.format(avg)
    print 'max villagers: {0}, families: {1}'.format(max(max_count_villagers), max(max_count_families))

