from house import House


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
    self.max_solo_outputs = {'farmer': 60, 'crafter': 20}

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
        self.kids = []

        self.food = 0

        # on startup, profession manually assigned
        if profession is not None:
            self.living_with_parents = False
            self.profession = profession
        else:
            self.profession = self.dad.profession
            self.living_with_parents = True
        self.output = self.__class__.max_solo_outputs[self.profession]
        # increase output base amt
        self.__class__.max_solo_outputs[self.profession] *= 1.25


        self.get_house()
        # set stats
        self.update_stats()


    def __repr__(self):
        return "{0}".format(self.dad)


    def yearly_update(self):
        pass

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
            self.food = self.req_food
            self.nourishment = "good"
            self.village.food -= self.req_food
        else:  # not enough food to be well-fed
            self.food = self.village.food
            self.nourishment = "poor"
            self.village.food = 0

        # get goods
        if self.village.goods >= self.req_goods:
            self.goods = self.req_goods
            self.preparedness = "good"
            self.village.goods -= self.req_goods
        else:  # not enough goods for max output
            self.goods = self.village.goods
            self.preparedness = "poor"
            self.village.goods = 0

        # villager update
        # Also handle deaths
        dad_status = self.dad.monthly_update()
        if not dad_status:
            # dad died!
            self.dad = None
            self.__class__.max_solo_outputs[self.profession] *= 0.75
            self.update_stats()

        mom_status = self.mom.monthly_update()
        if not mom_status:
            # mom died!
            self.mom = None
            self.__class__.max_solo_outputs[self.profession] *= 0.75
            self.update_stats()

        removal_indexes = []  # if child dies, need this to later remove them
        for kid in self.kids:
            status = kid.monthly_update()
            if not status:
            	# kid died!
            	removal_indexes.append(self.kids.index(kid))
        for indx in removal_indexes:
        	self.kids.remove(self.kids[indx])
        self.kids = filter(None, self.kids)
        self.update_stats()

        # if whole family dies off...
        if self.size == 0:
        	self.village.families.remove(self)
            # if we had a home, make it empty
            if not self.lives_with_parents:
                self.village.empty_houses.append(self.house)
        	return False

        # update family output
        output = self.update_output()
        if self.profession == 'farmer':
            self.village.food += output
        elif self.profession == 'crafter':
            self.village.goods += output

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
        self.max_solo_output = self.__class__.max_solo_outputs[self.profession]
        if self.dad:
            self.max_output += self.max_solo_output
        if self.mom:
            self.max_output += self.max_solo_output
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
        self.__class__.max_solo_outputs[self.profession] *= 1.25
        self.update_stats()
        return self


    #def parent_died(self, gender):
        #if gender is 'f':
            ## mom passed away :(
            #self.mom = None
            #pass
        #elif gender is 'm':
            ## dad passed away :(
            #self.dad = None
            #self.update_stats()


    def have_baby(self):
        """ have a new baby in family.
        Called by ???
        """
        if self.mom:
            baby = self.mom.give_birth()
            self.kids.append(baby)
            self.update_stats()
            return baby
        else:
            print "family %s can't have kids - no mom!" % self


    def get_house(self):
        """
        When family is living with parents of dad, try to get a diff house.
        This requires subtracting goods from village.
        """
        # first see if there is empty house
        if self.village.empty_houses:
            self.house = self.village.empty_houses.pop()
            self.living_with_parents = False
            print "{0} found an empty house!".format(self)
            return

        available_goods = self.village.goods
        if available_goods >= 100:
            self.house = House()
            self.village.goods -= 100
            self.living_with_parents = False
        else:
            print "{0} can't get new house!".format(self)
        return


    def print_status(self):
        if self.profession == 'crafter':
        	food = "-"
        	craft = self.output
        else:
        	food = self.output
        	craft = "-"

        print "%-10.10s hp: %6d %6s %6s" % (self, self.compute_hp(), food,
                craft)


    def update_output(self):
        """
        Output is affected by house, health of villagers.
        Update output every month.
        With no goods, family will last for 1 year.
        """
        max_o = self.max_output
        max_solo = self.max_solo_output
        if max_o == 0:
            print "No family members!"
            return

        fam_size = len(self.members)
        max_fam_hp = fam_size * 1000
        curr_fam_hp = float(self.compute_hp())
        hp_ratio = curr_fam_hp / max_fam_hp

        # living at home means lower productivity
        if self.living_with_parents:
            self.output -= max_solo * 0.20
        else:
        	pass

        # adjust for going over max or below min
        self.output = max_o if self.output > max_o else self.output
        self.output = 0 if self.output < 0 else self.output

        # check family preparedness
        if self.preparedness is "good":
            self.output += max_solo * 0.10
        else:
            self.output -= max_solo * 0.20
        # adjust for going over max or below min
        self.output = max_o if self.output > max_o else self.output
        self.output = 0 if self.output < 0 else self.output

        if 0.5 < hp_ratio <= 1:
        	pass
        elif 0.25 < hp_ratio <= 0.5:
            self.output -= max_solo * 0.20
        else:
        	self.output -= max_solo * 0.50
        # adjust for going over max or below min
        self.output = max_o if self.output > max_o else self.output
        self.output = 0 if self.output < 0 else self.output

        return self.output

