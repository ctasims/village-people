import random
from house import House
from villager import Villager
from family import Family
import sys


class Village:

    def __init__(self, rates, num_families):
        self.goods = 1000
        self.food = 1000
        self.year = 0
        self.peak_villagers = 0
        self.peak_families = 0

        self.villagers = []
        self.prospects = []  # list available mates
        self.families = []
        # avg years: 200
        #self.max_outputs = {'farmer': 400, 'crafter': 180, 'guard': 0}
        self.max_outputs = {'farmer': 180, 'crafter': 110, 'guard': 0}

        # profs
        self.prof_list = {
                'farmer': [],
                'crafter': [],
                'guard': [],
                }
        #self.new_prof_rate = 0.10

        # GA controls
        rate_total = sum(rates[:3])
        self.farmer_rate = rates[0] / rate_total
        self.crafter_rate = rates[1] / rate_total
        self.guard_rate = rates[2] / rate_total
        self.baby_rate = rates[3]
        #self.baby_rate = 0.15

        # houses
        self.houses = []
        # create empty houses
        self.empty_houses = [House() for x in range(num_families*2)]

        f = 'farmer'
        c = 'crafter'
        g = 'guard'
        possible_profs = [c, f, g]
        #if professions is None:  # standard spread, if we don't input
        professions = []
        for x in range(num_families):
            professions.append(self.new_profession())
        #professions = [f, f, f, f, c, c, c, c, g, g]
        self.profession_init = professions

        for indx in range(num_families):
            # the profs assigned here don't matter
            house = self.empty_houses.pop()
            new_fam = Family(self, house, None)
            new_woman = Villager(self, new_fam, 'f')
            new_fam.add_kid(new_woman)
            new_woman.force_grow_up()
            new_woman.family.set_profession(professions[indx])
        for indx in range(num_families):
            house = self.empty_houses.pop()
            new_fam = Family(self, house, None)
            new_man = Villager(self, new_fam, 'm')
            new_fam.add_kid(new_man)
            new_man.force_grow_up()
            new_man.family.set_profession(professions[indx])

        # start with 1 kid each
        for family in self.families:
            family.check_for_baby(1)
            family.update_stats(0)



    def run_village(self, years, printing=True):
        for year in range(years):
            self.year = year
            #import pdb
            #if year == 150:
                #pdb.set_trace()
            if self.families == []:
                if printing:
                    print "THE VILLAGE PEOPLE DIED IN YEAR {0}".format(year)
                    print "food: {0}, goods {1}".format(self.food, self.goods)
                    print self.profession_init
                return year, self.peak_villagers, self.peak_families
            elif len(self.families) > 100:
                return years, 1000, 100

            if printing:
                print "====== YEAR {0} ======".format(year)
                print "food: {0}, goods {1}".format(self.food, self.goods)
                print "{0} families, {1} villagers".format(len(self.families),
                    len(self.villagers))
                show_status = True
            else:
            	show_status = False

            # loop over each month
            for month in range(10):
                for family in self.families:
                    fam_status = family.monthly_update(show_status)
                if printing:
                    print '\n'
                    print "VILLAGE: {0}/{1}\n".format(self.food, self.goods)
                # update counts
            curr_villagers = len(self.villagers)
            if curr_villagers > self.peak_villagers:
                self.peak_villagers = curr_villagers
            curr_families = len(self.families)
            if curr_families > self.peak_families:
                self.peak_families = curr_families

            # annual update for each family
            for family in self.families:
                family.yearly_update()

            # every other year, 10% of food spoils
            if year % 2 == 0:
                self.food = round( self.food * 0.9)

        # YOU MADE IT!!!!!
        return year, self.peak_villagers, self.peak_families


    def remove_family(self, family):
        """
        family dies for 3 reasons:
        1. all members pass away
        2. only male children left, and they grow up
        3. no dad, and mother gets married
        """
        self.empty_houses.append(family.house)
        try:
            self.families.remove(family)
            prof = family.profession
            self.prof_list[prof].remove(family)
        except:
            #print "####### FAMILY VALUE ERROR ##########"
            pass
        if family.house:
            self.empty_houses.append(family.house)
        family = None
        

    def remove_villager(self, vgr):
        """
        if villager dies, need to get rid of them
        """
        try:
            self.villagers.remove(vgr)
        except:
            #print "####### VALUE ERROR ##########"
            pass
        dad = vgr.family.dad
        mom = vgr.family.mom
        if dad is not None and dad == vgr:
            vgr.family.dad = None
            if mom:
                vgr.family.mom.spouse = None
        if mom is not None and mom == vgr:
            vgr.family.mom = None
            if dad:
                vgr.family.dad.spouse = None
        else:  # was a kid
        	vgr.family.remove_kid(vgr)
        	

    def new_profession(self):
        """ roll for new profession and assign villager to it.
        Profession rates are stored as percentage, where range of all 3 is 100.
        e.g. farmer = 30, crafter = 60, guard = 99
        villager does random roll, and is assigned based on range.
        [0, 30] == farmer.
        [31, 60] == crafter
        [61, 99] == guard
        """
        rate = random.random()
        if rate <= self.farmer_rate:
            return 'farmer'
        elif rate <= self.farmer_rate + self.crafter_rate:
            return 'crafter'
        elif rate <= self.farmer_rate + self.crafter_rate + self.guard_rate:
            return 'guard'
        else:
            raise Exception("ERROR: new profession")


    def update_profession(self, new_prof_rate=0.1):
        """ every year, adult villagers 
        """
        #if random.random() < new_prof_rate:
        rate = random.random()
        if rate <= self.farmer_rate:
            return 'farmer'
        elif rate <= self.farmer_rate + self.crafter_rate:
            return 'crafter'
        elif rate <= self.farmer_rate + self.crafter_rate + self.guard_rate:
            return 'guard'
        #else:
            #return None


if __name__ == "__main__":
    rates = [0.59, 0.58, 0, 0.25]
    num_families = 10
    vill = Village(rates, num_families)
    fitness, count_villagers, count_families = vill.run_village(300)
    print fitness, count_villagers, count_families

