import csv
import MySQLdb
import json

features_path = './fullDataset.csv'
fasta_file_path = './fasta.txt'

db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="root",
                     db="pyfeat_features")

cursor = db.cursor()

with open(fasta_file_path, 'r') as fasta_file, open(features_path, 'r') as features_file:
    reader = csv.reader(features_file)
    rows_list = list(reader)
    counter = 0
    for line in fasta_file:
        line = line.strip()
        if line.startswith('>'):
            protein_id = line.split('>')[1]
            features = rows_list[counter][:-1]  # the last col is class which is not used!
            features_json = json.dumps(features)

            sql = "INSERT INTO protein (protein_id, features_json) VALUES (%s, %s)"
            val = (protein_id, features_json)
            cursor.execute(sql, val)

            db.commit()

            print(counter)
            counter += 1
