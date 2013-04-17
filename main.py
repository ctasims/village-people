from family import Family
from village import Village
from villager import Villager
from house import House


def create_initial_populace(village, num_families, professions):
    """
    Create men and women; they'll be children.
    Create families for each. THEN force grow them up.
    Women first, so they get added to prospects.
    """

    colonist_men = []
    colonist_women = []
    for indx in range(num_families):
        new_woman = Villager(village, None, 'f')
        new_woman.force_grow_up()
    for indx, prof in zip(range(num_families), professions):
        new_man = Villager(village, None, 'm')
        new_man.force_grow_up(prof)

    # They should all be married now
    # professions are random

    # start with 1 kid each
    for family in village.families:
        family.check_for_baby(1)

    # should have 30 people total, now

    return True



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
    vill = Village()
    vill.food = 1000
    vill.goods = 1000
    # create 10 empty houses
    houses = [House() for x in range(10)]
    vill.empty_houses = houses
    # create families
    c = 'crafter'
    f = 'farmer'
    g = 'guard'
    num_families = 2
    professions = [f, c]
    print "\n\n"
    create_initial_populace(vill, num_families, professions)

    # start sim!
    years = 400
    vill.run_village(years)





