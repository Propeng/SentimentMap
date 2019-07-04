import pandas as pd
import csv

import utils

with open("trainingdata.csv", "r") as csv_file:
    reader = csv.DictReader(csv_file, fieldnames=["polarity", "id", "date", "query", "username", "text"])
    data = [row for row in reader]

data_subset = data[0:5000] + data[len(data)-5000:len(data)]

df = pd.DataFrame(data_subset)
df.set_index('id', drop = True, inplace=True)

df['filtered_text'] = df.apply(utils.process, axis=1)
df.to_pickle("./training.pkl")
