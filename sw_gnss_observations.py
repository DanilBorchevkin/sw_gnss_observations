import csv
from collections import defaultdict

def parse_observations(in_path, in_filename, out_path):
    in_data = []

    # Open input file and read only data from it
    with open(in_path + in_filename, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=' ')

        for i,row in enumerate(csv_reader):
            if i in [0, 1]:
                # Header. Pass it
                continue
            else:
                # Data rows. We parse file with ' ' delimiter. so we have '' members of list
                # We should delete it and save only meaningful data
                clean_row = []
                for member in row:
                    if member != '':
                        clean_row.append(member)
                
                in_data.append(clean_row)
    
    # At this point we have cleared and right separated lines
    # Now we should separate data by sputnik and it's roundtrips
    out_file_start = in_filename.split('_')[0]
    round_trips = defaultdict(int)
    output_files_data = defaultdict(list)
    prevous_sputnik = ''
    current_sputnik = ''

    for observation in in_data:
        current_sputnik = observation[0]

        if current_sputnik != prevous_sputnik:
            round_trips[current_sputnik] += 1
        
        output_files_data['{}_{}_{}'.format(out_file_start, 
                                            str(round_trips[current_sputnik]), 
                                            str(current_sputnik))
        ].append(observation)

        prevous_sputnik = observation[0]

    # At this point we have separated data to keys in output dictionary
    # Write all files based on keys in dictionary 
    for key, value in output_files_data.items():
        print("Writing {} file".format(key))
        with open(out_path + key + '.txt', 'w') as out_file:
            csv_writer = csv.writer(out_file, delimiter='\t', lineterminator='\n')
            csv_writer.writerows(value)

if __name__ == "__main__":
    print("Script is started")

    # Change parameters here
    input_path = "./input/"
    filename = "KIR00315_Y.txt"
    output_path = "./output/"

    # Start parsing 
    parse_observations(input_path, filename, output_path)

    print("Script is ended")