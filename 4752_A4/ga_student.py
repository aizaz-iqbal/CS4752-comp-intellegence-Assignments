import random, math, heapq
from sudoku import Sudoku

def eval_sudoku(array):
    #return sum(array)  # un-comment this line and watch the GA optimize to all max numbers
    #return -sum(array) # un-comment this line and watch the GA optimize to all ones
    s = Sudoku(0)
    size = int(math.sqrt(len(array)))
    s.set_arr(array)
    fitness = 0
    # count unique values in each row
    for r in range(s.size()):
        vals = set()
        for c in range(s.size()):
            vals.add(s.get(r,c))
        fitness += len(vals)
    # count unique values in each column
    for c in range(s.size()):
        vals = set()
        for r in range(s.size()): 
            vals.add(s.get(r,c))
        fitness += len(vals)
    # count unique values in each square
    sqsize = int(math.sqrt(s.size()))
    for sr in range(sqsize):
        for sc in range(sqsize):
            vals = set()
            for r in range(sqsize):
                for c in range(sqsize):
                    vals.add(s.get(sr*sqsize+r, sc*sqsize+c))
            fitness += len(vals)
    return fitness

# the class that stores the genetic algorithm settings
class GASettings:
    # we need something in here so that python doesn't complain about blank classes
    description = 'Blank struct to hold our GA settings in'
 
def get_ga_settings(sudoko_size):
    settings = GASettings()
    settings.individual_values      = [(i+1) for i in range(sudoko_size)]   # list of possible values individuals can take
    settings.individual_size        = sudoko_size*sudoko_size               # length of an individual
    settings.fitness_function       = eval_sudoku                           # the fitness function of an individual
    settings.population_size        = 100                                   # total size of each population                            
    settings.elitism_ratio          = 0.3                                   # select top x% of individuals to survive                  
    settings.parent_roulette_ratio  = 0.2                                   # select x% of population as parents via roulette wheel     
    settings.mutation_rate          = 0.5                                   # mutation rate percentage                                  
    settings.crossover_index        = settings.individual_size // 2         # the index to split parents for recombination              
    return settings

def evolve(population, settings):
    length_of_population = len(population)
    sorted_pop = []
    pop_fitness = []
	#this loop creates a list of fitnesses and fills a heapq for the eliteism function later
    for i in range(length_of_population):                
        fitness = eval_sudoku(population[i])
        pop_fitness.append(fitness)
        heapq.heappush(sorted_pop,(-pop_fitness[i],population[i]))#using negative fitness values do that the largest gets poped 
    P = int(settings.parent_roulette_ratio * len(population))
    parents = []
    sum_of_pop = sum(pop_fitness)
	#This loop fills a list of randomly selected population members are parents in the next population
	#Selection is done through roulette wheel method where a random int is chosen between 0 and the sum_of_pop and then the fitnesses are sumed until the match is found
	#then the loop breaks and repeats with a new number
    while len(parents) < P:                              
        rand = random.randint(0,sum_of_pop)
        sum_of_fitness = 0
        for x in range(length_of_population):
            sum_of_fitness += pop_fitness[x]
            if sum_of_fitness >= rand:
                parents.append(population[x])
                break
           
    next_population = []
    E = int(settings.elitism_ratio * length_of_population)
	 # This loop fills E number of the next_population with elite members from the current population stored with heapq
    for z in range(E):                                 
        fitness,pop = heapq.heappop(sorted_pop)
        next_population.append(pop)
    offspring = []
	#Here parent members are randomly chosed to be combined into a series children made by splicing parts of the parents together
    while (len(offspring) + len(next_population) < length_of_population): 
        mother = parents[random.randint(0,len(parents)-1)]
        father = parents[random.randint(0,len(parents)-1)]
        if mother == father: continue
        child1 = mother[settings.crossover_index:] + father[:settings.crossover_index]
        child2 = mother[:settings.crossover_index] + father[settings.crossover_index:] 
        offspring.append(child1)
        offspring.append(child2)
    M = int(settings.mutation_rate * len(offspring))
    j = 0
    mutated_offspring = []
	#Here M number of children are mutated for the next generation
    while j <= M:
        individual = offspring[random.randint(0, len(offspring)-1)]
        if not individual in mutated_offspring:
            individual[random.randint(0,len(individual)-1)] = random.choice(settings.individual_values) # random position in the individual is changed to a random legal number
            mutated_offspring.append(individual)
            j += 1

    next_population = next_population + offspring
    return next_population
 
    
