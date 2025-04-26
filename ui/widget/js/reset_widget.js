function resetWidget() {
  document.getElementById('address-input').value = '';
  document.getElementById('address-suggestions').innerHTML = '';

  document.getElementById('property-info').innerHTML = `
    <div class="info-row"><div class="info-label">Property ID</div><div class="info-value">N/A</div></div>
    <div class="info-row"><div class="info-label">Address</div><div class="info-value">N/A</div></div>
    <div class="info-row"><div class="info-label">Neighborhood</div><div class="info-value">N/A</div></div>
    <div class="info-row"><div class="info-label">2024 Value</div><div class="info-value">N/A</div></div>
    <div class="info-row"><div class="info-label">2025 Value</div><div class="info-value">N/A</div></div>
  `;

  const ctx = document.getElementById('historic-value-chart').getContext('2d');
  ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
}

export { resetWidget };
