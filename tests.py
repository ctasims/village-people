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


class TestVillager(unittest.TestCase):

    def setUp(self):
        self.vill = Village()
        self.bob = villager(vill)

    def test_init(self):
        self.assertEqual(self.bob.age, 0)
        self.assertEqual(self.bob.age_group, 0)
        self.assertEqual(self.bob.age_label, 'infant')
        self.assertTrue(ppl in vill.villagers)

    def test_birthday(self):
        self.bob.have_birthday()
        self.assertEqual(self.age, 1)
        self.assertEqual(self.age_group, 0)
        self.assertEqual(self.age_label, 'infant')

    def test_force_grow_up(self):
        self.bob.force_grow_up()
        self.assertEqual(self.bob.age, 16)
        self.assertEqual(self.bob.age_group, 2)
        self.assertEqual(self.bob.age_label, 'prime')




if __name__ == '__main__':
	unittest.main()
