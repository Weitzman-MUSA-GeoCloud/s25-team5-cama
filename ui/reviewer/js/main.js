import { searchForAddress } from './search_bar.js';
import { highlightNeighborhood,findNeighborhoodForParcel, flyToNeighborhood } from './neighborhood.js';
import { createChart } from './charts.js';

let updatingFromAddressClick = false;

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

  map.addSource('highlighted-feature', {
    type: 'geojson',
    data: {
      type: 'FeatureCollection',
      features: []
    }
  });

  map.addLayer({
    id: 'highlighted-feature-line',
    type: 'line',
    source: 'highlighted-feature',
    paint: {
      'line-color': '#FFD700',
      'line-width': 3
    }
  });

  map.addSource('neighborhoods', {
    type: 'geojson',
    data: 'https://storage.googleapis.com/musa5090s25-team5-public/neighborhoods/neighborhoods.geojson'
  });

  fetch('https://storage.googleapis.com/musa5090s25-team5-public/neighborhoods/neighborhoods.geojson')
  .then(response => response.json())
  .then(data => {
    const bbox = [-75.5, 39.8, -74.9, 40.15]; // Bounding box around Philly
    const outer = turf.bboxPolygon(bbox);

    // Combine all neighborhood geometries into one MultiPolygon
    const combined = turf.combine({
      type: "FeatureCollection",
      features: data.features
    });
    const combinedNeighborhoods = turf.buffer(combined.features[0], 0); // Clean geometry
    const mask = turf.difference(outer, combinedNeighborhoods);

    // Add the mask as a source/layer
    map.addSource('mask', {
      type: 'geojson',
      data: mask
    });

    map.addLayer({
      id: 'mask-layer',
      type: 'fill',
      source: 'mask',
      paint: {
        'fill-color': '#d3d3d3',
        'fill-opacity': 0.6
      }
    }, 'neighborhoods-outline');
  });

  map.addLayer({
    id: 'neighborhoods-outline',
    type: 'line',
    source: 'neighborhoods',
    paint: {
      'line-color': '#8D80AD', 
      'line-width': 1 
    }
  });

  map.addLayer({
    id: 'neighborhoods-fade',
    type: 'fill',
    source: 'neighborhoods',
    paint: {
      'fill-color': '#d3d3d3',
      'fill-opacity': 0 // start fully transparent
    }
  }, 'neighborhoods-outline');

  let neighborhoodGeojson = null;

  fetch('https://storage.googleapis.com/musa5090s25-team5-public/neighborhoods/neighborhoods.geojson')
  .then(response => response.json())
  .then(data => {
    neighborhoodGeojson = data;

    // 🏙️ Populate dropdown
    const select = document.getElementById('neighborhood-select');
    const names = new Set();

    data.features.forEach(feature => {
      const name = feature.properties.NAME;
      if (name && !names.has(name)) {
        names.add(name);
        const option = document.createElement('option');
        option.value = name;
        option.textContent = name;
        select.appendChild(option);
      }
    });

    // 🖱️ Handle dropdown change
    select.addEventListener('change', function () {
      const selectedName = this.value;
      const selectedYear = document.querySelector(".nav-buttons button.active")?.getAttribute("data-year");

      highlightNeighborhood(map, selectedName);

      if (!updatingFromAddressClick) {
        map.getSource('highlighted-feature').setData({
          type: 'FeatureCollection',
          features: []
        });
      }
      
      // ✅ Always reset flag after dropdown change
      updatingFromAddressClick = false;
      
      
      // Find the feature
      const selectedFeature = neighborhoodGeojson.features.find(
        f => f.properties.NAME === selectedName
      );

      // Zoom to it if found
      if (selectedFeature) {
        flyToNeighborhood(map, selectedFeature);
      }

      if (selectedName && selectedYear) {
        fetch(neighborhoodData[selectedYear])
          .then(response => response.json())
          .then(data => {
            const filteredData = data.filter(d => d.neighborhood === selectedName);
            createChart(filteredData, "graph1");
          })
          .catch(error => console.error("Error loading neighborhood chart:", error));
      }
      
    });
  });

  function handleParcelClick(parcelFeature) {
    map.getSource('highlighted-feature').setData({
      type: 'FeatureCollection',
      features: [parcelFeature]
    });
  
    const [minLng, minLat, maxLng, maxLat] = turf.bbox(parcelFeature);
    map.fitBounds([[minLng, minLat], [maxLng, maxLat]], {
      padding: 40,
      duration: 1000
    });
  
    const centroid = turf.centroid(parcelFeature);
    const selectedNeighborhood = findNeighborhoodForParcel(centroid, neighborhoodGeojson);

  
    if (selectedNeighborhood) {
      highlightNeighborhood(map, selectedNeighborhood);
  
      const neighborhoodFeature = neighborhoodGeojson.features.find(
        f => f.properties.NAME === selectedNeighborhood
      );
      
      const selectedYear = document.querySelector(".nav-buttons button.active")?.getAttribute("data-year") || '2024';

      if (!selectedYear) {
        console.warn("No assessment year selected. Defaulting to 2024.");
        return;
    }

    fetch(neighborhoodData[selectedYear])
        .then(response => response.json())
        .then(data => {
            const filteredData = data.filter(d => d.neighborhood === selectedNeighborhood);
            createChart(filteredData, "graph1");
        })

      if (neighborhoodFeature) {
        flyToNeighborhood(map, neighborhoodFeature);
      }
  
      // Update dropdown to match
      const select = document.getElementById('neighborhood-select');
      select.value = selectedNeighborhood;

      updatingFromAddressClick = true;

      // Trigger the same effect as manually changing the dropdown
      const event = new Event('change');
      select.dispatchEvent(event);
    }
  }
  

  window.handleParcelClick = handleParcelClick;


  const searchInput = document.getElementById('search');

  searchInput.addEventListener('input', function () {
    const searchQuery = searchInput.value.toLowerCase();
    const suggestionBox = document.getElementById('suggestions');

  // If the search query is empty, hide the suggestions
    if (searchQuery.length === 0) {
      suggestionBox.innerHTML = ''; // Clear the suggestions
      map.getSource('highlighted-feature').setData({
        type: 'FeatureCollection',
        features: []
      });
      return; // Exit early to avoid unnecessary processing
    }

    if (searchQuery.length > 0) { // Start filtering once the query length is sufficient
      searchForAddress(map, searchQuery);
    }
  });

});

