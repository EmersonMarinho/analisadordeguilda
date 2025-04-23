let compareChart = null;

// Função para carregar jogadores de uma guilda
async function loadGuildPlayers(guildName, playerSelect) {
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ guild_name: guildName }),
        });

        const data = await response.json();
        
        if (response.ok) {
            if (data.total_players === 0) {
                throw new Error('Esta guilda não existe ou não possui jogadores registrados.');
            }
            
            playerSelect.innerHTML = '<option value="">Selecione um jogador</option>';
            data.players.forEach(player => {
                const option = document.createElement('option');
                option.value = player.player;
                option.textContent = `${player.player} (KDA: ${player.kda.toFixed(2)} - ${player.total_matches} partidas)`;
                playerSelect.appendChild(option);
            });
            playerSelect.disabled = false;
        } else {
            throw new Error(data.error || 'Esta guilda não existe.');
        }
    } catch (error) {
        alert(error.message);
        playerSelect.disabled = true;
        playerSelect.innerHTML = '<option value="">Selecione a guilda primeiro</option>';
    }
}

// Função para obter detalhes de um jogador
async function getPlayerDetails(playerName) {
    const response = await fetch(`/player/${encodeURIComponent(playerName)}`);
    if (!response.ok) {
        throw new Error('Erro ao carregar detalhes do jogador');
    }
    return response.json();
}

// Função para calcular estatísticas do jogador
function calculatePlayerStats(playerData) {
    const matches = playerData.matches;
    const totalMatches = matches.length;
    
    let totalKills = 0;
    let totalDeaths = 0;
    let totalDamage = 0;
    let totalCCs = 0;
    let wins = 0;

    matches.forEach(match => {
        totalKills += match.kills;
        totalDeaths += match.deaths;
        totalDamage += match.damage_dealt;
        totalCCs += match.ccs;
        if (match.result === 'Vitória') wins++;
    });

    return {
        totalMatches: totalMatches,
        kda: totalKills / Math.max(totalDeaths, 1),
        avgDamage: totalDamage / totalMatches,
        avgCCs: totalCCs / totalMatches,
        winRate: (wins / totalMatches) * 100
    };
}

// Função para atualizar a tabela de comparação
function updateComparisonTable(stats1, stats2) {
    // KDA
    document.querySelector('.player1-kd').textContent = stats1.kda.toFixed(2);
    document.querySelector('.player2-kd').textContent = stats2.kda.toFixed(2);
    document.querySelector('.diff-kd').textContent = (stats1.kda - stats2.kda).toFixed(2);

    // Dano
    document.querySelector('.player1-damage').textContent = Math.round(stats1.avgDamage).toLocaleString();
    document.querySelector('.player2-damage').textContent = Math.round(stats2.avgDamage).toLocaleString();
    document.querySelector('.diff-damage').textContent = Math.round(stats1.avgDamage - stats2.avgDamage).toLocaleString();

    // CC's
    document.querySelector('.player1-cc').textContent = stats1.avgCCs.toFixed(1);
    document.querySelector('.player2-cc').textContent = stats2.avgCCs.toFixed(1);
    document.querySelector('.diff-cc').textContent = (stats1.avgCCs - stats2.avgCCs).toFixed(1);

    // Taxa de Vitória
    document.querySelector('.player1-winrate').textContent = stats1.winRate.toFixed(1) + '%';
    document.querySelector('.player2-winrate').textContent = stats2.winRate.toFixed(1) + '%';
    document.querySelector('.diff-winrate').textContent = (stats1.winRate - stats2.winRate).toFixed(1) + '%';
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    const guild1Input = document.getElementById('guild1');
    const guild2Input = document.getElementById('guild2');
    const player1Select = document.getElementById('player1');
    const player2Select = document.getElementById('player2');
    const compareBtn = document.getElementById('compareBtn');
    const compareResults = document.getElementById('compareResults');

    // Carregar jogadores quando a guilda for digitada
    let guild1Timer, guild2Timer;
    
    guild1Input.addEventListener('input', function() {
        clearTimeout(guild1Timer);
        guild1Timer = setTimeout(() => {
            if (guild1Input.value.trim()) {
                loadGuildPlayers(guild1Input.value, player1Select);
            }
        }, 500);
    });

    guild2Input.addEventListener('input', function() {
        clearTimeout(guild2Timer);
        guild2Timer = setTimeout(() => {
            if (guild2Input.value.trim()) {
                loadGuildPlayers(guild2Input.value, player2Select);
            }
        }, 500);
    });

    // Habilitar/desabilitar botão de comparação
    function checkCompareButton() {
        compareBtn.disabled = !player1Select.value || !player2Select.value;
    }

    player1Select.addEventListener('change', checkCompareButton);
    player2Select.addEventListener('change', checkCompareButton);

    // Event listener para o botão de comparação
    compareBtn.addEventListener('click', async function() {
        try {
            const [player1Data, player2Data] = await Promise.all([
                getPlayerDetails(player1Select.value),
                getPlayerDetails(player2Select.value)
            ]);

            const stats1 = calculatePlayerStats(player1Data);
            const stats2 = calculatePlayerStats(player2Data);

            updateComparisonTable(stats1, stats2);
            compareResults.classList.remove('d-none');
        } catch (error) {
            alert(error.message);
        }
    });
}); 