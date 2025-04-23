import json
import logging
from datetime import datetime
from pathlib import Path
from scraper import get_guild_data  # importando a função que já existe para coletar dados

# Configuração de logging
logging.basicConfig(
    filename='update_data.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def update_json():
    try:
        # Cria o diretório data se não existir
        data_dir = Path('data')
        data_dir.mkdir(exist_ok=True)
        
        # Arquivo principal de dados
        data_file = data_dir / 'guild_data.json'
        
        # Arquivo de backup com timestamp
        backup_file = data_dir / f'guild_data_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        
        # Se existe um arquivo anterior, faz backup
        if data_file.exists():
            with open(data_file, 'r', encoding='utf-8') as f:
                old_data = json.load(f)
                with open(backup_file, 'w', encoding='utf-8') as bf:
                    json.dump(old_data, bf, ensure_ascii=False, indent=4)
            logging.info(f'Backup criado: {backup_file}')
        
        # Coleta novos dados
        new_data = get_guild_data()
        
        # Salva os novos dados
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, ensure_ascii=False, indent=4)
        
        # Limpa backups antigos (mantém apenas os últimos 5)
        backups = sorted(data_dir.glob('guild_data_backup_*.json'))
        if len(backups) > 5:
            for old_backup in backups[:-5]:
                old_backup.unlink()
                logging.info(f'Backup antigo removido: {old_backup}')
        
        logging.info('Atualização dos dados concluída com sucesso')
        return True
        
    except Exception as e:
        logging.error(f'Erro durante a atualização: {str(e)}')
        return False

if __name__ == '__main__':
    logging.info('Iniciando atualização dos dados')
    update_json() 