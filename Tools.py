import string
import os


class FileChanger:

    def __init__(self, string_name):
        # Create file
        self.filename = "GA_output_(" + string_name + ").txt"

        # Create directory for outputs
        if not os.path.exists('output'):
            os.makedirs('output')

        self.file = open('output' + '/' + self.filename, "w+")
        self.file.write("Target: " + string_name + '\n')

    def write_parameters_to_file(self, population, generations, kill_prcnt, mutation_chance, min_equal_prcnt):

        text = ('\nParameters'
                '\n'
                '============================='
                '\n'
                'Population: ' + str(population)
                + '\nGeneration: ' + str(generations)
                + '\nKill percent: ' + str(kill_prcnt)
                + '\nMutation chance: ' + str(mutation_chance)
                + '\nStop, when percent of equal: ' + str(min_equal_prcnt)
                + '\n'
                '=============================')
        self.file.write(text)

    def write_generation_to_file(self, generation, agents):
        text = "\n\nGeneration: " + str(generation)
        self.file.write(text)
        print(text, end='')
        text = "\n--------------------------------------------------------------------------\n"
        self.file.write(text)
        print(text, end='')
        for agent in agents:
            text = str(agent) + "\n"
            self.file.write(text)
            print(text, end='')

    def write_end_of_file(self, is_found):
        if is_found:
            text = '\n' \
                   '=============================\n' \
                   'The target string was found!'
        else:
            text = '\n' \
                   '=============================\n' \
                   'The target string wasn\'t found!'

        print(text, end='')
        self.file.write(text)

    def close_file(self):
        self.file.close()


# Create string of all characters without \n, \t, etc.
characters = string.ascii_letters + string.digits + ' ' + string.punctuation
