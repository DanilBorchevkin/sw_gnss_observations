# sw_gnss_observations

GNSS observations converter 

## Licence

BSD-2 Clause. Please see the LICENCE file.

## Dependencies

* ***numpy***

* ***matplotlib***

* ***mpl_toolkits.basemap***. For install use ```conda install -c anaconda basemap```

## Basemap problem

In case of error ***Key ERROR - PROJ_LIB*** please check this [woorkaround](https://ctcoding.wordpress.com/2019/01/29/solved-proj_lib-error-when-installing-basemap-on-windows-using-anaconda/)

Short overview:

1. Save [this file](https://github.com/matplotlib/basemap/blob/master/lib/mpl_toolkits/basemap/data/epsg) to the mpl_toolkit folder (for example *C:\software\Miniconda3\Lib\site-packages\mpl_toolkits\basemap*)

1. Add the following lines of code to the script

```
os.environ['PROJ_LIB'] = 'C:/software/Miniconda3/Lib/site-packages/mpl_toolkits/basemap'
```

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