from flask import Flask, render_template, request

app = Flask(__name__)

# 2012-2026 yillardagi Top 100 talik futbolchilar bazasi shabloni
# (Namuna sifatida eng asosiy yulduzlar va qolgan 100 talik o'rni ko'rsatilgan)
players_db = [
    {
        "rank": 1, "name": "Lionel Messi", "country": "Argentina 🇦🇷", "current_club": "Inter Miami",
        "yearly_stats": {
            "2026": {"goals": 15, "trophies": "MLS Supporters' Shield"},
            "2024": {"goals": 28, "trophies": "Copa America, Supporters' Shield"},
            "2023": {"goals": 32, "trophies": "Jahon Chempionati, Oltin To'p"},
            "2018": {"goals": 51, "trophies": "La Liga, Oltin Butsa"},
            "2015": {"goals": 58, "trophies": "UEFA Chempionlar Ligasi, La Liga"},
            "2012": {"goals": 73, "trophies": "Kopa del Rey, Oltin To'p (91 gol kalendar yil)"}
        }
    },
    {
        "rank": 2, "name": "Cristiano Ronaldo", "country": "Portugaliya 🇵🇹", "current_club": "Al-Nassr",
        "yearly_stats": {
            "2026": {"goals": 18, "trophies": "Qirol Cup"},
            "2024": {"goals": 44, "trophies": "Saudiya Ligasi To'purari"},
            "2018": {"goals": 44, "trophies": "UEFA Chempionlar Ligasi"},
            "2016": {"goals": 51, "trophies": "UEFA Chempionlar Ligasi, Yevro-2016, Oltin To'p"},
            "2012": {"goals": 60, "trophies": "La Liga Chempioni"}
        }
    },
    {
        "rank": 3, "name": "Robert Lewandowski", "country": "Polsha 🇵🇱", "current_club": "Barcelona",
        "yearly_stats": {
            "2026": {"goals": 25, "trophies": "La Liga"},
            "2020": {"goals": 55, "trophies": "UEFA Chempionlar Ligasi, Treble, FIFA Best"},
            "2013": {"goals": 36, "trophies": "Dortmund bilan YChL Finali"}
        }
    },
    {
        "rank": 4, "name": "Kylian Mbappé", "country": "Fransiya 🇫🇷", "current_club": "Real Madrid",
        "yearly_stats": {
            "2026": {"goals": 31, "trophies": "La Liga, UEFA Superkubogi"},
            "2022": {"goals": 44, "trophies": "Jahon Chempionati To'purari (Silver medal)"},
            "2018": {"goals": 26, "trophies": "Jahon Chempioni 🏆"}
        }
    },
    {
        "rank": 5, "name": "Erling Haaland", "country": "Norvegiya 🇳🇴", "current_club": "Manchester City",
        "yearly_stats": {
            "2026": {"goals": 34, "trophies": "Premyer Liga"},
            "2023": {"goals": 52, "trophies": "UEFA Chempionlar Ligasi, Treble, Oltin Butsa"}
        }
    }
]

# Qolgan 100 tagacha bo'lgan futbolchilarni avtomatik shablon sifatida to'ldiramiz
# Haqiqiy loyihada bularni ma'lumotlar bazasidan (PostgreSQL/SQLite) yuklab olinadi.
for i in range(6, 101):
    players_db.append({
        "rank": i,
        "name": f"Top Futbolchi №{i}",
        "country": "Xalqaro 🌐",
        "current_club": "Top Klub",
        "yearly_stats": {
            "2026": {"goals": 15, "trophies": "Mahalliy Kubok"},
            "2022": {"goals": 20, "trophies": "Chempionlik"},
            "2012": {"goals": 18, "trophies": "Yutuqlar"}
        }
    })


@app.route('/')
def index():
    # HTML-dan yil va qidiruv so'rovini olish
    selected_year = request.args.get('year', '2026')
    search_query = request.args.get('search', '').lower()

    filtered_players = []

    for p in players_db:
        # Ism bo'yicha qidiruv filtri
        if search_query and search_query not in p['name'].lower():
            continue

        # Tanlangan yildagi statistika mavjudligini tekshirish
        year_data = p['yearly_stats'].get(selected_year, {"goals": "-", "trophies": "Ma'lumot yo'q yoki o'ynamagan"})

        filtered_players.append({
            "rank": p['rank'],
            "name": p['name'],
            "country": p['country'],
            "club": p['current_club'],
            "goals": year_data['goals'],
            "trophies": year_data['trophies']
        })

    return render_template('index.html', players=filtered_players, year=selected_year, search=search_query)


if __name__ == '__main__':
    app.run(debug=True)