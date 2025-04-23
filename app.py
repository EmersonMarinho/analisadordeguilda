from flask import Flask, render_template, jsonify, request
from guild_analyzer import GuildAnalyzer
import json
from pathlib import Path

app = Flask(__name__)

# Carrega os dados do arquivo JSON
def load_data():
    data_file = Path('data/guild_data.json')
    if data_file.exists():
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

analyzer = GuildAnalyzer("ranking_players.json")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare')
def compare():
    return render_template('compare.html')

@app.route('/analyze', methods=['POST'])
def analyze_guild():
    guild_name = request.json.get('guild_name')
    if not guild_name:
        return jsonify({"error": "Nome da guilda não fornecido"}), 400

    data = load_data()
    if guild_name in data:
        return jsonify(data[guild_name])

    analysis = analyzer.analyze_guild_players()
    if "error" in analysis:
        return jsonify({"error": analysis["error"]}), 400

    return jsonify(analysis)

@app.route('/player/<guild_name>/<player_name>')
def player_details(guild_name, player_name):
    data = load_data()
    if guild_name in data and player_name in data[guild_name]['players']:
        return jsonify(data[guild_name]['players'][player_name])
    
    details = analyzer.get_player_details(player_name)
    if "error" in details:
        return jsonify({"error": details["error"]}), 404
    return jsonify(details)

@app.route('/api/guild/<guild_name>/players')
def get_guild_players(guild_name):
    data = load_data()
    if guild_name in data:
        return jsonify(list(data[guild_name]['players'].keys()))
    return jsonify([])

if __name__ == '__main__':
    app.run(debug=True) 