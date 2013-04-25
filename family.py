from house import House
import random
import uuid


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
        # first, family stats/data
        self.id = uuid.uuid4()
        self.village = village
        self.village.families.append(self)
        self.house = house
        self.hp = 100
        self.nourishment = "good"
        self.preparedness = "good"
        self.members = []
        self.food = 0
        self.output = 50
        # villager attrs
        self.vgr_req_food = 30
        self.vgr_req_goods = 10

        # relations
        self.mom = None
        self.dad = dad
        self.kids = []


        #self.new_prof_rate = 0.30

        # on startup, profession manually assigned
        if profession is not None:
            self.living_with_parents = False
            self.profession = profession
        else:
            self.living_with_parents = True
            self.profession = self.village.new_profession()
        self.village.prof_list[self.profession].append(self)

        self.update_stats(True)


    def __repr__(self):
        if self.dad:
        	label = "{0} ({1})".format(self.dad, self.size)
        elif self.mom:
        	label = "{0} ({1})".format(self.mom, self.size)
        else:
        	label = "KIDS ({1})".format(self.mom, self.size)
        return label

    def __eq__(self, other):
        """
        check if two families are the same
        """
        return self.id == other.id


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
        print "%-14.14s hp: %6d %6s %6s" % (self, self.hp, food,craft)


    def yearly_update(self):
        if self.dad:
            self.dad.birthday()
        if self.mom:
            self.mom.birthday()
        for kid in self.kids:
            kid.birthday()
        if len(self.kids) < 8:
            self.check_for_baby(self.village.baby_rate)
        # check if we need to change professions
        #if random.random() < self.new_prof_rate:
            #prof = self.profession
            #self.village.prof_list[prof].remove(self)
            #self.profession = self.village.update_profession()
            #self.village.prof_list[self.profession].append(self)


    def monthly_update(self, show_status=False):
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
            self.nourishment = "good"
            self.village.food -= self.req_food
        else:  # not enough food to be well-fed
            self.nourishment = "poor"
            self.village.food = 0

        # get goods
        if self.village.goods >= self.req_goods:
            self.preparedness = "good"
            self.village.goods -= self.req_goods
        else:  # not enough goods for max output
            self.preparedness = "poor"
            self.village.goods = 0

        # villager update
        losses = []
        self.hp = 0
        for member in self.members:
            if self.nourishment is "good":
                mod =  member.age_hp[member.age_group]
            else:
                mod = -300
            member.hp += mod
            member.hp = 1000 if member.hp > 1000 else member.hp
            self.hp += member.hp

            # villager dies!
            if member.hp < 0:
            	losses.append(member)

        for dead in losses:
            dead.die()
        # Also handle deaths
        #if self.dad:
            #dad_status = self.dad.monthly_update()
        #if self.mom:
            #mom_status = self.mom.monthly_update()

        #losses = []
        #for kid in self.kids:
            #status = kid.monthly_update()
            #if not status:
            	# kid died!
                #losses.append(kid)
        #for kid in losses:
            #self.remove_kid(kid)

        # update family output
        if self.profession == 'farmer':
            self.village.food += self.output
        elif self.profession == 'crafter':
            self.village.goods += self.output
        elif self.profession == 'guard':
            pass

        if show_status:
            self.print_status()

        return True


    def update_stats(self, initial=False):
        """
        Update all stats of family to ensure everything jives.
        Compile family members and store them.
        Compile family members to get size of family.
        Updates members, required stuff, output, max_output
        """
        # update family size and member info
        self.members = []
        if self.dad:
        	self.members = [self.dad]
        if self.mom:
        	self.members += [self.mom]
        if self.kids:
        	self.members += self.kids

        self.size = len(self.members)
        if not self.members and not initial:
        	self.village.remove_family(self)
        	return False

        self.req_food = self.vgr_req_food * self.size
        self.req_goods = self.vgr_req_goods * self.size
        #self.hp = sum([vgr.hp for vgr in self.members])

        # update profession details
        self.max_output = self.village.max_outputs[self.profession]
        self.output = self.update_output()


    def remove_kid(self, kid):
        if kid in self.kids:
        	self.kids.remove(kid)
        #self.update_stats()
        return self


    def set_profession(self, prof):
        self.profession = prof
        self.village.prof_list[prof].append(self)
        self.output = self.village.max_outputs[prof]
        self.max_output = self.village.max_outputs[prof]
        self.update_stats()


    def add_mom(self, mom):
        """
        Add mom to family.
        Called on marriage.
        """
        #prior_family = mom.family
        self.mom = mom
        mom.family = self
        #prior_family.update_stats()  # this should delete fam if it's empty
        if self.dad:
        	self.dad.spouse = self.mom
        	self.mom.spouse = self.dad
        self.update_stats()
        return self

    def add_dad(self, dad):
        prior_family = dad.family
        self.dad = dad
        dad.family = self
        prior_family.update_stats()  # this should delete fam if it's empty
        if self.mom:
        	self.dad.spouse = self.mom
        	self.mom.spouse = self.dad
        self.update_stats()

    def add_kid(self, kid):
        """
        Used when initializing populace
        """
        self.kids.append(kid)
        self.update_stats()

    def check_for_baby(self, chance):
        """ have a new baby in family.
        Called by ???
        """
        if random.random() < chance:
            if self.mom and self.mom.age <= 60:
                baby = self.mom.give_birth()
                self.kids.append(baby)
                self.update_stats()
                return baby
        return self


    def get_house(self):
        """
        When family is living with parents of dad, try to get a diff house.
        This requires subtracting goods from village.
        """
        if self.village.goods >= 100:
            if self.village.empty_houses:
                self.house = self.village.empty_houses.pop()
            else:
                self.house = House()
                self.village.goods -= 100
            self.living_with_parents = False


    def update_output(self):
        """
        Output is affected by house, health of villagers.
        Update output every month.
        With no goods, family will last for 1 year.
        """
        if self.profession == 'guard':
        	return 0
        if self.size == 0:
        	return 0

        max_out = self.max_output

        # living at home means lower productivity
        if self.living_with_parents:
            self.output -= max_out * 0.05
        else:
        	pass

        # adjust for going over max or below min
        self.output = max_out if self.output > max_out else self.output
        self.output = 0 if self.output < 0 else self.output

        # check family preparedness
        if self.preparedness is "good":
            self.output += max_out * 0.10
        else:
            self.output -= max_out * 0.05
        # adjust for going over max or below min
        self.output = max_out if self.output > max_out else self.output
        self.output = 0 if self.output < 0 else self.output

        max_fam_hp = self.size * 1000
        curr_fam_hp = float(self.hp)
        hp_ratio = curr_fam_hp / max_fam_hp
        if 0.5 < hp_ratio <= 1:
        	pass
        elif 0.25 < hp_ratio <= 0.5:
            self.output -= max_out * 0.05
        else:
        	self.output -= max_out * 0.10
        # adjust for going over max or below min
        self.output = max_out if self.output > max_out else self.output
        self.output = 0 if self.output < 0 else self.output

        return round(self.output)

