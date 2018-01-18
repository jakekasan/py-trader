#!/usr/bin/env python3

import time
import numpy as np
import pandas as pd
import datetime as dt
from datetime import timedelta
from ticker import createDataset, Ticker, Tracker

FILE_PATH = "../data-science/data/nyse/"

FILE = "prices.csv"


if __name__ == "__main__":
    print("Running")

    #createDataset(str(FILE_PATH+FILE),"symbol","close")

    actual_dataset = pd.read_csv("price_movements.csv")

    actual_dataset["date"] = pd.to_datetime(actual_dataset["date"])

    actual_dataset = actual_dataset.set_index("date")

    t = Ticker(actual_dataset)

    while(True):
        t.status()
        t.tick()
        time.sleep(1)
        t.request("AAPL")
