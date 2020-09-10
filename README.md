## FPL Lineup Optimizer
These Fantasy Premier League lineup optimisers optimise a lineup based on some constraints and a given objective. It currently uses the 2020/2021 season's player prices and the 2019/2020 season's points scored, and maximises the total points of all players in a lineup while staying within a specified budget and conforming to other FPL rules and constraints defined by the user.

## With Transfers
The `with_transfers/` folder contains instructions on how to get gameweek by gameweek data, and contains an optimiser that optimises points scored over these gameweeks, while allowing for one transfer per week. This optimiser is an extended version of `optimiser_B.py`, and contains many of the same parameters.

## Difference Between optimiser_A and optimiser_B
In optimiser_A, you can specify the teamsize and the optimiser will attempt to maximise points for all players.  

In optimiser_B, the teamsize is always 15, however you can specify a bench_strength that signifies what importance should be given to points on the bench. The optimiser maximises `(1-bench_strength)*(starting 11 points) + bench_strength*(bench points)`. In the returned dataframe, the first 11 players are the optimised lineup's 11 starting players.

**NOTE: This optimiser will only be as good as the data supplied to it - using last seasons's points scored is unlikely to be predictive of how many points players will score this season. If you want to use this to select a team, then it is highly recommended that you alter the points column in players_data.csv to something that is more predictive, such as week-on-week expected points.** 

## Usage
1. Clone this repository - `git clone "https://github.com/ChrisMusson/FPL_Optimiser"`
2. Install requirements from txt file - `pip install -r requirements.txt`
3. Run `get_data.py`. This will create a `players_data.csv` file containing information about every player in FPL this season, along with their points from last season. If you want to optimise something other than points from last season, then you can replace this final column with something else - the optimiser will still run so long as the csv file stays in the same format and the column headers remain unchanged.
4. Open `optimiser_A.py` or `optimiser_B.py` and change the arguments to the optimise function (a list of all available arguments can be found in the function's docstring). Run the program, and a dataframe containing the optimised lineup will be printed to the command line.

## Examples
### optimiser_A:
#### Input:
```
optimise(
    budget=81,
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


### optimiser_B
#### Input
```
optimise(
    DEF=4,
    in_team=["van Dijk", "vinagre", "jimenez"],
    out_team=["Lundstram"],
    banned_teams=["Burnley", "Aston Villa", "Man Utd"]
)
```

#### Output
|    |   id | team           | pos   | name             |   cost |   points |
|---:|-----:|:---------------|:------|:-----------------|-------:|---------:|
|  1 |   70 | Brighton       | G     | Ryan             |    4.5 |      135 |
|  2 |  259 | Liverpool      | D     | Alexander-Arnold |    7.5 |      210 |
|  3 |  255 | Liverpool      | D     | Robertson        |    7   |      181 |
|  4 |  250 | Liverpool      | D     | van Dijk         |    6.5 |      178 |
|  5 |  457 | Wolves         | D     | Doherty          |    6   |      167 |
|  6 |  272 | Man City       | M     | De Bruyne        |   11.5 |      251 |
|  7 |  275 | Man City       | M     | Mahrez           |    8.5 |      175 |
|  8 |  478 | Arsenal        | M     | Willian          |    8   |      168 |
|  9 |  366 | Southampton    | F     | Ings             |    8.5 |      198 |
| 10 |  460 | Wolves         | F     | Jiménez          |    8.5 |      194 |
| 11 |  140 | Crystal Palace | F     | Ayew             |    6   |      132 |
| 12 |  429 | West Ham       | G     | Martin           |    4   |       20 |
| 13 |  471 | Wolves         | D     | Vinagre          |    4.5 |       32 |
| 14 |   55 | Brighton       | M     | Stephens         |    4.5 |       63 |
| 15 |  364 | Southampton    | M     | Oriol Romeu      |    4.5 |       51 |

Total cost: £100.0m  
Total points: 1989 (+166 on the bench)