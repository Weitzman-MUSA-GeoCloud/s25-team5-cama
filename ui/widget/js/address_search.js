function searchForAddress(propertyData, onPropertyIdSelected) {
  const input = document.getElementById('address-input');
  const suggestionBox = document.getElementById('address-suggestions');

  input.addEventListener('input', () => {
    const query = input.value.trim().toLowerCase();
    const matches = [];

    if (query.length > 0) {
      for (const [propertyId, property] of Object.entries(propertyData)) {
        const address = property.address.toLowerCase();
        if (address.includes(query)) {
          matches.push({ propertyId, address: property.address });
          if (matches.length >= 5) break;
        }
      }
    }

    suggestionBox.innerHTML = '';

    if (matches.length === 0) {
      const noResults = document.createElement('li');
      noResults.textContent = 'No results found';
      suggestionBox.appendChild(noResults);
    } else {
      matches.forEach(match => {
        const listItem = document.createElement('li');
        listItem.textContent = match.address;
        listItem.addEventListener('click', () => {
          input.value = match.address;
          suggestionBox.innerHTML = '';
          onPropertyIdSelected(match.propertyId);
        });
        suggestionBox.appendChild(listItem);
      });
    }
  });
}

export { searchForAddress };
