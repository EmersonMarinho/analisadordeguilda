const axios = require('axios');
const fs = require('fs');
const path = require('path');

async function fetchAndMapPlayers() {
  try {
    const response = await axios.get('https://www.sa.playblackdesert.com/pt-BR/Intro/SAGuildLeagueSearch2025'); 
    const html = response.data;

    const match = html.match(/const ranking_data\s*=\s*(\{[\s\S]*?\});/);
    if (!match || !match[1]) throw new Error('ranking_data não encontrado.');

    const fixedJson = match[1].replace(/(\w+):/g, '"$1":');
    const rankingData = JSON.parse(fixedJson);

    const playersRaw = rankingData.sa;

    const players = Object.entries(playersRaw).map(([playerName, partidas]) => ({
      player: playerName,
      partidas: partidas.map(entry => ({
        classeId: entry[0],
        kd: entry[1],
        danoAplicado: entry[2],
        danoRecebido: entry[3],
        punicoes: entry[4],
        cura: entry[5],
        resultado: entry[6],
      }))
    }));

    fs.writeFileSync('ranking_players.json', JSON.stringify(players, null, 2));
    console.log('✅ Dados salvos em "ranking_players.json".');

  } catch (err) {
    console.error('❌ Erro ao buscar ou mapear jogadores:', err.message);
  }
}

function getPlayerData(nicks) {
  const nickList = Array.isArray(nicks) ? nicks : [nicks];

  const filePath = path.resolve(__dirname, 'ranking_players.json');

  if (!fs.existsSync(filePath)) {
    console.error('❌ Arquivo ranking_players.json não encontrado.');
    return [];
  }

  const rawData = fs.readFileSync(filePath, 'utf8');
  const players = JSON.parse(rawData);

  const filtered = players.filter(player => nickList.includes(player.player));

  if (filtered.length === 0) {
    console.log('⚠️ Nenhum jogador encontrado com esses nicknames.');
  }

  return filtered;
}

//descomente conforme seu uso \/

const result = getPlayerData(['hadox','crossfiters']); // aqui vc maqueico filtra por players
console.dir(result, { depth: null }); // aqui é só um console.log

fetchAndMapPlayers(); // aqui vc maqueico busca e extrai os players do site e salva num arquivo jason
