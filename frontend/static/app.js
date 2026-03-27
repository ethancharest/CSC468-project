async function checkHealth() {
    const healthStatus = document.getElementById('health-status');
    const badge = document.getElementById('system-status');
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        healthStatus.textContent = data.message;
        healthStatus.classList.add('ok');
        badge.innerHTML = '<span class="pulse"></span> Online';
        badge.classList.add('online');
    } catch (error) {
        healthStatus.textContent = 'Backend unreachable';
        healthStatus.classList.add('error');
        badge.innerHTML = '<span class="pulse"></span> Offline';
    }
}

async function fetchData() {
    const stackList = document.getElementById('stack-list');
    const apiMessage = document.getElementById('api-message');
    const hostname = document.getElementById('container-hostname');
    const python = document.getElementById('container-python');
    const timestamp = document.getElementById('container-timestamp');
    const responseTime = document.getElementById('response-time');
    try {
        const start = performance.now();
        const response = await fetch('/api/data');
        const data = await response.json();
        const elapsed = Math.round(performance.now() - start);
        stackList.innerHTML = data.stack.map(item => '<li>' + item + '</li>').join('');
        apiMessage.textContent = data.message;
        hostname.textContent = data.container.hostname;
        python.textContent = data.container.python_version;
        timestamp.textContent = new Date(data.container.timestamp).toLocaleTimeString();
        responseTime.textContent = elapsed + 'ms';
    } catch (error) {
        stackList.innerHTML = '<li>Failed to load</li>';
        apiMessage.textContent = 'Could not reach the backend API.';
    }
}

checkHealth();
fetchData();
