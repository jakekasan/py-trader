import numpy as np
import pandas as pd


class Trader:
    def __init__(self,ticker,wallet):
        self.holdings = []
        self.ticker = ticker
        self.currentTime = self.ticker.get_time()
        self.wallet = wallet
        self.net_value = wallet
        self.monitors = []
        self.autopilot = False
        for company in self.ticker.companies:
            self.monitors.append(Monitor(company,self.ticker))

    def goLong(self,company_id,volume,monitor):
        self.wallet -= volume * self.ticker.request(company_id)
        self.holdings.append(Holding(self.ticker,company_id,self.currentTime,volume,monitor))

    def goShort(self,company_id,volume):
        pass

    def update(self):
        self.currentTime = self.ticker.get_time()
        temp = 0
        for item in self.holdings:
            item.update()
            temp += item.get_net()
        self.net_value = temp
        print("%s : Current value of portfolio: %f" % (self.currentTime,self.net_value))
        self.decision_maker()

    def status(self):
        print("Trader up and running")
        print("\t%i monitors on, %i items in holding" % (len(self.monitors),len(self.holdings)))

    def decision_maker(self):
        for monitor in self.monitors:
            result = monitor.assess()
            if result != False and result < 0:
                print("An excessive p-value was found: %f" % result)

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
        return(self.current_price * self.volume)

    def get_net(self):
        return((self.current_price-self.purchase_price) * self.volume)

    def update(self):
        self.value = self.get_value()
        self.current_price = self.ticker.request(self.company_id)
        self.p_history.append(self.current_price)
        self.monitor.update()

class Monitor:
    def __init__(self,company_id,ticker,resolutions=[10,20,100]):
        self.company_id = company_id
        self.ticker = ticker
        self.p_history = []
        self.p_history.append(self.ticker.request(self.company_id))
        self.r_history = []
        self.r_history.append(0)
        self.beadlist = []
        self.resolutions = resolutions
        self.position = None
        for reso in resolutions:
            self.beadlist.append(Bead(reso,self))

    def update(self):
        self.p_history.append(self.ticker.request(self.company_id))
        self.r_history.append(self.p_history[len(self.p_history)]-self.p_history[len(p_history)-1])
        for bead in self.beadlist:
            bead.update()
        return

    def assess(self):
        p_values = []
        for bead in self.beadlist:
            p_values.append(bead.hypo_test())
        if False in p_values:
            return(False)
        return(np.mean(p_values))

class Bead:
    def __init__(self,resolution,monitor):
        self.resolution = resolution
        self.monitor = monitor
        self.stdev = 0
        self.mean = 0

    def get_stdev(self):
        return(np.std(self.monitor.r_history[-resolution:]))

    def get_mean(self):
        return(np.mean(self.monitor.r_history[-resolution:]))

    def hypo_test(self):
        if self.resolution > len(self.monitor.r_history):
            return(False)
        # SE = stdev / sqrt( resolution )
        # DF = resolution - 1
        # t-stat = (mean/hypo-mean) / SE
        t = (self.mean - 0) / (self.stdev / np.sqrt(self.resolution))
        s = np.random.standard_t((self.resolution-1),size=10000)
        p = np.sum(s<t) / float(len(s))
        return(p)

    def update(self):
        if self.resolution > len(self.monitor.r_history):
            return(False)
        self.stdev = self.get_stdev()
        self.mean = self.get_mean()
        return(True)
