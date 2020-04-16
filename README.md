# Roche Biochemical Pathway Generator

## NOTE

Recently I discovered that the files can be downloaded directly from [https://www.roche.com/sustainability/philanthropy/science_education/pathways/pathways-ordering.htm](here), thus making this tool obsolete.

## Overview

Generates a downloadable full size image of BOTH the Roche's biochemical pathway using the segments provided. This includes the metabolic pathway AND the cellular and molecular pathway. The origin of all the data is from [here](http://biochemical-pathways.com).

The file generated will be the full size image (maximum zoom) with the grid lines at the bottom. If you do not like grid lines, you are able to modify the operations in the `crawler.py` file.

Metabolic pathway preview:

![metabolic pathway](https://raw.githubusercontent.com/ZijunH/Roche_Biochemical_Pathway_generator/master/prev1.png)

Cellular and molecular pathway preview:

![cellular and molecular pathway](https://raw.githubusercontent.com/ZijunH/Roche_Biochemical_Pathway_generator/master/prev2.png)


## Requirements

- `python 3`
- At least 16GB of Ram
- At least 350MB of file space
- At least 1 hour of uninterrupted PC time (tested on overclocked i5-7600k)

Note: This particular program is extremely memory intensive, requiring at least 8GB to run the program alone. This is due to the formation of the final image, where the entire image is stored in memory, requiring 4 * 55000 * 39000 bytes. If you can find a way to solve this issue, please submit a pull request.

In fact, if you can find a way to optimise any problem while acheiving the desired outcome (downloadable full size image), please submit a pull request.

## How to use

1. Install python 3

2. Install the required libraries by typing the following in the command prompt (bash or cmd or powershell):

```
pip install -r requirements.txt
```

3. Run the python file:

```
python3 crawler.py
```

4. Enjoy :)

## Customisation

The following stuff should be implemented using different flags, but I am lazy, so you need to do all of them yourself.

- You can add or remove grid lines by deleting `grid` from the `features` list.

- You can change the white border around the image by changing `TOP_BOT_BORDER` and `LEFT_RIGHT_BORDER`.

- You can add or remove features by removing stuff in the `features` list. The order is from the lowest layer to the highest layer.

- You can change the zoom level (default is 6, the maximum zoom) by editing the sizes in `maps` and changing the `6` in `url_maker` to what you want.
