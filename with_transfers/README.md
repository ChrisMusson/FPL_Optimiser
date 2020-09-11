This optimiser takes week-by-week expected points values and maximises the total expected points subject to all the usual FPL constraints, allowing for up to 2 transfers per gameweek, but never allowing for hits. As in the other optimisers, all function parameters can be found in the `optimise()` function's docstring. 

The `optimise()` function requires a csv file with headers `[id, team, pos, name, cost]` along with `n_pts` for every gameweek you want to optimise for. 

## Getting the data
I would recommend using fplreview's massive data planner to get expected points data by gameweek. To do this, go to https://fplreview.com/massive-data-planner/, change projection to however many gameweeks you want to look into the future, input any team ID, submit, and then download the csv found on that page to the current working directory.

After you have done that, calling `python clean_fplreview_data.py <infile> <start_gw> <end_gw>` will create a `cleaned_data.csv` file for use in the optimiser function. Here, infile is the file you downloaded earlier. Note that there is currently no error checking in place for this as I had to rush to try and get this optimiser out before the start of the season, so ensure that you use it as shown above.

I have included my downloaded file `raw_fplreview_data.csv` and the cleaned version `cleaned_data.csv` in this repository, however the expected points change multiple times per day, so I would recommend that you download a more recent csv if you are going to use this optimiser.

## Running the optimiser
Now, open `optimiser.py`. In the `optimise()` function, you will see the parameters that can be edited in the function. Scroll to the bottom and change them as you see fit, and run the program.

