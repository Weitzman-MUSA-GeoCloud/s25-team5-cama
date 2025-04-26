function updateLayerProperty(property) {
    map.setPaintProperty('property-layer', 'fill-color', [
        'interpolate',
        ['linear'],
        ['get', property],
        0, '#f2f0f7',
        1000000, '#54278f'
    ]);
}

export { updateLayerProperty }