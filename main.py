from family import Family
from village import Village
from villager import Villager
from house import House

if __name__ == "__main__":
	"""
	THE MAIN FUNCTION!!!

    To initialize the sim we do the following:
    Create village itself. Just one!
    Create 10 homes for our new families.
    Create 10 families, each with:
    -- two parents and 1
    -- 1 child (alternating gender)

	"""
    ga_town = Village()
    num_colonists = 10
    houses = []
    families = []
    #for indx in range(num_colonists):
        #houses[indx] = House()
        #dad_fam = Family(ga_town, houses[indx])
        #dad = Villager



    v1 = Villager(ga_town)
    #v1 = Villager()
    #f1 = Family(v1)
    #h1 = House()
    import pdb; pdb.set_trace()

