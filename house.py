class House:
    num_houses = 0

    def __init__(self):
        self.__class__.num_houses += 1
        self.id = self.__class__.num_houses

    def __str__(self):
        return "House %s" % self.id

