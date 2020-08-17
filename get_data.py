import aiohttp
import asyncio
import csv


async def fetch(session, url):
    headers = {"User-Agent": ""}
    async with session.get(url, headers=headers) as response:
        assert response.status == 200
        return await response.json()


def team_converter(team_id):
    """Converts a team's ID to their actual name."""
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
    """Converts a player's `element_type` to their actual position."""
    position_map = {
        1: "Goalkeeper",
        2: "Defender",
        3: "Midfielder",
        4: "Forward"
    }
    return position_map[position]


async def main():
    async with aiohttp.ClientSession() as session:
        all_data = await fetch(session, "https://fantasy.premierleague.com/api/bootstrap-static/")
    players = all_data["elements"]
    important_data = [[x["id"], team_converter(x["team"]), position_converter(x["element_type"])[0], x["web_name"],
                       x["now_cost"] / 10, x["total_points"]] for x in players]

    with open("players_data.csv", "w", encoding="utf-8", newline="") as out:
        headers = ["id", "team", "pos", "name", "cost", "points"]

        writer = csv.writer(out)
        writer.writerow(headers)
        writer.writerows(important_data)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
