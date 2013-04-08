class Village:
    num_villagers = 0

    def __init__(self):
        self.supplies = 1000
        self.food = 1000

        self.villagers = []
        self.prospects = []  # list available mates

        # profs
        self.farmers = []
        self.crafters = []
        self.guards = []

        # houses
        self.houses = []
