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
    num_villagers = 0
    adult_food_req = 30
    req_supplies = 40

    def __init__(self, village):
        """ Called on birth.
        assign id, get age/label, hp, and stats
        """
        self.village = village
        self.__class__.num_villagers += 1
        self.id = self.__class__.num_villagers
        self.age_group = 0
        self.age_label = self.__class__.age_labels[self.age_group]

        # villager stats
        self.hp = self.__class__.birth_hp
        # req_food only changes at adulthood
        self.req_food = self.__class__.adult_food_req / 2
        # req supplies never changes
        self.req_supples = self.__class__.req_supplies
        self.nourishment = 3
        self.age = 0

    def have_birthday(self):
        """ every year, advance villager's age and refresh stats
        """
        self.age += 1
        # update age group and label
        for group in self.__class__.age_groups:
            if self.age_group <= group[1]:  # child or infant
            	self.age_group = self.__class__.age_groups.index(group)
                self.age_label = self.__class__.age_labels[self.age_group]
            else:
                pass
        if self.age == 16:
            self.grow_up()
        self.update_age_label()
        self.monthly_update()

    def grow_up(self):
        """ upon reaching adulthood villagers look for mate to start family with.
        If no mates, they wait.
        """
        self.req_food = self.__class__.adult_food_req
        # check for mate; if none, add self to Prospects list
        if self.village.prospects:
        	spouse = self.village.prospects.pop()
        	self.family = Family(self, spouse)
        else:
        	self.village.prospects.append(self)


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
