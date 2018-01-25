

class Strategy:
    def __init__(self,monitor):
        self.monitor = monitor
        self.data = []
        self.window = 2
        self.threshold = 10
        self.built = False
        self.mean = None
        self.stdev = None
        pass

    def add_data(self,point):
        self.data = self.data[1:-(window)] + [sum(self.monitor.r_history[-(x):])/(x) for x in range(window+window+1,window,-1)]
        pass

    def init_data(self,data):
        self.data = [sum([ x/(max(0,i-2)+(i+2)) for x in data[max(0,i-2):(i+2)] ] for i in range(len(data)))]
        pass

    def build(self):
        self.mean = sum(self.data)/threshold
        self.stdev = np.std(self.data)
        np.polyfit(self.data,[range(1,self.threshold+1)])

    def update(self):
        if threshold < len(self.monitor.r_history):
            return None
        if self.built == False:
            init_data()
        self.data = self.data[1:-(window)] + [sum(self.monitor.r_history[-(x):])/(x) for x in range(window+window+1,window,-1)]
        pass
