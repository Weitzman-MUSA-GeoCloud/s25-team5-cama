// Using Maplibre GL
const map = new maplibregl.Map({
  container: 'map',
  style: 'https://api.maptiler.com/maps/dataviz/style.json?key=xdCfCPvJINrcgKlAsJf4',
  center: [-75.1652, 39.9526],
  zoom: 12
});

map.on('load', () => {
  map.addSource('properties', {
      type: 'vector',
      tiles: [
          'https://storage.googleapis.com/musa5090s25-team5-public/tiles/properties/{z}/{x}/{y}.pbf'
      ],
      'minzoom': 12,
      'maxzoom': 20
  });
  map.addLayer({
      'id': 'properties-fill',
      'type': 'fill',
      'source': 'properties',
      'source-layer': 'property_tile_info',
      'paint': {
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
});

// Mapbox does not work with Maplibre GL, which works better with vector tiles

// mapboxgl.accessToken = 'pk.eyJ1Ijoic3lsdmlhdXBlbm4iLCJhIjoiY20weTdodGpiMGt4MDJsb2UzbzZnd2FmMyJ9.H6mn-LOHFUdv7swHpM7enA'

// const map = new mapboxgl.Map({
//     container: 'map', 
//     style: 'mapbox://styles/mapbox/light-v11',
//     center: [-75.1652, 39.9526], 
//     zoom: 12, 
//   });
