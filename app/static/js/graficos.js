document.addEventListener('DOMContentLoaded', function() {
    var ctx = document.getElementById('barChart').getContext('2d');

    // Obtener datos desde el contexto Jinja
    var chartData = document.getElementById('chartDataBar');
    var label = chartData.dataset.label;
    var labels = JSON.parse(chartData.dataset.labels);
    var values = JSON.parse(chartData.dataset.values);

    var barChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: values,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                        
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

document.addEventListener('DOMContentLoaded', function() {
    var ctx = document.getElementById('lineChart').getContext('2d');
    // Obtener datos desde el contexto Jinja
    var chartData = document.getElementById('chartDataLine');
    var label = chartData.dataset.label;
    var labels = JSON.parse(chartData.dataset.labels);
    var values = JSON.parse(chartData.dataset.values);

    var lineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: values,
                borderColor: 'rgba(75, 192, 192, 1)',
                fill: false
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

document.addEventListener('DOMContentLoaded', function() {
    var ctx = document.getElementById('pieChart').getContext('2d');
    var chartData = document.getElementById('chartDataPie');
    var label = chartData.dataset.label;
    var labels = JSON.parse(chartData.dataset.labels);
    var values = JSON.parse(chartData.dataset.values);
    
    var pieChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: values,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)'
                ],
                borderWidth: 1
            }]
        }
    });

});

document.addEventListener('DOMContentLoaded', function() {
    var ctx = document.getElementById('radarChart').getContext('2d');
    var chartData = document.getElementById('chartDataRadar');
    var label = chartData.dataset.label;
    var labels = JSON.parse(chartData.dataset.labels);
    var values = JSON.parse(chartData.dataset.values);
    
    var radarChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: values,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                r: {
                    beginAtZero: true
                }
            }
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var ctx = document.getElementById('doughnutChart').getContext('2d');
    var chartData = document.getElementById('chartDataDoughnut');
    var label = chartData.dataset.label;
    var labels = JSON.parse(chartData.dataset.labels);
    var values = JSON.parse(chartData.dataset.values);
    
    var doughnutChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: labels,
        datasets: [{
            label: label,
            data: values,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)'
            ],
            borderWidth: 1
        }]
    }
});


});