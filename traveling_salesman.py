import random
import math
import sys

cities = []
for _ in range(int(sys.argv[1])):
    cities.append([random.randint(-10,10),random.randint(-10,10)])

def fact(n):
    if n < 2:
        return 1
    else:
        return n * fact(n-1)

def possibilities(arr1,arr2):
    result = []
    if len(arr2) < 2:
        return [arr1 + arr2]
    for i in range(len(arr2)):
        temp_arr = arr2[:]
        elem = [temp_arr.pop(i)] + arr1
        result += (possibilities(elem,temp_arr))
    return result

def getDistance(cities):
    dist = 0
    for i in range(len(cities)-1):
        dist += vectorDist(cities[i],cities[i+1])
    return dist

def vectorDist(first,second):
    a = first[0] - second[0]
    b = first[1] - second[0]
    return math.sqrt(a**2 + b**2)

def run(cities):
    poss = possibilities([],cities)
    max_dist = 1000000000000000
    winner = ""
    for pos in poss:
        dist = getDistance(pos)
        if dist < max_dist:
            winner = pos
            max_dist = dist
    print("Winner: {}\nDistance: {}".format(winner,max_dist))

def runGA(cities,pop_size,mut_rate):
    pop = getInitialPopulation(cities,pop_size)

    return

def getInitialPopulation(cities,pop_size):
    pop = []
    for _ in range(pop_size):
        pop.append(randon.sample(cities,len(cities)))
    return pop

def reproducePopulation(pop):
    new_pop = []
    


run(cities)
