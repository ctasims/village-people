
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

    def __init__(self, village, house, dad=None):
        # dad is only None on startup, for initial families
        # house is home of dad's parents. On startup it's just an empty house.
        self.size = 1 if dad else 0
        self.village = village
        self.house = house
        self.dad = dad
        self.output = 100
        self.mom = None
        self.kids = []

        self.food = 0
        self.output = 1

        # on startup, dad will be None
        if dad is None:
        	self.living_with_parents = False
        else:
            self.living_with_parents = True

        self.get_house()
        # set stats
        self.update_stats()


    def __repr__(self):
        return "{0}'s family".format(self.dad)


    def monthly_update(self):
        """
        If family living with dad's parents, checks to build new one.
        """


    def get_members(self):
        if self.size is 0:
        	return []
        else:
        	members = [self.dad, self.mom] + self.kids
        	return filter(None, members)  # get rid of None elements


    def update_stats(self):
        self.compute_size()
        self.compute_reqs()
        self.compute_hp()
        # update max_output based on # parents
        self.max_output = 0
        if self.dad:
        	self.max_output += 100
        if self.mom:
        	self.max_output += 100
        self.update_output()

        return self


    def compute_size(self):
        """ returns number of villagers in family
        Should be called every birth/death
        """
        self.size = len(self.get_members())
        return self.size


    def compute_reqs(self):
        """ Calculates required food and supplies for entire family
        """
        members = self.get_members()
        self.req_food = sum([vill.req_food for vill in members])
        self.req_supplies = sum([vill.req_supplies for vill in members])
        return {'food': self.req_food, 'supplies': self.req_supplies}


    def compute_hp(self):
        """ Calculates total health of family
        """
        self.hp = sum([vill.hp for vill in self.get_members()])
        return self.hp


    def add_mom(self, villager):
        """ add mom to family.
        Called on marriage.
        """
        self.mom = villager
        self.output += 100
        self.update_stats()
        return self


    def parent_died(self, gender):
        if gender is 'f':
        	# mom passed away :(
        	self.mom = None
        	pass
        elif gender is 'm':
            # dad passed away :(
            self.dad = None
        self.update_stats()


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


    def get_groceries(self, total_village_food):
        """
        take family's desired monthly portion of food from village total.
        If not enough, take what's left.
        Return amount of food taken.
        """
        if total_village_food >= self.required_food:
        	self.food = self.required_food
        else:  # not enough food to be well-fed
        	self.food = total_village_food
        return self.food

    
    def get_house(self):
        """
        When family is living with parents of dad, try to get a diff house.
        This requires subtracting supplies from village.
        """
        available_supplies = self.village.supplies
        if available_supplies >= 100:
        	self.house = House()
        	self.village.supplies -= 100
        	self.living_with_parents = False
        else:
        	print "{0} can't get new house!".format(self)



    def update_output(self):
        """
        Output is affected by house, health of villagers
        """
        if self.max_output == 0:
        	print "No family members!"
        	return

        if self.living_with_parents:
        	self.output -= 10

        fam_size = len(self.get_members())
        max_fam_hp = fam_size * 1000
        curr_fam_hp = self.compute_hp()
        self.output *= curr_fam_hp / max_fam_hp

        return self.output

