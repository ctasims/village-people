

class Family:
    """ Family containing villagers in Jamestown
    """
    def __init__(self):
        self.food = 0
        self.dad = None  # [id]
        self.mom = None  # [id]
        self.kids = []   # [id]s

    def get_members(self):
        return {
                'dad': self.dad,
                'mom': self.mom,
                'kids': self.kids
                }

    def member_count(self):
        """ returns number of villagers in family
        """
        return len(self.get_members)

    def add_mom(self, villager):
        self.mom = villager 

    def get_food(self, total_food):



class Villager:
    """ class representing single villager in Jamestown.
    """
    num_villagers = 0

    def __init__(self):
        """ Called on birth.
        """
        num_villagers += 1
        self.id = num_villagers

    def createAdult(self):
        """ Advances villager to adulthood.
        Used when populating village for first time with villagers.
        """

    def nourishment(self):
        """ returns nourishment level of villager.
        Based on family's monthly amount of food.
        """

