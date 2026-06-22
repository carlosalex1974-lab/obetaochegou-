const IS_LOCAL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' || window.location.protocol === 'file:';
const API_URL = IS_LOCAL 
    ? "http://localhost:8000/api/v1/matches/predictions" 
    : "https://obetaochegou-api.onrender.com/api/v1/matches/predictions";

document.addEventListener("DOMContentLoaded", () => {
    const grid = document.getElementById("predictions-grid");
    const btn = document.getElementById("refresh-btn");
    const statusText = document.getElementById("status-text");
    const dot = document.querySelector(".dot");
    
    // Filtros e Busca
    const searchInput = document.getElementById("search-input");
    const filterPills = document.querySelectorAll(".filter-pill");

    let allPredictions = [];
    let currentFilter = "all";

    function getPercentageNum(str) {
        if (!str || str === "N/A") return 0;
        return parseInt(str.replace("%", "")) || 0;
    }

    function renderCards() {
        grid.innerHTML = "";
        const searchTerm = searchInput.value.toLowerCase();
        
        let filtered = allPredictions.filter(p => {
            const matchHome = p.home_team.toLowerCase().includes(searchTerm);
            const matchAway = p.away_team.toLowerCase().includes(searchTerm);
            const matchLeague = p.league.toLowerCase().includes(searchTerm);
            return matchHome || matchAway || matchLeague;
        });

        if (currentFilter === "today") {
            const todayStr = new Date().toISOString().split("T")[0];
            filtered = filtered.filter(p => p.match_time && p.match_time.startsWith(todayStr));
        }

        if (filtered.length === 0) {
            grid.innerHTML = "<p style='grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 2rem;'>Nenhuma previsão corresponde à busca ou filtro.</p>";
            return;
        }

        filtered.forEach((p, index) => {
            const matchDate = p.match_time ? new Date(p.match_time).toLocaleString('pt-BR', { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' }) : 'Horário a definir';
            
            const pHome = getPercentageNum(p.predictions.home_win_prob);
            const pDraw = getPercentageNum(p.predictions.draw_prob);
            const pAway = getPercentageNum(p.predictions.away_win_prob);

            const card = document.createElement("div");
            card.className = "match-card";
            card.style.animationDelay = `${index * 0.1}s`; // Staggered animation
            card.innerHTML = `
                <div style="text-align: center; color: var(--primary-neon); font-size: 0.85rem; margin-bottom: 0.5rem; font-weight: 600;">
                    🏆 ${p.league} | 📅 ${matchDate}
                </div>
                <div class="match-teams">
                    <span class="home">${p.home_team}</span>
                    <span class="vs">VS</span>
                    <span class="away">${p.away_team}</span>
                </div>
                <div class="prediction-stats">
                    <div class="stat">
                        <span>Casa</span>
                        <div class="progress-bg"><div class="progress-fill fill-home" style="width: 0%" data-target="${pHome}%"></div></div>
                        <strong>${p.predictions.home_win_prob}</strong>
                    </div>
                    <div class="stat">
                        <span>Empate</span>
                        <div class="progress-bg"><div class="progress-fill fill-draw" style="width: 0%" data-target="${pDraw}%"></div></div>
                        <strong>${p.predictions.draw_prob}</strong>
                    </div>
                    <div class="stat">
                        <span>Fora</span>
                        <div class="progress-bg"><div class="progress-fill fill-away" style="width: 0%" data-target="${pAway}%"></div></div>
                        <strong>${p.predictions.away_win_prob}</strong>
                    </div>
                </div>
                <div class="recommendation">
                    <span>Recomendação OBetão</span>
                    <h3>${p.predictions.recommended_bet}</h3>
                    <p style="margin-top: 0.5rem; font-size: 0.85rem; color: var(--text-muted);">
                        ${p.predictions.over_2_5_goals ? 'Mais de 2.5 Gols: SIM' : 'Mais de 2.5 Gols: NÃO'}
                    </p>
                    <a href="#" class="link-analysis" onclick="openAnalysisModal(event, ${p.id})">Ler Análise Completa 📄</a>
                </div>
            `;
            grid.appendChild(card);
        });

        // Trigger animations for progress bars slightly after mount
        setTimeout(() => {
            const fills = document.querySelectorAll(".progress-fill");
            fills.forEach(fill => {
                fill.style.width = fill.getAttribute("data-target");
            });
        }, 50);
    }

    async function fetchPredictions() {
        statusText.textContent = "Buscando inteligência do backend...";
        dot.classList.add("pulse");
        dot.style.backgroundColor = "var(--primary-neon)";

        try {
            const response = await fetch(API_URL);
            if (!response.ok) throw new Error("Erro na API");
            
            const data = await response.json();
            allPredictions = data.predictions || [];
            window.predictionsData = allPredictions;

            renderCards();

            statusText.textContent = "Sincronizado e pronto.";
            dot.classList.remove("pulse");
        } catch (error) {
            console.error(error);
            statusText.textContent = "Falha ao conectar com o backend.";
            dot.classList.remove("pulse");
            dot.style.backgroundColor = "red";
            grid.innerHTML = "<p style='grid-column: 1/-1; text-align: center; color: red;'>Erro ao carregar dados. O backend está rodando em http://localhost:8000?</p>";
        }
    }

    btn.addEventListener("click", fetchPredictions);
    searchInput.addEventListener("input", renderCards);

    filterPills.forEach(pill => {
        pill.addEventListener("click", (e) => {
            filterPills.forEach(p => p.classList.remove("active"));
            e.target.classList.add("active");
            currentFilter = e.target.getAttribute("data-filter");
            renderCards();
        });
    });
    
    // Auto-fetch on load
    fetchPredictions();
});

function formatMarkdown(text) {
    if (!text) return "";
    let html = text
        .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;') // escape HTML
        .replace(/\n\n/g, '</p><p>') // paragraphs
        .replace(/\*\*(.*?)\*\*/g, '<strong style="color: var(--primary-neon);">$1</strong>') // bold
        .replace(/\*(.*?)\*/g, '<em>$1</em>') // italic
        .replace(/Força:\s*(Alta|Média|Media|Baixa)/gi, (match, force) => {
            const f = force.toLowerCase().replace('é', 'e');
            return `Força: <span class="badge strength-${f}">${force}</span>`;
        })
        .replace(/PARTE 1:/g, '<strong style="color: white; font-size: 1.1rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.2rem; display: block; margin-top: 1rem;">📝 Resumo Analítico</strong>')
        .replace(/PARTE 2:/g, '<strong style="color: white; font-size: 1.1rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.2rem; display: block; margin-top: 1.5rem; margin-bottom: 0.5rem;">🎯 5 Palpites de Apostas</strong>')
        .replace(/\n- (.*?)(?=\n|$)/g, '<li style="margin-bottom: 0.3rem; margin-left: 1rem; color: #cbd5e1;">$1</li>') // simple lists
        .replace(/\n/g, '<br>'); // remaining line breaks
    
    return `<p style="line-height: 1.6; color: var(--text-color);">${html}</p>`;
}

// Modal logic
window.openAnalysisModal = function(event, id) {
    event.preventDefault();
    const prediction = window.predictionsData.find(p => p.id === id);
    if (!prediction) return;
    
    document.getElementById("modal-title").textContent = `Análise: ${prediction.home_team} vs ${prediction.away_team}`;
    document.getElementById("modal-text").innerHTML = formatMarkdown(prediction.predictions.rationale);
    document.getElementById("analysis-modal").style.display = "flex";
}

document.getElementById("close-modal-btn").addEventListener("click", () => {
    document.getElementById("analysis-modal").style.display = "none";
});

window.addEventListener("click", (e) => {
    const modal = document.getElementById("analysis-modal");
    if (e.target === modal) {
        modal.style.display = "none";
    }
});
