
class Monitor:
    def __init__(self,company_id,ticker,trader):
        self.company_id = company_id
        self.ticker = ticker
        self.p_last = 0
        self.p_current = self.ticker.request(self.company_id)
        self.r_history = []
        self.trader = trader
        self.strategies = [Strategy(self)]

    def update(self):
        self.p_last = self.p_current
        self.p_current = self.ticker.request(self.company_id)
        self.r_history = ()
        for strat in self.strategies:
            strat.update()
        return

    def get_smooth_data(self,length,window):
        return(self.running_mean())

    def running_mean(x,n):
        cs = np.cumsum(np.insert(x,0,0))
        return((cs[n:] - cs[:-n])/float(n))

    def assess(self):
        for strat in self.strategies:
            if strat.assess() == "Buy":
                self.monitor.goLong(self.company_id,1,self)
