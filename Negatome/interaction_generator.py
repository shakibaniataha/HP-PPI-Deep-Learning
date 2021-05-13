import csv
import random


def get_id_sequence_pairs(filepath):
    pairs = []
    with open(filepath, 'r') as input_file:
        for line in input_file:
            line = line.strip()
            if line.startswith('>'):
                header = line.split('>')[1]
            else:
                pairs.append([header, line])

    return pairs


positive_set_file_path = 'data/interaction_generation/input/positive_set.csv'

negative_human_file_path = 'data/interaction_generation/input/negative_human.fasta'
negative_bacteria_file_path = 'data/interaction_generation/input/negative_bacteria.fasta'

negative_interactions_file_path = 'data/interaction_generation/output/negative_set.csv'
negative_interactions_field_names = ['host_id', 'pathogen_id', 'host_sequence', 'pathogen_sequence']

human_id_seq_pairs = get_id_sequence_pairs(negative_human_file_path)
bacteria_id_seq_pairs = get_id_sequence_pairs(negative_bacteria_file_path)
output_pairs = []
f_all_data = open(positive_set_file_path)
all_data_reader = list(csv.DictReader(f_all_data))
total_interactions = len(all_data_reader)

for row in all_data_reader:
    temp = (row['host_id'], row['pathogen_id'])
    output_pairs.append(temp)

remaining_interactions = total_interactions

with open(negative_interactions_file_path, 'w') as output_file:
    writer = csv.DictWriter(output_file, fieldnames=negative_interactions_field_names)
    writer.writeheader()

    while remaining_interactions > 0:
        host_index = random.randint(0, len(human_id_seq_pairs) - 1)
        pathogen_index = random.randint(0, len(bacteria_id_seq_pairs) - 1)
        host_id = human_id_seq_pairs[host_index][0]
        host_seq = human_id_seq_pairs[host_index][1]
        pathogen_id = bacteria_id_seq_pairs[pathogen_index][0]
        pathogen_seq = bacteria_id_seq_pairs[pathogen_index][1]

        if (host_id, pathogen_id) not in output_pairs:
            output_pairs.append((host_id, pathogen_id))
            writer.writerow({
                'host_id': host_id,
                'pathogen_id': pathogen_id,
                'host_sequence': host_seq,
                'pathogen_sequence': pathogen_seq,
            })
            remaining_interactions -= 1
            print(remaining_interactions)

f_all_data.close()
