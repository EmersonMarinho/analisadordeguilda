import json
from typing import List, Dict
import asyncio
import requests
from bs4 import BeautifulSoup

class GuildAnalyzer:
    def __init__(self, ranking_file: str):
        self.ranking_file = ranking_file
        self.player_data = self._load_ranking_data()
        self.guild_cache = set()
        self.class_names = {
            1: "", 2: "", 3: "", 4: "",
            5: "", 6: "", 7: "", 8: "",
            9: "", 10: "", 11: "", 12: "",
            13: "", 14: "", 15: "", 16: "",
            17: "", 18: "", 19: "", 20: "",
            21: "", 22: "", 23: "", 24: "",
            25: "", 26: ""
        }

    def _load_ranking_data(self) -> List[Dict]:
        try:
            with open(self.ranking_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar arquivo de ranking: {e}")
            return []

    async def update_guild_cache(self, guild_name: str):
        """Atualiza o cache com os jogadores da guilda especificada"""
        url = f'https://www.sa.playblackdesert.com/pt-BR/Adventure/Guild/GuildProfile?guildName={guild_name}&region=SA'
        try:
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Erro ao acessar {url}: {response.status_code}")
                return

            soup = BeautifulSoup(response.content, 'html.parser')
            adventure_list = soup.find_all('ul', class_='adventure_list_table')
            if not adventure_list:
                print(f"Sem jogadores encontrados para a guilda: {guild_name}")
                return

            new_cache = set()
            for ul in adventure_list:
                list_items = ul.find_all('li')
                for item in list_items:
                    first_column = item.find_all('div', class_='guild_name')[0].find('a')
                    first_text = first_column.get_text().strip().lower() if first_column else ""

                    second_column = item.find_all('div', class_='guild_name')[1].find('a') if len(item.find_all('div', class_='guild_name')) > 1 else None
                    second_text = second_column.get_text().strip().lower() if second_column else ""

                    if first_text:
                        new_cache.add(first_text)
                    if second_text:
                        new_cache.add(second_text)

            self.guild_cache = new_cache
            print(f"\nCache atualizado para a guilda {guild_name} ({len(self.guild_cache)} jogadores):")
            for player in self.guild_cache:
                print(f"- {player}")

        except Exception as e:
            print(f"Erro ao processar URL {url}: {e}")

    def get_player_details(self, player_name: str) -> Dict:
        """Retorna detalhes de todas as partidas de um jogador"""
        for player in self.player_data:
            if player["player"].lower() == player_name.lower():
                matches = []
                for match in player["partidas"]:
                    class_name = self.class_names.get(match["classeId"], f"Classe {match['classeId']}")
                    kills, deaths = map(int, match["kd"].split(" / "))
                    
                    matches.append({
                        "class_name": class_name,
                        "kills": kills,
                        "deaths": deaths,
                        "damage_dealt": match["danoAplicado"],
                        "damage_received": match["danoRecebido"],
                        "ccs": match["punicoes"],
                        "healing": match["cura"],
                        "result": "Vitória" if match["resultado"] == 1 else "Derrota"
                    })

                return {
                    "player": player["player"],
                    "total_matches": len(matches),
                    "matches": sorted(matches, key=lambda x: (x["kills"], -x["deaths"]), reverse=True)
                }
        
        return {"error": "Jogador não encontrado"}

    def analyze_guild_players(self) -> Dict:
        """Analisa o desempenho dos jogadores da guilda no ranking"""
        if not self.guild_cache:
            return {"error": "Cache da guilda vazio. Execute update_guild_cache primeiro."}

        guild_players = []
        for player_data in self.player_data:
            if player_data["player"].lower() in self.guild_cache:
                total_matches = len(player_data["partidas"])
                if total_matches == 0:
                    continue

                total_kills = 0
                total_deaths = 0
                total_damage = 0
                total_ccs = 0
                wins = 0

                for match in player_data["partidas"]:
                    kills, deaths = map(int, match["kd"].split(" / "))
                    total_kills += kills
                    total_deaths += deaths
                    total_damage += match["danoAplicado"]
                    total_ccs += match["punicoes"]
                    wins += 1 if match["resultado"] == 1 else 0

                player_stats = {
                    "player": player_data["player"],
                    "total_matches": total_matches,
                    "win_rate": (wins / total_matches) * 100,
                    "kills": total_kills,
                    "deaths": total_deaths,
                    "kda": total_kills / max(total_deaths, 1),
                    "avg_damage": total_damage / total_matches,
                    "avg_ccs": total_ccs / total_matches
                }
                guild_players.append(player_stats)

        return {
            "total_players": len(guild_players),
            "players": sorted(guild_players, key=lambda x: x["kda"], reverse=True)
        }

async def main():
    analyzer = GuildAnalyzer("ranking_players.json")
    guild_name = input("Digite o nome da guilda para analisar: ")
    
    # Atualiza o cache com os jogadores da guilda
    await analyzer.update_guild_cache(guild_name)
    
    # Analisa o desempenho dos jogadores
    analysis = analyzer.analyze_guild_players()
    
    if "error" in analysis:
        print(analysis["error"])
        return

    print(f"\nAnálise da guilda {guild_name}:")
    print(f"Total de jogadores encontrados: {analysis['total_players']}")
    print("\nDesempenho dos jogadores:")
    for player in analysis["players"]:
        print(f"\nJogador: {player['player']}")
        print(f"Total de partidas: {player['total_matches']}")
        print(f"Taxa de vitória: {player['win_rate']:.2f}%")
        print(f"Kills: {player['kills']}")
        print(f"Deaths: {player['deaths']}")
        print(f"KDA: {player['kda']:.2f}")
        print(f"Média de dano causado: {player['avg_damage']:.2f}")
        print(f"Média de penalidades: {player['avg_ccs']:.2f}")

if __name__ == "__main__":
    asyncio.run(main()) 