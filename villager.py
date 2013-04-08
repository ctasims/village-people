from family import Family


class Villager:
    """ a single villager in Jamestown.
    Villagers are born, age, marry, have children and die.
    Their main stat is hp.
    """
    birth_hp = 150
    age_labels = ['infant', 'child', 'prime', 'middle', 'old']
    age_groups = [[0, 5], [6, 15], [16, 40], [41, 60], [61, 200]]
    age_hp = [20, 100, 100, -100, -400]
    num_villagers = 0
    req_food = 30
    req_supplies = 40

    def __init__(self, village):
        """ Called on birth.
        assign id, get age/label, hp, and stats
        """
        self.village = village
        self.village.villagers.append(self)
        self.family = None
        self.__class__.num_villagers += 1
        self.id = self.__class__.num_villagers
        self.age_group = 0
        self.age_label = self.__class__.age_labels[self.age_group]

        # villager stats
        self.age = 0
        self.hp = self.__class__.birth_hp
        # req_food only changes at adulthood
        self.req_food = self.__class__.req_food / 2
        # req supplies never changes
        self.req_supples = self.__class__.req_supplies
        self.nourishment = 3

    def have_birthday(self):
        """ every year, advance villager's age and refresh stats
        """
        self.age += 1
        # update age group and label
        for group in self.__class__.age_groups:
            if self.age <= group[1]:  # child or infant
            	self.age_group = self.__class__.age_groups.index(group)
                self.age_label = self.__class__.age_labels[self.age_group]
                break
            else:
                pass
        if self.age == 16:
            self.grow_up()
        self.hp += self.__class__.age_hp[self.age_group]
        self.hp = 1000 if self.hp > 1000 else self.hp

    def grow_up(self):
        """ upon reaching adulthood villagers look for mate to start family with.
        If no mates, they wait.
        """
        self.req_food = self.__class__.req_food
        # check for mate; if none, add self to Prospects list
        if self.village.prospects:
        	spouse = self.village.prospects.pop()
        	self.family = Family(self, spouse)
        	spouse.family = self.family
        else:
        	self.village.prospects.append(self)

    def force_grow_up(self):
        """ Advances villager to adulthood.
        Used when populating village for first time with villagers.
        """
        while self.age is not 16:
        	self.have_birthday()
        return self
