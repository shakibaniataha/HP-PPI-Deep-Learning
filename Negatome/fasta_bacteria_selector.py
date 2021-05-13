def format_output_data(header, sequence):
    return '>' + header.split('|')[1] + "\n" + sequence + "\n"


with open('data/uniprot/input/all_proteins.fasta', 'r') as data_file, open(
        'data/uniprot/output/bacteria_proteins.fasta', 'w') as output_file:
    sequence = ''
    header = ''
    count = 0
    for line in data_file:
        line = str(line.strip())
        if line.startswith('>'):
            if sequence != '':
                if 'bacter' in header:
                    count += 1
                    print(count)
                    output_file.write(format_output_data(header, sequence))
                sequence = ''

            header = line

        else:
            sequence += line
