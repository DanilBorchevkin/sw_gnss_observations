import csv
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap

class FileMetadata:
    def __init__(self, metadataList):
        self.baseName = metadataList[0]
        self.baseLat = float(metadataList[1])
        self.baseLong = float(metadataList[2])
        self.year = int(metadataList[3])
        self.month = int(metadataList[4])
        self.day = int(metadataList[5])
        self.sources = metadataList[6]
    
    def getDate(self):
        return "{:02d}.{:02d}.{}".format(self.day, self.month, self.year) 

def parse_row_to_list(row):
    '''
    This function extract only meaningful members from list
    For example - we have tle following list:
    ['', '', '16', '', '', '11.1']
    The output will be:
    ['16', '11.1']
    '''
    clean_row = []
    for member in row:
        if member != '':
            clean_row.append(member)

    return clean_row

def parse_observations(in_path, in_filename):
    in_data = []
    metadata = None

    print("Parse observations to hte dictionary")
    # Open input file and read only data from it
    with open(in_path + in_filename, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=' ')

        for i,row in enumerate(csv_reader):
            if i == 0:
                # Info section. Parse it to metadata class
                metadata = FileMetadata(parse_row_to_list(row))
            elif i == 1:
                # Header. Pass it
                continue
            else:
                # Data rows.
                # We parse file with ' ' delimiter. so we have '' members of list
                # We should delete it and save only meaningful data               
                in_data.append(parse_row_to_list(row))
    
    # At this point we have cleared and right separated lines
    # Now we should separate data by sputnik and it's roundtrips
    out_file_start = in_filename.split('_')[0]
    round_trips = defaultdict(int)
    observations = defaultdict(list)
    prevous_sputnik = ''
    current_sputnik = ''

    for observation in in_data:
        current_sputnik = observation[0]

        if current_sputnik != prevous_sputnik:
            round_trips[current_sputnik] += 1
        
        observations['{}_{}_{}'.format(out_file_start, 
                                            str(round_trips[current_sputnik]), 
                                            str(current_sputnik))
        ].append(observation)

        prevous_sputnik = observation[0]

    return (observations, metadata)

def save_observations_to_files(observations, out_path):
    print("Save observations to files")
    # At this point we have separated data to keys in output dictionary
    # Write all files based on keys in dictionary 
    for key, value in observations.items():
        print("Writing {} file".format(key))
        with open(out_path + key + '.txt', 'w') as out_file:
            csv_writer = csv.writer(out_file, delimiter='\t', lineterminator='\n')
            csv_writer.writerows(value)

def save_passage_graphs(observations, metadata, output_path):
    data = observations["KIR00315_1_1"]
    print(data)

    lats = []
    longs = []

    for line in data:
        lats.append(float(line[4]))
        longs.append(float(line[5]))

    fig, ax = plt.subplots()
    ax.plot(lats, longs)

    # Set labels for graphs
    ax.set(xlabel='Lats, grads', 
            ylabel='Longs, grads',
            title='KIR03015')

    ax.grid()

    plt.show()

def save_passage_graphs_at_map(observations, metadata, output_path, outstand=5000000):
    print("Start plot and save graphs")

    for key, data in observations.items():
        print("Plotting {} file".format(key))

        lats = []
        longs = []

        for line in data:
            lats.append(float(line[4]))
            longs.append(float(line[5]))

        m = Basemap(projection="lcc", resolution='l',
            width=outstand, height=outstand,
            lat_0=metadata.baseLat, lon_0=metadata.baseLong )

        # Plot passage path
        x,y = m(longs,lats)
        m.plot(x, y, linewidth=4, color='r') 

        # Plot base point
        x,y = m(metadata.baseLong, metadata.baseLat)
        m.plot(x, y, 'r^', markersize=8)
        #plt.text(x+120000, y+120000, "Station", color='green', fontsize=8, fontweight='bold')

        # Plot title
        plt.title(key)

        # Nasa-style
        #m.bluemarble()

        # Shaded relief style
        #m.shadedrelief()
        
        # Countries and coasts
        m.drawcoastlines()
        m.drawcountries()

        # Show parrarelts and meridians
        parallels = np.arange(0.,81,5.)
        m.drawparallels(parallels,labels=[False,True,False,False])
        meridians = np.arange(0.,351.,10.)
        m.drawmeridians(meridians,labels=[False,False,False,True])

        #plt.show()
        plt.savefig("{}{}_{}.png".format(output_path, key, "map"))

        # Delete passage to prevent multi-passages on one graph
        # For show on graphs each prevous passages please comment this line
        plt.clf()

def main():
    print("Script is started")

    # Change parameters here
    input_path = "./input/"
    filename = "KIR00315_Y.txt"
    output_path = "./output/"

    # Parse observations to defaultdict and get metadata from file
    observations, metadata = parse_observations(input_path, filename)
    # Save observations to files
    save_observations_to_files(observations, output_path)
    # Save passage graphics for observations. Outstand is a value in meters for region which we draw on map - width and height of map in meters with base in center
    #save_passage_graphs(observations, metadata, output_path)
    save_passage_graphs_at_map(observations, metadata, output_path, outstand=2000000)

    print("Script is ended")

if __name__ == "__main__":
    main()