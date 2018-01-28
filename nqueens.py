"""
Created on January 21 2018

@author: Kirill Kostin
"""
import random
import math


class Solver_8_queens:

    def __init__(self, pop_size=100, cross_prob=0.95, mut_prob=0.25, is_rang=False, is_multi_cross=False):
        self.n = 8
        self.n_bit = 24
        self.m = 3
        self.pop_size = pop_size
        self.cross_prob = cross_prob
        self.mut_prob = mut_prob
        
        self.population = list()
        self.fitness_list = list()

        self.is_rang = is_rang
        self.is_multi = is_multi_cross
        
    def solve(self, min_fitness=1, max_epochs=200):
        # Generate the first population
        self.generate_population()
        
        epochs = 0
        max_fitness = max(self.fitness_list)
        max_index = self.fitness_list.index(max(self.fitness_list))
        while (max_epochs is None or epochs <= max_epochs) and (min_fitness is None or max_fitness < min_fitness):

            if self.is_rang:
                # Rang method
                cross_pop = self.rang()
            else:
                # Roulette method
                cross_pop = self.roulette()
            
            # crossing over
            new_pop = self.crossing_over(cross_pop, self.is_multi)
                    
            # form a new population
            self.form_result_population(new_pop)
            
            # mutation
            new_pop = self.mutation(self.population)
                
            # form a new population
            self.form_result_population(new_pop)
                
            epochs = epochs + 1
            max_fitness = max(self.fitness_list)
            max_index = self.fitness_list.index(max(self.fitness_list))       
        
        return max_fitness, epochs, self.visualization(self.population[max_index])
    
    def visualization(self, individual_2):
        individual = self.convert_to_dec(individual_2)
        s = ''
        for i in range(self.n):
            for j in range(self.n):
                if individual[i] == j:
                    s += 'Q'
                else:
                    s += '+'
                s += ' '
            s += '\n'
        return s
    
    def generate_individual(self):
        s = ''
        for i in range(self.n_bit):
            s += str(random.randint(0, 1))
        return s
            
    # Find a number of attacked pairs of Queens 
    def fitness(self, individual_2):
        individual = self.convert_to_dec(individual_2)
        res = 0
        for i in range(self.n):
            gen = individual[i]
            j = i + 1
            while j < self.n:
                # Check lines
                if individual[j] == gen:
                    res += 1
                # Check diagonal
                if (j - i) == math.fabs(individual[j] - individual[i]):
                    res += 1
                j += 1
                    
        return 1 - (res*2)/(self.n * 4)
        
    def roulette(self):
        # Find the number of hits for each chromosome
        roulette = list()
        sum_fit = sum(self.fitness_list)
        len_pop = len(self.population)
        for fit in self.fitness_list:
            roulette.append(round(fit / sum_fit * len_pop))
        
        # population for crossing over
        cross_pop = list()
        for i in range(len(self.population)):
            while roulette[i] > 0:
                cross_pop.append(self.population[i])
                roulette[i] = roulette[i] - 1
        return cross_pop

    def rang(self):
        # Find the number of hits for each chromosome
        rang = list()
        sum_fit = sum(self.fitness_list)
        len_pop = len(self.population)
        self.fitness_list.sort(reverse=True)
        a = random.random() + 1
        b = 2 - a
        for i in range(len(self.fitness_list)):
            res = (1/len_pop) * (a-(a-b)*(i/(len_pop - 1)))
            rang.append(round(res * len_pop))

        # population for crossing over
        cross_pop = list()
        for i in range(len(self.population)):
            while rang[i] > 0:
                cross_pop.append(self.population[i])
                rang[i] = rang[i] - 1
        return cross_pop
    
    # Divide the desk on 2 part and stick them in a new chromosome
    def crossing_over(self, cross_pop, is_multi=False):
        new_population = list()
        pairs = random.sample(range(len(cross_pop)), len(cross_pop))
        for i in range(0, len(cross_pop)-1, 2):
            if random.random() <= self.cross_prob:
                individual_1 = cross_pop[pairs[i]]
                individual_2 = cross_pop[pairs[i+1]]
                if is_multi:
                    k1 = random.randint(1, len(individual_1) - 2)
                    k2 = random.randint(k1 + 1, len(individual_1) - 1)
                    new_individual_1 = individual_1[0:k1] + individual_2[k1:k2] + individual_1[k2:self.n_bit]
                    new_population.append(new_individual_1)

                    new_individual_2 = individual_2[0:k1] + individual_1[k1:k2] + individual_2[k2:self.n_bit]
                    new_population.append(new_individual_2)
                else:
                    k1 = random.randint(1, len(individual_1) - 2)
                    new_individual_1 = individual_1[0:k1] + individual_2[k1:self.n_bit]
                    new_population.append(new_individual_1)

                    new_individual_2 = individual_2[0:k1] + individual_1[k1:self.n_bit]
                    new_population.append(new_individual_2)

        return new_population
    
    # Swap 2 horizontal stripes in the desk
    def mutation(self, pop):
        new_pop = list()
        for individual in pop:
            if random.random() <= self.mut_prob:
                r = random.randint(0, self.n_bit - 1)
                gen = individual[r]
                new_gen = '0'
                if gen == '0':
                    new_gen = '1'
                new_individual = individual[0:r] + new_gen + individual[r + 1:self.n_bit]
                new_pop.append(new_individual)

        return new_pop
          
    # Make a new population based on the old and new chromosomes
    def form_result_population(self, new_pop):
        for individual in self.population:
            new_pop.append(individual)

        new_fitness_list = list()
        for individual in new_pop:
            new_fitness_list.append(self.fitness(individual))

        for i in range(len(self.population)):
            index = new_fitness_list.index(max(new_fitness_list))
            self.population[i] = new_pop.pop(index)
            self.fitness_list[i] = new_fitness_list.pop(index)
            
    def generate_population(self):
        for i in range(self.pop_size):
            self.population.append(self.generate_individual())
            self.fitness_list.append(self.fitness(self.population[i]))
            
    def convert_to_dec(self, s):
        individual = list()
        for i in range(0, len(s), self.m):
            gen = int(s[i:i+self.m], 2)
            individual.append(gen)
        return individual
