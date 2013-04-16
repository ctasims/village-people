import random


class Village:
    num_villagers = 0

    def __init__(self):
        self.supplies = 1000
        self.food = 1000

        self.villagers = []
        self.prospects = []  # list available mates
        self.families = []

        # profs
        self.farmers = []
        self.crafters = []
        #self.guards = []
        self.farmer_rate = 0.50
        self.crafter_rate = 0.99
        #self.farmer_rate = 0.33
        #self.crafter_rate = 0.66
        #self.guard_rate = 0.99
        self.new_prof_rate = 0.10

        # houses
        self.houses = []
        self.empty_houses = []


    def run_village(self, years):
        num_years = 10
        for year in range(num_years):
            for month in range(10):
                empty_families = []

                for family in self.families:
                    fam_status = family.monthly_update()
                    if not fam_status:
                    	empty_families.append(family)
                    print "\n"
                # if all members are dead, need to remove family
                # what about house?
                for empty_fam in empty_families:
                	self.families.remove(empty_fam)
                self.families = filter(None, self.families)

                print "food: {0}, supplies {1}".format(self.food, self.supplies)
            import pdb; pdb.set_trace()

            # annual update for each family
            for family in self.families:
                family.yearly_update()

            print "END OF YEAR"
            print "food: {0}, supplies {1}".format(self.food, self.supplies)
            print "{0} families".format(len(self.families))


    def new_profession(self, villager):
        """ roll for new profession and assign villager to it.
        Profession rates are stored as percentage, where range of all 3 is 100.
        e.g. farmer = 30, crafter = 60, guard = 99
        villager does random roll, and is assigned based on range.
        [0, 30] == farmer.
        [31, 60] == crafter
        [61, 99] == guard
        """
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

