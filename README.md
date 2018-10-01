# Roche Biochemical Pathway Generator

## Overview

Generates a downloadable full size image of BOTH the Roche's biochemical pathway using the segments provided. This includes the metabolic pathway AND the cellular and molecular pathway. The origin of all the data is from [here](http://biochemical-pathways.com).

The file generated will be the full size image (maximum zoom) with the grid lines at the bottom. If you do not like grid lines, please go into the python file and delete `grid` from the `features` list.

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
