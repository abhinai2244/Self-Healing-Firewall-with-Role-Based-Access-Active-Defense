document.addEventListener("DOMContentLoaded", function() {
    const ctx = document.getElementById('attackChart').getContext('2d');
    
    // Initial Data
    const initialData = {
        labels: [],
        datasets: [{
            label: 'Total Attacks Detected',
            data: [],
            borderColor: 'rgba(255, 99, 132, 1)',
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            fill: true,
            tension: 0.1
        }]
    };

    const config = {
        type: 'line',
        data: initialData,
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    suggestedMax: 10
                }
            },
            animation: {
                duration: 0
            }
        }
    };

    const attackChart = new Chart(ctx, config);

    function fetchStats() {
        fetch('/api/stats')
            .then(response => response.json())
            .then(data => {
                // Update Badge Counts
                document.getElementById('total-attacks').innerText = data.total_attacks;
                document.getElementById('active-bans').innerText = data.active_bans;

                // Update Chart
                const now = new Date().toLocaleTimeString();
                
                // Add new data point
                if (attackChart.data.labels.length > 20) {
                    attackChart.data.labels.shift();
                    attackChart.data.datasets[0].data.shift();
                }
                
                attackChart.data.labels.push(now);
                attackChart.data.datasets[0].data.push(data.total_attacks);
                
                attackChart.update();
            })
            .catch(err => console.error('Error fetching stats:', err));
    }

    // Poll every 2 seconds
    setInterval(fetchStats, 2000);
    fetchStats();
});
