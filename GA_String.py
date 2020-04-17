from fuzzywuzzy import fuzz
import random
import Tools
from StringAgent import StringAgent


def genetic_algorithm():

    # Initialize all agents
    agents = init_agents()

    for generation in range(generations):

        # Calculate fitness in current population
        agents = calculate_fitness(agents)

        # Write current generation to the file
        tools.write_generation_to_file(generation, agents)

        # Remove the worst agents
        agents = kill_weak_agents(agents)

        # Create new agents
        agents = do_crossover(agents)

        # Create mutation
        agents = do_mutations(agents)

        # If one of agent have fitness better than minimal equal then end of programm
        if any(agent.fitness > min_equal_prcnt for agent in agents):
            tools.write_end_of_file(True)
            exit(0)
    tools.write_end_of_file(False)


def init_agents():
    string_agents = [StringAgent(target_str_len) for _ in range(population)]
    return string_agents


def calculate_fitness(agents):
    # For all agents checking string match
    for agent in agents:
        agent.fitness = fuzz.ratio(agent.string, target_str)
    return agents


def kill_weak_agents(agents):

    # Sort agents from maximum fitness to minimum fitness
    agents = sorted(agents, key=lambda agent: agent.fitness, reverse=True)

    # Remove input percent agents
    agents = agents[: len(agents) - int(kill_prcnt * len(agents))]

    return agents


def do_crossover(agents):

    childs = []

    # Recover population
    while len(childs) + len(agents) < population:

        # Choose random parents
        parent_1 = random.choice(agents)
        parent_2 = random.choice(agents)

        # Choose random split index for string
        split_index = random.randint(0, target_str_len)

        # Create childs
        child_1 = StringAgent(target_str_len)
        child_2 = StringAgent(target_str_len)

        # Each child gets a piece of the parents' string
        child_1.string = parent_1.string[:split_index] + parent_2.string[split_index:]
        child_2.string = parent_2.string[:split_index] + parent_1.string[split_index:]

        childs.append(child_1)
        childs.append(child_2)

    # Add list of childs to current agents
    agents.extend(childs)

    return agents


def do_mutations(agents):
    # Create mutation in letter
    for agent in agents:
        for index, letter in enumerate(agent.string):

            # If random is mutation then choose random letter to agent string
            if random.randrange(0, 100) < mutation_chance:
                agent.string = agent.string[:index] + random.choice(Tools.characters) + agent.string[index + 1:]

    return agents


# Start program

target_str = input("Target string: ")
target_str_len = len(target_str)


# Default parameters
population = 20
generations = 100000
kill_prcnt = 0.8
mutation_chance = 10
min_equal_prcnt = 90

print('\nDefault parameters'
      '\n'
      '============================='
      '\n'
      'Population: ' + str(population)
      + '\nGeneration: ' + str(generations)
      + '\nKill percent: ' + str(kill_prcnt)
      + '\nMutation chance: ' + str(mutation_chance)
      + '\nStop, when percent of equal: ' + str(min_equal_prcnt)
      + '\n=============================\n')


# User choice
choice = -1
while choice != 1 and choice != 2:
    choice = int(input("Default or user parameters?\n1. Default\n2. User parameters\n"))

# Scan user choice
if choice == 2:
    population = int(input("Count of agents in population: "))
    generations = int(input("Count of max generations: "))
    kill_prcnt = int(input("Percent of killing agents: ")) / 100.0
    mutation_chance = int(input("Chance of mutation: "))
    min_equal_prcnt = int(input("Stop, when percent of equal: "))


# Create file
tools = Tools.FileChanger(target_str)
tools.write_parameters_to_file(population, generations, kill_prcnt, mutation_chance, min_equal_prcnt)

# Start GA
genetic_algorithm()

tools.close_file()
