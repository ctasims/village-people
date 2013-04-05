class Villager:
    """ a single villager in Jamestown.
    Villagers are born, age, marry, have children and die.
    Their main stat is hp.
    """
    #required_food = 2000 * 30
    birth_hp = 150
    age_labels = ['infant', 'child', 'prime', 'middle', 'old']
    age_groups = [[0, 5], [6, 15], [16, 40], [41, 60], [61, 200]]
    age_hp = [1.5, 8.5, 10, -10, -40]
    num_people = 0
    adult_food_req = 30
    adult_supply_req = 40
    genders = ('m', 'f')
    next_gender = 0

    def __init__(self, village):
        """ Called on birth.
        assign id, get age/label, hp, and stats
        """
        self.village = village
        self.__class__.num_people += 1
        self.id = self.__class__.num_people
        self.age_group = 0
        self.age_label = self.__class__.age_labels[self.age_group]

        # assign gender and toggle so alternate between m/f
        self.gender = self.__class__.genders[self.__class__.next_gender]
        self.__class__.next_gender = 1 - self.__class__.next_gender

        # villager stats
        self.hp = self.__class__.birth_hp
        self.food_req = self.__class__.adult_food_req / 2
        self.supplies_req = self.__class__.adult_supply_req
        self.nourishment = 3
        self.age = 0

    def have_birthday(self):
        """ every year, advance villager's age and refresh stats
        """
        self.age += 1
        # update age group and label
        for group in self.__class__.age_groups:
            if self.age_group <= group[1]:
            	self.age_group = self.__class__.age_groups.index(group)
                self.age_label = self.__class__.age_labels[self.age_group]
            else:
                pass
        if self.age == 16:
            self.grow_up()
        self.update_age_label()
        self.monthly_update()

    def grow_up(self):
        """ upon reaching adulthood women become available for marriage and 
        men start their own family (with only them in it)
        """
        self.food_req = self.__class__.adult_food_req
        # guys start family; girls become available for marriage
        if self.gender = 'm':
        	self.family = Family(self)
        elif self.gender = 'f':
        	self.village.prospects += self
        else:
        	raise Exception("Growing pains!")


    def monthly_update(self):
        self.hp + self.__class__.self.age_hp[self.age_group]


    def force_grow_up(self):
        """ Advances villager to adulthood.
        Used when populating village for first time with villagers.
        """
        self.age = 16
        self.hp = 1000
        self.advance_age()
        return self
