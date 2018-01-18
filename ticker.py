import time
import numpy as np
import pandas as pd
import datetime as dt


FILE_PATH = "../data-science/data/nyse/"

FILE = "prices.csv"

def createDataset(FULL_FILEPATH,name_col="symbol",closing_col="close"):
    data_raw = pd.read_csv(FULL_FILEPATH)
    data_new = pd.DataFrame()
    companies_index = data_raw[name_col].unique()
    # establish date index
    data_new["date"] = pd.to_datetime(data_raw.loc[data_raw[name_col]==companies_index[1],"date"].values)

    # fix date index in raw data
    data_raw["date"] = pd.to_datetime(data_raw["date"])

    # initialize empty columns
    data_raw = data_raw.set_index("date")
    data_new = data_new.set_index("date")

    for company in companies_index:
        data_new[company] = [np.nan for _ in range(len(range(data_new.shape[0])))]

    print(data_new.head(5))

    for company in companies_index:
        temp = data_raw.loc[(data_raw[name_col]==company),closing_col]
        data_new.loc[temp.index,company] = temp.values
    print(data_new.head(10))

    try:
        data_new.to_csv("price_movements.csv")
        print("Wrote to file")
    except:
        print("Could not write file")


def tick(company_id,last_date,dataset):
    if (last_data + dt.datetime(0,0,1)) not in dataset.index.values:
        return(dataset[company_id])

class Ticker:

    startup_greeting = "\nNew ticker started.\n"

    def __init__(self,data):
        self.companies = []
        self.data = data
        for comp in data.columns:
            self.companies.append(comp)
        self.currentTime = data.index.values[0]
        print("Up and running at %s" % (str(self.currentTime).split("T")[0]))

    def request(self,company_id):
        if self.currentTime not in self.data.index.values:
            print("Market is closed")
            return
        print(str(company_id) + "  " + str(self.data[company_id][self.currentTime]))
        return(self.data[company_id][self.currentTime])

    def tick(self):
        self.currentTime += np.timedelta64(1,"D")
        pass

    def get_time(self):
        return(self.currentTime)

    def status(self):
        print("Up and running at %s" % (str(self.currentTime).split("T")[0]))
        print("Listing %i companies." % len(self.companies))
        #for comp in self.companies:
            #print(comp)
