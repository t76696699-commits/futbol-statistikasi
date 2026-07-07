from flask import Flask, render_template, request

app = Flask(__name__)

# Mukammal ma'lumotlar strukturasi
players_db = [
  {
    "rank": 1,
    "name": "Lionel Messi",
    "country": "Argentina 🇦🇷",
    "yearly_stats": {
      "2012": {"club": "Barcelona", "games": 60, "goals": 73, "assists": 29, "trophies": "Oltin To'p"},
      "2015": {"club": "Barcelona", "games": 57, "goals": 58, "assists": 31, "trophies": "UEFA Chempionlar Ligasi 🏆"},
      "2023": {"club": "PSG / Inter Miami", "games": 44, "goals": 32, "assists": 25, "trophies": "Jahon Chempionati 🏆, Oltin To'p"},
      "2026": {"club": "Inter Miami", "games": 18, "goals": 14, "assists": 9, "trophies": "MLS Cup"}
    }
  },
  {
    "rank": 2,
    "name": "Cristiano Ronaldo",
    "country": "Portugaliya 🇵🇹",
    "yearly_stats": {
      "2012": {"club": "Real Madrid", "games": 55, "goals": 60, "assists": 12, "trophies": "La Liga"},
      "2016": {"club": "Real Madrid", "games": 48, "goals": 51, "assists": 15, "trophies": "Yevro-2016 🏆, Oltin To'p"},
      "2024": {"club": "Al-Nassr", "games": 47, "goals": 44, "assists": 13, "trophies": "Saudiya Ligasi To'purari"},
      "2026": {"club": "Al-Nassr", "games": 22, "goals": 19, "assists": 4, "trophies": "Yo'q"}
    }
  },
  {
    "rank": 3,
    "name": "Neymar Jr",
    "country": "Braziliya 🇧🇷",
    "yearly_stats": {
      "2015": {"club": "Barcelona", "games": 51, "goals": 39, "assists": 25, "trophies": "UEFA Chempionlar Ligasi 🏆"},
      "2020": {"club": "PSG", "games": 27, "goals": 19, "assists": 12, "trophies": "Ligue 1, YChL Finali"},
      "2026": {"club": "Al-Hilal", "games": 12, "goals": 5, "assists": 8, "trophies": "Yo'q"}
    }
  },
  {
    "rank": 4,
    "name": "Luka Modrić",
    "country": "Xorvatiya 🇭🇷",
    "yearly_stats": {
      "2018": {"club": "Real Madrid", "games": 46, "goals": 5, "assists": 11, "trophies": "Oltin To'p, JCh Kumush medali"},
      "2024": {"club": "Real Madrid", "games": 43, "goals": 2, "assists": 8, "trophies": "La Liga, YChL 🏆"},
      "2026": {"club": "Real Madrid", "games": 15, "goals": 1, "assists": 3, "trophies": "Yo'q"}
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
