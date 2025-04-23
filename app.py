from flask import Flask, render_template, jsonify, request
from guild_analyzer import GuildAnalyzer
import asyncio

app = Flask(__name__)
analyzer = GuildAnalyzer("ranking_players.json")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare')
def compare():
    return render_template('compare.html')

@app.route('/analyze', methods=['POST'])
async def analyze_guild():
    guild_name = request.json.get('guild_name')
    if not guild_name:
        return jsonify({"error": "Nome da guilda não fornecido"}), 400

    await analyzer.update_guild_cache(guild_name)
    analysis = analyzer.analyze_guild_players()
    
    if "error" in analysis:
        return jsonify({"error": analysis["error"]}), 400

    return jsonify(analysis)

@app.route('/player/<player_name>')
def player_details(player_name):
    details = analyzer.get_player_details(player_name)
    if "error" in details:
        return jsonify({"error": details["error"]}), 404
    return jsonify(details)

if __name__ == '__main__':
    app.run(debug=True) 