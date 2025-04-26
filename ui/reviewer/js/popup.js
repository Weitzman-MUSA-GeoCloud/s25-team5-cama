let activePopup = null;

function showParcelPopup(map, feature, apiData) {
    const props = feature.properties;
    const coords = turf.centroid(feature).geometry.coordinates;

    const address = props.address;
    const assessment2024 = apiData.market_value_2024;
    const predicted = apiData.market_value_2025;
    const changePercent = apiData.change_percent;

    const formattedChange = changePercent !== undefined
        ? `<span style="color:${changePercent >= 0 ? 'green' : 'red'}">${changePercent}%</span>`
        : "N/A";

    const content = `
        <div style="
            font-family: 'Trebuchet MS', sans-serif;
            font-size: 14px;
            max-width: 300px;
            white-space: normal;
            word-wrap: break-word;
            line-height: 1.4;
        ">

        <div>
            <strong>${address}</strong><br/>
            2024 Value: $${Number(assessment2024).toLocaleString()}<br/>
            Predicted Value: $${Number(predicted).toLocaleString()}<br/>
            Change: ${formattedChange}
        </div>
    `;

    // Remove existing popup if there is one
    if (activePopup) {
        activePopup.remove();
    }

    // Create new popup and store it
    activePopup = new maplibregl.Popup({ offset: [0, -10], maxWidth: "300px" })
        .setLngLat(coords)
        .setHTML(content)
        .addTo(map);
}

export { showParcelPopup };
