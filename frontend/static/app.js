// Check backend health on page load
async function checkHealth() {
    const healthStatus = document.getElementById('health-status');

    try {
        const response = await fetch('/api/health');
        const data = await response.json();

        healthStatus.textContent = data.message;
        healthStatus.classList.add('ok');
    } catch (error) {
        healthStatus.textContent = 'Backend unreachable';
        healthStatus.classList.add('error');
    }
}

// Fetch data from backend and render it on the page
async function fetchData() {
    const stackList = document.getElementById('stack-list');
    const apiMessage = document.getElementById('api-message');

    try {
        const response = await fetch('/api/data');
        const data = await response.json();

        // Render the stack list
        stackList.innerHTML = data.stack
            .map(item => `<li>✓ ${item}</li>`)
            .join('');

        // Render the message
        apiMessage.textContent = data.message;
    } catch (error) {
        stackList.innerHTML = '<li>Failed to load data</li>';
        apiMessage.textContent = 'Could not reach the backend API.';
    }
}

// Run both on page load
checkHealth();
fetchData();