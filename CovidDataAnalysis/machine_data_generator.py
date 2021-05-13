import csv
import json

import MySQLdb

db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="root",
                     db="pyfeat_features")

interactions_file_path = 'data/output/interactions_with_negative_human.csv'
machine_data_file_path = 'data/output/machine_data_without_class.csv'

cursor = db.cursor()

features_table = 'protein'


def get_features(protein_id):
    global features_table
    global cursor
    cursor.execute("select features_json from " + features_table + " where protein_id = '" + protein_id + "'")
    features_obj = cursor.fetchone()
    if not features_obj:
        raise Exception("Could not find features for protein_id {}".format(protein_id))

    features_json = json.loads(features_obj[0])

    return features_json


with open(interactions_file_path, 'r') as interactions_file, open(machine_data_file_path, 'w') as machine_data_file:
    reader = csv.DictReader(interactions_file)
    writer = csv.writer(machine_data_file)

    for row in reader:
        host_features = get_features(row['host_id'])
        pathogen_features = get_features(row['pathogen_id'])

        output_row = host_features + pathogen_features
        writer.writerow(output_row)
