function updateLayerProperty(map, propertyName) {
    if (!map.getLayer('properties-fill')) return;
  
    map.setPaintProperty('properties-fill', 'fill-color', [
      'interpolate',
      ['linear'],
      ['get', propertyName],
      0, '#f0f9e8',
      500000, '#bae4bc',
      1000000, '#7bccc4',
      5000000, '#2b8cbe',
      10000000, '#08589e'
    ]);
  }

export { updateLayerProperty }

  