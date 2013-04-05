class Village:
    num_villagers = 0

    def __init__(self):
        self.supplies = 600  # enough for 5 people/yr
        self.food = 2000  # enough to feed 2 people for a year

        # profs
        self.farmer_ct = 0
        self.farmers = []
        self.crafter_ct = 0
        self.crafters = []
        self.guard_ct = 0
        self.guards = []

        # houses
        self.house_ct = 0
        self.houses = []
