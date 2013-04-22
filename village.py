import random
from house import House
from villager import Villager
import sys


class Village:

    def __init__(self, rates, num_families):
        self.num_villagers = 0
        self.goods = 1000
        self.food = 1000
        self.year = 0

        self.villagers = []
        self.prospects = []  # list available mates
        self.families = []
        self.max_solo_outputs = {'farmer': 80, 'crafter': 30, 'guard': 0}
        self.max_fam_outputs = {'farmer': 240, 'crafter': 90, 'guard': 0}

        # profs
        #self.farmers = []
        #self.crafters = []
        #self.guards = []
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
        #self.baby_rate = rates[3]
        self.baby_rate = 0.15

        # houses
        self.houses = []
        # create 10 empty houses
        self.empty_houses = [House() for x in range(10)]

        c = 'crafter'
        f = 'farmer'
        g = 'guard'
        professions = [f, f, f, c, f, c, f, c, c, g]

        colonist_men = []
        colonist_women = []
        num_families = num_families
        for indx in range(num_families):
            new_woman = Villager(self, None, 'f')
            new_woman.force_grow_up()
        #for indx, prof in zip(range(num_families), professions):
        for indx in range(num_families):
            new_man = Villager(self, None, 'm')
            new_man.force_grow_up(profession=professions[indx])

        # start with 1 kid each
        for family in self.families:
            family.check_for_baby(1)


    def run_village(self, years):
        for year in range(years):
            self.year = year
            if self.families == []:
                #print "THE VILLAGE PEOPLE DIED IN YEAR {0}".format(year)
                print "food: {0}, goods {1}".format(self.food, self.goods)
                return year

            print "\n\n====== YEAR {0} ======".format(year)
            print "food: {0}, goods {1}".format(self.food, self.goods)
            print "{0} families, {1} villagers".format(len(self.families),
                len(self.villagers))

            # loop over each month
            for month in range(10):
                for family in self.families:
                    fam_status = family.monthly_update()

                #print "VILLAGE: {0}/{1}\n".format(self.food, self.goods)

            # annual update for each family
            for family in self.families:
                family.yearly_update()

            # every other year, 10% of food spoils
            if year % 2 == 0:
                self.food = round( self.food * 0.9)
            

    def new_profession(self, villager, profession=None):
        """ roll for new profession and assign villager to it.
        Profession rates are stored as percentage, where range of all 3 is 100.
        e.g. farmer = 30, crafter = 60, guard = 99
        villager does random roll, and is assigned based on range.
        [0, 30] == farmer.
        [31, 60] == crafter
        [61, 99] == guard
        """
        if profession:
        	# set profession manually
            #if profession == 'farmer':
                #self.farmers.append(villager)
            #elif profession == 'crafter':
                #self.crafters.append(villager)
            #elif profession == 'guard':
                #self.guards.append(villager)
            #else:
                #raise Exception("ERROR: Bad profession given.")
            return profession
        else:
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
    rates = [0.2, 0.6, 0, 0.1]
    for x in range(10):
        vill = Village(rates)
        fitness = vill.run_village(300)
        print fitness
        vill = None

