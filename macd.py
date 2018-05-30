import pandas as pd
#from matplotlib import pyplot as plt
import copy as copy
import random as random

df = pd.read_csv("./price_movements.csv")
df["date"] = pd.DatetimeIndex(df["date"])
df.set_index("date")

#print(df["date"].index)

#print(df.tail())
#df.plot(y="AAPL")
#plt.show()

#print(df.columns)

def getMacd(stock,df,long=26,short=12,mac=9):
    temp = pd.DataFrame()

    temp["{}".format(stock)] = df[stock]

    temp["{}_26ema".format(stock)] = pd.Series.ewm(df[stock],span=long).mean()

    temp["{}_12ema".format(stock)] = pd.Series.ewm(df[stock],span=short).mean()

    temp["{}_MACD".format(stock)] = (temp["{}_12ema".format(stock)] - temp["{}_26ema".format(stock)])

    temp["{}_MACD_signal".format(stock)] = pd.Series.ewm(temp["{}_MACD".format(stock)],span=mac).mean()

    return temp

#macd = getMacd("AAPL",df)

class Trader:
    def __init__(self,name,top,bottom):
        self.bought = False
        self.money = 0
        self.name = name
        self.top = top
        self.bottom = bottom

    def trade(self,row):
        signal = self.getDecision(row)
        if signal == 0:
            return
        if signal == 1:
            if self.bought:
                return
            self.bought = True
            self.money -= row[self.name]
            return
        if signal == -1:
            if self.bought:
                self.bought = False
                self.money += row[self.name]
                return
            return

    def getDecision(self,row):
        signal = row["{}_MACD_signal".format(self.name)] - row["{}_MACD".format(self.name)]
        if signal > self.top:
            return 1
        elif signal < self.bottom:
            return -1
        else:
            return 0

    def __str__(self):
        return ("Trader balance: {}".format(self.money))

class GATrader:
    def __init__(self,df,name,top,bottom,long=26,short=12,mac=9):
        self.bought = False
        self.money = 0
        self.name = name
        self.df = df
        self.top = top
        self.bottom = bottom
        self.long = long
        self.short = short
        self.mac = mac

    def trade(self,row):
        signal = self.getDecision(row)
        if signal == 0:
            return
        if signal == 1:
            if self.bought:
                return
            self.bought = True
            self.money -= row[self.name]
            return
        if signal == -1:
            if self.bought:
                self.bought = False
                self.money += row[self.name]
                return
            return

    def getDecision(self,row):
        signal = row["{}_MACD_signal".format(self.name)] - row["{}_MACD".format(self.name)]
        if signal > self.top:
            return 1
        elif signal < self.bottom:
            return -1
        else:
            return 0

    def getProfit(self):
        self.money = 0
        self.bought = False
        if self.name not in self.df.columns:
            print("Stock not found. Exiting")
            return
        macd = getMacd(self.name,self.df,long=self.long,short=self.short,mac=self.mac)
        for index,row in macd.iterrows():
            self.trade(row)
        if self.bought:
            self.money += row[self.name]
        return self.money

    def __str__(self):
        return ("Top: {}, Bottom: {}, Long: {}, Short: {}, Mac: {}, Window: {}, Profit: {}".format(self.top,self.bottom,self.long,self.short,self.mac,self.window,self.getProfit()))



def trade(name,df):
    if name not in df.columns:
        print("Stock not found. Exiting")
        return
    macd = getMacd(name,df)
    trader = Trader(name)
    for index,row in macd.iterrows():
        trader.trade(row)
    #print(trader)
    return trader.money

def run(df):
    balance = 0
    failed = 0
    for stock in df.columns:
        if stock == "date":
            continue
        try:
            profit = trade(stock,df)
            balance += profit
            print("Stock: {} Profit: {}".format(stock,profit))
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            return
        except:
            failed += 1
            #print("Stock: {} Failed".format(stock))

    print("Total balance: {}".format(balance))
    print("Total failed: {}".format(failed))

def GA(popSize,stock,df,mut_rate,two=False):
    """
    @params:
    popSize: the size of the population
    stock: the name of the stock being targeted
    df: a dataframe which contains a column with the name of the stock as its name
    mut_rate: The mutation rate to apply when reproducing a new population
    two: boolean for if the short and long variables in the MACD signal should be subject to the genetic algorithm

    """
    population = []
    for _ in range(popSize):
        if two:
            population.append(GATrader(df,stock,random.random()*2,random.random()*(-2)))
        else:
            population.append(GATrader(df,stock,random.random()*2,random.random()*(-2),max(1,int(random.random()*100)),max(1,int(random.random()*50)),max(1,int(random.random()*10))))
    print("Starting Profits: ")
    printPopulation(population,two=two)
    print("\n")
    for _ in range(1000):
        fitness = []
        for trader in population:
            fitness.append(trader.getProfit())
        fitness = normalise(fitness)
        if fitness == False:
            population = []
            for _ in range(popSize):
                if two:
                    population.append(GATrader(df,stock,random.random()*2,random.random()*(-2)))
                else:
                    population.append(GATrader(df,stock,random.random()*2,random.random()*(-2),max(1,int(random.random()*100)),max(1,int(random.random()*50)),max(1,int(random.random()*10))))
            continue
        new_pop = []
        for _ in population:
            a, b = selectTwoTraders(fitness,population)
            new_pop.append(altOtherReproduce(a,b,mut_rate))
        population = new_pop

    print("End Profits:")
    printPopulation(population,two=two)

