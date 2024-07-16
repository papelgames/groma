document.addEventListener('DOMContentLoaded', function () {
    var ctx = document.getElementById('radarChart').getContext('2d');
    var labels = JSON.parse(document.getElementById('chartDataRadar').dataset.labels);
    var values = JSON.parse(document.getElementById('chartDataRadar').dataset.values);

    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: [{
                label: document.getElementById('chartDataRadar').dataset.label,
                data: values,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
