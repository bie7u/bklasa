from calendar import month
from time import process_time, perf_counter
import json
from types import NoneType

import psycopg2


with open("tabela.json", "r", encoding="utf-8") as f:
    tabela_json = json.load(f)
def league_name():
    for k, v in tabela_json["Tabela"][-1].items():
        return k

def teams_names():
    teams_names_list = []
    list_with_data_for_table = []
    for k, v in tabela_json["Tabela"][-1].items():
        for i in v:
            list_with_data_for_table.append(i)
    for i in list_with_data_for_table:
        for k, v in i.items():
            if k == "Nazwa":
                teams_names_list.append(v)
    return sorted(teams_names_list)

def kolejka():
    list_with_round_dict = []
    list_with_round = []
    for k, v in tabela_json["Tabela"][-1].items():
        for i in v:
            if list(i.keys())[0] == "Terminarz":
                list_with_round_dict.append(list(i.values())[0])
    for i in list_with_round_dict:
        for k, v in i.items():
            list_with_round.append(k)
    return list_with_round


con = psycopg2.connect(
            host = 'localhost',
            database = 'dbtest',
            user = 'postgres',
            port = "5432",
            password = 'buber2006')
con.autocommit = True

cur = con.cursor()

cur.execute(f'DROP TABLE IF EXISTS "timetable"')
cur.execute(f'DROP TABLE IF EXISTS "clubs_names"')

cur.execute(f'CREATE TABLE "clubs_names" (league_name VARCHAR(255) NOT NULL, club_id serial PRIMARY KEY, club_name VARCHAR(255) NOT NULL)')

#rows = cur.fetchall()
cur.execute(f"""CREATE TABLE "timetable"(
        league_name VARCHAR(255) NOT NULL,
        id SERIAL PRIMARY KEY,
        round_number INT,
        date_round VARCHAR(60),
        home_team_id INT,
        CONSTRAINT FK_Home_team FOREIGN KEY (home_team_id) REFERENCES "clubs_names"(club_id),
        team_one_goals INT,
        away_team_id INT,
        CONSTRAINT FK_AWAY_team FOREIGN KEY (away_team_id) REFERENCES "clubs_names"(club_id),
        team_two_goals INT,
        home_team_win BOOLEAN,
        draw BOOLEAN,
        away_team_win BOOLEAN
);""")

calatabela = []
terminarzcaly = []
wyniki = []
all_months = 'lipca sierpnia września października listopada grudnia lutego marca kwietnia maja czerwca'
for liga in tabela_json["Tabela"]:
    for k, v in liga.items():
        if k == league_name():
            calatabela = liga[league_name()][0:len(teams_names())]
            terminarzcaly = liga[league_name()][len(teams_names()):][0]


for dane_druzyn in teams_names():
    cur.execute(f'INSERT INTO "clubs_names" (league_name, club_name) '
                f'VALUES (%s, %s);', (league_name(), dane_druzyn))

for r in range(len(kolejka())):
    for i in terminarzcaly["Terminarz"][kolejka()[r]]:

        if ":" in i:
            for i1 in i.split()[:-3]:
                if i1 not in " ".join(teams_names()) or i1 == '-':
                    wyniki.append({kolejka()[r]:" ".join(i.split()[:-3]).replace(f"{i1} ", f"/{i1}/").split("/")})
        else:
            if '-' in i.split():
                wyniki.append({kolejka()[r]: [" ".join(i.split()[:i.split().index("-")]), '-', " ".join(i.split()[i.split().index("-") + 1:])]})
            else:
                try:
                    if not i.split()[-1] in all_months.split():
                        for i1 in i.split():
                            if i1[1] == "-" or i1[0] == "-" :
                                wyniki.append({kolejka()[r]:i.replace(f"{i1} ", f"/{i1}/").split("/")})
                    else:
                        match_day = " ".join(i.split()[-2:])
                        print(match_day)
                        for i1 in i.split():
                            if i1[1] == "-" or i1[0] == "-" :
                                wyniki.append({kolejka()[r]:i.replace(f"{i1} ", f"/{i1}/").replace(match_day, "").split("/")})
                except IndexError:
                    pass

for r in range(len(kolejka())):
    for i in wyniki:
        try:
            team_one_goals = int(i[kolejka()[r]][1].split("-")[0]) if i[kolejka()[r]][1].split("-")[0] != '' else 'Null'
            team_two_goals =int(i[kolejka()[r]][1].split("-")[1]) if i[kolejka()[r]][1].split("-")[1] != '' else 'Null'
            date_round = kolejka()[r].split()[3:]
            cur.execute(f"""INSERT INTO "timetable" (league_name, round_number, date_round, home_team_id, team_one_goals, team_two_goals, away_team_id, home_team_win, draw, away_team_win)
VALUES ('{league_name()}', '{kolejka()[r].split()[1]}', '{" ".join(date_round)}', (SELECT club_id FROM clubs_names WHERE club_name = '{i[kolejka()[r]][0].strip()}'),
{team_one_goals}, {team_two_goals},
(SELECT club_id FROM clubs_names WHERE club_name = '{i[kolejka()[r]][2].strip()}'),
{True if team_one_goals > team_two_goals else False}, {True if team_one_goals == team_two_goals and team_one_goals != 'Null' else False}, {True if team_one_goals < team_two_goals else False})
;""")
        except KeyError:
            continue
con.close()

#http://www.90minut.pl/liga/1/liga13482.html esa
#http://www.90minut.pl/liga/1/liga13888.html aklasa

def start():
    pass
    # Zapytaj o link
    # Zescrapuj json (argument=link)
    # Zapisz w bazie