def normalise(fitness):
    fitness = list(map(lambda x: max(0,x),fitness))
    totalFit = sum(fitness)
    if totalFit == 0:
        return False
    fitness = list(map(lambda x: x/totalFit,fitness))
    return fitness


def printPopulation(population,two=True):
    if two:
        for trader in population:
            print("Top: {}\tBottom: {}\tProfit: {}".format(trader.top,trader.bottom,trader.getProfit()))
    else:
        for trader in population:
            print("Top: {}, Bottom: {}, Long: {}, Short: {}, Mac: {}, Profit: {}".format(trader.top,trader.bottom,trader.long,trader.short,trader.mac,trader.getProfit()))

def selectTrader(fitness,population):
    index = -1
    r = random.random()
    while r > 0:
        if index >= len(fitness):
            index = -1
        index += 1
        r -= fitness[index]
    return copy.deepcopy(population[index])

def selectTwoTraders(fitness,population):
    first = selectTrader(fitness,population)
    second = selectTrader(fitness,population)
    return first,second

def reproduce(first,second,mut_rate):
    arr1 = getParameterArray(first)
    arr2 = getParameterArray(second)
    r = int(random.random()*len(arr1))
    newArr = arr1[r:] + arr2[:r]
    for i in range(len(newArr)):
        if random.random() < mut_rate:
            if i < 2:
                newArr[i] = ((random.random()*2)-1) + newArr[i]
            elif i == 2:
                newArr[i] = max(newArr[3]+1,int(random.random()*100))
            elif i == 3:
                newArr[i] = min(max(newArr[4]+1,int(random.random()*newArr[2])),newArr[2])
            elif i == 4:
                newArr[i] = min(newArr[3]-1,int(random.random()*newArr[3]))
    if len(newArr) == 2:
        return GATrader(first.df,first.name,newArr[0],newArr[1],first.long,first.short,first.mac)
    trader = GATrader(first.df,first.name,newArr[0],newArr[1],max(1,int(newArr[2])),max(1,int(newArr[3])),max(1,int(newArr[4])))
    return trader

def altReproduce(first,second,mut_rate):
    """
        An alternative function which take two trader objects and returns a new one with their blended DNA
        @params:
        first: the first trader
        second: the second trader
        mut_rate: the rate of mutation

    """
    if random.random() > 0.5:
        top = first.top
    else:
        top = second.top
    if random.random() > 0.5:
        bottom = first.bottom
    else:
        bottom = second.bottom
    if random.random() > 0.5:
        long = first.long
    else:
        long = second.long
    if random.random() > 0.5:
        short = first.short
    else:
        short = second.short
    if random.random() > 0.5:
        mac = first.mac
    else:
        mac = second.mac

    if random.random() < mut_rate:
        top = top * (random.random() * 2)
    if random.random() < mut_rate:
        bottom = bottom * (random.random() * 2)
    if random.random() < mut_rate:
        long = max(short,int(long * (random.random() * 2)))
    if random.random() < mut_rate:
        short = max(mac,int(short * (random.random() * 2)))
    if random.random() < mut_rate:
        mac = max(1,int(mac * (random.random() * 2)))

    trader = GATrader(first.df,first.name,top,bottom,long,short,mac)
    return trader

def altOtherReproduce(first,second,mut_rate):
    """
        An alternative function which take two trader objects and returns a new one with their blended DNA
        @params:
        first: the first trader
        second: the second trader
        mut_rate: the rate of mutation

    """

    top = blendNumbers(first.top,second.top)
    bottom = blendNumbers(first.bottom,second.bottom)
    long = int(blendNumbers(first.long,second.long))
    short = int(blendNumbers(first.short,second.short))
    mac = int(blendNumbers(first.mac,second.mac))

    if random.random() < mut_rate:
        top = top * (random.random() * 2)
    if random.random() < mut_rate:
        bottom = bottom * (random.random() * 2)
    if random.random() < mut_rate:
        long = max(short,int(long * (random.random() * 2)))
    if random.random() < mut_rate:
        short = max(mac,int(short * (random.random() * 2)))
    if random.random() < mut_rate:
        mac = max(1,int(mac * (random.random() * 2)))

    trader = GATrader(first.df,first.name,top,bottom,long,short,mac)
    return trader

def blendNumbers(first,second):
    return ((max(first,second)-min(first,second))*random.random())+min(first,second)


def getParameterArray(trader):
    return [trader.top,trader.bottom]
    #return [trader.top,trader.bottom,trader.long,trader.short,trader.mac]

#run(df)



GA(10,df.columns[5],df,0.2,two=False)

#trader = GATrader(df,"AAPL",0.1,-1.6)
#0.054623795010173115
#print(trader.getProfit())
#print(trade("AAPL",df))

#df[df.columns[3]].plot()
#plt.show()
