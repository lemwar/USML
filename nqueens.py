'''
Created on January 21 2018 

@author: kkostin
'''
import random
import math
from test.test_itertools import gen3

class Solver_8_queens:
    '''
    classdocs
    '''
    def __init__(self, pop_size=100, cross_prob=0.95, mut_prob=0.25):
        self.n = 8
        self.nbit = 24
        self.m = 3
        self.pop_size = pop_size
        self.cross_prob = cross_prob
        self.mut_prob = mut_prob
        
        self.population = list()
        self.fitness_list = list()
        
        
    def solve(self, min_fitness=1, max_epochs=100):
        # Generate the first population
        self.generate_population()
        
        epochs = 0
        max_fitness = max(self.fitness_list)
        max_index = self.fitness_list.index(max(self.fitness_list))
        #while False:
        while (max_epochs is None or epochs <= max_epochs) and (min_fitness is None or max_fitness < min_fitness):

            # Roulette method
            cross_pop = self.roulette()
            
            # crossingover
            new_pop = self.crossingover(cross_pop)   
                    
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
    
    
    def visualization(self, chrom2):
        chrom = self.convertToDec(chrom2)
        s = ''
        for i in range(self.n):
            for j in range(self.n):
                if (chrom[i] == j):
                    s += 'Q'
                else:
                    s += '+'
                s += ' '
            s += '\n'
        return s
    
    def generate_chrom(self):      
        s = ''
        for i in range(self.nbit):
            s += str(random.randint(0,1))     
        return s
            
    # Find a number of attacked pairs of Queens 
    def fitness(self, chrom2): 
        chrom = self.convertToDec(chrom2)
        res = 0
        for i in range(self.n):
            gen = chrom[i]
            j = i + 1
            while j < self.n:
                # Check lines
                try:
                    if chrom[j] == gen:
                        res += 1
                except IndexError:
                    print()
                # Check diagonal
                if (j - i) == math.fabs(chrom[j] - chrom[i]):
                    res += 1
                j += 1
                    
        return 1 - (res*2)/(self.n * 4)
        
    def roulette(self):
        # Find the number of hits for each chromosome
        roulette = list.copy(self.fitness_list)
        for i in range(len(self.population)):
            roulette[i] = round(roulette[i] / sum(self.fitness_list) * len(self.population))
        
        # population for crossingover
        cross_pop = list()
        for i in range(len(self.population)):
            while roulette[i] > 0:
                cross_pop.append(self.population[i])
                roulette[i] = roulette[i] - 1
        return cross_pop
    
    # Divide the desk on 2 part and stick them in a new chromosome
    def crossingover(self, cross_pop):
        new_population = list()
        pairs = random.sample(range(len(cross_pop)), len(cross_pop))
        for i in range(0, len(cross_pop)-1, 2):
            if random.random() <= self.cross_prob:
                chrom1 = cross_pop[pairs[i]]
                chrom2 = cross_pop[pairs[i+1]]
                k = random.randint(1, len(chrom1) - 1)
                new_chrom1 = chrom1[0:k] + chrom2[k:len(chrom2)]
                new_population.append(new_chrom1)

        return new_population
    
    # Swap 2 horizontal stripes in the desk
    def mutation(self, pop):
        new_pop = list()
        for i in range(len(pop)):
            if random.random() <= self.mut_prob:
            #if False:
                chrom = pop[i]
                r = random.randint(0, self.nbit - 1)
                gen = chrom[r]
                new_gen = '0'
                if gen == '0':
                    new_gen = '1'
                new_chrom = chrom[0 : r] + new_gen + chrom[r + 1 : len(chrom)]
                
                new_pop.append(new_chrom)
        return new_pop
          
    # Make a new population based on the old and new chromosomes
    def form_result_population(self, new_pop):
        for i in range(len(self.population)):
            new_pop.append(self.population[i])
        new_fitness_list = list()
        
        for i in range(len(new_pop)):
            new_fitness_list.append(self.fitness(new_pop[i]))    

        for i in range(len(self.population)):
            index = new_fitness_list.index(max(new_fitness_list))
            self.population[i] = new_pop.pop(index)
            self.fitness_list[i] = new_fitness_list.pop(index)
            
    def generate_population(self):
        for i in range(self.pop_size):
            self.population.append(self.generate_chrom())
            self.fitness_list.append(self.fitness(self.population[i]))
            
    def convertToBin(self, chrom):
        s=''
        for i in range(len(chrom)):
            gen = str(bin(chrom[i]))[2:]
            while len(gen) < 3:
                gen = '0' + gen
            s += gen
        return s
            
    def convertToDec(self, s):
        chrom = list()
        for i in range(0, len(s), self.m):
            gen = int(s[i:i+self.m], 2)
            chrom.append(gen)
            
        return chrom
            
            