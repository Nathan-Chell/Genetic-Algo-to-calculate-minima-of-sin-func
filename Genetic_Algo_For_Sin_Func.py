#Implimentation of a genetic algo
import math
from copy import deepcopy
from random import randint, random

#Int the function we want to calculate the minima/ maxima of.
def objective(x):
	return math.sin(x)

#Initilise a random population.
def starting_pop(n_pop, n_bits, bounds):

    pop = []
    for _ in range(n_pop):
        arr = []
        for __ in range(len(bounds)-1):
            temp = ""
            for ___ in range(n_bits):
                temp += str(randint(0,1))
            pop.append(temp)
    return pop

def decode(bounds, n_bits, bitstring):
    largest = 2**n_bits
    for i in range(len(bounds)-1):
        #extracting the substring
        #convert bitstring to string of chars
        chars = ''.join([str(s) for s in bitstring])
        #convert to integer
        integer = int(chars, 2)
        #scale value to correct range
        value = bounds[0] + (integer/largest) * (bounds[1] - bounds[0])
    return value

def selection(pop, values, k=3):

    #source: https://www.geeksforgeeks.org/tournament-selection-ga/
    #Tournament selection
    rand_pop = randint(0, len(pop) - 1)
    for i in range(0, k):
        selected_pop = randint(0, len(pop) - 1)
        if values[selected_pop] < values[rand_pop]:
            rand_pop = selected_pop
    return pop[rand_pop]

def crossover(pair, r_cross, n_bits):
    #copy values into the children
    c1, c2 = deepcopy(pair[0]), deepcopy(pair[1])

    #if a random float between 0,1 is less than our cross overrate
    #then we change the bits, this results in a 90% crossover with a r_cross of 0.9
    #give enough iterations.
    if random() < r_cross:
        #Select a point in the bitstring to change e.g bit 4 onwards or bit 7 onwards
        point = randint(1, (n_bits-2))

        c1 = pair[0][:point] + pair[1][point:]
        c2 = pair[1][:point] + pair[0][point:]

    #May not always crossover
        #print(len(c1))
    return [c1, c2]

def mutation(cur, r_mut):
    for i in range(len(cur)):
        if random() < r_mut:
            #cur[i] = 1 - int(cur[i])
            temp = cur
            if cur[i] == "0":
                cur = cur[:(i-1)] + "1" + cur[i:]
            else:
                cur = cur[:(i-1)] + "0" + cur[i:]

    return cur


def main():

    #Int vars
    #Population size
    n_pop = 100
    #Total iterations
    n_iter = 100
    # crossover rate
    r_cross = 0.9
    # define range for input
    bounds = [-1.0, 1.0]
    # bits per variable
    n_bits = 16
    # mutation rate
    r_mut = 1.0 / (float(n_bits) * len(bounds))

    pop = starting_pop(n_pop, n_bits, bounds)

    #Track best solutions

    best, best_eval = 0, objective(decode(bounds, n_bits, pop[0]))

    #enumerate generations
    for gen in range(n_iter):
        #decode population
        decoded = [decode(bounds, n_bits, p) for p in pop]

        #determine the values of the current population.
        values = [objective(d) for d in decoded]
        #assign new best_eval
        for i in range(n_pop):
            if values[i] < best_eval:
                best, best_eval = pop[i], values[i]
                print("Found new best in gen: {}, current best_eval: {}, from values: {}".format(gen, values[i], decoded[i]))

        #select parents for new Population
        selected = [selection(pop, values, 3) for _ in range(n_pop)]
        #after selecting the parents we need to alter them to create the new generation

        children = list()
        for i in range(0, n_pop):
            temp = []
            for c in crossover(selected[i], r_cross, n_bits):
                temp.append(mutation(c, r_mut))
            children.append(temp)
        pop = children

    print("Done")
    decoded = decode(bounds, n_bits, best)
    print("Values {}, result in the best score of {}".format(decoded, best_eval))


if __name__ == '__main__':
    main()
