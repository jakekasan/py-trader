class Strategy:
    def __init__(self,monitor):
        self.monitor = monitor
        pass

    def add_data(self,point):
        #self.data = self.data[1:-(window)] + [sum(self.monitor.r_history[-(x):])/(x) for x in range(window+window+1,window,-1)]
        pass

    def init_data(self,data):
        #self.data = [sum([ x/(max(0,i-2)+(i+2)) for x in data[max(0,i-2):(i+2)] ] for i in range(len(data)))]
        return

    def build(self):
        # if enough data is available from the monitor, the model will build itself
        return


    def update(self):


    def assess(self):
        # return either buy, sell or neither
