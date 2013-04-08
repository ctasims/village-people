
class Family:
    """ Family containing villagers in Jamestown
    """

    def __init__(self, dad, mom):
        self.dad = dad
        self.mom = mom
        self.kids = []

        self.food = 0
        self.output = 1
        self.house = None
        # set stats
        self.compute_stats()

    def get_members(self):
        return {
                'dad': self.dad,
                'mom': self.mom,
                'kids': self.kids
                }

    def update_stats(self):
        self.compute_size()
        self.compute_reqs()
        self.compute_hp()
        self.compute_output()
        return self

    def compute_size(self):
        """ returns number of villagers in family
        Should be called every birth/death
        """
        self.size = len(self.get_members())
        return self.size

    def compute_reqs(self):
        """ Calculates required food and supplies for entire family
        """
        self.req_food = Villager.req_food * self.size
        self.req_supplies = 40 * self.size
        return {'food': self.req_food, 'supplies': self.req_supplies}

    def compute_hp(self):
        """ Calculates total health of family
        """
        self.hp = self.dad.hp + self.mom.hp
        for kid in self.kids:
        	self.hp += kid.hp
        return self.hp

    def add_mom(self, villager):
        """ add mom to family.
        Called on marriage.
        """
        self.mom = villager 
        self.update_stats()
        return self

    def birth(self):
        """ create new villager and add them to family
        """
        new_kid = Villager()
        self.kids.append(new_kid)
        self.update_stats()
        return self
        
    def get_groceries(self, total_village_food):
        """ take family's desired monthly portion of food from village total.
        If not enough, take what's left.
        Return amount of food taken.
        """
        if total_village_food >= self.required_food:
        	self.food = self.required_food
        else:  # not enough food to be well-fed
        	self.food = total_village_food
        return self.food

    def compute_output(self):
        """ family's profession output is based solely on family health.
        curr hp / max hp
        """
        max_output = 1000 * self.size
        self.output = self.hp / max_output
        return self.output
