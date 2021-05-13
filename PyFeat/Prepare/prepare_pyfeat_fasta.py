import csv


def format_output_data(header, sequence):
    return '>' + header + "\n" + sequence + "\n"


input_file_paths = [
    'Negatome/data/interaction_generation/input/positive_set.csv',
    'Negatome/data/interaction_generation/output/negative_set_1.csv',
    'Negatome/data/interaction_generation/output/negative_set_2.csv',
    'Negatome/data/interaction_generation/output/negative_set_3.csv',
]
output_file_path = './output_fasta.txt'
output_file = open(output_file_path, 'w')
distinct_ids = []

for input_file in input_file_paths:
    data = open(input_file)
    data_reader = list(csv.DictReader(data))
    for row in data_reader:
        host_id = row['host_id']
        pathogen_id = row['pathogen_id']
        host_sequence = row['host_sequence']
        pathogen_sequence = row['pathogen_sequence']

        if host_id not in distinct_ids:
            distinct_ids.append(host_id)
            output_file.write(format_output_data(host_id, host_sequence))

        if pathogen_id not in distinct_ids:
            distinct_ids.append(pathogen_id)
            output_file.write(format_output_data(pathogen_id, pathogen_sequence))

    data.close()

output_file.close()
