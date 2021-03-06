from mip import BINARY, Model, maximize, xsum
import pandas as pd
import unicodedata


def optimise(
    start_gw,
    end_gw,
    filepath="cleaned_data.csv",
    budget=100,
    in_team=[],
    out_team=[],
    bench_strength=0.1,
    future_gw_multiplier=1,
    max_from_team=3,
):
    """
    :param start_gw - int: the first gameweek in the range of gameweeks you want to optimise for
    :param end_gw - int: the last gameweek in the range of gameweeks you want to optimise for
    :param filepath - str: the filepath that points to the csv that contains the data you want to optimise
    :param budget - int or float: the maximum sum of costs allowed in the optimised 15 man squad
    :param in_team - list<int or str>: list of players that must be included in the optimised 15 man squad for every gameweek
    :param out_team - list<int or str>: list of players that must never be included in the optimised 15 man squad
    :param bench_strength - float: a number between 0 and 1 inclusive that denotes how much to take the bench into account when optimising the squad
    :param future_gw_multiplier - float: a number between 0 and 1 inclusive that denotes how much importance to give to future gameweeks
        i.e. gw1 has multiplier x**0 = 1, gw2 has multiplier x**1 = x, gw3 has multiplier x**2, etc. Lower number = more emphasis on closer gws
    :param max_from_team - int: maximum number of players allowed from a single team
    """

    def remove_accents(input_str):
        """a function that removes all diacritics from latin characters"""
        nfkd_form = unicodedata.normalize("NFKD", input_str)
        return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

    def print_dfs():
        """prints out the optimised squads and transfers in an easy to read format"""
        total_starting_pts, total_bench_pts = 0, 0
        for gw in range(num_gameweeks):
            i_start = [i for i in I if y[gw][i].x == 1]
            starting = df.iloc[i_start].copy()
            starting.pos = pd.Categorical(starting.pos, categories=["G", "D", "M", "F"])
            starting = starting.sort_values(
                by=["pos", f"{start_gw + gw}_pts"], ascending=[True, False]
            )

            i_bench = [i for i in I if x[gw][i].x == 1 and y[gw][i].x == 0]
            bench = df.iloc[i_bench].copy()
            sorted_bench = pd.concat(
                [
                    bench.loc[bench.pos == "G"],
                    bench.loc[bench.pos != "G"].sort_values(
                        by=f"{start_gw + gw}_pts", ascending=False
                    ),
                ]
            )

            captain_i = [i for i in I if z[gw][i].x == 1][0]
            starting.loc[captain_i, "name"] += " (c)"
            starting.loc[captain_i, f"{start_gw + gw}_pts"] *= 2

            result = pd.concat([starting, sorted_bench])
            result = result.reset_index(drop=True)
            result.index += 1

            total_starting_pts += starting[f"{start_gw + gw}_pts"].sum()
            total_bench_pts += bench[f"{start_gw + gw}_pts"].sum()

            # prints out full points dataframe for each gameweek - could easily be changed later
            print(f"GW {gw + start_gw}")
            print(
                result.loc[
                    :,
                    ["id", "team", "pos", "name", "cost"]
                    + [f"{start_gw+x}_pts" for x in range(num_gameweeks)],
                ]
            )
            print(f"\nCost: £{result.cost.sum()}m")
            print(
                f"Points: {starting[f'{start_gw + gw}_pts'].sum():.2f} (+{bench[f'{start_gw + gw}_pts'].sum():.2f} on the bench)\n\n"
            )

            if gw != num_gameweeks - 1:
                t_in = df.iloc[
                    [i for i in I if x[gw + 1][i].x == 1 and x[gw][i].x == 0]
                ]
                t_out = df.iloc[
                    [i for i in I if x[gw][i].x == 1 and x[gw + 1][i].x == 0]
                ]
                if len(t_out) > 0:
                    [print(f"OUT: {t_out.name.iloc[j]}") for j in range(len(t_out))]
                    [print(f"IN: {t_in.name.iloc[j]}") for j in range(len(t_in))]
                    print("\n")

        print(
            f"Total points from GW {start_gw}-{end_gw}: {total_starting_pts:.2f} (+{total_bench_pts:.2f} on the bench)\n\n"
        )

    num_gameweeks = end_gw - start_gw + 1
    df = pd.read_csv(filepath)

    # remove all players in out_team from dataframe
    for player in out_team:
        if isinstance(player, str):
            player = remove_accents(player.lower())
            df = df[df.name.apply(lambda x: remove_accents(x.lower())) != player]
        elif isinstance(player, int):
            df = df[df.id != player]

    I = range(len(df))
    df = df.reset_index(drop=True)
    model = Model()

    x = []  # players in 15-man squad
    y = []  # players in starting 11
    z = []  # player chosen as captain
    both = []  # players in both 15 man squads between 2 gameweeks

    for a in range(num_gameweeks):
        x.append([model.add_var(var_type=BINARY) for i in I])
        y.append([model.add_var(var_type=BINARY) for i in I])
        z.append([model.add_var(var_type=BINARY) for i in I])

        # ensure captain is a subset of the starting xi, which is itself a subset of the 15 man squad
        for i in I:
            model += z[a][i] <= y[a][i]
            model += y[a][i] <= x[a][i]

        # add budget constraint
        model += xsum(df.cost[i] * x[a][i] for i in I) <= budget

        # add positional and teamsize constraints
        model += xsum(x[a][i] for i in I if df.pos[i] == "G") == 2
        model += xsum(y[a][i] for i in I if df.pos[i] == "G") == 1

        rules = {
            "DEF": [3, 5],
            "MID": [2, 5],
            "FWD": [1, 3],
        }
        for pos in ["DEF", "MID", "FWD"]:
            model += xsum(x[a][i] for i in I if df.pos[i] == pos[0]) == rules[pos][1]
            model += (
                rules[pos][0]
                <= xsum(y[a][i] for i in I if df.pos[i] == pos[0])
                <= rules[pos][1]
            )

        # 15 in entire squad, 11 in starting squad, 1 captain
        model += xsum(x[a][i] for i in I) == 15
        model += xsum(y[a][i] for i in I) == 11
        model += xsum(z[a][i] for i in I) == 1

        # add max_from_team constraint
        for team in df.team.unique():
            model += xsum(x[a][i] for i in I if df.team[i] == team) <= max_from_team

    # add in_team constraints
    for player in in_team:
        if isinstance(player, str):
            player = remove_accents(player.lower())
            ind = df.index[df.name.apply(lambda x: remove_accents(x.lower())) == player]
            if len(ind) != 1:
                print(
                    f"There is more than one player with the name {player}. Specify which one you mean by using their ID instead."
                )
                return
        elif isinstance(player, int):
            ind = df.index[df.id == player]

        for gw in range(num_gameweeks):
            model += x[gw][ind[0]] == 1

    # add constraint that says that a maximum of 2 transfers can be made between gameweeks
    # TODO: remove this constraint and take it into account in the objective function instead
    for a in range(num_gameweeks - 1):
        both.append([model.add_var(var_type=BINARY) for i in I])
        model += xsum(both[a][i] for i in I) >= 13
        for i in I:
            model += x[a][i] >= both[a][i]
            model += x[a + 1][i] >= both[a][i]

        # maximum of n transfers after n gameweeks
        model += xsum(15 - xsum(both[k][i] for i in I) for k in range(a + 1)) <= a + 1

    # add the objective function
    model.objective = maximize(
        xsum(
            [
                future_gw_multiplier ** j
                * (
                    (1 - bench_strength)
                    * (
                        xsum(df[f"{start_gw + j}_pts"][i] * y[j][i] for i in I)
                        + xsum(df[f"{start_gw + j}_pts"][i] * z[j][i] for i in I)
                    )
                    + bench_strength
                    * (
                        xsum(df[f"{start_gw + j}_pts"][i] * x[j][i] for i in I)
                        - xsum(df[f"{start_gw + j}_pts"][i] * y[j][i] for i in I)
                    )
                )
                for j in range(num_gameweeks)
            ]
        )
    )

    # find an optimal solution and print it
    model.optimize()
    print_dfs()


optimise(
    start_gw=1,
    end_gw=5,
    # in_team=["werner", "salah"],
    # out_team=["vinagre", "nyland", 451],
)
