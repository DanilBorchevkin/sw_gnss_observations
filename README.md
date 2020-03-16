# sw_gnss_observations

GNSS observations converter 

## Licence

BSD-2 Clause. Please see the LICENCE file.

## Dependencies

* ***numpy***

* ***matplotlib***

* ***mpl_toolkits.basemap***. For install use ```conda install -c anaconda basemap```

## What included

* ***./input*** - default folder for input data

* ***./output*** - default folder for output data

* ***./sw_gnss_observations.py*** - main script

## Techical requirements

### Task desctiption

There are GNSS observation stations data from several stations. Each file included all sputnik's round trip during all days. 

We need separate all round trips for each sputnik to didecated files.

Input file has name ***KIR00315_Y*** where:

* ***KIR0*** - name of station.

* ***03*** - month.

* ***15*** - day.

* ***Y*** - mark for "Observations" data.

### Requirements to output file

Output file has name ***KIR00315_1_16*** where:

* ***KIR0*** - name of station.

* ***03*** - month

* ***_1*** - number from 1 to n - number of round trip.

* ***_16*** - number of sputnik