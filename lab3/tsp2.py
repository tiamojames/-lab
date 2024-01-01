import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd


# Define the City class
class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, city):
        x_dis = abs(self.x - city.x)
        y_dis = abs(self.y - city.y)
        return np.sqrt((x_dis ** 2) + (y_dis ** 2))

    def __repr__(self):
        return f"({self.x},{self.y})"


# Define the Fitness class
class Fitness:
    def __init__(self, route):
        self.route = route
        self.distance = 0
        self.fitness = 0.0

    def route_distance(self):
        if self.distance == 0:
            path_distance = 0
            for i in range(len(self.route)):
                from_city = self.route[i]
                to_city = None
                if i + 1 < len(self.route):
                    to_city = self.route[i + 1]
                else:
                    to_city = self.route[0]
                path_distance += from_city.distance(to_city)
            self.distance = path_distance
        return self.distance

    def route_fitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.route_distance())
        return self.fitness


# Create initial random route
def create_route(city_list):
    route = random.sample(city_list, len(city_list))
    return route


# Create initial population
def initial_population(pop_size, city_list):
    population = []

    for i in range(0, pop_size):
        population.append(create_route(city_list))
    return population


# Rank routes
def rank_routes(population):
    fitness_results = {}
    for i in range(len(population)):
        fitness_results[i] = Fitness(population[i]).route_fitness()
    return sorted(fitness_results.items(), key=lambda x: x[1], reverse=True)


# Selection function
def selection(pop_ranked, elite_size):
    selection_results = []
    df = pd.DataFrame(np.array(pop_ranked), columns=["Index", "Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100 * df.cum_sum / df.Fitness.sum()

    for i in range(elite_size):
        selection_results.append(pop_ranked[i][0])
    for i in range(len(pop_ranked) - elite_size):
        pick = 100 * random.random()
        for i in range(len(pop_ranked)):
            if pick <= df.iat[i, 3]:
                selection_results.append(pop_ranked[i][0])
                break
    return selection_results


# Mating pool function
def mating_pool(population, selection_results):
    pool = []
    for i in range(len(selection_results)):
        index = selection_results[i]
        pool.append(population[index])
    return pool


# Breed function (crossover)
def breed(parent1, parent2):
    child = []
    childP1 = []
    childP2 = []

    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))

    start_gene = min(geneA, geneB)
    end_gene = max(geneA, geneB)

    for i in range(start_gene, end_gene):
        childP1.append(parent1[i])

    childP2 = [item for item in parent2 if item not in childP1]

    child = childP1 + childP2
    return child


# Breeding population function
def breed_population(mating_pool, elite_size):
    children = []
    length = len(mating_pool) - elite_size
    pool = random.sample(mating_pool, len(mating_pool))

    for i in range(elite_size):
        children.append(mating_pool[i])

    for i in range(length):
        child = breed(pool[i], pool[len(mating_pool) - i - 1])
        children.append(child)
    return children


# Mutation function
def mutate(individual, mutation_rate):
    for swapped in range(len(individual)):
        if random.random() < mutation_rate:
            swap_with = int(random.random() * len(individual))

            city1 = individual[swapped]
            city2 = individual[swap_with]

            individual[swapped] = city2
            individual[swap_with] = city1
    return individual


# Mutate population function
def mutate_population(population, mutation_rate):
    mutated_pop = []

    for ind in range(len(population)):
        mutated_ind = mutate(population[ind], mutation_rate)
        mutated_pop.append(mutated_ind)
    return mutated_pop


# Next generation function
def next_generation(current_gen, elite_size, mutation_rate):
    pop_ranked = rank_routes(current_gen)
    selection_results = selection(pop_ranked, elite_size)
    matingpool = mating_pool(current_gen, selection_results)
    children = breed_population(matingpool, elite_size)
    next_gen = mutate_population(children, mutation_rate)
    return next_gen


# Genetic algorithm main function
def genetic_algorithm(population, pop_size, elite_size, mutation_rate, generations):
    pop = initial_population(pop_size, population)
    initial_distance = 1 / rank_routes(pop)[0][1]
    print("Initial distance: " + str(1 / rank_routes(pop)[0][1]))

    best_distance = initial_distance
    best_generation = 0
    best_route = None

    for i in range(generations):
        pop = next_generation(pop, elite_size, mutation_rate)
        current_best_distance = 1 / rank_routes(pop)[0][1]

        if current_best_distance < best_distance:
            best_distance = current_best_distance
            best_generation = i+1
            best_route_index = rank_routes(pop)[0][0]
            best_route = pop[best_route_index]

        print(f"Generation {i + 1}: Distance = {current_best_distance}")

    print(f"Generation {best_generation} : Final distance:{best_distance} ")
    # best_route_index = rank_routes(pop)[0][0]
    # best_route = pop[best_route_index]
    return best_route if best_route else pop[rank_routes(pop)[0][0]]


# Plotting function
def plot_route(route):
    x = []
    y = []
    for city in route:
        x.append(city.x)
        y.append(city.y)
    x.append(route[0].x)
    y.append(route[0].y)
    plt.plot(x, y, 'ro-')
    plt.title("Route")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.show()


# Define your cities here
city_list = []
#10个城市
coordinates = [(87, 7), (91, 38), (83, 46), (71, 44), (64, 60), (68, 58), (83, 69), (87, 76), (74, 78), (71, 71)]

for i in range(len(coordinates)):
    city_list.append(City(x=coordinates[i][0], y=coordinates[i][1]))

# Set parameters for the genetic algorithm
pop_size = 100
elite_size = 20
mutation_rate = 0.01
generations = 500

# Run the genetic algorithm
best_route = genetic_algorithm(population=city_list, pop_size=pop_size, elite_size=elite_size,
                               mutation_rate=mutation_rate, generations=generations)

# Plot the best route
plot_route(best_route)




# coordinates = [
#     (87, 7), (91, 38), (83, 46), (71, 44), (64, 60),
#     (68, 58), (83, 69), (87, 76), (74, 78), (71, 71),
#     (58, 69), (54, 62), (51, 67), (37, 84), (41, 94),
#     (2, 99), (7, 64), (22, 60), (25, 62), (18, 54),
#     (4, 50), (13, 40), (18, 40), (24, 42), (25, 38),
#     (41, 26), (45, 21), (44, 35), (58, 35), (62, 32)
# ]