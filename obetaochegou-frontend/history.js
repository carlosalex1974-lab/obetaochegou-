const IS_LOCAL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' || window.location.protocol === 'file:';
const API_URL = IS_LOCAL 
    ? "http://localhost:8000/api/v1/matches/history" 
    : "https://obetaochegou-api.onrender.com/api/v1/matches/history";

document.addEventListener("DOMContentLoaded", () => {
    const statsContainer = document.getElementById("stats-container");
    const historyList = document.getElementById("history-list");
    const statusText = document.getElementById("history-status-text");
    const dot = document.getElementById("history-dot");

    async function fetchHistory() {
        statusText.textContent = "Buscando histórico do banco de dados...";
        dot.classList.add("pulse");
        dot.style.backgroundColor = "var(--primary-neon)";

        try {
            const response = await fetch(API_URL);
            if (!response.ok) throw new Error("Erro na API");
            
            const data = await response.json();
            renderStats(data.stats);
            renderHistory(data.history);

            statusText.textContent = "Histórico Sincronizado.";
            dot.classList.remove("pulse");
        } catch (error) {
            console.error(error);
            statusText.textContent = "Falha ao carregar histórico.";
            dot.classList.remove("pulse");
            dot.style.backgroundColor = "red";
        }
    }

    function renderStats(stats) {
        if (!stats) return;

        statsContainer.innerHTML = `
            <div class="stat-card winrate" style="animation-delay: 0.1s">
                <div class="stat-title">Win Rate Global</div>
                <div class="stat-value">${stats.win_rate}%</div>
                <div style="color: var(--text-muted); font-size: 0.9rem; margin-top: 0.5rem;">Total de Palpites: ${stats.total_predictions}</div>
            </div>
            <div class="stat-card green" style="animation-delay: 0.2s">
                <div class="stat-title">Greens Acertados ✅</div>
                <div class="stat-value">${stats.total_greens}</div>
            </div>
            <div class="stat-card red" style="animation-delay: 0.3s">
                <div class="stat-title">Reds Errados ❌</div>
                <div class="stat-value">${stats.total_reds}</div>
            </div>
        `;
    }

    function renderHistory(historyData) {
        if (!historyData || historyData.length === 0) {
            historyList.innerHTML = "<p style='text-align: center; color: var(--text-muted); padding: 2rem;'>Nenhum jogo auditado encontrado no banco de dados.</p>";
            return;
        }

        historyList.innerHTML = "";

        historyData.forEach((match, index) => {
            const matchDate = new Date(match.date).toLocaleString('pt-BR', { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' });
            
            let predictionsHtml = "";
            if (match.predictions && match.predictions.length > 0) {
                match.predictions.forEach(p => {
                    const isGreen = p.resultado.toUpperCase() === "GREEN";
                    const statusClass = isGreen ? "green" : "red";
                    const badge = isGreen ? "✅ GREEN" : "❌ RED";
                    
                    predictionsHtml += `
                        <div class="prediction-item ${statusClass}">
                            <div style="display: flex; justify-content: space-between;">
                                <span class="pred-title">${p.palpite}</span>
                                <span class="badge badge-${statusClass}">${badge}</span>
                            </div>
                            <div class="pred-rationale">${p.explicacao}</div>
                        </div>
                    `;
                });
            } else {
                predictionsHtml = "<p style='color: var(--text-muted);'>Nenhum palpite registrado para este jogo.</p>";
            }

            const card = document.createElement("div");
            card.className = "history-card";
            card.style.animationDelay = `${(index * 0.1) + 0.3}s`;
            
            card.innerHTML = `
                <div class="history-header">
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <span style="font-size: 1.2rem; font-weight: 600;">${match.home_team}</span>
                        <div class="match-score">${match.home_goals !== null ? match.home_goals : '-'} x ${match.away_goals !== null ? match.away_goals : '-'}</div>
                        <span style="font-size: 1.2rem; font-weight: 600;">${match.away_team}</span>
                    </div>
                    <div class="match-date">${matchDate}</div>
                </div>
                <div style="margin-bottom: 1rem; display: flex; gap: 1rem;">
                    <span style="background: rgba(34, 197, 94, 0.1); color: #22c55e; padding: 0.3rem 0.8rem; border-radius: 12px; font-size: 0.85rem; font-weight: 600;">
                        ${match.match_greens} Greens
                    </span>
                    <span style="background: rgba(239, 68, 68, 0.1); color: #ef4444; padding: 0.3rem 0.8rem; border-radius: 12px; font-size: 0.85rem; font-weight: 600;">
                        ${match.match_reds} Reds
                    </span>
                </div>
                <div class="predictions-grid-history">
                    ${predictionsHtml}
                </div>
            `;
            
            historyList.appendChild(card);
        });
    }

    // Auto-fetch on load
    fetchHistory();
});
