from flask import Flask, render_template, request

app = Flask(__name__)

# Mukammal ma'lumotlar strukturasi
players_db = [
    {
        "rank": 1,
        "name": "Lionel Messi",
        "country": "Argentina 🇦🇷",
        "current_club": "Inter Miami",
        # Har bir yil uchun alohida o'yin, gol va kuboklar (Haqiqiy o'zgaruvchan ma'lumotlar)
        "yearly_stats": {
            "2026": {"games": 18, "goals": 14, "assists": 9, "trophies": "MLS Cup"},
            "2024": {"games": 35, "goals": 28, "assists": 15, "trophies": "Copa America 🏆"},
            "2023": {"games": 44, "goals": 32, "assists": 25, "trophies": "Jahon Chempionati 🏆, Oltin To'p"},
            "2018": {"games": 54, "goals": 51, "assists": 26, "trophies": "La Liga, Oltin Butsa"},
            "2015": {"games": 57, "goals": 58, "assists": 31, "trophies": "UEFA Chempionlar Ligasi 🏆, La Liga"},
            "2012": {"games": 60, "goals": 73, "assists": 29, "trophies": "Kopa del Rey, Oltin To'p"}
        }
    },
    {
        "rank": 2,
        "name": "Cristiano Ronaldo",
        "country": "Portugaliya 🇵🇹",
        "current_club": "Al-Nassr",
        "yearly_stats": {
            "2026": {"games": 22, "goals": 19, "assists": 4, "trophies": "Saudiya Superkubogi"},
            "2024": {"games": 47, "goals": 44, "assists": 13, "trophies": "Saudiya Ligasi To'purari"},
            "2018": {"games": 44, "goals": 44, "assists": 8, "trophies": "UEFA Chempionlar Ligasi 🏆"},
            "2016": {"games": 48, "goals": 51, "assists": 15, "trophies": "UEFA Chempionlar Ligasi 🏆, Yevro-2016 🏆"},
            "2012": {"games": 55, "goals": 60, "assists": 12, "trophies": "La Liga Chempioni"}
        }
    }
]

# Qolgan 100 tagacha futbolchilarni test uchun to'ldirish
for i in range(3, 101):
    players_db.append({
        "rank": i,
        "name": f"Futbolchi №{i}",
        "country": "Xalqaro 🌐",
        "current_club": "Yevropa Klubi",
        "yearly_stats": {
            "2026": {"games": 20, "goals": 10, "assists": 5, "trophies": "Yo'q"},
            "2024": {"games": 38, "goals": 22, "assists": 8, "trophies": "Milliy Kubok"},
            "2012": {"games": 30, "goals": 12, "assists": 4, "trophies": "Yo'q"}
        }
    })

@app.route('/')
def index():
    selected_year = request.args.get('year', '2026')
    search_query = request.args.get('search', '').lower()
    
    output_players = []
    
    for p in players_db:
        if search_query and search_query not in p['name'].lower():
            continue
            
        # 1. UMUMIY (KARYERA) STATISTIKASINI AVTOMATIK HISOBLASH
        total_games = sum(data['games'] for data in p['yearly_stats'].values())
        total_goals = sum(data['goals'] for data in p['yearly_stats'].values())
        
        # Kuboklar ro'yxatini yig'ish (bo'sh bo'lmaganlarini)
        all_trophies = [data['trophies'] for data in p['yearly_stats'].values() if data['trophies'] != "Yo'q"]
        total_trophies_count = len(all_trophies) 
        
        # 2. TANLANGAN YILDAGI STATISTIKA
        year_data = p['yearly_stats'].get(selected_year, {"games": 0, "goals": 0, "assists": 0, "trophies": "O'ynamagan yoki Ma'lumot yo'q"})
        
        # O'yin/Gol koeffitsiyenti (Samaradorlik)
        efficiency = round(year_data['goals'] / year_data['games'], 2) if year_data['games'] > 0 else 0
        
        output_players.append({
            "rank": p['rank'],
            "name": p['name'],
            "country": p['country'],
            "club": p['current_club'],
            
            # Karyera (Obshiy)
            "total_games": total_games,
            "total_goals": total_goals,
            "total_trophies": total_trophies_count,
            
            # Shu yildagi (Specific)
            "year_games": year_data['games'],
            "year_goals": year_data['goals'],
            "year_assists": year_data['assists'],
            "year_trophies": year_data['trophies'],
            "efficiency": efficiency
        })
        
    return render_template('index.html', players=output_players, year=selected_year, search=search_query)

if __name__ == '__main__':
    app.run(debug=True)