## Warnings
Please know that this optimisation is computationally very hard (I will try and improve efficiency at a later date, but I can't promise anything), so it will take a while to calculate the optimal lineup and transfer strategy. To give you an idea, it takes me ~9 seconds to calculate for gameweeks 1-3, ~50 seconds for gameweeks 1-4, ~100 seconds for gameweeks 1-5, etc.

One way to make it run quicker is supplying players to `in_team` and `out_team`, as that will reduce the solution space. So if there are some players who are 100% in your team, then you may as well add them to `in_team`.

The optimiser currently only allows up to 2 transfers per gameweek and doesn't allow taking hits. I know that this is not perfect, but I believe that giving the optimiser the ability to take hits could make the solution space too large to be feasible. I will however look at seeing if it could work, but again, no promises.

The optimiser also doesn't account for any price changes, so there could easily be a situation where the optimiser's plan in a future gameweek will no longer work.

Finally, this is just some code that solves a mathematical optimisation problem - although a lot of work has gone into it, it's not some magical tool to pick out the best team and best transfer strategy - **make sure to think for yourself and to not blindly follow the advice it gives.**

## Example

### Input:
```
optimise(
    start_gw=1,
    end_gw=5,
    in_team=["werner", "salah"],
    out_team=["vinagre", "nyland", 451],
)
```

### Output:
GW 1

|    |   id | team           | pos   | name             |   cost |   1_pts |   2_pts |   3_pts |   4_pts |   5_pts |
|---:|-----:|:---------------|:------|:-----------------|-------:|--------:|--------:|--------:|--------:|--------:|
|  1 |  363 | Southampton    | G     | McCarthy         |    4.5 |   3.818 |   3.441 |   3.768 |   3.776 |   3.057 |
|  2 |  259 | Liverpool      | D     | Alexander-Arnold |    7.5 |   5.456 |   3.411 |   4.368 |   5.006 |   4.268 |
|  3 |  255 | Liverpool      | D     | Robertson        |    7   |   5.376 |   3.393 |   4.17  |   4.899 |   4.249 |
|  4 |  457 | Spurs          | D     | Doherty          |    6   |   4.265 |   3.505 |   4.415 |   2.222 |   4.062 |
|  5 |  395 | Spurs          | D     | Davies           |    5   |   3.514 |   3.018 |   3.833 |   1.908 |   3.332 |
|  6 |  254 | Liverpool      | M     | Salah (c)        |   12   |  14.564 |   5.156 |   6.044 |   6.815 |   5.763 |
|  7 |    4 | Arsenal        | M     | Aubameyang       |   12   |   6.547 |   6.521 |   3.957 |   5.722 |   3.762 |
|  8 |  370 | Southampton    | M     | Ward-Prowse      |    6   |   3.466 |   3.208 |   3.495 |   3.901 |   2.678 |
|  9 |  117 | Chelsea        | F     | Werner           |    9.5 |   5.779 |   4.625 |   6.2   |   6.007 |   5.577 |
| 10 |  506 | Newcastle      | F     | Wilson           |    6.5 |   3.987 |   4.027 |   3.227 |   4.053 |   3.083 |
| 11 |  184 | Fulham         | F     | Mitrović         |    6   |   3.723 |   3.531 |   4.285 |   3.093 |   3.32  |
| 12 |   70 | Brighton       | G     | Ryan             |    4.5 |   3.256 |   3.711 |   3.235 |   3.45  |   3.619 |
| 13 |  364 | Southampton    | M     | Oriol Romeu      |    4.5 |   2.082 |   2.006 |   2.043 |   2.204 |   1.7   |
| 14 |  131 | Crystal Palace | M     | McCarthy         |    4.5 |   2.068 |   1.749 |   2.04  |   1.783 |   2.019 |
| 15 |  197 | Leeds          | D     | Ayling           |    4.5 |   1.623 |   4.608 |   3.429 |   1.544 |   3.196 |

Cost: £100.0m  
Points: 60.49 (+9.03 on the bench)


OUT: Davies  
IN: Shaw  

GW 2

|    |   id | team           | pos   | name             |   cost |   1_pts |   2_pts |   3_pts |   4_pts |   5_pts |
|---:|-----:|:---------------|:------|:-----------------|-------:|--------:|--------:|--------:|--------:|--------:|
|  1 |   70 | Brighton       | G     | Ryan             |    4.5 |   3.256 |   3.711 |   3.235 |   3.45  |   3.619 |
|  2 |  197 | Leeds          | D     | Ayling           |    4.5 |   1.623 |   4.608 |   3.429 |   1.544 |   3.196 |
|  3 |  300 | Man Utd        | D     | Shaw             |    5   |   0     |   4.316 |   3.66  |   3.226 |   3.671 |
|  4 |  457 | Spurs          | D     | Doherty          |    6   |   4.265 |   3.505 |   4.415 |   2.222 |   4.062 |
|  5 |  259 | Liverpool      | D     | Alexander-Arnold |    7.5 |   5.456 |   3.411 |   4.368 |   5.006 |   4.268 |
|  6 |  255 | Liverpool      | D     | Robertson        |    7   |   5.376 |   3.393 |   4.17  |   4.899 |   4.249 |
|  7 |    4 | Arsenal        | M     | Aubameyang (c)   |   12   |   6.547 |  13.042 |   3.957 |   5.722 |   3.762 |
|  8 |  254 | Liverpool      | M     | Salah            |   12   |   7.282 |   5.156 |   6.044 |   6.815 |   5.763 |
|  9 |  117 | Chelsea        | F     | Werner           |    9.5 |   5.779 |   4.625 |   6.2   |   6.007 |   5.577 |
| 10 |  506 | Newcastle      | F     | Wilson           |    6.5 |   3.987 |   4.027 |   3.227 |   4.053 |   3.083 |
| 11 |  184 | Fulham         | F     | Mitrović         |    6   |   3.723 |   3.531 |   4.285 |   3.093 |   3.32  |
| 12 |  363 | Southampton    | G     | McCarthy         |    4.5 |   3.818 |   3.441 |   3.768 |   3.776 |   3.057 |
| 13 |  370 | Southampton    | M     | Ward-Prowse      |    6   |   3.466 |   3.208 |   3.495 |   3.901 |   2.678 |
| 14 |  364 | Southampton    | M     | Oriol Romeu      |    4.5 |   2.082 |   2.006 |   2.043 |   2.204 |   1.7   |
| 15 |  131 | Crystal Palace | M     | McCarthy         |    4.5 |   2.068 |   1.749 |   2.04  |   1.783 |   2.019 |

Cost: £100.0m  
Points: 53.33 (+10.40 on the bench)


OUT: Aubameyang  
IN: Sterling

GW 3

|    |   id | team           | pos   | name             |   cost |   1_pts |   2_pts |   3_pts |   4_pts |   5_pts |
|---:|-----:|:---------------|:------|:-----------------|-------:|--------:|--------:|--------:|--------:|--------:|
|  1 |  363 | Southampton    | G     | McCarthy         |    4.5 |   3.818 |   3.441 |   3.768 |   3.776 |   3.057 |
|  2 |  457 | Spurs          | D     | Doherty          |    6   |   4.265 |   3.505 |   4.415 |   2.222 |   4.062 |
|  3 |  259 | Liverpool      | D     | Alexander-Arnold |    7.5 |   5.456 |   3.411 |   4.368 |   5.006 |   4.268 |
|  4 |  255 | Liverpool      | D     | Robertson        |    7   |   5.376 |   3.393 |   4.17  |   4.899 |   4.249 |
|  5 |  300 | Man Utd        | D     | Shaw             |    5   |   0     |   4.316 |   3.66  |   3.226 |   3.671 |
|  6 |  197 | Leeds          | D     | Ayling           |    4.5 |   1.623 |   4.608 |   3.429 |   1.544 |   3.196 |
|  7 |  254 | Liverpool      | M     | Salah            |   12   |   7.282 |   5.156 |   6.044 |   6.815 |   5.763 |
|  8 |  276 | Man City       | M     | Sterling         |   11.5 |   0     |   5.316 |   5.922 |   5.789 |   5.482 |
|  9 |  370 | Southampton    | M     | Ward-Prowse      |    6   |   3.466 |   3.208 |   3.495 |   3.901 |   2.678 |
| 10 |  117 | Chelsea        | F     | Werner (c)       |    9.5 |   5.779 |   4.625 |  12.4   |   6.007 |   5.577 |
| 11 |  184 | Fulham         | F     | Mitrović         |    6   |   3.723 |   3.531 |   4.285 |   3.093 |   3.32  |
| 12 |   70 | Brighton       | G     | Ryan             |    4.5 |   3.256 |   3.711 |   3.235 |   3.45  |   3.619 |
| 13 |  506 | Newcastle      | F     | Wilson           |    6.5 |   3.987 |   4.027 |   3.227 |   4.053 |   3.083 |
| 14 |  364 | Southampton    | M     | Oriol Romeu      |    4.5 |   2.082 |   2.006 |   2.043 |   2.204 |   1.7   |
| 15 |  131 | Crystal Palace | M     | McCarthy         |    4.5 |   2.068 |   1.749 |   2.04  |   1.783 |   2.019 |

Cost: £99.5m  
Points: 55.96 (+10.54 on the bench)


OUT: Doherty  
IN: Alonso

GW 4

|    |   id | team           | pos   | name             |   cost |   1_pts |   2_pts |   3_pts |   4_pts |   5_pts |
|---:|-----:|:---------------|:------|:-----------------|-------:|--------:|--------:|--------:|--------:|--------:|
|  1 |  363 | Southampton    | G     | McCarthy         |    4.5 |   3.818 |   3.441 |   3.768 |   3.776 |   3.057 |
|  2 |  259 | Liverpool      | D     | Alexander-Arnold |    7.5 |   5.456 |   3.411 |   4.368 |   5.006 |   4.268 |
|  3 |  255 | Liverpool      | D     | Robertson        |    7   |   5.376 |   3.393 |   4.17  |   4.899 |   4.249 |
|  4 |  104 | Chelsea        | D     | Alonso           |    6   |   3.734 |   2.401 |   4.053 |   4.165 |   3.793 |
|  5 |  300 | Man Utd        | D     | Shaw             |    5   |   0     |   4.316 |   3.66  |   3.226 |   3.671 |
|  6 |  254 | Liverpool      | M     | Salah (c)        |   12   |   7.282 |   5.156 |   6.044 |  13.63  |   5.763 |
|  7 |  276 | Man City       | M     | Sterling         |   11.5 |   0     |   5.316 |   5.922 |   5.789 |   5.482 |
|  8 |  370 | Southampton    | M     | Ward-Prowse      |    6   |   3.466 |   3.208 |   3.495 |   3.901 |   2.678 |
|  9 |  117 | Chelsea        | F     | Werner           |    9.5 |   5.779 |   4.625 |   6.2   |   6.007 |   5.577 |
| 10 |  506 | Newcastle      | F     | Wilson           |    6.5 |   3.987 |   4.027 |   3.227 |   4.053 |   3.083 |
| 11 |  184 | Fulham         | F     | Mitrović         |    6   |   3.723 |   3.531 |   4.285 |   3.093 |   3.32  |
| 12 |   70 | Brighton       | G     | Ryan             |    4.5 |   3.256 |   3.711 |   3.235 |   3.45  |   3.619 |
| 13 |  364 | Southampton    | M     | Oriol Romeu      |    4.5 |   2.082 |   2.006 |   2.043 |   2.204 |   1.7   |
| 14 |  131 | Crystal Palace | M     | McCarthy         |    4.5 |   2.068 |   1.749 |   2.04  |   1.783 |   2.019 |
| 15 |  197 | Leeds          | D     | Ayling           |    4.5 |   1.623 |   4.608 |   3.429 |   1.544 |   3.196 |

Cost: £99.5m  
Points: 57.54 (+8.98 on the bench)


OUT: Wilson  
IN: Wood

GW 5

|    |   id | team           | pos   | name             |   cost |   1_pts |   2_pts |   3_pts |   4_pts |   5_pts |
|---:|-----:|:---------------|:------|:-----------------|-------:|--------:|--------:|--------:|--------:|--------:|
|  1 |   70 | Brighton       | G     | Ryan             |    4.5 |   3.256 |   3.711 |   3.235 |   3.45  |   3.619 |
|  2 |  259 | Liverpool      | D     | Alexander-Arnold |    7.5 |   5.456 |   3.411 |   4.368 |   5.006 |   4.268 |
|  3 |  255 | Liverpool      | D     | Robertson        |    7   |   5.376 |   3.393 |   4.17  |   4.899 |   4.249 |
|  4 |  104 | Chelsea        | D     | Alonso           |    6   |   3.734 |   2.401 |   4.053 |   4.165 |   3.793 |
|  5 |  300 | Man Utd        | D     | Shaw             |    5   |   0     |   4.316 |   3.66  |   3.226 |   3.671 |
|  6 |  197 | Leeds          | D     | Ayling           |    4.5 |   1.623 |   4.608 |   3.429 |   1.544 |   3.196 |
|  7 |  254 | Liverpool      | M     | Salah (c)        |   12   |   7.282 |   5.156 |   6.044 |   6.815 |  11.526 |
|  8 |  276 | Man City       | M     | Sterling         |   11.5 |   0     |   5.316 |   5.922 |   5.789 |   5.482 |
|  9 |  117 | Chelsea        | F     | Werner           |    9.5 |   5.779 |   4.625 |   6.2   |   6.007 |   5.577 |
| 10 |   91 | Burnley        | F     | Wood             |    6.5 |   0     |   3.321 |   3.875 |   3.578 |   3.911 |
| 11 |  184 | Fulham         | F     | Mitrović         |    6   |   3.723 |   3.531 |   4.285 |   3.093 |   3.32  |
| 12 |  363 | Southampton    | G     | McCarthy         |    4.5 |   3.818 |   3.441 |   3.768 |   3.776 |   3.057 |
| 13 |  370 | Southampton    | M     | Ward-Prowse      |    6   |   3.466 |   3.208 |   3.495 |   3.901 |   2.678 |
| 14 |  131 | Crystal Palace | M     | McCarthy         |    4.5 |   2.068 |   1.749 |   2.04  |   1.783 |   2.019 |
| 15 |  364 | Southampton    | M     | Oriol Romeu      |    4.5 |   2.082 |   2.006 |   2.043 |   2.204 |   1.7   |

Cost: £99.5m  
Points: 52.61 (+9.45 on the bench)


Total points from GW 1-5: 279.93 (+48.41 on the bench)