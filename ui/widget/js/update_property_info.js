function updatePropertyInfo(property) {
  if (!property) return;

  document.getElementById('property-info').innerHTML = `
    <div class="info-row"><div class="info-label">Property ID</div><div class="info-value">${property.property_id || 'N/A'}</div></div>
    <div class="info-row"><div class="info-label">Address</div><div class="info-value">${property.address || 'N/A'}</div></div>
    <div class="info-row"><div class="info-label">Neighborhood</div><div class="info-value">${property.neighborhood || 'N/A'}</div></div>
    <div class="info-row"><div class="info-label">2024 Value</div><div class="info-value">${property.market_value_historic?.['2024'] ?? 'N/A'}</div></div>
    <div class="info-row"><div class="info-label">2025 Value</div><div class="info-value">${property.market_value_2025 ?? 'N/A'}</div></div>
  `;
}

export { updatePropertyInfo };
