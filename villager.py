from family import Family
import random


class Villager:
    """ a single villager in Jamestown.
    Villagers are born, age, marry, have children and die.
    Villagers do not remarry if a spouse dies.
    Their main stat is hp.
    """
    birth_hp = 150
    age_labels = ['infant', 'child', 'prime', 'middle', 'old']
    age_groups = [[0, 5], [6, 15], [16, 40], [41, 60], [61, 200]]
    age_hp = [20, 100, 100, -100, -400]
    num_villagers = 0
    req_food = 30
    req_supplies = 40
    genders = ['f', 'm']
    next_gender = 1
    professions = ['farmer', 'craftsman', 'guard']

    # get list of random names
    # from http://listofrandomnames.com/
    file = open('male_names.txt', 'r')
    male_names = file.read().splitlines()
    file.close()
    file = open('female_names.txt', 'r')
    female_names = file.read().splitlines()
    file.close()



    def __init__(self, village, family, manual_gender=None):
        """ Called on birth.
        assign id, get age/label, hp, and stats
        """
        self.village = village
        self.profession = None
        self.village.villagers.append(self)
        self.family = family
        self.house = self.family.house
        self.__class__.num_villagers += 1
        self.id = self.__class__.num_villagers
        self.age_group = 0
        self.age_label = self.__class__.age_labels[self.age_group]

        # get gender and name
        if manual_gender is None:
            self.gender = self.__class__.genders[self.__class__.next_gender]
            self.__class__.next_gender = 1 - self.__class__.next_gender
        else:
        	self.gender = manual_gender
        if self.gender is 'f':
        	self.name = random.choice(self.__class__.female_names)
        else:
        	self.name = random.choice(self.__class__.male_names)

        # villager stats
        self.age = 0
        self.hp = self.__class__.birth_hp
        # req_food only changes at adulthood
        self.req_food = self.__class__.req_food / 2
        # req supplies never changes
        self.req_supples = self.__class__.req_supplies
        self.nourishment = 3

    def __repr__(self):
        return self.name


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
        # adjust hp
        self.hp += self.__class__.age_hp[self.age_group]
        self.hp = 1000 if self.hp > 1000 else self.hp
        # adult only stuff
        if self.age > 16:
            # TODO: update prof sometimes?
            #self.profession = self.village.update_profession(self)
            print "\n{0} is now a {1}".format(self, self.profession)
        	# check for mate if single
            if self.spouse is None:
                self.check_mate()


    def grow_up(self):
        """ upon reaching adulthood males start family and look for mate.
        females go onto Prospects list.
        """
        self.req_food = self.__class__.req_food
        # get profession

        if self.gender == 'm':
            self.family = Family(self)
            self.profession = self.village.new_profession(self)
            self.family.profession = self.profession
            print "\n{0} becomes a {1}".format(self, self.profession)
        elif self.gender == 'f':
            pass
        else: 
        	raise Exception("no gender!")

        self.check_mate()
        return self


    def check_mate(self):  # har har har
        """ grab mate from prospects list, if available
        Called from grow_up and on yearly update when adult is single.
        Villagers do not remarry if spouse dies.
        """
        # women go on prospects list
        if self.gender == 'f':
        	self.village.prospects.append(self)
        elif self.gender == 'm':
            if self.village.prospects:
                self.spouse = self.village.prospects.pop()
                self.spouse.spouse = self
                self.spouse.family = self.family
                self.family.add_mom(self.spouse)
                print "\n%s married %s!" % (self, self.spouse)
            else:
                pass
                print "\n%s found no prospects" % self
        return self


    def force_grow_up(self):
        """ Advances villager to adulthood.
        Used when populating village for first time with villagers.
        """
        while self.age is not 16:
        	self.have_birthday()
        return self


    def give_birth(self):
        """ create new villager and add them to family
        """
        if self.gender is 'f':
            baby = Villager(self.village, self.family)
            return baby
        else:
        	raise Exception("dad can't have a baby!")
        	return None

