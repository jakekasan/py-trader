import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv("./price_movements.csv")
df["date"] = pd.DatetimeIndex(df["date"])
df.set_index("date")

print(df["date"].index)

#print(df.tail())
#df.plot(y="AAPL")
#plt.show()

#print(df.columns)

def getMacd(stock,df):
    temp = pd.DataFrame()

    temp["{}".format(stock)] = df[stock]

    temp["{}_26ema".format(stock)] = pd.ewma(df[stock],span=26)

    temp["{}_12ema".format(stock)] = pd.ewma(df[stock],span=12)

    temp["{}_MACD".format(stock)] = (temp["{}_12ema".format(stock)] - temp["{}_26ema".format(stock)])

    temp["{}_MACD_signal".format(stock)] = pd.ewma(temp["{}_MACD".format(stock)],span=9)

    return temp

#macd = getMacd("AAPL",df)

class Trader:
    def __init__(self,name):
        self.bought = False
        self.money = 0
        self.name = name

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
        if signal > 0.5:
            return 1
        elif signal < -0.5:
            return -1
        else:
            return 0

    def __str__(self):
        return ("Trader balance: {}".format(self.money))

class Population:
    def __init__(self):
        self.name = 0

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
        try:
            balance += trade(stock,df)
            #print("Stock: {} Profit: {}".format(stock,trade(stock,df)))
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            return
        except:
            failed += 1
            #print("Stock: {} Failed".format(stock))

    print("Total balance: {}".format(balance))
    print("Total failed: {}".format(failed))

#run(df)
