// Function to search for the address within the vector tiles
function searchForAddress(map, query) {
    // Query the features in the vector tile layer
    const features = map.queryRenderedFeatures({
      layers: ['properties-fill'] // The layer from your vector tile source
    });
  
    const matchingAddresses = features.filter(feature => {
      // Check if the feature has an address attribute and matches the search query
      const address = feature.properties.address; // Adjust based on your vector tile attribute
      if (address) {
        // Normalize the address and query to lowercase and trim spaces
        const normalizedAddress = address.toLowerCase().trim();
        const normalizedQuery = query.toLowerCase().trim();
    
        // Check if the normalized address includes the normalized query
        return normalizedAddress.includes(normalizedQuery);
      }
      return false;
    });
  
    // If matching addresses are found, display them
    displaySuggestions(matchingAddresses, map);
  }
  
  // Function to display suggestions (could be in a dropdown or list)
  function displaySuggestions(matches, map) {
    const suggestionBox = document.getElementById('suggestions');
    suggestionBox.innerHTML = ''; // Clear previous suggestions
  
    if (matches.length === 0) {
        const noResults = document.createElement('li');
        noResults.textContent = 'No results found';
        suggestionBox.appendChild(noResults);
      } else {

        const limitedMatches = matches.slice(0, 5);

        limitedMatches.forEach(match => {
          const listItem = document.createElement('li');
          listItem.textContent = match.properties.address; // Adjust based on your feature's attribute
          listItem.addEventListener('click', () => {
            const searchInput = document.getElementById('search');
            searchInput.value = match.properties.address;

            suggestionBox.innerHTML = '';

            map.getSource('highlighted-feature').setData(match);

            zoomToFeature(map, match);
        });

        suggestionBox.appendChild(listItem);
    });
  }
}

  // Function to zoom to the selected feature
  function zoomToFeature(map, feature) {
    // Get the geometry of the feature, e.g., polygon or point

    if (!map || typeof map.flyTo !== 'function') {
        console.error('Map is either not initialized or does not have flyTo method.');
        return;
      }

    if (!feature || !feature.geometry) {
        console.error('Feature or geometry is undefined:', feature);
        return; // Exit if feature or geometry is undefined
      }
    
      const geometry = feature.geometry;
  
    // If it's a point, use the point directly
    if (geometry.type === 'Point') {
      const coords = geometry.coordinates;
      map.flyTo({
        center: coords,
        zoom: 17
      });
    }
    // If it's a polygon, zoom to the centroid of the polygon (or use another logic for bounding box)
    else if (geometry.type === 'Polygon' || geometry.type === 'MultiPolygon') {
      const centroid = turf.centroid(feature); // You can use Turf.js for centroid calculation
      map.flyTo({
        center: centroid.geometry.coordinates,
        zoom: 15
      });
    }else {
        console.error('Unsupported geometry type:', geometry.type);
  }
}

  export{searchForAddress}