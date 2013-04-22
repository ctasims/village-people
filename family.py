from house import House
import random


class Family:
    """ A family of villagers.
    Families are created when a villager grows up and marries another from the prospect list.

    The profession output is determined on a family-by-family basis.
    Output is on scale of 1 to 200.
    If only 1 parent, max is 100.
    Output is affected by things like:
    -- # family members
    -- if family living with dad's parents
    -- health of family members
    """

    def __init__(self, village, house, dad, profession=None):
        # dad is only None on startup, for initial families
        # dad is the dad of THIS family, i.e. the main man
        # house is home of dad's parents. On startup it's just an empty house.
        self.size = 1 if dad else 0
        self.village = village
        self.house = house
        self.output = None  # depends on profession
        self.mom = None
        self.dad = dad
        #self.chance_of_baby = self.village.baby_rate
        self.nourishment = "good"
        self.kids = []

        self.food = 0

        self.new_prof_rate = 0.01
        # on startup, profession manually assigned
        if profession is not None:
            self.living_with_parents = False
            self.profession = profession
        else:
            self.profession = self.dad.profession
            # add family to prof list
            self.living_with_parents = True
        self.village.prof_list[self.profession].append(self)
        self.output = self.village.max_solo_outputs[self.profession]
        # increase output base amt
        self.village.max_solo_outputs[self.profession] = round(self.village.max_solo_outputs[self.profession] * 1.1)


        self.get_house()
        # set stats
        self.update_stats()


    def __repr__(self):
        return "{0} ({1})".format(self.dad, self.size)

    def print_status(self):
        if self.profession == 'crafter':
        	food = "-"
        	craft = self.output
        elif self.profession == 'farmer':
        	food = self.output
        	craft = "-"
        else:  # guard
        	food = "-"
        	craft = "g"
        #print "%-14.14s hp: %6d %6s %6s" % (self, self.compute_hp(), food,craft)


    def yearly_update(self):
        if self.dad:
            self.dad.birthday()
        if self.mom:
            self.mom.birthday()
        for kid in self.kids:
            kid.birthday()
        self.check_for_baby(self.village.baby_rate)
        # check if we need to change professions
        if random.random() < self.new_prof_rate:
            prof = self.profession
            self.village.prof_list[prof].remove(self)
            self.profession = self.village.update_profession()
            self.village.prof_list[self.profession].append(self)



    def monthly_update(self):
        """
        update stats.
        update output.
        get output and add to village stores, based on prof.
        get required food and goods.
        get house if family doesn't have its own.
        """
        self.update_stats()

        if self.living_with_parents:
            self.get_house()

        # get food
        if self.village.food >= self.req_food:
            #self.food = self.req_food
            self.nourishment = "good"
            self.village.food -= self.req_food
        else:  # not enough food to be well-fed
            #self.food = self.village.food
            self.nourishment = "poor"
            self.village.food = 0

        # get goods
        if self.village.goods >= self.req_goods:
            #self.goods = self.req_goods
            self.preparedness = "good"
            self.village.goods -= self.req_goods
        else:  # not enough goods for max output
            #self.goods = self.village.goods
            self.preparedness = "poor"
            self.village.goods = 0

        # villager update
        # Also handle deaths
        if self.dad:
            dad_status = self.dad.monthly_update()
        else:
        	dad_status = None
        if not dad_status:
            # dad died!
            self.dad = None
            prof = self.profession
            self.village.max_solo_outputs[prof] = round(self.village.max_solo_outputs[prof] * 0.95)
            self.update_stats()

        if self.mom:
            mom_status = self.mom.monthly_update()
        else:
        	mom_status = None
        if not mom_status:
            # mom died!
            self.mom = None
            prof = self.profession
            self.village.max_solo_outputs[prof] = round(self.village.max_solo_outputs[prof] * 0.98)
            self.update_stats()

        removal_indexes = []  # if child dies, need this to later remove them
        for kid in self.kids:
            status = kid.monthly_update()
            if not status:
            	# kid died!
            	removal_indexes.append(self.kids.index(kid))
        for indx in removal_indexes:
        	self.kids[indx] = None
        self.kids = filter(None, self.kids)
        self.update_stats()

        # if whole family dies off...
        if self.size == 0:
            prof = self.profession
            self.village.families.remove(self)
            self.village.prof_list[prof].remove(self)
            self.village.families = filter(None, self.village.families)

            if self.house:
                self.village.empty_houses.append(self.house)

        	return False

        # update family output
        output = self.update_output()
        if self.profession == 'farmer':
            self.village.food += output
        elif self.profession == 'crafter':
            self.village.goods += output
        elif self.profession == 'guard':
            pass

        self.print_status()
        return True


    def update_stats(self):
        """
        Update all stats of family to ensure everything jives.
        Updates members, required stuff, output, max_output
        """
        members = self.get_members()  # update members
        self.req_food = sum([vill.req_food for vill in members])
        self.req_goods = sum([vill.req_goods for vill in members])
        # update max_output based on # parents
        self.max_output = 0
        self.max_solo_output = self.village.max_solo_outputs[self.profession]
        if self.dad:
            self.max_output += self.max_solo_output
        if self.mom:
            self.max_output += self.max_solo_output
        if self.kids:
        	self.max_output += len(self.kids) * self.max_solo_output
        #self.output = self.max_output
        self.compute_hp()


    def get_members(self):
        """
        Determine family members and size of family.
        Should be called on every birth/death/new parent
        """
        members = []
        members = [self.dad, self.mom] + self.kids
        members = filter(None, members)  # get rid of None elements
        if not members:
            self.size = 0
        else:
            self.size = len(members)
        self.members = members
        return self.members


    def compute_hp(self):
        """ Calculates total health of family
        """
        self.hp = sum([vill.hp for vill in self.members])
        return self.hp


    def add_mom(self, villager):
        """ add mom to family.
        Called on marriage.
        """
        self.mom = villager
        self.output += self.max_solo_output
        prof = self.profession
        self.village.max_solo_outputs[prof] = round(self.village.max_solo_outputs[prof] * 1.1)
        self.update_stats()
        return self


    def check_for_baby(self, chance):
        """ have a new baby in family.
        Called by ???
        """
        if random.random() < chance:
            if self.mom:
                baby = self.mom.give_birth()
                self.kids.append(baby)
                self.update_stats()
                #print "{0} HAD A BABY!!".format(self)
                return baby
            else:
            	pass
                #print "family %s can't have kids - no mom!" % self
        else:
        	pass


    def get_house(self):
        """
        When family is living with parents of dad, try to get a diff house.
        This requires subtracting goods from village.
        """
        # first see if there is empty house
        if self.village.empty_houses:
            self.house = self.village.empty_houses.pop()
            self.living_with_parents = False
            #print "{0} found an empty house!".format(self)
            return

        available_goods = self.village.goods
        if available_goods >= 100:
            self.house = House()
            self.village.goods -= 100
            self.living_with_parents = False
        else:
        	pass
            #print "{0} can't get new house!".format(self)
        return


    def update_output(self):
        """
        Output is affected by house, health of villagers.
        Update output every month.
        With no goods, family will last for 1 year.
        """
        if self.profession == 'guard':
        	return 0
        max_o = self.max_output

        max_solo = self.max_solo_output
        if max_o == 0:
            #print "No family members!"
            return

        fam_size = self.size
        max_fam_hp = fam_size * 1000
        curr_fam_hp = float(self.compute_hp())
        hp_ratio = curr_fam_hp / max_fam_hp

        # living at home means lower productivity
        if self.living_with_parents:
            self.output -= max_solo * 0.01
        else:
        	pass

        # adjust for going over max or below min
        self.output = max_o if self.output > max_o else self.output
        self.output = 0 if self.output < 0 else self.output

        # check family preparedness
        if self.preparedness is "good":
            self.output += max_solo * 0.10
        else:
            self.output -= max_solo * 0.10
        # adjust for going over max or below min
        self.output = max_o if self.output > max_o else self.output
        self.output = 0 if self.output < 0 else self.output

        if 0.5 < hp_ratio <= 1:
        	pass
        elif 0.25 < hp_ratio <= 0.5:
            self.output -= max_solo * 0.10
        else:
        	self.output -= max_solo * 0.15
        # adjust for going over max or below min
        self.output = max_o if self.output > max_o else self.output
        self.output = 0 if self.output < 0 else self.output

        # family can only produce so much. We'll cap max output
        max_fam_output = self.village.max_fam_outputs[self.profession]
        if self.output > max_fam_output:
            self.output = max_fam_output

        return round(self.output)

