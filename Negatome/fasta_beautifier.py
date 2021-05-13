def format_output_data(header, sequence):
    return header.split('|')[0].strip() + "\n" + sequence + "\n"


with open('data/uniprot/input/unformatted_fasta.fasta', 'r') as data_file, open(
        'data/uniprot/output/formatted_fasta.fasta', 'w') as output_file:
    sequence = ''
    header = ''
    for line in data_file:
        line = str(line.strip())
        if line.startswith('>'):
            if sequence != '':
                output_file.write(format_output_data(header, sequence))
                sequence = ''

            header = line

        else:
            sequence += line
