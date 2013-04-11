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
        self.fam = Family()
        self.dad = Villager(self.vill, self.fam, 'm')
        self.mom = Villager(self.vill, self.fam, 'f')

    def test_init(self):
        self.assertEqual(self.dad.age, 0)
        self.assertEqual(self.dad.age_group, 0)
        self.assertEqual(self.dad.age_label, 'infant')
        self.assertTrue(self.vill.villagers)

    def test_birthday(self):
        self.dad.have_birthday()
        self.assertEqual(self.dad.age, 1)
        self.assertEqual(self.dad.age_group, 0)
        self.assertEqual(self.dad.age_label, 'infant')

    def test_force_grow_up_male(self):
        self.dad.force_grow_up()
        self.assertEqual(self.dad.age, 16)
        self.assertEqual(self.dad.age_group, 2)
        self.assertEqual(self.dad.age_label, 'prime')
        self.assertFalse(self.vill.prospects)

    def test_force_grow_up_female(self):
        self.mom.force_grow_up()
        self.assertEqual(self.mom.age, 16)
        self.assertEqual(self.mom.age_group, 2)
        self.assertEqual(self.mom.age_label, 'prime')
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
        self.fam = None


class TestFamily(unittest.TestCase):

    def setUp(self):
        self.vill = Village()
        self.fam1 = Family()
        self.fam2 = Family()
        self.dad = Villager(self.vill, self.fam1, 'm')
        self.mom = Villager(self.vill, self.fam2, 'f')

    def test_init(self):
        self.assertEqual(len(self.vill.villagers), 2)
        self.assertNotEqual(self.fam1, self.fam2)
        self.assertNotEqual(self.dad.family, self.mom.family)

    def test_start_family(self):
        self.mom.force_grow_up()
        self.dad.force_grow_up()  # mom available
        self.assertTrue(self.dad.family)
        self.assertTrue(self.mom.family)
        self.assertEqual(self.mom.family, self.dad.family)

    def test_baby(self):
        self.mom.force_grow_up()
        self.dad.force_grow_up()
        self.baby = self.dad.family.have_baby()
        self.assertEqual(len(self.vill.villagers), 3)
        self.assertEqual(self.mom.family, self.baby.family)
        self.assertEqual(self.dad.family, self.baby.family)

    def tearDown(self):
        self.vill = None
        self.dad = None
        self.mom = None
        self.family = None


if __name__ == '__main__':
	unittest.main()

