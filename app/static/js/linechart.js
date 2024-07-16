document.addEventListener('DOMContentLoaded', function () {
    var ctx = document.getElementById('lineChart').getContext('2d');
    var labels = JSON.parse(document.getElementById('chartDataLine').dataset.labels);
    var values = JSON.parse(document.getElementById('chartDataLine').dataset.values);

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: document.getElementById('chartDataLine').dataset.label,
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
