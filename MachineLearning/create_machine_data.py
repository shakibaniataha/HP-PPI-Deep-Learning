import csv
import json
import MySQLdb


db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="root",
                     db="pyfeat_features")

cursor = db.cursor()

input_files = (
    ('../Negatome/data/interaction_generation/input/positive_set.csv', 1),
    ('../Negatome/data/interaction_generation/output/negative_set_3.csv', 0),
)

output_file_path = './machine_data_3.csv'

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


with open(output_file_path, 'w') as output_file:
    writer = csv.writer(output_file)

    row_count = 0
    for item in input_files:
        file_path = item[0]
        data_class = item[1]

        csv_file = open(file_path, 'r')
        reader = csv.DictReader(csv_file)

        for row in reader:
            host_features = get_features(row['host_id'])
            pathogen_features = get_features(row['pathogen_id'])

            output_row = host_features + pathogen_features + [data_class]
            writer.writerow(output_row)

            row_count += 1
            print(row_count)

        csv_file.close()
