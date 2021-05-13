import csv
import itertools
import pandas as pd


file = './machine_data_1.csv'

# This part is only to get the number of columns of data before reading it
reader1, reader2 = itertools.tee(csv.reader(open(file, 'r'), delimiter=','))
num_columns = len(next(reader1))
del reader1
del reader2

feature_cols = [str(x) for x in range(1, num_columns)]
col_names = feature_cols + ['label']
# load dataset
data = pd.read_csv(file, header=None, names=col_names)
