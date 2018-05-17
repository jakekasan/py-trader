import random
import math
import sys

cities = []
for _ in range(int(sys.argv[1])):
    cities.append([random.randint(-10,10),random.randint(-10,10)])
mutation_rate = 0.01


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
    counter = 0
    gens = 0
    while(True):
        pop = reproducePopulation(pop,mut_rate)
        gens += 1
        counter += 1

    return

def printStatus(pop,gens):
    min_dist,index = getDistIndex(pop)
    print("Distance")

def getDistIndex(pop):
    listmap = list(map(getDistance,pop))
    min_dist = min(listmap)
    for i in range(len(listmap)):
        if listmap[i] == min_dist:
            return min_dist,i



def getInitialPopulation(cities,pop_size):
    pop = []
    for _ in range(pop_size):
        pop.append(randon.sample(cities,len(cities)))
    return pop

def reproducePopulation(pop,mutation_rate):
    mating_pool = []
    new_pop = []
    min_dist = min(list(map(getDistance,pop)))
    for cities in pop:
        fitness = int(min_dist/(getDistance(cities))*100)
        for i in range(fitness):
            mating_pool.append(cities)
    for _ in pop:
        new_pop.append(reproduceTwo(random.choice(mating_pool),random.choice(mating_pool)))
    for i in range(len(new_pop)):
        if random.random() < mutation_rate:
            new_pop[i] = mutate(new_pop[i])
    return new_pop

def reproduceTwo(one,two):
    newList = [0 for _ in one]
    a = random.randint(0,(len(one)-2))
    b = random.randint(a+1,(len(one)-1))
    if a == b:
        newList[a:(b+1)] = one[a:(b+1)]
    for i in range(len(two)):
        if (two[i] not in newList) and (i not in range(a,b+1)):
            newList[i] = two.pop(i)
    while 0 in newList:
        for i in range(len(newList)):
            if newList[i] == 0:
                newList[i] = two.pop(0)
    return newList

def mutate(cities):
    ind = [x for x in range(len(cities))]
    a = ind.pop(random.choice(ind))
    b = random.choice(ind)

    hold = cities[a]
    cities[a] = cities[b]
    cities[b] = hold

    return cities








run(cities)
