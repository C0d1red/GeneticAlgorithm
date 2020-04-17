import random
import Tools


class StringAgent:

    def __init__(self, length):

        # Set fitness to default
        self.fitness = -1

        # Create random string from characters
        self.string = "".join(random.choice(Tools.characters) for _ in range(length))

    def __str__(self):
        return "String: " + self.string + " | Fitness: " + str(self.fitness)
