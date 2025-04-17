let cachedAddresses = [];

async function fetchDataset() {
  if (cachedAddresses.length > 0) return cachedAddresses;

  const url = 'https://storage.googleapis.com/YOUR_BUCKET_NAME/your_dataset.json'; // or API endpoint
  const response = await fetch(url);
  const data = await response.json();

  cachedAddresses = data; // Cache it
  return cachedAddresses;
}

async function showAutocompleteOptions() {
  const query = el.value.toLowerCase();
  const dataset = await fetchDataset();

  const matches = dataset.filter(item => 
    item.address.toLowerCase().includes(query)
  ).slice(0, 5); // Limit results to 5

  autocompleteOptionsList.classList.remove('hidden');
  autocompleteOptionsList.innerHTML = '';

  for (const place of matches) {
    const option = htmlToElement(`
      <li class="autocomplete-option">
        ${place.address}
      </li>
    `);
    option.addEventListener('click', () => {
      const feature = {
        type: 'Feature',
        geometry: {
          type: 'Point',
          coordinates: [place.longitude, place.latitude],
        },
        properties: {
          address: place.address,
          assessed_value: place.assessed_value,
        },
      };

      const autocompleteEvt = new CustomEvent('autocompleteselected', { detail: feature });
      events.dispatchEvent(autocompleteEvt);

      const manualAdjustEvt = new CustomEvent('manualadjust', { detail: [place.longitude, place.latitude] });
      events.dispatchEvent(manualAdjustEvt);

      el.value = place.address;
      autocompleteOptionsList.classList.add('hidden');
    });
    autocompleteOptionsList.appendChild(option);
  }
}

export {initAddressSearch};