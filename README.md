## FPL Lineup Optimizer
This Fantasy Premier League lineup optimiser optimises a lineup based on some constraints and a given objective. It currently uses the 2020/2021 season's player prices and the 2019/2020 season's points scored, and maximises the total points of all players in a lineup while staying within a specified budget and conforming to other FPL rules and constraints defined by the user.

## Usage
1. Clone this repository - `git clone "https://github.com/ChrisMusson/FPL_Optimiser"`
2. Install requirements from txt file - `pip install -r requirements.txt`
3. Run `get_data.py`. This will create a `players_data.csv` file containing information about every player in FPL this season, along with their points from last season. If you want to optimise something other than points from last season, then you can replace this final column with something else - the optimiser will still run so long as the csv file stays in the same format and the column headers remain unchanged.
4. Open `optimiser.py` and change the arguments to the optimise function (a list of all available arguments can be found in the function's docstring). Run the program, and a dataframe containing the optimised lineup will be printed to the command line.

## Example
#### Input:
```
optimise(
    budget=82,
    teamsize=11,
    in_team=["Salah", "Vinagre", 259],
    out_team=["Lundstram", 1],
    GK=1,
    MID=4
    )
```

#### Output:
|    |   id | team        | pos   | name             |   cost |   points |
|---:|-----:|:------------|:------|:-----------------|-------:|---------:|
|  1 |   96 | Burnley     | G     | Pope             |    5.5 |      170 |
|  2 |  259 | Liverpool   | D     | Alexander-Arnold |    7.5 |      210 |
|  3 |  250 | Liverpool   | D     | van Dijk         |    6.5 |      178 |
|  4 |  457 | Wolves      | D     | Doherty          |    6   |      167 |
|  5 |   81 | Burnley     | D     | Tarkowski        |    5.5 |      143 |
|  6 |  471 | Wolves      | D     | Vinagre          |    4.5 |       32 |
|  7 |  272 | Man City    | M     | De Bruyne        |   11.5 |      251 |
|  8 |  254 | Liverpool   | M     | Salah            |   12   |      233 |
|  9 |  478 | Arsenal     | M     | Willian          |    8   |      168 |
| 10 |   89 | Burnley     | M     | Westwood         |    5.5 |      118 |
| 11 |  366 | Southampton | F     | Ings             |    8.5 |      198 |

Total cost: £81.0m  
Total points: 1868