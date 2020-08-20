import mip
import pandas as pd


def optimise(budget=100, teamsize=11, GK=None, DEF=None, MID=None, FWD=None, in_team=[], out_team=[], max_from_team=3):
    '''
    :param budget - int or float: the maximum sum of costs allowed in the optimised lineup
    :param teamsize - int: the number of players to include in the optimised lineup
    :param GK, DEF, MID, FWD - int: the number of players of this position to include in the optimised lineup
    :param in_team - list<int or str>: list of players that must be included in the optimised lineup
    :param out_team - list<int or str>: list of players that must not be included in the optimised lineup
    :param max_from_team - int: the maximum number of players from a single team allowed in the optimised lineup

    '''
    rules = {
        "min_gks": 1,
        "max_gks": 2,
        "min_defs": 3,
        "max_defs": 5,
        "min_mids": 2,
        "max_mids": 5,
        "min_fwds": 1,
        "max_fwds": 3
    }
    df = pd.read_csv('players_data.csv')
    I = range(len(df))

    model = mip.Model()

    # add a binary value to the model for each player that defines if they are picked - 1 for in, 0 for out
    x = [model.add_var(var_type=mip.BINARY) for i in I]

    # add objective function - points scored
    model.objective = mip.maximize(mip.xsum(df.points[i] * x[i] for i in I))

    # add budget constraint
    model += mip.xsum(df.cost[i] * x[i] for i in I) <= budget

    # add teamsize contraint
    model += mip.xsum(x[i] for i in I) == teamsize

    # add constraint of min/max number of players from each position
    if GK:
        model += mip.xsum(x[i] for i in I if df.pos[i] == "G") == GK
    else:
        model += mip.xsum(x[i] for i in I if df.pos[i] == "G") >= rules["min_gks"]
        model += mip.xsum(x[i] for i in I if df.pos[i] == "G") <= rules["max_gks"]

    if DEF:
        model += mip.xsum(x[i] for i in I if df.pos[i] == "D") == DEF
    else:
        model += mip.xsum(x[i] for i in I if df.pos[i] == "D") >= rules["min_defs"]
        model += mip.xsum(x[i] for i in I if df.pos[i] == "D") <= rules["max_defs"]

    if MID:
        model += mip.xsum(x[i] for i in I if df.pos[i] == "M") == MID
    else:
        model += mip.xsum(x[i] for i in I if df.pos[i] == "M") >= rules["min_mids"]
        model += mip.xsum(x[i] for i in I if df.pos[i] == "M") <= rules["max_mids"]

    if FWD:
        model += mip.xsum(x[i] for i in I if df.pos[i] == "F") == FWD
    else:
        model += mip.xsum(x[i] for i in I if df.pos[i] == "F") >= rules["min_fwds"]
        model += mip.xsum(x[i] for i in I if df.pos[i] == "F") <= rules["max_fwds"]

    # add constraint of maximum number of players from each team
    for team in df.team.unique():
        model += mip.xsum(x[i] for i in I if df.team[i] == team) <= max_from_team

    # add constraints so that players in in_team must be in the optimised lineup and players in out_team must not be in the optimised lineup.
    # note that using a player's name might run into problems if the name is shared by more than one player,
    # so using a player's ID in in_team and out_team is also allowed.
    for player in in_team:
        if isinstance(player, str):
            model += mip.xsum(x[i] for i in I if df.name[i].lower() == player.lower()) == 1
        elif isinstance(player, int):
            model += mip.xsum(x[i] for i in I if df.id[i] == player) == 1

    for player in out_team:
        if isinstance(player, str):
            model += mip.xsum(x[i] for i in I if df.name[i].lower() == player.lower()) == 0
        elif isinstance(player, int):
            model += mip.xsum(x[i] for i in I if df.id[i] == player) == 0

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
optimise(budget=81,
         teamsize=11,
         in_team=["Salah", "Vinagre", 259],
         out_team=["Lundstram", 1],
         GK=1,
         MID=4
         )
