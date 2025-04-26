import Chart from 'chart.js/auto';

let chartInstance = null;

function drawHistoricChart(property) {
  const ctx = document.getElementById('historic-value-chart').getContext('2d');
  const years = Object.keys(property.market_value_historic);
  const values = Object.values(property.market_value_historic);

  if (chartInstance) {
    chartInstance.destroy();
  }

  chartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: years,
      datasets: [{
        label: 'Historic Market Value',
        data: values,
        borderColor: '#0f4d90',
        borderWidth: 2,
        fill: false,
        tension: 0.3
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: false
        }
      }
    }
  });
}

export { drawHistoricChart };
