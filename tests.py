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
        self.bob = Villager(self.vill, self.fam)

    def test_init(self):
        self.assertEqual(self.bob.age, 0)
        self.assertEqual(self.bob.age_group, 0)
        self.assertEqual(self.bob.age_label, 'infant')
        self.assertTrue(self.vill.villagers)

    def test_birthday(self):
        self.bob.have_birthday()
        self.assertEqual(self.bob.age, 1)
        self.assertEqual(self.bob.age_group, 0)
        self.assertEqual(self.bob.age_label, 'infant')

    def test_force_grow_up(self):
        self.bob.force_grow_up()
        self.assertEqual(self.bob.age, 16)
        self.assertEqual(self.bob.age_group, 2)
        self.assertEqual(self.bob.age_label, 'prime')
        self.assertTrue(self.vill.prospects)

    def test_grow_up(self):
        self.setUp()  # set bob to baby
        while self.bob.age is not 16:
        	self.bob.have_birthday()
        self.assertEqual(self.bob.age, 16)
        self.assertEqual(self.bob.req_food, 30)
        self.assertEqual(self.bob.hp, 1000)
        self.assertTrue(self.vill.prospects)


    def tearDown(self):
        self.vill = None
        self.bob = None
        self.fam = None


class TestFamily(unittest.TestCase):

    def setUp(self):
        self.vill = Village()
        self.fam1 = Family()
        self.fam2 = Family()
        self.bob = Villager(self.vill, self.fam1)
        self.mary = Villager(self.vill, self.fam2)

    def test_init(self):
        self.assertEqual(len(self.vill.villagers), 2)
        self.assertNotEqual(self.fam1, self.fam2)
        self.assertNotEqual(self.bob.family, self.mary.family)

    def test_start_family(self):
        self.bob.force_grow_up()
        self.mary.force_grow_up()  # bob available so they'll get married
        self.family = self.mary.family
        self.assertTrue(self.bob.family)
        self.assertTrue(self.mary.family)
        self.assertEqual(self.mary.family, self.bob.family)

    def test_baby(self):
        self.mary.force_grow_up()
        self.bob.force_grow_up()
        self.family = self.bob.family
        self.baby = self.family.have_baby()
        self.assertEqual(len(self.vill.villagers), 3)
        self.assertEqual(self.mary.family, self.baby.family)
        self.assertEqual(self.bob.family, self.baby.family)

    def tearDown(self):
        self.vill = None
        self.bob = None
        self.mary = None
        self.family = None




if __name__ == '__main__':
	unittest.main()
