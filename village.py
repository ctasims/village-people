import random


class Village:
    num_villagers = 0

    def __init__(self, rates):
        self.goods = 1000
        self.food = 1000
        self.year = 0

        self.villagers = []
        self.prospects = []  # list available mates
        self.families = []

        # profs
        self.farmers = []
        self.crafters = []
        self.guards = []
        #self.new_prof_rate = 0.10

        # GA controls
        rate_total = sum(rates[:3])
        self.farmer_rate = rates[0] / rate_total
        self.crafter_rate = rates[1] / rate_total
        self.guard_rate = rates[2] / rate_total
        self.baby_rate = rates[3]

        # houses
        self.houses = []
        self.empty_houses = []


    def run_village(self, years):
        for year in range(years):
        	self.year = year
        	# End simulation if everyone's dead
            if self.families == []:
                print "THE VILLAGE PEOPLE DIED IN YEAR {0}".format(year)
                return year

            print "\n\n====== YEAR {0} ======".format(year)
            print "food: {0}, goods {1}".format(self.food, self.goods)
            print "{0} families, {1} villagers".format(len(self.families),
                len(self.villagers))

            # loop over each month
            for month in range(10):
                for family in self.families:
                    fam_status = family.monthly_update()

                print "VILLAGE: {0}/{1}\n".format(self.food, self.goods)

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
            if profession == 'farmer':
                self.farmers.append(villager)
            elif profession == 'crafter':
                self.crafters.append(villager)
            elif profession == 'guard':
                self.guards.append(villager)
            else:
                raise Exception("ERROR: Bad profession given.")
            return profession
        else:
            random.seed()
            rate = random.uniform()
            if rate <= self.farmer_rate:
                self.farmers.append(villager)
                return 'farmer'
            elif rate <= self.farmer_rate + self.crafter_rate:
                self.crafters.append(villager)
                return 'crafter'
            elif rate <= self.farmer_rate + self.crafter_rate + self.guard_rate:
                self.guards.append(villager)
                return 'guard'

    def update_profession(self, villager):
        """ every year, adult villagers 
        """
        pass

