import random
import sys

if len(sys.argv) < 2:
    target = list("These violent delights have violent ends...")
else:
    target = list(sys.argv[1])

mutation_rate = 0.01

max_error = (ord('z') - ord('a'))*len(target)

possible = []

for i in range((ord('z')-ord('a'))):
    possible.append(chr(i+ord('a')))
    possible.append(chr(i+ord('A')))

possible += [" ",".",",","/","'","\"","\.","%"]

#print(possible)

def getInitialPopulation(num,target):
    population = []
    for _ in range(num):
        new_string = []
        for _ in range(len(target)):
            new_string.append(random.sample(possible,1)[0])
        population.append(new_string)
    return population

def getFitness(target,string):
    score = 0
    n = len(target)
    for i in range(n):
        try:
            if target[i] == string[i]:
                score += 1
        except:
            print("Failed!")
            print(target)
            print(string)
    #print((score+max_error)/max_error)
    return score/n


def reproducePopulation(population,target,mutation_rate):
    mating_pool = []
    new_pop = []
    bestAttempt = ""
    bestFitness = -1
    for thing in population:
        fitness = getFitness(target,thing)
        if fitness > bestFitness:
            bestAttempt = thing
            bestFitness = fitness
        for _ in range(int(fitness*100)):
            mating_pool.append(thing)
    if mating_pool == []:
        return getInitialPopulation(100,target)
    for _ in range(len(population)):
        new_pop += makeOffspring(mating_pool)
    for thing in new_pop:
        for i in range(len(thing)):
            if random.random() < mutation_rate:
                thing[i] = random.sample(possible,1)[0]
    return new_pop, bestAttempt, bestFitness

def makeOffspring(mating_pool):
    first = random.sample(mating_pool,1)[0]
    second = random.sample(mating_pool,1)[0]
    random_split = int(random.random()*len(first))
    offspring = [first[:random_split]+second[random_split:]]
    return offspring



def run(target):
    pop = getInitialPopulation(1000,target)
    i = 0
    while target not in pop:
        try:
            pop, bestAttempt,bestFitness = reproducePopulation(pop,target,mutation_rate)
            i += 1
        except:
            print("Program stopped after {} generations".format(i))
            print("Best attempt: {}".format(bestAttempt))
            print("Fitness: {}".format(bestFitness))
            return

    print("Found target after {} generations".format(i))
    print(target)

run(target)
