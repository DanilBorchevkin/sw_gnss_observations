import csv
from collections import defaultdict
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.basemap import Basemap

def parse_observations(in_path, in_filename):
    in_data = []

    print("Parse observations to hte dictionary")
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

    return observations

def save_observations_to_files(observations, out_path):
    print("Save observations to files")
    # At this point we have separated data to keys in output dictionary
    # Write all files based on keys in dictionary 
    for key, value in observations.items():
        print("Writing {} file".format(key))
        with open(out_path + key + '.txt', 'w') as out_file:
            csv_writer = csv.writer(out_file, delimiter='\t', lineterminator='\n')
            csv_writer.writerows(value)

def save_passage_graphs(observations, base_lat, base_long, output_path):
    data = observations["KIR00315_1_1"]
    print(data)

    timestamps = []
    timestamps_ticks = []
    lats = []
    longs = []

    for line in data:
        timestamps.append(line[1])
        lats.append(float(line[4]))
        longs.append(float(line[5]))

    timestamps_ticks = range(len(timestamps))

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax = fig.add_subplot(111, projection='3d')

    ax.plot(longs, timestamps_ticks, lats)

    ax.set_xlabel('Longs')
    ax.set_ylabel('Time')
    ax.set_zlabel('Lats')

    #plt.yticks(timestamps_ticks, timestamps)
    plt.yticks([timestamps_ticks[0], timestamps_ticks[-1]], [timestamps[0], timestamps[-1]])

    plt.show()

def save_passage_graphs_at_map(observations, base_lat, base_long, output_path, outstand=5000000):
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
            lat_0=base_lat, lon_0=base_long )

        # Plot passage path
        x,y = m(longs,lats)
        m.plot(x, y, linewidth=5, color='r') 

        # Plot base point
        x,y = m(base_long, base_lat)
        m.plot(x, y, 'g^', markersize=12)
        plt.text(x+120000, y+120000, "Station", color='green', fontsize=14, fontweight='bold')

        # Plot title
        plt.title(key)
        #m.plot(longs,lats,linewidth=1.5,color='r')

        # Nasa-style or shaded relief
        m.bluemarble()
        #m.shadedrelief()

        #plt.show()
        plt.savefig("{}{}.png".format(output_path, key))

        # Delete passage to prevent multi-passages on one graph
        plt.clf()

def main():
    print("Script is started")

    # Change parameters here
    input_path = "./input/"
    filename = "KIR00315_Y.txt"
    output_path = "./output/"
    base_lat = 55.0
    base_long = 35.0

    # Parse observations to defaultdict
    observations = parse_observations(input_path, filename)
    # Save observations to files
    save_observations_to_files(observations, output_path)
    # Save passage graphics for observations. Outstand is a value in meters for region which we draw on map - width and height of map in meters with base in center
    save_passage_graphs_at_map(observations, base_lat, base_long, output_path, outstand=5000000)

    print("Script is ended")

if __name__ == "__main__":
    main()