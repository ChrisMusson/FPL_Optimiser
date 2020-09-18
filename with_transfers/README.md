This optimiser takes week-by-week expected points values and maximises the total expected points subject to all the usual FPL constraints, allowing for up to 2 transfers per gameweek, but never allowing for hits. As in the other optimisers, all function parameters can be found in the `optimise()` function's docstring. `optimiser_preseason.py` is the original file that could have been used to create the optimised team before the season started. `optimiser.py` is what you should use now that the season has begun.

The `optimise()` function requires a csv file with headers `[id, team, pos, name, sale_value]` along with `n_pts` for every gameweek you want to optimise for. 

## Getting the data
I would recommend using fplreview's massive data planner to get expected points data by gameweek. To do this, go to https://fplreview.com/massive-data-planner/, change projection to however many gameweeks you want to look into the future, input your team ID, submit, and then download the csv found on that page to the current working directory.

After you have done that, calling `python clean_fplreview_data.py <infile> <start_gw> <end_gw>` will create a `cleaned_data.csv` file for use in the optimiser function. Here, `infile` is the file you downloaded earlier. Note that there is currently no error checking in place for this as I had to rush to try and get this optimiser out before the start of the season, so ensure that you use it as shown above.

I have included my downloaded file `raw_fplreview_data.csv` and the cleaned version `cleaned_data.csv` in this repository, however the expected points change multiple times per day, so I would recommend that you download a more recent csv if you are going to use this optimiser.

## Running the optimiser
Now, open `optimiser.py`. In the `optimise()` function, you will see the parameters that can be edited in the function. Scroll to the bottom and change them as you see fit, and run the program.

