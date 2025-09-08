const ctx = document.getElementById('myChart').getContext('2d');
let labels = Array.from({length: 30}, (_, i) => i+1);
let data = labels.map(x => Math.sin(x/4));
let chartType = 'line';

let chart = new Chart(ctx, {
    type: chartType,
    data: {
        labels: labels,
        datasets: [{
            label: 'Dynamique',
            data: [...data],
            borderColor: '#007ACC',
            backgroundColor: '#FF5733aa',
            borderWidth: 2,
            fill: false
        }]
    },
    options: {
        responsive: false,
        animation: false,
        scales: {
            x: { beginAtZero: true },
            y: { beginAtZero: true }
        }
    }
});

let frame = 0;
let animInterval = null;

function animate() {
    frame += 1;
    if (chartType === 'line') {
        chart.data.datasets[0].data = labels.map(x => Math.sin(x/4 + frame*0.08));
    } else {
        chart.data.datasets[0].data = labels.map(x => Math.abs(Math.sin(x/4 + frame*0.08)));
    }
    chart.update();
}

function startAnimation() {
    clearInterval(animInterval);
    frame = 0;
    chartType = document.getElementById('type').value;
    chart.config.type = chartType;
    let color = chartType === 'line' ? '#007ACC' : '#FF5733aa';
    chart.data.datasets[0].borderColor = color;
    chart.data.datasets[0].backgroundColor = color;
    chart.update();

    let speed = parseInt(document.getElementById('speed').value, 10) || 100;
    animInterval = setInterval(animate, speed);
}

document.getElementById('startBtn').onclick = startAnimation;