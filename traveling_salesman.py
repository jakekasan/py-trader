import random
import math
import sys
#from ts_tools import City
#Member,setup

#pop_size = int(sys.argv[1])
cities = []
# for _ in range(int(sys.argv[1])):
#     cities.append(City(rand=True))



class City:
    def __init__(self,name=None,x=None,y=None,rand=True):
        if rand == True:
            self.name = random.choice(city_names)
            self.x = random.randint(-100,100)
            self.y = random.randint(-100,100)
        else:
            self.name = name
            self.x = x
            self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getName(self):
        return self.name

    def distanceTo(self,city):
        a = self.x - city.x
        b = self.y - city.y
        return math.sqrt(a**2 + b**2)

    def __str__(self):
        return "{}, x: {}, y: {}".format(self.name,self.x,self.y)

    def __eq__(self,other):
        if (self.name == other.name) and (self.x == other.x) and (self.y == other.y):
            return True
        else:
            return False

    def __copy__(self):
        return type(self)(name=self.name,x=self.x,y=self.y,rand=False)

cities.append(City(name="Roudnice",x=98,y=62,rand=False))
cities.append(City(name="San Jose",x=98,y=27,rand=False))
cities.append(City(name="Oban",x=84,y=29,rand=False))
cities.append(City(name="Cupar",x=58,y=6,rand=False))
cities.append(City(name="San Francisco",x=67,y=-18,rand=False))
cities.append(City(name="Brno",x=4,y=-88,rand=False))
cities.append(City(name="Glasgow",x=-53,y=-81,rand=False))
cities.append(City(name="Plzen",x=-57,y=-65,rand=False))
cities.append(City(name="Edinburgh",x=-64,y=72,rand=False))
cities.append(City(name="Helsinki",x=-62,y=2,rand=False))
cities.append(City(name="Prague",x=-92,y=32,rand=False))
# cities.append(City(name="London",x=45,y=-23,rand=False))
# cities.append(City(name="Dallas",x=82,y=17,rand=False))

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
    if dist == 0:
        dist = 1
    return dist

def vectorDist(first,second):
    a = first.getX() - second.getX()
    b = first.getY() - second.getY()
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
    print("Winner:")
    for city in winner:
        print(city)
    print("Distance: {}".format(max_dist))

def runGA(cities,pop_size,mut_rate):
    pop = getInitialPopulation(cities,pop_size)
    printPop(pop)
    return
    counter = 0
    gens = 0
    while(True):
        pop = reproducePopulation(pop,mut_rate)
        gens += 1
        print(gens)
        counter += 1
        if counter >= 25:
            printStatus(pop,gens)
            counter = 0
    return

def printStatus(pop,gens):
    min_dist,index = getDistIndex(pop)
    print("Total distance: {}\nPoints: {}".format(min_dist,pop[index]))

def printPop(pop):
    i = 0
    for cities in pop:
        print("List #{}".format(i))
        for city in cities:
            print("Name: {}, X: {}, Y: {}".format(city.name,city.x,city.y))

def getDistIndex(pop):
    listmap = list(map(getDistance,pop))
    min_dist = min(listmap)
    for i in range(len(listmap)):
        if listmap[i] == min_dist:
            return min_dist,i

def getInitialPopulation(cities,pop_size):
    pop = []
    for _ in range(pop_size):
        pop.append(random.sample(cities,len(cities)))
    return pop

def reproducePopulation(pop,mutation_rate):
    mating_pool = []
    new_pop = []
    min_dist = min(list(map(getDistance,pop)))
    for cities in pop:
        fitness = int(min_dist/(getDistance(cities))*100)
        if fitness > 0:
            for i in range(fitness):
                mating_pool.append(cities)
    selection = random.sample(mating_pool,(len(pop)*2))
    for i in range(0,len(selection),2):
        new_pop.append(reproduceTwo(selection[i],selection[i+1]))
    for i in range(len(new_pop)):
        if random.random() < mutation_rate:
            new_pop[i] = mutate(new_pop[i])
    print("Mating pool: {}\nNew pop: {}\nMin distance: {}".format(len(mating_pool),len(new_pop),min_dist))
    printPop(new_pop)
    return new_pop

def reproduceTwo(one,two):
    newList = []
    a = random.randint(0,(len(one)-1))
    newList += one[a:]
    for i in range((len(two)-1),0,-1):
        if two[i] in newList:
            two.pop(i)
    newList += two
    return newList

def mutate(cities):
    ind = [x for x in range(len(cities))]
    a = ind.pop(random.choice(ind))
    b = random.choice(ind)

    hold = cities[a]
    cities[a] = cities[b]
    cities[b] = hold

    return cities

#runGA(cities,pop_size,mutation_rate)
run(cities)