## Warnings
Please know that this optimisation is computationally very hard (I will try and improve efficiency at a later date, but I can't promise anything), so it will take a while to calculate the optimal lineup and transfer strategy. To give you an idea, it takes me ~9 seconds to calculate for 3 gameweeks, ~50 seconds for 4 gameweeks, ~100 seconds for 5 gameweeks 1-5, etc. if `wildcard=True`. If `wildcard=False`, then it is much quicker - ~5 seconds, ~14 seconds, and ~22 seconds for 3, 4, and 5 gameweeks.

One way to make it run quicker is supplying players to `in_team` and `out_team`, as that will reduce the solution space. So if there are some players who will 100% be in your team for the whole duration that you are maximising over, then you may as well add them to `in_team`.

The optimiser currently only allows up to 2 transfers per gameweek and doesn't allow taking hits. I know that this is not perfect, but I believe that giving the optimiser the ability to take hits could make the solution space too large to be feasible. I will however look at seeing if it could work, but again, no promises.

The optimiser also doesn't account for any price changes, so there could easily be a situation where the optimiser's plan in a future gameweek will no longer work.

Finally, this is just some code that solves a mathematical optimisation problem - although a lot of work has gone into it, it's not some magical tool to pick out the best team and best transfer strategy - **make sure to think for yourself and to not blindly follow the advice it gives.**

## Example

### Input:
```
optimise(
    352,
    5,
    future_gw_multiplier=0.9,
)
```

### Output:
CURRENT SQUAD

|    |   id | team        | pos   | name             |   sale_value |   2_pts |   3_pts |   4_pts |   5_pts |   6_pts |
|---:|-----:|:------------|:------|:-----------------|-------------:|--------:|--------:|--------:|--------:|--------:|
|  0 |  363 | Southampton | G     | McCarthy         |          4.5 |   3.494 |   3.86  |   3.977 |   3.156 |   3.623 |
|  1 |  239 | Leicester   | D     | Justin           |          4.5 |   3.644 |   1.149 |   3.247 |   3.473 |   2.081 |
|  2 |  259 | Liverpool   | D     | Alexander-Arnold |          7.5 |   2.998 |   3.783 |   4.631 |   3.924 |   4.838 |
|  3 |   17 | Arsenal     | D     | Tierney          |          5.5 |   3.654 |   1.582 |   3.658 |   1.279 |   2.891 |
|  4 |  390 | Spurs       | M     | Son              |          9   |   4.109 |   5.112 |   3.502 |   4.801 |   4.407 |
|  5 |    4 | Arsenal     | M     | Aubameyang       |         12   |   6.502 |   3.91  |   5.688 |   3.831 |   5.313 |
|  6 |  338 | Newcastle   | M     | Saint-Maximin    |          5.5 |   2.948 |   2.468 |   2.982 |   2.413 |   2.431 |
|  7 |  254 | Liverpool   | M     | Salah            |         12   |   5.619 |   6.619 |   7.828 |   6.289 |   7.295 |
|  8 |  377 | Southampton | F     | Adams            |          6   |   3.435 |   3.56  |   4.118 |   2.788 |   3.378 |
|  9 |  184 | Fulham      | F     | Mitrović         |          6   |   3.352 |   4.391 |   3.096 |   3.407 |   3.989 |
| 10 |  117 | Chelsea     | F     | Werner           |          9.5 |   3.297 |   5.541 |   5.591 |   5.223 |   4.167 |
| 11 |   70 | Brighton    | G     | Ryan             |          4.5 |   3.724 |   3.301 |   3.418 |   3.731 |   3.877 |
| 12 |  364 | Southampton | M     | Oriol Romeu      |          4.5 |   2.206 |   2.266 |   2.432 |   1.914 |   2.143 |
| 13 |   97 | Burnley     | D     | Taylor           |          4.5 |   1.897 |   2.541 |   2.557 |   2.608 |   1.917 |
| 14 |  197 | Leeds       | D     | Ayling           |          4.5 |   4.262 |   3.188 |   1.314 |   2.953 |   3.13  |

OUT: Tierney  
IN: Maguire

GW 2

|    |   id | team        | pos   | name             |   sale_value |   2_pts |   3_pts |   4_pts |   5_pts |   6_pts |
|---:|-----:|:------------|:------|:-----------------|-------------:|--------:|--------:|--------:|--------:|--------:|
|  1 |   70 | Brighton    | G     | Ryan             |          4.5 |   3.724 |   3.301 |   3.418 |   3.731 |   3.877 |
|  2 |  298 | Man Utd     | D     | Maguire          |          5.5 |   4.637 |   3.929 |   3.301 |   4.044 |   2.798 |
|  3 |  197 | Leeds       | D     | Ayling           |          4.5 |   4.262 |   3.188 |   1.314 |   2.953 |   3.13  |
|  4 |  239 | Leicester   | D     | Justin           |          4.5 |   3.644 |   1.149 |   3.247 |   3.473 |   2.081 |
|  5 |  259 | Liverpool   | D     | Alexander-Arnold |          7.5 |   2.998 |   3.783 |   4.631 |   3.924 |   4.838 |
|  6 |    4 | Arsenal     | M     | Aubameyang (c)   |         12   |  13.004 |   3.91  |   5.688 |   3.831 |   5.313 |
|  7 |  254 | Liverpool   | M     | Salah            |         12   |   5.619 |   6.619 |   7.828 |   6.289 |   7.295 |
|  8 |  390 | Spurs       | M     | Son              |          9   |   4.109 |   5.112 |   3.502 |   4.801 |   4.407 |
|  9 |  377 | Southampton | F     | Adams            |          6   |   3.435 |   3.56  |   4.118 |   2.788 |   3.378 |
| 10 |  184 | Fulham      | F     | Mitrović         |          6   |   3.352 |   4.391 |   3.096 |   3.407 |   3.989 |
| 11 |  117 | Chelsea     | F     | Werner           |          9.5 |   3.297 |   5.541 |   5.591 |   5.223 |   4.167 |
| 12 |  363 | Southampton | G     | McCarthy         |          4.5 |   3.494 |   3.86  |   3.977 |   3.156 |   3.623 |
| 13 |  338 | Newcastle   | M     | Saint-Maximin    |          5.5 |   2.948 |   2.468 |   2.982 |   2.413 |   2.431 |
| 14 |  364 | Southampton | M     | Oriol Romeu      |          4.5 |   2.206 |   2.266 |   2.432 |   1.914 |   2.143 |
| 15 |   97 | Burnley     | D     | Taylor           |          4.5 |   1.897 |   2.541 |   2.557 |   2.608 |   1.917 |

Cost: £100.0m  
Points: 52.08 (+10.54 on the bench)


OUT: Aubameyang  
IN: Sterling

GW 3

|    |   id | team        | pos   | name             |   sale_value |   2_pts |   3_pts |   4_pts |   5_pts |   6_pts |
|---:|-----:|:------------|:------|:-----------------|-------------:|--------:|--------:|--------:|--------:|--------:|
|  1 |  363 | Southampton | G     | McCarthy         |          4.5 |   3.494 |   3.86  |   3.977 |   3.156 |   3.623 |
|  2 |  298 | Man Utd     | D     | Maguire          |          5.5 |   4.637 |   3.929 |   3.301 |   4.044 |   2.798 |
|  3 |  259 | Liverpool   | D     | Alexander-Arnold |          7.5 |   2.998 |   3.783 |   4.631 |   3.924 |   4.838 |
|  4 |  197 | Leeds       | D     | Ayling           |          4.5 |   4.262 |   3.188 |   1.314 |   2.953 |   3.13  |
|  5 |   97 | Burnley     | D     | Taylor           |          4.5 |   1.897 |   2.541 |   2.557 |   2.608 |   1.917 |
|  6 |  254 | Liverpool   | M     | Salah (c)        |         12   |   5.619 |  13.238 |   7.828 |   6.289 |   7.295 |
|  7 |  276 | Man City    | M     | Sterling         |         11.5 |   5.124 |   5.988 |   5.742 |   5.448 |   5.99  |
|  8 |  390 | Spurs       | M     | Son              |          9   |   4.109 |   5.112 |   3.502 |   4.801 |   4.407 |
|  9 |  117 | Chelsea     | F     | Werner           |          9.5 |   3.297 |   5.541 |   5.591 |   5.223 |   4.167 |
| 10 |  184 | Fulham      | F     | Mitrović         |          6   |   3.352 |   4.391 |   3.096 |   3.407 |   3.989 |
| 11 |  377 | Southampton | F     | Adams            |          6   |   3.435 |   3.56  |   4.118 |   2.788 |   3.378 |
| 12 |   70 | Brighton    | G     | Ryan             |          4.5 |   3.724 |   3.301 |   3.418 |   3.731 |   3.877 |
| 13 |  338 | Newcastle   | M     | Saint-Maximin    |          5.5 |   2.948 |   2.468 |   2.982 |   2.413 |   2.431 |
| 14 |  364 | Southampton | M     | Oriol Romeu      |          4.5 |   2.206 |   2.266 |   2.432 |   1.914 |   2.143 |
| 15 |  239 | Leicester   | D     | Justin           |          4.5 |   3.644 |   1.149 |   3.247 |   3.473 |   2.081 |

Cost: £99.5m  
Points: 55.13 (+9.18 on the bench)


OUT: Saint-Maximin  
IN: Podence

GW 4

|    |   id | team        | pos   | name             |   sale_value |   2_pts |   3_pts |   4_pts |   5_pts |   6_pts |
|---:|-----:|:------------|:------|:-----------------|-------------:|--------:|--------:|--------:|--------:|--------:|
|  1 |  363 | Southampton | G     | McCarthy         |          4.5 |   3.494 |   3.86  |   3.977 |   3.156 |   3.623 |
|  2 |  259 | Liverpool   | D     | Alexander-Arnold |          7.5 |   2.998 |   3.783 |   4.631 |   3.924 |   4.838 |
|  3 |  298 | Man Utd     | D     | Maguire          |          5.5 |   4.637 |   3.929 |   3.301 |   4.044 |   2.798 |
|  4 |  239 | Leicester   | D     | Justin           |          4.5 |   3.644 |   1.149 |   3.247 |   3.473 |   2.081 |
|  5 |  254 | Liverpool   | M     | Salah (c)        |         12   |   5.619 |   6.619 |  15.656 |   6.289 |   7.295 |
|  6 |  276 | Man City    | M     | Sterling         |         11.5 |   5.124 |   5.988 |   5.742 |   5.448 |   5.99  |
|  7 |  469 | Wolves      | M     | Podence          |          5.5 |   2.711 |   3.537 |   4.074 |   3.378 |   3.8   |
|  8 |  390 | Spurs       | M     | Son              |          9   |   4.109 |   5.112 |   3.502 |   4.801 |   4.407 |
|  9 |  117 | Chelsea     | F     | Werner           |          9.5 |   3.297 |   5.541 |   5.591 |   5.223 |   4.167 |
| 10 |  377 | Southampton | F     | Adams            |          6   |   3.435 |   3.56  |   4.118 |   2.788 |   3.378 |
| 11 |  184 | Fulham      | F     | Mitrović         |          6   |   3.352 |   4.391 |   3.096 |   3.407 |   3.989 |
| 12 |   70 | Brighton    | G     | Ryan             |          4.5 |   3.724 |   3.301 |   3.418 |   3.731 |   3.877 |
| 13 |   97 | Burnley     | D     | Taylor           |          4.5 |   1.897 |   2.541 |   2.557 |   2.608 |   1.917 |
| 14 |  364 | Southampton | M     | Oriol Romeu      |          4.5 |   2.206 |   2.266 |   2.432 |   1.914 |   2.143 |
| 15 |  197 | Leeds       | D     | Ayling           |          4.5 |   4.262 |   3.188 |   1.314 |   2.953 |   3.13  |

Cost: £99.5m  
Points: 56.94 (+9.72 on the bench)

GW 5

|    |   id | team        | pos   | name             |   sale_value |   2_pts |   3_pts |   4_pts |   5_pts |   6_pts |
|---:|-----:|:------------|:------|:-----------------|-------------:|--------:|--------:|--------:|--------:|--------:|
|  1 |   70 | Brighton    | G     | Ryan             |          4.5 |   3.724 |   3.301 |   3.418 |   3.731 |   3.877 |
|  2 |  298 | Man Utd     | D     | Maguire          |          5.5 |   4.637 |   3.929 |   3.301 |   4.044 |   2.798 |
|  3 |  259 | Liverpool   | D     | Alexander-Arnold |          7.5 |   2.998 |   3.783 |   4.631 |   3.924 |   4.838 |
|  4 |  239 | Leicester   | D     | Justin           |          4.5 |   3.644 |   1.149 |   3.247 |   3.473 |   2.081 |
|  5 |  197 | Leeds       | D     | Ayling           |          4.5 |   4.262 |   3.188 |   1.314 |   2.953 |   3.13  |
|  6 |  254 | Liverpool   | M     | Salah (c)        |         12   |   5.619 |   6.619 |   7.828 |  12.578 |   7.295 |
|  7 |  276 | Man City    | M     | Sterling         |         11.5 |   5.124 |   5.988 |   5.742 |   5.448 |   5.99  |
|  8 |  390 | Spurs       | M     | Son              |          9   |   4.109 |   5.112 |   3.502 |   4.801 |   4.407 |
|  9 |  469 | Wolves      | M     | Podence          |          5.5 |   2.711 |   3.537 |   4.074 |   3.378 |   3.8   |
| 10 |  117 | Chelsea     | F     | Werner           |          9.5 |   3.297 |   5.541 |   5.591 |   5.223 |   4.167 |
| 11 |  184 | Fulham      | F     | Mitrović         |          6   |   3.352 |   4.391 |   3.096 |   3.407 |   3.989 |
| 12 |  363 | Southampton | G     | McCarthy         |          4.5 |   3.494 |   3.86  |   3.977 |   3.156 |   3.623 |
| 13 |  377 | Southampton | F     | Adams            |          6   |   3.435 |   3.56  |   4.118 |   2.788 |   3.378 |
| 14 |   97 | Burnley     | D     | Taylor           |          4.5 |   1.897 |   2.541 |   2.557 |   2.608 |   1.917 |
| 15 |  364 | Southampton | M     | Oriol Romeu      |          4.5 |   2.206 |   2.266 |   2.432 |   1.914 |   2.143 |

Cost: £99.5m  
Points: 52.96 (+10.47 on the bench)


OUT: Werner  
OUT: Maguire  
IN: Robertson  
IN: Jiménez  


GW 6

|    |   id | team        | pos   | name             |   sale_value |   2_pts |   3_pts |   4_pts |   5_pts |   6_pts |
|---:|-----:|:------------|:------|:-----------------|-------------:|--------:|--------:|--------:|--------:|--------:|
|  1 |   70 | Brighton    | G     | Ryan             |          4.5 |   3.724 |   3.301 |   3.418 |   3.731 |   3.877 |
|  2 |  255 | Liverpool   | D     | Robertson        |          7   |   3.251 |   4.201 |   5.065 |   4.202 |   5.167 |
|  3 |  259 | Liverpool   | D     | Alexander-Arnold |          7.5 |   2.998 |   3.783 |   4.631 |   3.924 |   4.838 |
|  4 |  197 | Leeds       | D     | Ayling           |          4.5 |   4.262 |   3.188 |   1.314 |   2.953 |   3.13  |
|  5 |  254 | Liverpool   | M     | Salah (c)        |         12   |   5.619 |   6.619 |   7.828 |   6.289 |  14.59  |
|  6 |  276 | Man City    | M     | Sterling         |         11.5 |   5.124 |   5.988 |   5.742 |   5.448 |   5.99  |
|  7 |  390 | Spurs       | M     | Son              |          9   |   4.109 |   5.112 |   3.502 |   4.801 |   4.407 |
|  8 |  469 | Wolves      | M     | Podence          |          5.5 |   2.711 |   3.537 |   4.074 |   3.378 |   3.8   |
|  9 |  460 | Wolves      | F     | Jiménez          |          8.5 |   3.653 |   4.462 |   5.015 |   4.106 |   4.617 |
| 10 |  184 | Fulham      | F     | Mitrović         |          6   |   3.352 |   4.391 |   3.096 |   3.407 |   3.989 |
| 11 |  377 | Southampton | F     | Adams            |          6   |   3.435 |   3.56  |   4.118 |   2.788 |   3.378 |
| 12 |  363 | Southampton | G     | McCarthy         |          4.5 |   3.494 |   3.86  |   3.977 |   3.156 |   3.623 |
| 13 |  364 | Southampton | M     | Oriol Romeu      |          4.5 |   2.206 |   2.266 |   2.432 |   1.914 |   2.143 |
| 14 |  239 | Leicester   | D     | Justin           |          4.5 |   3.644 |   1.149 |   3.247 |   3.473 |   2.081 |
| 15 |   97 | Burnley     | D     | Taylor           |          4.5 |   1.897 |   2.541 |   2.557 |   2.608 |   1.917 |

Cost: £100.0m  
Points: 57.78 (+9.76 on the bench)


Total points from GW 2-6: 274.89 (+49.68 on the bench)