import csv
import random

# Configs
covid_fasta_file_path = 'data/input/formatted_covid_proteins.fasta'
host_file_path = 'data/input/negative_set_1.csv'
output_file_path = 'data/output/interactions.csv'
output_file_field_names = ['host_id', 'pathogen_id', 'host_sequence', 'pathogen_sequence']
NUM_INTERACTIONS = 100


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


with open(host_file_path, 'r') as positive_set_file, open(output_file_path, 'w') as output_file:
    interaction_pairs = []
    covid_id_seq_pairs = get_id_sequence_pairs(covid_fasta_file_path)

    reader = csv.reader(positive_set_file)
    positive_data_list = list(reader)[1:]

    writer = csv.DictWriter(output_file, fieldnames=output_file_field_names)
    writer.writeheader()

    remaining_interactions = NUM_INTERACTIONS

    while remaining_interactions > 0:
        host_index = random.randint(0, len(positive_data_list) - 1)
        covid_index = random.randint(0, len(covid_id_seq_pairs) - 1)
        host_id = positive_data_list[host_index][0]
        host_seq = positive_data_list[host_index][2]
        covid_id = covid_id_seq_pairs[covid_index][0]
        covid_seq = covid_id_seq_pairs[covid_index][1]

        if (host_id, covid_id) not in interaction_pairs:
            interaction_pairs.append((host_id, covid_id))
            writer.writerow({
                'host_id': host_id,
                'pathogen_id': covid_id,
                'host_sequence': host_seq,
                'pathogen_sequence': covid_seq,
            })
            remaining_interactions -= 1
            print(remaining_interactions)
