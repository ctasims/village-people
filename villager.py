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
    adulthood = 15
    age_groups = [[0, 5], [6, adulthood-1], [adulthood, 40], [41, 60], [61, 200]]
    age_hp = [5, 10, 50, -50, -100]
    req_food = 30
    req_goods = 10
    genders = ['f', 'm']
    next_gender = 1
    professions = ['farmer', 'crafter', 'guard']

    # get list of random names
    # from http://listofrandomnames.com/
    file = open('male_names.txt', 'r')
    male_names = file.read().splitlines()
    file.close()
    file = open('female_names.txt', 'r')
    female_names = file.read().splitlines()
    file.close()



    def __init__(self, village, family=None, manual_gender=None):
        """ Called on birth.
        assign id, get age/label, hp, and stats
        """
        self.village = village
        self.profession = None
        self.family = family
        self.spouse = None
        self.village.num_villagers += 1
        self.id = self.village.num_villagers
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
        # req goods never changes
        self.req_goods = self.__class__.req_goods

        # on startup, create family-less villagers
        if family is None:
            pass

        self.village.villagers.append(self)

    def __repr__(self):
        return self.name


    def monthly_update(self):
        """
        every month villagers get food and update their hp.
        Without food, family will last 2-3 months before dying.
        """
        if self.family.nourishment is "good":
        	self.update_hp(self.age_hp[self.age_group])
        else:
        	self.update_hp(-300)

        # villager dies!
        if self.hp == 0:
            self.die()
            return False

        return True

    def update_hp(self, mod):
        self.hp += mod
        self.hp = 1000 if self.hp > 1000 else self.hp
        self.hp = 0 if self.hp < 0 else self.hp
        return self.hp

    def birthday(self, profession=None):
        """ every year, advance villager's age and refresh stats
        Can set profession manually. Only applies once they grow up.
        Yes, it's a hack...
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
        if self.age == self.adulthood:
            self.grow_up(profession)
        elif self.age > self.adulthood:
        # adult only stuff
            # TODO: update prof sometimes?
            #self.profession = self.village.update_profession(self)
        	# check for mate if single
            if self.spouse is None:
                self.check_mate()


    def die(self):
        """
        You have died!
        Notify your family.
        If male, remove from prof list
        """
        try:
            self.village.villagers.remove(self)
        except:
            pass
        #print "{0} HAS DIED!".format(self)


    def grow_up(self, profession=None):
        """ upon reaching adulthood males start family and look for mate.
        females go onto Prospects list.
        can set profession manually.
        """
        self.req_food = self.__class__.req_food
        # get profession

        if self.gender == 'm':
            self.profession = self.village.new_profession(self, profession)
            if self.family:
                dad_house = self.family.house
                self.family.kids.remove(self)
            else:
                dad_house = None
            self.family = Family(self.village, dad_house, dad=self)
            #print "\n{0} becomes a {1}".format(self, self.profession)
        elif self.gender == 'f':
            if self.family:
                self.family.kids.remove(self)
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
        if self.gender == 'f' and self not in self.village.prospects:
        	self.village.prospects.append(self)
        elif self.gender == 'm':
            if self.village.prospects:
                bride = None
                for girl in self.village.prospects:
                    if girl.family == self.family:  # sister!
                    	continue
                    else:
                    	bride = girl
                    	self.village.prospects.remove(girl)
                    	break
                if bride is None:  # prospects are all sisters
                	return self
                # get married! If woman has children, they tag along
                kids = None
                if bride.family:
                    if bride.family.kids != []:
                        kids = bride.family.kids

                if kids is not None:
                	# add kids to new dad's family and remove from old
                    for kid in kids:
                    	kid.family = self.family
                        self.family.kids.append(kid)
                    bride.family.kids = []
                # clear references...
                if bride.family in self.village.families:
                    self.village.families.remove(bride.family)
                bride.family = None
                bride.family = self.family
                bride.spouse = self
                self.spouse = bride
                self.family.add_mom(self.spouse)
                #print "\n%s married %s!" % (self, self.spouse)
            else:
                pass
                #print "\n%s found no prospects" % self
        return self


    def force_grow_up(self, profession=None):
        """ Advances villager to adulthood.
        Used when populating village for first time with villagers.
        """
        while self.age is not self.adulthood:
        	self.birthday(profession)
        self.hp = 1000
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

