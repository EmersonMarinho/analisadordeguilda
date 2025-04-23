function showLoading() {
    document.getElementById('loading').classList.remove('d-none');
    document.getElementById('error').classList.add('d-none');
    document.getElementById('results').classList.add('d-none');
}

function showError(message) {
    document.getElementById('loading').classList.add('d-none');
    document.getElementById('error').classList.remove('d-none');
    document.getElementById('error').textContent = message;
    document.getElementById('results').classList.add('d-none');
}

function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

function showResults(data) {
    document.getElementById('loading').classList.add('d-none');
    document.getElementById('error').classList.add('d-none');
    document.getElementById('results').classList.remove('d-none');

    // Atualiza o nome da guilda e contagem de jogadores
    document.getElementById('guildNameDisplay').textContent = data.guild_name;
    document.getElementById('playerCount').textContent = `${data.total_players} jogadores encontrados`;

    // Limpa a tabela
    const tableBody = document.getElementById('playerTable');
    tableBody.innerHTML = '';

    // Adiciona os jogadores à tabela
    data.players.forEach(player => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${player.player}</td>
            <td>${player.total_matches}</td>
            <td>${player.win_rate.toFixed(1)}%</td>
            <td><span class="kd-stat">${player.kills}/${player.deaths}</span> (${player.kda.toFixed(2)})</td>
            <td><span class="damage-stat">${formatNumber(Math.round(player.avg_damage))}</span></td>
            <td><span class="cc-stat">${player.avg_ccs.toFixed(1)}</span></td>
            <td>
                <button class="btn btn-sm btn-outline-primary" onclick="showPlayerDetails('${player.player}')">
                    <i class="fas fa-info-circle"></i>
                </button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

async function analyzeGuild() {
    const guildName = document.getElementById('guildName').value.trim();
    if (!guildName) {
        showError('Por favor, digite o nome da guilda');
        return;
    }

    showLoading();

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
            data.guild_name = guildName; // Adiciona o nome da guilda aos dados
            showResults(data);
        } else {
            showError(data.error || 'Erro ao analisar a guilda');
        }
    } catch (error) {
        showError('Erro ao conectar com o servidor');
    }
}

async function showPlayerDetails(playerName) {
    const modal = new bootstrap.Modal(document.getElementById('playerModal'));
    const modalContent = document.getElementById('modalContent');
    const modalLoading = document.getElementById('modalLoading');
    const modalError = document.getElementById('modalError');
    const matchTable = document.getElementById('matchTable');
    
    document.getElementById('modalPlayerName').textContent = playerName;
    modalContent.classList.add('d-none');
    modalError.classList.add('d-none');
    modalLoading.classList.remove('d-none');
    modal.show();

    try {
        const response = await fetch(`/player/${encodeURIComponent(playerName)}`);
        const data = await response.json();

        if (response.ok) {
            matchTable.innerHTML = '';
            
            // Adiciona cada partida à tabela
            data.matches.forEach(match => {
                const row = document.createElement('tr');
                const resultClass = match.result === 'Vitória' ? 'text-success' : 'text-danger';
                
                row.innerHTML = `
                    <td>
                        <span class="kd-stat">${match.kills}/${match.deaths}</span>
                    </td>
                    <td>
                        <span class="damage-stat">${formatNumber(match.damage_dealt)}</span>
                    </td>
                    <td>
                        <span class="damage-stat">${formatNumber(match.damage_received)}</span>
                    </td>
                    <td>
                        <span class="cc-stat">${match.ccs}</span>
                    </td>
                    <td>
                        <span class="heal-stat">${formatNumber(match.healing)}</span>
                    </td>
                    <td class="${resultClass}">
                        ${match.result}
                    </td>
                `;
                matchTable.appendChild(row);
            });

            modalLoading.classList.add('d-none');
            modalContent.classList.remove('d-none');
        } else {
            throw new Error(data.error || 'Erro ao carregar detalhes do jogador');
        }
    } catch (error) {
        modalLoading.classList.add('d-none');
        modalError.classList.remove('d-none');
        modalError.textContent = error.message;
    }
}

// Adiciona evento de tecla para o input
document.getElementById('guildName').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        analyzeGuild();
    }
}); 