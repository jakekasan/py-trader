
class Monitor:
    def __init__(self,company_id,ticker,resolutions,trader):
        self.company_id = company_id
        self.ticker = ticker
        self.p_last = 0
        self.p_current = self.ticker.request(self.company_id)
        self.r_history = []
        self.beadlist = []
        self.resolutions = resolutions
        self.trader = trader
        for reso in resolutions:
            self.beadlist.append(Bead(reso,self))

    def update(self):
        self.p_last = self.p_current
        self.p_current = self.ticker.request(self.company_id)
        self.r_history = ()
        for bead in self.beadlist:
            bead.update()
        return

    def assess(self):
        intervals = []
        for bead in self.beadlist:
            conf = bead.confidence_intervals()
            if conf == False:
                return("Pass")
            for x in conf:
                intervals.append(x)
        if all(x > 0 for x in intervals):
            return("Buy")
        elif any(x < 0 for x in intervals):
            return("Sell")
        else:
            return("Pass")

class Bead:
    def __init__(self,resolution,monitor):
        self.resolution = resolution
        self.monitor = monitor
        self.stdev = 0
        self.mean = 0
        self.smoothing = 2

    def get_stdev(self):
        return(np.std(self.smooth(self.monitor.r_history[-self.resolution:],self.smoothing)))

    def get_mean(self):
        return(np.mean(self.smooth(self.monitor.r_history[-self.resolution:],self.smoothing)))

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

    def confidence_intervals(self,alpha=1.96):
        if self.resolution > len(self.monitor.r_history):
            return(False)
        margin = alpha * self.stdev * np.sqrt(self.resolution)
        return(self.mean + margin,self.mean - margin)

    def smooth(self,data,window):
        temp = []
        for i in range(len(data)):
            temp.append(np.mean(data[(max(0,i-window)):(min(len(data)-1,i+window))]))
        return(temp)

    def update(self):
        if self.resolution > len(self.monitor.r_history):
            return(False)
        self.stdev = self.get_stdev()
        self.mean = self.get_mean()
        return(True)
