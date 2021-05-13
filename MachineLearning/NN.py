import csv
import itertools

import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn import metrics
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

filename = "path to train data, e.g. train_1.csv"
# filename = "/home/taha/PycharmProjects/biohelper/FeatureExtractor/data/ml_data/mmkgapdata/train_1.csv"
test_filename = "path to test data, e.g. test_1.csv"
# test_filename = "/home/taha/PycharmProjects/biohelper/FeatureExtractor/data/ml_data/mmkgapdata/test_1.csv"

# This part is only to get the number of columns of data before reading it
reader1, reader2 = itertools.tee(csv.reader(open(filename, 'r'), delimiter=','))
num_columns = len(next(reader1))
del reader1
del reader2

feature_cols = [str(x) for x in range(1, num_columns)]
col_names = feature_cols + ['label']
# load dataset
data = pd.read_csv(filename, header=None, names=col_names)
test_data = pd.read_csv(test_filename, header=None, names=col_names)

######################## Selecting best features ##############################

X = data[feature_cols]
y = data.label

X_test = test_data[feature_cols]
y_test = test_data.label

clf = MLPClassifier()

clf = clf.fit(X, y)

# Predict the response for test dataset
y_pred = clf.predict(X_test)

# Model Accuracy, how often is the classifier correct?
print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
print("Precision:", metrics.precision_score(y_test, y_pred))
print("Recall:", metrics.recall_score(y_test, y_pred))
print("F1_score:", metrics.f1_score(y_test, y_pred))
