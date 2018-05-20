import random as random
import math
import copy

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

class Member:
    def __init__(self,cities):
        self.cities = cities

    def getScore(self):
        dist = 0
        for i in range(len(self.cities)-1):
            dist += self.cities[i].distanceTo(self.cities[i+1])
        if dist == 0:
            dist = 1
        return 1/dist

    def reverse(self):
        temp = []
        for i in range(len(self.cities)-1,-1,-1):
            temp.append(self.cities[i])
        return temp

class Population:
    def __init__(self,members=[],mut_rate=0.05):
        self.members = members
        self.mut_rate = mut_rate
        self.generation = 0
        self.best_path, self.best_score = self.getBest()

    def nextGeneration(self):
        #get probabilities from fitness scores
        probs = self.getFitnessProbs()
        self.best_path,self.best_score = self.getBest()
        new_pop = []
        while len(new_pop) < (len(self.members)-1):
            #print("\n--- End of members ---\n")
            #new_pop.append(self.selectMemberToReproduce(probs))
            new_pop.append(self.reproduceTwo(self.selectMemberToReproduce(probs),self.selectMemberToReproduce(probs)))
            #print("Appended new member, new population now {} elements long\n".format(len(new_pop)))
        new_pop = self.mutatePop(new_pop)
        new_pop.append(self.best_path)
        #print("\nFinishing function, length of replacement population is {}\n".format(len(new_pop)))
        self.members = new_pop
        self.generation += 1

    def getFitnessProbs(self):
        scores = []
        for member in self.members:
            scores.append(self.getScore(member))
        total = sum(scores)
        probs = [x/total for x in scores]
        return probs

    def selectMemberToReproduce(self,probs):
        index = -1
        r = random.random()
        while r > 0:
            if index >= len(self.members):
                index = -1
            index += 1
            r -= probs[index]
        #print("Selected member to reproduce:")
        return copy.deepcopy(self.members[index])

    def getScore(self,cities):
        dist = 0
        for i in range(len(cities)-1):
            dist += cities[i].distanceTo(cities[i+1])
        return 1/(dist+1)

    def getDist(self,cities):
        dist = 0
        for i in range(len(cities)-1):
            dist += cities[i].distanceTo(cities[i+1])
        return dist

    def reproduceTwo(self,one,two):
        r = int(random.random()*(len(one)-1))
        cities = one[r:]
        for i in range((len(two)-1),-1,-1):
            if two[i] in cities:
                two.pop(i)
        for i in range(0,r):
            cities.insert(i,two.pop(0))
        cities += two[0:]
        return cities

    def mutatePop(self,pop):
        for cities in pop:
            if random.random() < self.mut_rate:
                a = random.choice([x for x in range(1,len(cities)-2)])
                b = random.choice([a-1,a+1])
                cities[a],cities[b] = cities[b],cities[a]
        return pop

    def printBest(self):
        best_score = 100000000000000
        best_path = None
        for cities in self.members:
            fitness = self.getDist(cities)
            if fitness < best_score:
                best_path = cities
                best_score = fitness
        if best_path == None:
            print("No good path")
            return
        print("--- Path ---")
        for city in best_path:
            print(city)
        print("Distance: {}".format(best_score))
        return

    def getBest(self):
        best_score = 100000000000000
        best_path = None
        for cities in self.members:
            fitness = self.getDist(cities)
            if fitness < best_score:
                best_path = cities
                best_score = fitness
        return best_path,best_score

def printMember(member):
    for city in member:
        print(city)


city_names = ["San Francisco","Prague","San Jose","Los Angeles","Dallas","Edinburgh","Fort William","Oban","Aberdeen","Glasgow","Brno","Plzen","Most","Roudnice","Perth","Cupar","Oslo","Helsinki","Bratislava","Rome","Milan","Paris","Nuremburg","Berlin"]


# init a population
cities = []
members = []
#
# for _ in range(len(city_names)):
#     city = city_names.pop(int(random.random()*len(city_names)))
#     cities.append(City(name=city,x=random.randint(-100,100),y=random.randint(-100,100),rand=False))

#
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

for _ in range(100):
    members.append(random.sample(cities,len(cities)))

pop = Population(members=members,mut_rate=0.2)

pop.nextGeneration()
pop.printBest()

while pop.generation < 100000:
    pop.nextGeneration()
    if (pop.generation % 100) == 0:
        pop.printBest()
pop.printBest()
