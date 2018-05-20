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

    def __str__(self):
        return "{}, x: {}, y: {}".format(self.name,self.x,self.y)

class Member:
    def __init__(self,cities):
        this.cities = cities

    def getDistance(self):
        pass


class Population:
    def __init__(self):
        self.members =

city_names = ["San Francisco","Prague","San Jose","Los Angeles","Dallas","Edinburgh","Fort William","Oban","Aberdeen","Glasgow","Brno","Plzen","Most","Roudnice","Perth","Cupar","Oslo","Helsinki","Bratislava","Rome","Milan","Paris","Nuremburg","Berlin"]

def
