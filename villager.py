from family import Family
import random
import uuid


class Villager:
    """ a single villager in Jamestown.
    Villagers are born, age, marry, have children and die.
    Villagers do not remarry if a spouse dies.
    Their main stat is hp.
    """
    age_labels = ['infant', 'child', 'prime', 'middle', 'old']
    adulthood = 15
    age_groups = [[0, 5], [6, adulthood-1], [adulthood, 40], [41, 60], [61, 200]]
    age_hp = [5, 10, 50, -50, -100]
    req_food = 30
    req_goods = 10
    genders = ['f', 'm']
    next_gender = 1

    # get list of random names, from http://listofrandomnames.com/
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
        self.id = uuid.uuid4()
        # villager stats
        self.age = 0
        self.hp = 150
        self.age_group = 0
        self.age_label = self.__class__.age_labels[self.age_group]
        self.req_food = self.__class__.req_food
        self.req_goods = self.__class__.req_goods

        # villager relations
        self.village = village
        self.village.villagers.append(self)
        self.family = family

        # get gender and name
        if manual_gender is None:
            self.gender = self.__class__.genders[self.__class__.next_gender]
            self.__class__.next_gender = 1 - self.__class__.next_gender
        else:
        	self.gender = manual_gender
        if self.gender is 'f':
        	self.name = random.choice(self.__class__.female_names)
        	self.name = self.name.upper()
        else:
        	self.name = random.choice(self.__class__.male_names)

        # adult stuff, for later
        self.spouse = None


    def __repr__(self):
        return self.name


    def __eq__(self, other):
        """
        check if two villagers are the same
        """
        return self.id == other.id


    def update_hp(self, mod):
        self.hp += mod
        self.hp = 1000 if self.hp > 1000 else self.hp
        self.hp = 0 if self.hp < 0 else self.hp
        return self.hp


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
        else:
            return True


    def birthday(self):
        """
        Every year, advance villager's age and refresh stats
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
            self.grow_up()
        elif self.age > self.adulthood:
        # adult only stuff
            if self.spouse is None:
                self.check_mate()


    def die(self):
        """
        You have died!
        Notify your family.
        If male, remove from prof list
        """
        self.village.remove_villager(self)
        #print "{0} HAS DIED!".format(self)


    def grow_up(self):
        """ upon reaching adulthood males start family and look for mate.
        females go onto Prospects list.
        can set profession manually.
        """
        if self.gender == 'm':
            prior_family = self.family
            self.family = Family(self.village, self.family.house, dad=self)
            prior_family.remove_kid(self)
        elif self.gender == 'f':
            pass

        self.check_mate()
        return self


    def check_mate(self):  # har har har
        """ grab mate from prospects list, if available
        Called from grow_up and on yearly update when adult is single.
        Villagers do not remarry if spouse dies.
        Single women go on prospects list.
        Single men search prospects list for mate.
        If one available, she and her kids join his family.
        """
        # WOMAN
        if self.gender == 'f' and self not in self.village.prospects:
        	self.village.prospects.append(self)

        # MAN 
        elif self.gender == 'm':
            if not self.village.prospects:
            	return self
            else:  # get married
                bride = self.village.prospects.pop()
                prior_family = bride.family
                self.family.add_mom(bride)
                if bride is not prior_family.mom:  # just a kid growing up
                	prior_family.remove_kid(bride)
                else:  # she's a widow. Get kids, if any.
                    #import pdb; pdb.set_trace()
                    #if bride.family.kids:
                        #for kid in bride.family.kids:
                            #self.family.kids.append(kid)
                            ##kid.family = self.family
                        #for kid in self.family:
                            #kid.family = self.family
                        #bride.family.kids = []
                    prior_family.mom = None
                prior_family.update_stats()
                bride.family.update_stats()


    def force_grow_up(self):
        """ Advances villager to adulthood.
        Used when populating village for first time with villagers.
        """
        while self.age is not self.adulthood:
        	self.birthday()
        self.hp = 1000
        return self


    def give_birth(self):
        """ create new villager and add them to family
        """
        baby = Villager(self.village, self.family)
        return baby

