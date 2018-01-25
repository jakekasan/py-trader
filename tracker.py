import numpy as np
import pandas as pd


class Trader:
    def __init__(self,ticker,wallet):
        self.holdings = []
        self.ticker = ticker
        self.currentTime = self.ticker.get_time()
        self.wallet = float(wallet)
        self.net_value = wallet
        self.monitors = []
        self.autopilot = False
        for company in self.ticker.companies:
            self.monitors.append(Monitor(company,self.ticker,[10],self))

    def goLong(self,company_id,volume,monitor):
        if self.ticker.request(company_id) == np.nan:
            return
        print(str(self.currentTime).split("T")[0] + " : \tBuying " + str(company_id) + " @ " + str(monitor.p_history[-1]))
        monitor.position = "Long"
        self.wallet -= float(volume * self.ticker.request(company_id))
        self.holdings.append(Holding(self.ticker,company_id,self.currentTime,volume,monitor))
        self.monitors.remove(monitor)

    def sellLong(self,holding):
        print(str(self.currentTime).split("T")[0] + " : \tSelling " + str(holding.company_id) + " @ " + str(holding.value))
        self.wallet += holding.get_value()
        self.monitors.append(holding.monitor)
        self.holdings.remove(holding)
        del holding

    def goShort(self,company_id,volume):
        pass

    def update(self):
        for monitor in self.monitors:
            monitor.update()
        self.currentTime = self.ticker.get_time()
        temp = 0
        for item in self.holdings:
            item.update()
            temp += item.get_net()
        self.net_value = temp
        #print("%s : Current value of portfolio: %f" % (self.currentTime,self.net_value))
        self.decision_maker()

    def status(self):
        print("%s\tTrader up and running - wallet is at: %s" % (str(self.currentTime).split("T")[0],self.wallet))
        #print("\t%i monitors on, %i items in holding" % (len(self.monitors),len(self.holdings)))

    def decision_maker(self):
        for monitor in self.monitors:
            if(monitor.assess()) == "Buy":
                self.goLong(monitor.company_id,1,monitor)

class Holding:
    def __init__(self,ticker,company_id,time_invested,volume,monitor):
        self.time_invested = time_invested
        self.company_id = company_id
        self.volume = volume
        self.ticker = ticker
        self.purchase_price = ticker.request(self.company_id)
        self.current_price = self.purchase_price
        self.value = 0
        self.p_history = []
        self.p_history.append(self.current_price)
        self.monitor = monitor

    def get_value(self):
        return(float(self.current_price * self.volume))

    def get_net(self):
        return(float((self.current_price-self.purchase_price) * self.volume))

    def update(self):
        self.value = self.get_value()
        self.current_price = self.ticker.request(self.company_id)
        self.p_history.append(self.current_price)
        self.monitor.update()
        if(self.monitor.assess()) == "Sell":
            self.monitor.trader.sellLong(self)
