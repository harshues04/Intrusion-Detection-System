document.addEventListener('DOMContentLoaded', () => {
    const predictions = JSON.parse('{{ predictions | tojson }}');
    const results = predictions.reduce((acc, pred) => {
        acc[pred.result] = (acc[pred.result] || 0) + 1;
        return acc;
    }, {});
    const ctx = document.getElementById('attackChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(results),
            datasets: [{
                label: 'Attack Distribution',
                data: Object.values(results),
                backgroundColor: ['#ff6384', '#36a2eb']
            }]
        }
    });
});