// Creating charts
// Define paths for JSON data
const phillyData = {
  "2025": "https://storage.googleapis.com/musa5090s25-team5-public/configs/chart_current_year_philadelphia.json",
  "2024": "https://storage.googleapis.com/musa5090s25-team5-public/configs/chart_tax_year_philadelphia.json"
};

const neighborhoodData = {
  "2025": "https://storage.googleapis.com/musa5090s25-team5-public/configs/chart_current_year_neighborhood.json",
  "2024": "https://storage.googleapis.com/musa5090s25-team5-public/configs/chart_tax_year_neighborhood.json"
};

// Initial load for 2024 data and activate the 2024 button
window.addEventListener('DOMContentLoaded', () => {
  const defaultYear = '2024';
  const defaultButton = document.getElementById('past-btn');
  defaultButton.classList.add('active');

  fetch(phillyData[defaultYear])
    .then(response => response.json())
    .then(data => {
      const filteredData = data.filter(d => d.tax_year == defaultYear);
      createChart(filteredData, "graph2");
    })
    .catch(error => console.error("Error loading initial Philly chart:", error));
});

// Function to update Philadelphia chart based on button clicks
document.querySelectorAll(".nav-buttons button").forEach(button => {
  button.addEventListener("click", () => {
      const selectedYear = button.getAttribute("data-year");
      console.log("Selected Year:", selectedYear);

      document.querySelectorAll(".nav-buttons button").forEach(btn => btn.classList.remove("active"));
      button.classList.add("active");

      fetch(phillyData[selectedYear])
          .then(response => response.json())
          .then(data => {
            const filteredData = data.filter(d => d.tax_year == selectedYear);
    
            // Log the filtered data to check it
            console.log("Filtered Philly Data for " + selectedYear + ":", filteredData);

            // Call createChart with the filtered data
            createChart(filteredData, "graph2");
          })
          .catch(error => console.error("Error loading Philly data:", error));

      const selectedNeighborhood = document.getElementById("neighborhood-select").value;
      if (selectedNeighborhood) {
        fetch(neighborhoodData[selectedYear])
        .then(response => response.json())
        .then(data => {
          const filteredData = data.filter(d => d.neighborhood === selectedNeighborhood);
          createChart(filteredData, "graph1");
          })
          .catch(error => console.error("Error loading neighborhood chart:", error));
        }
  });
});

// Reset button 
document.getElementById('reload-button').addEventListener('click', () => {
  const source = map.getSource('properties');
  
  if (source) {
    // This will force a re-render and refetch the tiles
    map.removeLayer('properties-fill');
    map.removeSource('properties');

    // Re-add the source
    map.addSource('properties', {
      type: 'vector',
      tiles: [
        'https://storage.googleapis.com/musa5090s25-team5-public/tiles/properties/{z}/{x}/{y}.pbf'
      ],
      minzoom: 12,
      maxzoom: 20
    });

    // Re-add the layer
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
  }

  map.flyTo({
    center: [-75.1652, 39.9526], // your original center
    zoom: 12,
    speed: 1.2 // optional: smoother transition
  });

  document.getElementById('search').value = ''; 
  document.getElementById('neighborhood-select').value = '';

  highlightNeighborhood(map, null);

  // Clear the highlighted feature
  map.getSource('highlighted-feature').setData({
    type: 'FeatureCollection',
    features: [] // No features, essentially unhighlighting
  });

  // Reset the highlighted feature ID
  let highlightedFeatureId = null;

  d3.select("#graph1 svg").remove();
});

