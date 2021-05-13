import itertools
import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier
import sys
import os
import csv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


train_file_path = "/home/taha/PycharmProjects/final_bio_helper/MachineLearning/machine_data_1.csv"
covid_file_path = "./data/output/machine_data_with_positive_human_without_class.csv"

output_file_path = './data/output/covid_predictions.csv'
output_file = open(output_file_path, 'w')
writer = csv.writer(output_file)


reader1, reader2 = itertools.tee(csv.reader(open(train_file_path, 'r'), delimiter=','))
num_columns = len(next(reader1))
del reader1
del reader2

feature_cols = [str(x) for x in range(1, num_columns)]
col_names = feature_cols + ['label']

all_data = pd.read_csv(train_file_path, header=None, names=col_names)
all_data = all_data.sample(frac=1).reset_index(drop=True)
chunked_data = np.array_split(all_data, 4)

covid_data = pd.read_csv(covid_file_path, header=None, names=feature_cols)

data_tuples = (
    (pd.concat([chunked_data[0], chunked_data[1], chunked_data[2]], ignore_index=True), chunked_data[3]),
    (pd.concat([chunked_data[1], chunked_data[2], chunked_data[3]], ignore_index=True), chunked_data[0]),
    (pd.concat([chunked_data[2], chunked_data[3], chunked_data[0]], ignore_index=True), chunked_data[1]),
    (pd.concat([chunked_data[3], chunked_data[0], chunked_data[1]], ignore_index=True), chunked_data[2])
)


def create_decision_tree(x_train, x_test, y_train, y_test):
    clf = DecisionTreeClassifier()
    clf = clf.fit(x_train, y_train)
    y_pred = clf.predict(x_test)
    accuracy = metrics.accuracy_score(y_test, y_pred)
    covid_pred = clf.predict(covid_data)

    print("Accuracy: {}".format(accuracy))
    print("\n")
    print(covid_pred)
    print("\n\n")
    writer.writerow(covid_pred)


for item in data_tuples:
    create_decision_tree(
        item[0][feature_cols],
        item[1][feature_cols],
        item[0].label,
        item[1].label
    )

output_file.close()
