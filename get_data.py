from urllib.request import urlopen
from json import loads
from csv import writer


def team_converter(team_id):
    '''Converts a team's ID to their actual name'''
    team_map = {
        1: "Arsenal",
        2: "Aston Villa",
        3: "Brighton",
        4: "Burnley",
        5: "Chelsea",
        6: "Crystal Palace",
        7: "Everton",
        8: "Fulham",
        9: "Leicester",
        10: "Leeds",
        11: "Liverpool",
        12: "Man City",
        13: "Man Utd",
        14: "Newcastle",
        15: "Sheffield Utd",
        16: "Southampton",
        17: "Spurs",
        18: "West Brom",
        19: "West Ham",
        20: "Wolves",
        None: None
    }
    return team_map[team_id]


def position_converter(position):
    '''Converts a player's element_type to their actual position'''
    position_map = {
        1: "Goalkeeper",
        2: "Defender",
        3: "Midfielder",
        4: "Forward"
    }
    return position_map[position]


def main():
    all_data = loads(urlopen("https://fantasy.premierleague.com/api/bootstrap-static/").read())
    players = all_data["elements"]

    important_data = [
        [
            x["id"],
            team_converter(x["team"]),
            position_converter(x["element_type"])[0],
            x["web_name"],
            x["now_cost"] / 10,
            x["total_points"]
        ]
        for x in players
    ]

    with open("players_data.csv", "w", encoding="utf-8", newline="") as out:
        headers = ["id", "team", "pos", "name", "cost", "points"]
        w = writer(out)
        w.writerow(headers)
        w.writerows(important_data)

if __name__ == "__main__":
    main()
