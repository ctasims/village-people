from family import Family
from village import Village
from villager import Villager
from house import House
import unittest

class TestVillage(unittest.TestCase):

    def setUp(self):
        self.vill = Village()

    def test_init(self):
        self.assertEqual(len(self.vill.villagers), 0)

    def tearDown(self):
        self.vill = None

class TestVillager(unittest.TestCase):

    def setUp(self):
        self.vill = Village()
        self.dad = Villager(self.vill, None, 'm')
        self.mom = Villager(self.vill, None, 'f')

    def test_init(self):
        self.assertEqual(self.dad.age, 0)
        self.assertEqual(self.dad.age_group, 0)
        self.assertEqual(self.dad.age_label, 'infant')
        self.assertEqual(self.dad.nourishment, 3)
        self.assertTrue(self.vill.villagers)
        self.assertEqual(self.dad.req_food, 15)

    def test_one_birthday(self):
        self.dad.have_birthday()
        self.assertEqual(self.dad.age, 1)
        self.assertEqual(self.dad.age_group, 0)
        self.assertEqual(self.dad.age_label, 'infant')
        self.assertEqual(self.dad.req_food, 15)

    def test_grow_to_child(self):
        for x in range(6):
            self.dad.have_birthday()
        self.assertEqual(self.dad.age, 6)
        self.assertEqual(self.dad.age_group, 1)
        self.assertEqual(self.dad.nourishment, 3)
        self.assertEqual(self.dad.age_label, 'child')
        self.assertEqual(self.dad.req_food, 15)

    def test_grow_to_prime(self):
        for x in range(16):
            self.dad.have_birthday()
        self.assertEqual(self.dad.age, 16)
        self.assertEqual(self.dad.age_group, 2)
        self.assertEqual(self.dad.nourishment, 3)
        self.assertEqual(self.dad.age_label, 'prime')
        self.assertEqual(self.dad.req_food, 30)
        # villager will have house built from village goods
        self.assertFalse(self.dad.family.house == None)

    def test_grow_to_middle_age(self):
        for x in range(41):
            self.dad.have_birthday()
        self.assertEqual(self.dad.age, 41)
        self.assertEqual(self.dad.age_group, 3)
        self.assertEqual(self.dad.nourishment, 3)
        self.assertEqual(self.dad.age_label, 'middle')
        self.assertEqual(self.dad.req_food, 30)

    def test_grow_to_old_age(self):
        for x in range(61):
            self.dad.have_birthday()
        self.assertEqual(self.dad.age, 61)
        self.assertEqual(self.dad.age_group, 4)
        self.assertEqual(self.dad.nourishment, 3)
        self.assertEqual(self.dad.age_label, 'old')
        self.assertEqual(self.dad.req_food, 30)

    def test_force_grow_up_male(self):
        self.dad.force_grow_up()
        self.assertEqual(self.dad.age, 16)
        self.assertEqual(self.dad.age_group, 2)
        self.assertEqual(self.dad.age_label, 'prime')
        self.assertEqual(self.dad.req_food, 30)
        self.assertEqual(self.dad.hp, 1000)
        self.assertFalse(self.vill.prospects)

    def test_force_grow_up_female(self):
        self.mom.force_grow_up()
        self.assertEqual(self.mom.age, 16)
        self.assertEqual(self.mom.age_group, 2)
        self.assertEqual(self.mom.age_label, 'prime')
        self.assertEqual(self.mom.req_food, 30)
        self.assertEqual(self.mom.hp, 1000)
        self.assertTrue(self.vill.prospects)

    def test_grow_up_male(self):
        self.setUp()  # set dad to baby
        while self.dad.age is not 16:
        	self.dad.have_birthday()
        self.assertEqual(self.dad.age, 16)
        self.assertEqual(self.dad.req_food, 30)
        self.assertEqual(self.dad.hp, 1000)
        self.assertFalse(self.vill.prospects)

    def test_grow_up_female(self):
        self.setUp()  # set dad to baby
        while self.mom.age is not 16:
        	self.mom.have_birthday()
        self.assertEqual(self.mom.age, 16)
        self.assertEqual(self.mom.req_food, 30)
        self.assertEqual(self.mom.hp, 1000)
        self.assertTrue(self.vill.prospects)


    def tearDown(self):
        self.vill = None
        self.dad = None
        self.mom = None


class TestFamily(unittest.TestCase):

    def setUp(self):
        self.vill = Village()
        # need empty parent families. Once people come of age, these are empty.
        self.dad = Villager(self.vill, None, 'm')
        self.mom = Villager(self.vill, None, 'f')
        self.mom.force_grow_up()
        self.dad.force_grow_up()  # mom available

    def test_init(self):
        self.assertEqual(len(self.vill.villagers), 2)

    def test_start_family(self):
        self.assertTrue(self.dad.family)
        self.assertTrue(self.mom.family)
        self.assertEqual(self.mom.family, self.dad.family)

    def test_get_members(self):
        members = self.dad.family.get_members()
        self.assertEqual(members, [self.dad, self.mom])

    def test_update_stats(self):
        self.dad.family.update_stats()
        self.assertEqual(self.dad.family.size, 2)
        self.assertEqual(self.dad.family.req_food, 60)
        self.assertEqual(self.dad.family.req_goods, 80)
        self.assertEqual(self.dad.family.size, 2)

    def test_compute_hp(self):
        self.dad.family.compute_hp()
        self.assertEqual(self.dad.family.hp, 2000)

    def test_add_mom(self):
        pass

    def test_have_baby(self):
        self.mom.force_grow_up()
        self.dad.force_grow_up()
        self.baby = self.dad.family.have_baby()
        self.assertEqual(len(self.vill.villagers), 3)
        self.assertEqual(self.mom.family, self.baby.family)
        self.assertEqual(self.dad.family, self.baby.family)

    def test_get_groceries(self):
        pass
    def test_compute_output(self):
        pass

    def tearDown(self):
        self.vill = None
        self.dad = None
        self.mom = None


if __name__ == '__main__':
	unittest.main()

