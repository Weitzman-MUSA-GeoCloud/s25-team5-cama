function resetWidget() {
  // Clear address input
  document.getElementById('address-input').value = '';
  document.getElementById('address-suggestions').innerHTML = '';

  // Reset property info section
  document.getElementById('property-info').innerHTML = `
    <div class="info-row"><div class="info-label">Property ID</div><div class="info-value">N/A</div></div>
    <div class="info-row"><div class="info-label">Address</div><div class="info-value">N/A</div></div>
    <div class="info-row"><div class="info-label">Neighborhood</div><div class="info-value">N/A</div></div>
    <div class="info-row"><div class="info-label">2024 Value</div><div class="info-value">N/A</div></div>
    <div class="info-row"><div class="info-label">2025 Value</div><div class="info-value">N/A</div></div>
  `;

  // Clear SVG content
  const svg = document.getElementById('historic-value-chart');
  while (svg.firstChild) {
    svg.removeChild(svg.firstChild);
  }
}

export { resetWidget };
