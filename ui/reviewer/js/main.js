import { showAutocompleteOptions } from './address_search.js';

// Using Maplibre GL
const map = new maplibregl.Map({
  container: 'map',
  style: 'https://api.maptiler.com/maps/dataviz/style.json?key=xdCfCPvJINrcgKlAsJf4',
  center: [-75.1652, 39.9526],
  zoom: 12
});

map.on('load', () => {
  // Add properties vector tile source
  map.addSource('properties', {
    type: 'vector',
    tiles: [
      'https://storage.googleapis.com/musa5090s25-team5-public/tiles/properties/{z}/{x}/{y}.pbf'
    ],
    minzoom: 12,
    maxzoom: 20
  });

  // Add properties fill layer
  map.addLayer({
    id: 'properties-fill',
    type: 'fill',
    source: 'properties',
    'source-layer': 'property_tile_info',
    paint: {
      'fill-color': [
        'interpolate',
        ['linear'],
        ['get', 'tax_year_assessed_value'],
        0, '#f0f9e8',
        500000, '#bae4bc',
        1000000, '#7bccc4',
        5000000, '#2b8cbe',
        10000000, '#08589e'
      ],
      'fill-opacity': 0.4
    }
  });

  // 🔄 Load neighborhood GeoJSON source
  map.addSource('neighborhoods', {
    type: 'geojson',
    data: 'https://storage.googleapis.com/musa5090s25-team5-raw_data/neighborhoods/neighborhoods.geojson'
  });

  // Display all neighborhoods (light gray)
  map.addLayer({
    id: 'neighborhoods-fill',
    type: 'fill',
    source: 'neighborhoods',
    paint: {
      'fill-color': '#ccc',
      'fill-opacity': 0.2,
      'fill-outline-color': '#999'
    }
  });

  // Highlight layer for selected neighborhood (starts off empty)
  map.addLayer({
    id: 'neighborhood-highlight-layer',
    type: 'fill',
    source: 'neighborhoods',
    paint: {
      'fill-color': '#ffbf00',
      'fill-opacity': 0.4
    },
    filter: ['==', 'name', ''] // ← match by 'name' property
  });
});

document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.querySelector('#search-bar input[type="text"]');
  const events = new EventTarget();

  // When address is selected from autocomplete
  events.addEventListener('autocompleteselected', (event) => {
    const feature = event.detail;
    console.log('Address selected:', feature.properties.address);
  });

  // When coordinates are manually adjusted or an address is clicked
  events.addEventListener('manualadjust', async (event) => {
    const coordinates = event.detail;

    // Zoom to the selected point
    map.flyTo({
      center: coordinates,
      zoom: 16,
      speed: 1.2,
      curve: 1
    });

    // 🔴 Highlight selected property
    const selectedProperty = {
      type: 'FeatureCollection',
      features: [{
        type: 'Feature',
        geometry: {
          type: 'Point',
          coordinates: coordinates
        },
        properties: {}
      }]
    };

    if (map.getSource('selected-property')) {
      map.getSource('selected-property').setData(selectedProperty);
    } else {
      map.addSource('selected-property', {
        type: 'geojson',
        data: selectedProperty
      });

      map.addLayer({
        id: 'selected-property-circle',
        type: 'circle',
        source: 'selected-property',
        paint: {
          'circle-radius': 10,
          'circle-color': '#d7263d',
          'circle-stroke-width': 2,
          'circle-stroke-color': '#ffffff'
        }
      });
    }

    // 🟡 Highlight matching neighborhood using Turf.js
    const neighborhoods = map.getSource('neighborhoods')._data;
    const point = turf.point(coordinates);

    const matching = neighborhoods.features.find(feature =>
      turf.booleanPointInPolygon(point, feature)
    );

    if (matching) {
      const neighborhoodName = matching.properties.name;
      map.setFilter('neighborhood-highlight-layer', ['==', ['get', 'name'], neighborhoodName]);
    } else {
      // No match: clear highlight
      map.setFilter('neighborhood-highlight-layer', ['==', 'name', '']);
    }
  });

  // Initialize address search
  if (searchInput) {
    initAddressSearch(searchInput, events);
  } else {
    console.error("The address input element was not found.");
  }
});
