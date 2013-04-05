
class Family:
    """ Family containing villagers in Jamestown
    """

    def __init__(self, dad):
        self.dad = dad
        self.mom = None
        self.kids = []

        self.food = 0
        self.productivity = 1
        self.family_hp = dad.hp
        self.family_size = 1
        self.house = None

    def get_members(self):
        return {
                'dad': self.dad,
                'mom': self.mom,
                'kids': self.kids
                }

    def get_family_size(self):
        """ returns number of villagers in family
        """
        self.family_size = len(self.get_members)
        self.required_food = Villager.required_food * self.family_size
        return self.family_size

    def get_family_hp(self):
        hp = self.dad.hp + self.mom.hp
        for kid in self.kids:
        	hp += kid.hp
        self.family_hp = hp
        return hp

    def compute_required_food(self):
        """ calculate calorie reqs of family for month to be well-fed
        """

    def add_mom(self, villager):
        """ add mom to family.
        Called on marriage.
        """
        self.mom = villager 
        self.update_family_size()

    def birth(self):
        """ create new villager and add them to family
        """
        new_kid = Villager()
        self.kids.append(new_kid)
        self.update_family_size()
        
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

    def compute_productivity(self):
        """ family's profession output is based solely on family health
        """
        max_productivity = 1000 * self.family_size
        self.productivity = self.family_hp / max_productivity
        return self.productivity
