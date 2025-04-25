const booleanPointInPolygon = turf.booleanPointInPolygon;

function highlightNeighborhood(map, selectedName) {
  if (!selectedName) {
    map.setPaintProperty('neighborhoods-fade', 'fill-opacity', 0);
  } else {
    map.setPaintProperty('neighborhoods-fade', 'fill-opacity', [
      'case',
      ['==', ['get', 'NAME'], selectedName],
      0,
      0.5
    ]);
  }
}

function findNeighborhoodForParcel(parcelFeature, neighborhoodGeojson) {
  for (const hood of neighborhoodGeojson.features) {
    if (booleanPointInPolygon(parcelFeature, hood)) {
      return hood.properties.NAME;
    }
  }
  return null;
}

function flyToNeighborhood(map, neighborhoodFeature) {
    // Get the bounding box of the selected neighborhood
    const bbox = turf.bbox(neighborhoodFeature);
  
    // Use map.fitBounds to fly to the bounding box
    map.fitBounds(bbox, {
      padding: 40,
      duration: 1000, // Optional: smoother transition
    });
  }

export { highlightNeighborhood, findNeighborhoodForParcel, flyToNeighborhood };
