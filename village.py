import random


class Village:
    num_villagers = 0

    def __init__(self):
        self.goods = 1000
        self.food = 1000

        self.villagers = []
        self.prospects = []  # list available mates
        self.families = []

        # profs
        self.farmers = []
        self.crafters = []
        #self.guards = []
        self.farmer_rate = 0.50
        self.crafter_rate = 1.0
        #self.farmer_rate = 0.33
        #self.crafter_rate = 0.66
        #self.guard_rate = 0.99
        self.new_prof_rate = 0.10

        # houses
        self.houses = []
        self.empty_houses = []


    def run_village(self, years):
        for year in range(years):
            if self.families == []:
                print "ALL GONE YOU FAIL"
                break
            #if year == 16:
                #import pdb
                #pdb.set_trace()
            print "\n\n====== YEAR {0} ======".format(year)
            print "food: {0}, goods {1}".format(self.food, self.goods)
            print "{0} families, {1} villagers".format(len(self.families),
                len(self.villagers))
            for month in range(10):
                #print "\n-- MONTH {0} --".format(month)
                for family in self.families:
                    fam_status = family.monthly_update()
                    #import pdb; pdb.set_trace()

                print "VILLAGE: {0}/{1}".format(self.food, self.goods)
            #import pdb; pdb.set_trace()

            # annual update for each family
            for family in self.families:
                family.yearly_update()


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
            if profession == 'farmer':
                self.farmers.append(villager)
            elif profession == 'crafter':
                self.crafters.append(villager)
            else:
                raise Exception("ERROR: Bad profession given.")
            return profession
        else:
            random.seed()
            rate = random.random()
            if rate <= self.farmer_rate:
                self.farmers.append(villager)
                return 'farmer'
            elif rate <= self.crafter_rate:
                self.crafters.append(villager)
                return 'crafter'
            else:
                raise Exception("No prof!")
                #self.guards.append(villager)
                #return 'guard'

    def update_profession(self, villager):
        """ every year, adult villagers 
        """
        pass

