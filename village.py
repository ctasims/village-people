import random


class Village:
    num_villagers = 0

    def __init__(self):
        self.supplies = 1000
        self.food = 1000

        self.villagers = []
        self.prospects = []  # list available mates

        # profs
        self.farmers = []
        self.craftsmen = []
        self.guards = []
        self.farmer_rate = 0.33
        self.craftsman_rate = 0.66
        self.guard_rate = 0.99
        self.new_prof_rate = 0.10

        # houses
        self.houses = []

    def new_profession(self, villager):
        """ roll for new profession and assign villager to it.
        Profession rates are stored as percentage, where range of all 3 is 100.
        e.g. farmer = 30, craftsman = 60, guard = 99
        villager does random roll, and is assigned based on range.
        [0, 30] == farmer.
        [31, 60] == craftsman
        [61, 99] == guard
        """
        random.seed()
        rate = random.random()
        if rate <= self.farmer_rate:
        	self.farmers.append(villager)
        	return 'farmer'
        elif rate <= self.craftsman_rate:
        	self.craftsmen.append(villager)
        	return 'craftsman'
        else:
        	self.guards.append(villager)
        	return 'guard'

    def update_profession(self, villager):
        """ every year, adult villagers 
        """
            
