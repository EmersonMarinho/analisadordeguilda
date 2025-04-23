# Analisador de Guilda

Uma aplicação web para análise e comparação de estatísticas de jogadores de guildas.

## Funcionalidades

- Visualização de estatísticas de jogadores
- Comparação entre jogadores de diferentes guildas
- Atualização automática dos dados a cada hora
- Sistema de backup automático

## Requisitos

- Python 3.8+
- Dependências listadas em `requirements.txt`

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/EmersonMarinho/analisadordeguilda.git
cd analisadordeguilda
```

2. Crie um ambiente virtual e instale as dependências:
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
pip install -r requirements.txt
```

## Configuração

1. Configure a atualização automática:
   - Use o Windows Task Scheduler para executar `update_data.bat` a cada hora
   - O script irá atualizar os dados e manter backups automáticos

2. Inicie o servidor:
```bash
./run_server.bat
```

O servidor estará disponível em `http://localhost:5000`

## Estrutura do Projeto

- `app.py` - Aplicação Flask principal
- `update_data.py` - Script de atualização automática dos dados
- `run_server.bat` - Script para iniciar o servidor
- `update_data.bat` - Script para atualização manual dos dados
- `data/` - Diretório onde os dados são armazenados
  - `guild_data.json` - Dados atuais
  - `guild_data_backup_*.json` - Backups automáticos

## Logs

Os logs de atualização são armazenados em `update_data.log`

## Contribuição

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request 