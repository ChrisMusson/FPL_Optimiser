from mip import BINARY, Model, xsum, maximize
import pandas as pd
import unicodedata

def optimise(
    filepath="players_data.csv", 
    budget=100, 
    teamsize=15, 
    GK=None, 
    DEF=None, 
    MID=None, 
    FWD=None, 
    in_team=[], 
    out_team=[], 
    banned_teams=[],
    max_from_team=3
    ):
    '''
    :param filepath - str: the filepath that points to the csv that contains the data you want to optimise
    :param budget - int or float: the maximum sum of costs allowed in the optimised lineup
    :param teamsize - int: the number of players to include in the optimised lineup
    :param GK, DEF, MID, FWD - int: the number of players of this position to include in the optimised lineup
    :param in_team - list<int or str>: list of players that must be included in the optimised lineup
    :param out_team - list<int or str>: list of players that must not be included in the optimised lineup
    :param banned_teams - list<str>: list of clubs for whom no players in the optimised 15 man squad can play
    :param max_from_team - int: the maximum number of players from a single team allowed in the optimised lineup

    '''

    def remove_accents(input_str):
        '''a function that removes all diacritics from latin characters'''
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
    
    df = pd.read_csv(filepath)
    names = df.name.str.lower().apply(remove_accents).copy()
    I = range(len(df))

    model = Model()

    # add a binary value to the model for each player that defines if they are picked - 1 for in, 0 for out
    x = [model.add_var(var_type=BINARY) for i in I]

    # add objective function - points scored
    model.objective = maximize(xsum(df.points[i] * x[i] for i in I))

    # add budget constraint
    model += xsum(df.cost[i] * x[i] for i in I) <= budget

    # add teamsize contraint
    model += xsum(x[i] for i in I) == teamsize

    # dict containing min/max num of players by position
    rules = {
        "GK": [1, 2],
        "DEF": [3, 5],
        "MID": [2, 5],
        "FWD": [1, 3]
    }
    
    # add constraint of min/max number of players from each position
    for pos in ["GK", "DEF", "MID", "FWD"]:
        if eval(pos):
            assert(rules[pos][0] <= eval(pos) <= rules[pos][1]), f"That is not a valid value for {pos}"
            model += xsum(x[i]for i in I if df.pos[i] == pos[0]) == eval(pos)
        else:
            model += rules[pos][0] <= xsum(x[i] for i in I if df.pos[i] == pos[0]) 
            model += xsum(x[i] for i in I if df.pos[i] == pos[0]) <= rules[pos][1]

    # add constraint of maximum number of players from each team, teams being case insensitive
    banned_teams = [x.lower() for x in banned_teams]
    for team in df.team.unique():
        team = team.lower()
        if team in banned_teams:
            model += xsum(x[i] for i in I if df.team[i].lower() == team) == 0
        else:
            model += xsum(x[i] for i in I if df.team[i].lower() == team) <= max_from_team

    # add constraints so that players in in_team must be in the optimised lineup and players in out_team must not be in the optimised lineup.
    # note that using a player's name might run into problems if the name is shared by more than one player,
    # so using a player's ID in in_team and out_team is also allowed.
    for player in in_team:
        if isinstance(player, str):
            player = remove_accents(player.lower())
            model += xsum(x[i] for i in I if names[i] == player) == 1
        elif isinstance(player, int):
            model += xsum(x[i] for i in I if df.id[i] == player) == 1

    for player in out_team:
        if isinstance(player, str):
            player = remove_accents(player.lower())
            model += xsum(x[i] for i in I if df.name[i].lower() == player.lower()) == 0
        elif isinstance(player, int):
            model += xsum(x[i] for i in I if df.id[i] == player) == 0

    model.optimize()

    result = df.iloc[[i for i in I if x[i].x == 1]].copy()

    result.pos = pd.Categorical(result.pos, categories=["G", "D", "M", "F"])
    result = result.sort_values(by=["pos", "points"], ascending=[True, False])

    result = result.reset_index(drop=True)
    result.index += 1

    print(result)
    print(f"\nTotal cost: £{result.cost.sum()}m")
    print(f"Total points: {result.points.sum()}\n")


# example:
optimise(
    budget=83,
    teamsize=11
    )
