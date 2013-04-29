import random
from village import Village
import datetime
import matplotlib
matplotlib.use('TkAgg')
import time
import matplotlib.pyplot as plt
from matplotlib import mpl
import numpy as np


class Lord_GA(object):

    def __init__(self, villages_per_gen):
        """
        Initialize first batch of values
        """
        self.init_P = []
        for x in range(villages_per_gen):
            self.init_P.append(self.generate_genome())


    def run(self, plot_file=None):
        """
        GA repeatedly creates a village, runs it with values, then judges its
        performance and modifies values.
        Runs in groups of 10 villages.
        """
        gen = 0
        total_results = []
        P = self.init_P
        printing = False

        villages_per_gen = 30
        num_families = 10
        max_gens = 100
        max_fitness = 500
        use_ga = True
        elitism = True
        catastrophe = False
        presentation = True
        if use_ga:
            suptitle = 'Village evolution with GA'
        else:
            suptitle = 'Village evolution without GA'
        if catastrophe:
            suptitle += ' and with catastrophes'

        if presentation:
            fig = plt.figure(figsize=(8, 6), dpi=150,)
        else:
            fig = plt.figure(figsize=(12, 10), dpi=200,)
        ax = fig.add_subplot(111, aspect='auto')
        ax.set_xlabel('Generation')
        ax.set_ylabel('village trial')

        # FOR LIGHT PLOT
        #fig.suptitle(suptitle, fontsize=14, fontweight='bold')
        #cmap = 'GnBu'
        #facecolor = 'white'
        #fontcolor = 'black'

        # FOR DARK PLOT
        fig.set_facecolor('black')
        ax.set_axis_bgcolor('white')
        fig.suptitle(suptitle, fontsize=14, fontweight='bold', color='white')
        ax.spines['bottom'].set_color('gray')
        ax.spines['top'].set_color('gray')
        ax.spines['left'].set_color('gray')
        ax.spines['right'].set_color('gray')
        xa = ax.xaxis
        xa.set_tick_params(labelcolor='white')
        xa.label.set_color('white')
        ya = ax.yaxis
        ya.set_tick_params(labelcolor='white')
        ya.label.set_color('white')
        cmap='gist_earth'
        facecolor = 'black'
        fontcolor = 'white'
        if presentation:
            cmap = 'gist_ncar'

        fitness_array = np.zeros([villages_per_gen, max_gens])
        fit_plot = plt.imshow(fitness_array, interpolation='nearest',
                                cmap=cmap, origin='lower', vmin=0, vmax=max_fitness)
        ax.set_aspect('auto')
        cbar = plt.colorbar(fit_plot)
        cbytick_obj = plt.getp(cbar.ax.axes, 'yticklabels')
        plt.setp(cbytick_obj, color=fontcolor)

        # BEGIN EVOLUTION
        while gen < max_gens:
            results = []
            vill = None
            fitness = None
            print gen

            # RUN ONE VILLAGE FOR EACH GENOME
            P_index = 0
            for prof_designations in P:
                vill = Village(num_families, prof_designations)
                fitness = vill.run_village(max_fitness, printing,
                        catastrophe, presentation)
                #fitness, count_villagers, count_fams = 1, 2, 3
                results.append((fitness, prof_designations))
                vill = None

                # animation
                #curr_village = P.index(prof_designations)
                fitness_array[P_index][gen] = fitness
                #print 'f %s: %s' % (P_index, fitness)
                if presentation and P_index % 10 == 0:
                    fit_plot = plt.imshow(fitness_array, interpolation='nearest',
                                            cmap=cmap, origin='lower', vmin=0, vmax=400)
                    ax.set_aspect('auto')
                    plt.draw()
                    plt.show(block=False)
                P_index += 1

            # append set of 10 results to main set of results
            total_results.append(results)
            fit_plot = plt.imshow(fitness_array, interpolation='nearest',
                                    cmap=cmap, origin='lower', vmin=0, vmax=400)
            ax.set_aspect('auto')

            if elitism:
                fitnesses = [run[0] for run in results]
                indexes = range(len(P))
                max_fit_index = fitnesses.index(max(fitnesses))
                best_genome = P[max_fit_index][:]
            else:
                best_genome = None

            if use_ga:
                P = self.tournament_select(P, results, elitism, best_genome)
                #P = self.mutate(P, elitism, best_genome)
                #P = self.mutate_blocks(P, elitism, best_genome)
                P = self.mutate_elems(P, elitism, best_genome)
                P = self.alternate_crossover(P, elitism, best_genome)
                #P = self.three_point_crossover(P)

            else:
                # BASE: replace P with random vals
                P = []
                for x in range(villages_per_gen):
                    P.append(self.generate_genome())

            gen += 1

        plt.savefig(plot_file, bbox_inches=0, facecolor=facecolor)
        return total_results


    def generate_genome(self):
        f = 'farmer'
        c = 'crafter'
        g = 'guard'
        prof_designations = []
        for x in range(500):
            prof_designations.append(random.choice([c, f, g]))
        return prof_designations


    def tournament_select(self, P, results, elitism=False, best=None):
        """
        Take random pairs, and add the winner
        """
        # get actual fitness values for each trial. They're first elem in tuple.
        fitnesses = [run[0] for run in results]
        indexes = range(len(P))
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
        if elitism:
            new_P[0] = best[:]
        return new_P


    def mutate_blocks(self, P, elitism=False, best=None):
        """
        mutate randomly selected elements by creating random new values for
        rates
        """
        mutate_chance = 0.2
        indexes = range(len(P))
        num_genes = len(P[0])
        # get indexes that start blocks of 10
        block_starts = [10*x for x in range(num_genes/10 - 1)]
        prof_list = ['farmer', 'crafter', 'guard']
        new_P = []

        for x in indexes:
            if random.random() < mutate_chance:
                new_row = P[x][:]
                block_indexes = random.sample(block_starts, 10)
                for block in block_indexes:
                    # select profession block
                    new_prof = random.choice(prof_list)
                    new_prof_block = [new_prof] * 10
                    new_row[block:block+10] = new_prof_block[:]
                new_P.append(new_row)
            else:
            	new_P.append(P[x])

        if elitism:
            new_P[0] = best[:]
        return new_P

    def mutate_elems(self, P, elitism=False, best=None):
        """
        mutate randomly selected elements by creating random new values for
        rates
        """
        mutate_chance = 0.2
        indexes = range(len(P))
        # get indexes that start blocks of 10
        prof_list = ['farmer', 'farmer', 'crafter', 'crafter', 'guard']
        new_P = []

        for x in indexes:
            new_row = P[x][:]
            if random.random() < mutate_chance:
                for elem_indx in range(len(new_row)):
                    rem = random.sample([0,1],1)[0]
                    if elem_indx % 2 ==rem:
                        new_row[elem_indx] = random.choice(prof_list)
            new_P.append(new_row)

        if elitism:
            new_P[0] = best[:]
        return new_P


    def mutate(self, P, elitism=False, best=None):
        """
        mutate randomly selected elements by creating random new values for
        rates
        """
        mutate_chance = 0.1
        indexes = range(len(P))
        new_P = []

        for x in indexes:
            if random.random() < mutate_chance:
                row = self.generate_genome()
                new_P.append(row)
            else:
            	new_P.append(P[x])

        if elitism:
            new_P[0] = best[:]
        return new_P
        
    def alternate_crossover(self, P, elitism=False, best=None):
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
            new_P[0] = best[:]
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

    runs = 0
    while runs < 2:
        #### BASE RUNS ####

        villages_per_gen = 30
        timestr = time.strftime("%Y%m%d-%H%M%S")
        result_dir = os.path.join(os.path.dirname(os.path.os.path.realpath(__file__)), 'results')
        result_file = os.path.join(result_dir, timestr) + '.csv'
        summary_file = os.path.join(result_dir, timestr) + '_summary.csv'
        plot_file = os.path.join(result_dir, timestr) + '_timeline.png'

        ga = Lord_GA(villages_per_gen)

        total_results = ga.run(plot_file)

        profs_num_averages = []

        with open(result_file, 'wb') as file1:
            outs = csv.writer(file1)
            run = 1
            max_fit_list = []
            avg_fit_list = []
            max_profs_list = []
            for results in total_results:
                total_num_farmers = 0
                total_num_crafters = 0
                total_num_guards = 0
                for row in results:
                    num_farmers = row[1].count('farmer')
                    total_num_farmers += num_farmers
                    num_crafters = row[1].count('crafter')
                    total_num_crafters += num_crafters
                    num_guards = row[1].count('guard')
                    total_num_guards += num_guards
                    new_row = [num_farmers, num_crafters, num_guards] + row[1]
                    outs.writerow(new_row)
                fitnesses = [row[0] for row in results]
                prof_lists = [row[1] for row in results]
                max_fit = max(fitnesses)
                avg_fit = round(sum(filter(None, fitnesses)) * 1.0 / len(fitnesses))

                # get rates from the gen with max fitness
                max_fit_indx = fitnesses.index(max_fit)
                max_profs = results[max_fit_indx][1]

                max_fit_list.append(max_fit)
                max_profs_list.append(max_profs)

                avg_fit_list.append(avg_fit)

                profs = [total_num_farmers/30, total_num_crafters/30, total_num_guards/30]
                profs_num_averages.append(profs)
                outs.writerow(profs)
                summary = ['max fit', max_fit, '', 'avg fit', avg_fit]
                outs.writerow(summary)
                outs.writerow('')
                outs.writerow(['NEW RUN', run])
                run += 1

        # Save max fitnesses to summary file
        with open(summary_file, 'wb') as file2:
            outs2 = csv.writer(file2)
            outs2.writerow(['', 'gen', 'max fit', 'avg fit'])
            for i in range(len(max_fit_list)):
                # generation, max fit, avg fit, f rate, c rate, g rate, birth rate, # vgs, # fams
                outs2.writerow([
                    '', i, max_fit_list[i], avg_fit_list[i]])
            outs2.writerow([''])
            for prof_nums in profs_num_averages:
                outs2.writerow(prof_nums)

        print 'max: {0}'.format(max(max_fit_list))
        print max_fit_list
        # average
        avg = sum(avg_fit_list) / len(avg_fit_list)
        print 'average: {0}'.format(avg)
        #print 'max villagers: {0}, families: {1}'.format(max(max_count_villagers), max(max_count_families))

        runs += 1

