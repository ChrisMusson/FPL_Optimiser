from urllib.request import urlopen
from json import loads
from csv import writer


class Team_sorter:
    def team_mapping(self, team_data):
        self.team_map = {}
        for team in team_data:
            self.team_map[team['id']] = team['name']
    def team_converter(self, team_id):
        '''Converts a team's ID to their actual name'''
        return  self.team_map[team_id]

class Position_sorter:
    def position_mapping(self, position_data):
        self.position_map = {}
        for position in position_data:
            self.position_map[position['id']] = position['plural_name']
    
    def position_converter(self, position):
        '''Converts a player's element_type to their actual position'''
        return self.position_map[position]


def main():
    all_data = loads(urlopen("https://fantasy.premierleague.com/api/bootstrap-static/").read())
    players = all_data["elements"]
    #Dynamically updating teams each year.
    t = Team_sorter()
    t.team_mapping(all_data['teams'])
    #Code to get map positions dynamically.
    p = Position_sorter()
    p.position_mapping(all_data['element_types'])
    important_data = [
        [
            x["id"],
            t.team_converter(x["team"]),
            p.position_converter(x["element_type"])[0],
            x["web_name"],
            x["now_cost"] / 10,
            x["total_points"],
            
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
