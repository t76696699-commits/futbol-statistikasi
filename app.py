import json
from flask import Flask, render_template, request

app = Flask(__name__)


def load_players_data():
    with open('players.json', 'r', encoding='utf-8') as file:
        return json.load(file)


@app.route('/')
def index():
    selected_year = request.args.get('year', '2026')
    search_query = request.args.get('search', '').lower()

    players_db = load_players_data()
    output_players = []

    for p in players_db:
        if search_query and search_query not in p['name'].lower():
            continue

        # 1. Karyera statistikasi
        total_games = sum(data.get('games', 0) for data in p['yearly_stats'].values())
        total_goals = sum(data.get('goals', 0) for data in p['yearly_stats'].values())
        all_trophies = [data['trophies'] for data in p['yearly_stats'].values() if data.get('trophies') != "Yo'q"]
        total_trophies_count = len(all_trophies)

        # O'zgaruvchilarni oldindan e'lon qilib qo'yamiz (PyCharm chizmasligi uchun)
        current_club = "Mavjud emas"
        year_games = 0
        year_goals = 0
        year_assists = 0
        year_trophies = "Ma'lumot yo'q"

        # 2. Tanlangan yildagi statistika
        if selected_year in p['yearly_stats']:
            year_data = p['yearly_stats'][selected_year]
            current_club = year_data.get('club', 'Noma\'lum')
            year_games = year_data.get('games', 0)
            year_goals = year_data.get('goals', 0)
            year_assists = year_data.get('assists', 0)
            year_trophies = year_data.get('trophies', "Yo'q")
        else:
            current_club = "O'ynamagan / Jarohat"
            year_games, year_goals, year_assists = "-", "-", "-"
            year_trophies = "Ma'lumot yo'q"

        if isinstance(year_games, int) and year_games > 0:
            efficiency = round(year_goals / year_games, 2)
        else:
            efficiency = 0

        output_players.append({
            "rank": p['rank'],
            "name": p['name'],
            "country": p['country'],
            "club": current_club,
            "total_games": total_games,
            "total_goals": total_goals,
            "total_trophies": total_trophies_count,
            "year_games": year_games,
            "year_goals": year_goals,
            "year_assists": year_assists,
            "year_trophies": year_trophies,
            "efficiency": efficiency
        })

    return render_template('index.html', players=output_players, year=selected_year, search=search_query)


if __name__ == '__main__':
    app.run(debug=True)
