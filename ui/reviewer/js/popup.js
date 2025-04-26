function showParcelPopup(map, feature) {
    const props = feature.properties;
    const coords = turf.centroid(feature).geometry.coordinates; // Get parcel center for popup

    // Extract needed values
    const address = props.address;
    const assessment2024 = props.assessment_2024;
    const predicted = props.predicted_assessment;

    // Get % change from assessmentChanges JSON
    const key = props.address || address.toLowerCase(); // Use whatever your JSON is keyed by
    const changePercent = assessmentChanges[key]?.change_percent;

    // Format % change
    const formattedChange = changePercent !== undefined
        ? `<span style="color:${changePercent >= 0 ? 'green' : 'red'}">${changePercent}%</span>`
        : "N/A";

    // Create popup content
    const content = `
        <div style="font-family:Trebuchet MS, sans-serif; font-size:14px;">
            <strong>${address}</strong><br/>
            🏠 2024 Assessment: $${Number(assessment2024).toLocaleString()}<br/>
            🔮 Predicted: $${Number(predicted).toLocaleString()}<br/>
            📈 Change: ${formattedChange}
        </div>
    `;

    // Create and show the popup
    new maplibregl.Popup({ offset: [0, -10] })
        .setLngLat(coords)
        .setHTML(content)
        .addTo(map);
}
