import json
import time
import requests
from datetime import datetime
import os
import sys

def get_bot_js_data():
    """Obtém os dados do BOT.JS"""
    try:
        url = "https://www.sa.playblackdesert.com/Adventure/Guild/GuildRanking?targetDate=&searchText=&region=SA"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Erro ao acessar o BOT.JS: {response.status_code}")
        
        # Aqui você precisará implementar a lógica específica para extrair os dados do BOT.JS
        # Este é apenas um exemplo, você precisa adaptar de acordo com a estrutura real dos dados
        data = response.json()
        return data
    except Exception as e:
        print(f"Erro ao obter dados do BOT.JS: {e}")
        return None

def update_ranking_file():
    """Atualiza o arquivo ranking_players.json com novos dados"""
    try:
        # Obtém os novos dados
        new_data = get_bot_js_data()
        if not new_data:
            return False

        # Faz backup do arquivo atual
        if os.path.exists("ranking_players.json"):
            backup_name = f"ranking_players_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            os.rename("ranking_players.json", backup_name)
            print(f"Backup criado: {backup_name}")

        # Salva os novos dados
        with open("ranking_players.json", "w", encoding="utf-8") as f:
            json.dump(new_data, f, ensure_ascii=False, indent=2)
        
        print(f"Arquivo ranking_players.json atualizado em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return True
    except Exception as e:
        print(f"Erro ao atualizar arquivo: {e}")
        return False

def main():
    print("Iniciando serviço de atualização do ranking...")
    interval = 3600  # 1 hora em segundos
    
    while True:
        try:
            print(f"\nVerificando atualizações em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            update_ranking_file()
            
            # Aguarda o próximo ciclo
            print(f"Próxima verificação em 1 hora...")
            time.sleep(interval)
            
        except KeyboardInterrupt:
            print("\nServiço interrompido pelo usuário.")
            sys.exit(0)
        except Exception as e:
            print(f"Erro no ciclo de atualização: {e}")
            print("Tentando novamente em 5 minutos...")
            time.sleep(300)

if __name__ == "__main__":
    main() 