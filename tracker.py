class Tracker:
    def __init__(self,ticker,wallet):
        self.holdings = []
        self.ticker = ticker
        self.currentTime = ticker.get_time()
        self.wallet = wallet
        pass

    def newHolding(self,company_id,time_invested):
        self.holdings.append(Holding(self.ticker,company_id,self.currentTime,volume,))
        pass

    def update(self):
        for item in self.holdings:
            item.update()

    def status(self):
        pass

class Holding:
    def __init__(self,ticker,company_id,time_invested,volume,purchase_price):
        self.time_invested = time_invested
        self.company_id = company_id
        self.volume = volume
        self.ticker = ticker
        self.purchase_price = ticker.request(self.company_id)
        self.current_price = self.purchase_price
        self.p_history = []


    def get_value(self):
        return

    def update(self):
        self.p_history.append(self.current_price)
        self.purchase_price = self.ticker.request(self.company_id)
