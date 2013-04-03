


class House:
    num_houses = 0

    def __init__(self):
        self.__class__.num_houses += 1
        self.id = self.__class__.num_houses

    def __str__(self):
        return "House %s" % self.id

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


class Villager:
    """ a single villager in Jamestown.
    Villagers are born, age, marry, have children and die.
    Their main stat is hp.
    """
    #required_food = 2000 * 30
    base_hp = 150
    base_age = 0
    age_labels = ['infant', 'child', 'prime', 'middle', 'boring', 'wizened']
    age_groups = [[0, 5], [6, 15], [16, 40], [41, 60], [61, 200]]
    num_people = 0
    adult_monthly_food = 30

    def __init__(self, village):
        """ Called on birth.
        """
        self.__class__.num_people += 1
        self.id = self.__class__.num_people
        self.age = self.__class__.base_age
        self.age_group = 0
        self.age_label = self.__class__.age_labels[self.age_group]
        self.hp = self.__class__.base_hp
        self.village = village
        # nourishment: [well, adequate, poor, danger] == [4,3,2,1]
        self.nourishment = 3
        # get monthly good req
        self.update_food_req()

    def grow_up(self):
        """ Advances villager to adulthood.
        Used when populating village for first time with villagers.
        """
        self.age = 16
        self.hp = 1000
        return self

    def update_food_req(self):
        """ Calculates, stores and returns monthly food requirements for this villager.
        Infants and children require 1/3 and 1/2 of everyone else.
        """
        if self.age_group <= 1:
            self.monthly_food_req = self.__class__.adult_monthly_food / (self.age_group + 1)
        else:
            self.monthly_food_req = self.__class__.adult_monthly_food
        return self.monthly_food_req

    def update_age_label(self):
        """ determine age label of this villager, store and return it
        """
        self.age_group = 0
        for group in self.__class__.age_groups:
            if self.age_group >= group[0] and self.age_group <= group[1]:
            	self.age_group = self.__class__.age_groups.index(group)
                # return matching age label
                self.age_label = self.__class__.age_labels[self.age_group]
                return self.age_label
            else:
                pass
        raise Exception("ERROR: no age group found!")



if __name__ == "__main__":
    #v1 = Villager()
    #f1 = Family(v1)
    h1 = House()
    import pdb; pdb.set_trace()

