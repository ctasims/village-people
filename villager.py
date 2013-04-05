class Villager:
    """ a single villager in Jamestown.
    Villagers are born, age, marry, have children and die.
    Their main stat is hp.
    """
    #required_food = 2000 * 30
    base_hp = 150
    age_labels = ['infant', 'child', 'prime', 'middle', 'old']
    age_groups = [[0, 5], [6, 15], [16, 40], [41, 60], [61, 200]]
    age_hp = [1.5, 8.5, 10, -10, -40]
    num_people = 0
    adult_monthly_food = 30

    def __init__(self, village):
        """ Called on birth.
        """
        self.__class__.num_people += 1
        self.id = self.__class__.num_people
        self.age_group = 0
        self.age_label = self.__class__.age_labels[self.age_group]
        self.hp = self.__class__.base_hp
        self.village = village
        # nourishment: [well, adequate, poor, danger] == [4,3,2,1]
        self.nourishment = 3
        self.age = -1

        # update stats
        self.have_birthday()

    def have_birthday(self):
        """ every year, advance villager's age and refresh stats
        """
        self.age += 1
        if self.age == 16:
            self.grow_up()
        self.update_food_req()
        self.update_age_label()
        self.monthly_update()

    def monthly_update(self):
        self.hp + self.__class__.self.age_hp[self.age_group]


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

    def force_grow_up(self):
        """ Advances villager to adulthood.
        Used when populating village for first time with villagers.
        """
        self.age = 16
        self.hp = 1000
        self.advance_age()
        return self
