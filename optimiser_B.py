from mip import BINARY, Model, xsum, maximize
import pandas as pd
import unicodedata


def optimise(filepath="players_data.csv",
             col_to_max="points",
             budget=100,
             DEF=None,
             MID=None,
             FWD=None,
             bench_strength=0.1,
             in_team=[],
             starting=[],
             on_bench=[],
             out_team=[],
             banned_teams=[]
             ):
    '''
    :param filepath - str: the filepath that points to the csv that contains the data you want to optimise
    :param col_to_max - str: the name of the column in the csv that will be maximised
    :param budget - int or float: the maximum sum of costs allowed in the optimised 15 man squad
    :param DEF, MID, FWD - int: the number of players of this position to be included in starting 11 of the optimised 15 man squad
    :param bench_strength - float: a number between 0 and 1 inclusive that denotes how much to take the bench into account when optimising the squad
    :param in_team - list<int or str>: list of players that must be included in the optimised 15 man squad
    :param starting - list<int or str>: list of players who must be included in the first 11 of the optimised 15 man squad
    :param on_bench - list<int or str>: list of players who must be in the 15 man squad but must not be included in the first 11
    :param out_team - list<int or str>: list of players that must not be included in the optimised 15 man squad
    :param banned_teams - list<str>: list of clubs for whom no players in the optimised 15 man squad can play

    '''

    def remove_accents(input_str):
        '''a function that removes all diacritics from latin characters'''
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
    
    df = pd.read_csv(filepath)
    names = df.name.str.lower().apply(remove_accents).copy()
    I = range(len(df))
    model = Model()

    # add a binary value to the model for each player that defines if they are in the 15 man squad - 1 for in, 0 for out
    x = [model.add_var(var_type=BINARY) for i in I]

    # add a binary value to the model for each player that defines if they are in the starting 11 - 1 for in, 0 for out
    y = [model.add_var(var_type=BINARY) for i in I]

    # ensure y only contains 11 players
    model += xsum(y[i] for i in I) == 11

    # ensure players in y are also in x
    for i in I:
        model += x[i] >= y[i]

    # add constraint of maximum number of players from each team, teams being case insensitive
    banned_teams = [x.lower() for x in banned_teams]
    for team in df.team.unique():
        team = team.lower()
        if team in banned_teams:
            model += xsum(x[i] for i in I if df.team[i].lower() == team) == 0
        else:
            model += xsum(x[i] for i in I if df.team[i].lower() == team) <= 3

    # dict containing min/max num of players by position
    rules = {
        "DEF": [3, 5],
        "MID": [2, 5],
        "FWD": [1, 3],
    }

    # add position constraints
    model += xsum(x[i] for i in I if df.pos[i] == "G") == 2
    model += xsum(y[i] for i in I if df.pos[i] == "G") == 1
    for pos in ["DEF", "MID", "FWD"]:
        model += xsum(x[i]for i in I if df.pos[i] == pos[0]) == rules[pos][1]
        if eval(pos):
            assert(rules[pos][0] <= eval(pos) <= rules[pos][1]), f"That is not a valid value for {pos}"
            model += xsum(y[i]for i in I if df.pos[i] == pos[0]) == eval(pos)
        else:
            model += rules[pos][0] <= xsum(y[i] for i in I if df.pos[i] == pos[0]) <= rules[pos][1]

    # add budget constraint
    model += xsum(df.cost[i] * x[i] for i in I) <= budget

    # add constraints for in_team, on_bench, and out_team
    # note that using a player's name might run into problems if the name is shared by more than one player,
    # so using a player's ID is also allowed.
    for player in in_team:
        if isinstance(player, str):
            player = remove_accents(player.lower())
            model += xsum(x[i] for i in I if names[i] == player) == 1
        elif isinstance(player, int):
            model += xsum(x[i] for i in I if df.id[i] == player) == 1

    for player in starting:
        if isinstance(player, str):
            player = remove_accents(player.lower())
            model += xsum(x[i] for i in I if names[i] == player) == 1
            model += xsum(y[i] for i in I if names[i] == player) == 1
        elif isinstance(player, int):
            model += xsum(x[i] for i in I if df.id[i] == player) == 1
            model += xsum(y[i] for i in I if df.id[i] == player) == 1

    for player in on_bench:
        if isinstance(player, str):
            player = remove_accents(player.lower())
            model += xsum(x[i] for i in I if names[i] == player) == 1
            model += xsum(y[i] for i in I if names[i] == player) == 0
        elif isinstance(player, int):
            model += xsum(x[i] for i in I if df.id[i] == player) == 1
            model += xsum(y[i] for i in I if df.id[i] == player) == 0

    for player in out_team:
        player = remove_accents(player.lower())
        if isinstance(player, str):
            model += xsum(x[i] for i in I if names[i] == player) == 0
        elif isinstance(player, int):
            model += xsum(x[i] for i in I if df.id[i] == player) == 0

    # add objective function - points scored by starting 11 + points scored by the bench, 
    # with the weight of each term defined by the user in bench_strength
    assert(0 <= bench_strength <= 1), "that is not a valid value for bench strength"
    
    model.objective = maximize(
        (1 - bench_strength) * xsum(df[col_to_max][i] * y[i] for i in I) +
        bench_strength * (xsum(df[col_to_max][i] * x[i] for i in I) - xsum(df[col_to_max][i] * y[i] for i in I))
    )

    model.optimize()

    start_i = [i for i in I if y[i].x == 1]
    start = df.iloc[start_i].copy()

    bench_i = [i for i in I if x[i].x == 1 and y[i].x == 0]
    bench = df.iloc[bench_i].copy()

    start.pos = pd.Categorical(start.pos, categories=["G", "D", "M", "F"])
    start = start.sort_values(by=["pos", "points"], ascending=[True, False])

    bench.pos = pd.Categorical(bench.pos, categories=["G", "D", "M", "F"])
    bench = bench.sort_values(by=["pos", "points"], ascending=[True, False])

    result = pd.concat([start, bench])
    result = result.reset_index(drop=True)
    result.index += 1

    print(result.loc[:, ["id", "team", "pos", "name", "cost", "points"]])
    print(f"\nTotal cost: £{result.cost.sum()}m")
    print(f"Total points: {round(start.points.sum(), 2)} (+{round(bench.points.sum(), 2)} on the bench)\n")


optimise(
    DEF=4,
    in_team=["van Dijk", "vinagre", "jimenez"],
    out_team=["Lundstram"],
    banned_teams=["Burnley", "Aston Villa", "Man Utd"]
)
