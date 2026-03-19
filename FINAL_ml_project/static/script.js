// Safe Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    const placementForm = document.getElementById('placementForm');
    if (placementForm) {
        placementForm.addEventListener('submit', handlePlacementSubmit);
    }

    const recommendForm = document.getElementById('recommendForm');
    if (recommendForm) {
        recommendForm.addEventListener('submit', handleRecommendSubmit);
    }

    // Theme Toggle Logic
    const themeBtn = document.getElementById('themeToggle');
    const body = document.body;

    // Apply saved theme
    if (localStorage.getItem('theme') === 'dark') {
        body.classList.add('dark-mode');
        if (themeBtn) themeBtn.innerHTML = '☀️ Light Mode';
    }

    if (themeBtn) {
        themeBtn.addEventListener('click', () => {
            body.classList.toggle('dark-mode');
            const isDark = body.classList.contains('dark-mode');
            themeBtn.innerHTML = isDark ? '☀️ Light Mode' : '🌙 Dark Mode';
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
        });
    }
});

// Prediction Handler
async function handlePlacementSubmit(event) {
    event.preventDefault();
    const btn = event.target.querySelector('button');
    btn.innerHTML = 'Analyzing...';
    btn.disabled = true;

    const data = {
        CGPA: parseFloat(document.getElementById('cgpa').value),
        Mock_OA_Score: parseInt(document.getElementById('mock_oa').value),
        Projects: parseInt(document.getElementById('projects').value),
        Internships_Done: parseInt(document.getElementById('internships').value)
    };

    try {
        const response = await fetch('/predict-placement', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await response.json();

        displayPlacementResult(result);
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to get prediction. Ensure backend is running.');
    } finally {
        btn.innerHTML = 'Analyze Profile';
        btn.disabled = false;
    }
}

function displayPlacementResult(result) {
    const box = document.getElementById('placementResult');
    box.classList.remove('hidden', 'safe', 'risk');

    const isSafe = result.status === 'Safe';
    box.classList.add(isSafe ? 'safe' : 'risk');

    // Generate Analysis List HTML
    let analysisHtml = '';
    if (result.analysis && result.analysis.length > 0) {
        analysisHtml = '<div class="analysis-box"><h4>Detailed Analysis:</h4><ul class="analysis-list">';
        result.analysis.forEach(item => {
            analysisHtml += `<li>${item}</li>`;
        });
        analysisHtml += '</ul></div>';
    }

    box.innerHTML = `
        <div class="result-title">${result.placement_probability}% Chance</div>
        <div class="result-desc">Status: <strong>${result.status}</strong></div>
        <div class="result-desc" style="margin-top:0.5rem; font-size:0.9rem">${result.message}</div>
        ${analysisHtml}
    `;
}

// Recommendation Handler
async function handleRecommendSubmit(event) {
    event.preventDefault();
    const btn = event.target.querySelector('button');
    const originalText = btn.innerHTML;
    btn.innerHTML = 'Finding Matches...';
    btn.disabled = true;

    const data = {
        Preferred_Role: document.getElementById('role').value,
        Skills: document.getElementById('skills').value,
        Location: document.getElementById('location').value
    };

    try {
        const response = await fetch('/recommend-internships', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const recommendations = await response.json();

        displayRecommendations(recommendations);
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to fetch recommendations.');
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

function displayRecommendations(list) {
    const container = document.getElementById('internshipList');
    container.innerHTML = '';

    if (list.length === 0) {
        container.innerHTML = '<div class="empty-state">No matching internships found. Try different keywords.</div>';
        return;
    }

    list.forEach(item => {
        const card = document.createElement('div');
        card.className = 'card glass';
        card.innerHTML = `
            <h4>${item.Role}</h4>
            <span class="company">${item.Company}</span>
            <div class="card-details">📍 ${item.Location}</div>
            <div class="card-details">💰 ${item.Stipend}</div>
            <div class="card-details" style="margin-top:0.8rem; font-style:italic; opacity:0.8">Skills: ${item.Required_Skills}</div>
        `;
        container.appendChild(card);
    });
}
