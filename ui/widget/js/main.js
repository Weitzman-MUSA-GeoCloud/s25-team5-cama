import { searchPropertyFromAPI } from "./search_property_api.js";
import { updatePropertyInfo } from "./update_property_info.js";
import { createChart } from "./create_chart.js";
import { resetWidget } from "./reset_widget.js";

const apiUrl = "https://query-historic-property-info-873709980123.us-east4.run.app";

document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById('address-input');
  const suggestionBox = document.getElementById('address-suggestions');
  const clearButton = document.getElementById('clear-button');

  input.addEventListener('input', async () => {
    const query = input.value.trim();
    if (query.length > 0) {
      const properties = await searchPropertyFromAPI(apiUrl, query);
      suggestionBox.innerHTML = '';

      if (properties.length === 0) {
        const noResults = document.createElement('li');
        noResults.textContent = 'No results found';
        suggestionBox.appendChild(noResults);
      } else {
        properties.forEach(property => {
          const listItem = document.createElement('li');
          listItem.textContent = property.address;
          listItem.addEventListener('click', () => {
            input.value = property.address;
            suggestionBox.innerHTML = '';

            console.log("Selected property data:", property);
            
            updatePropertyInfo(property);
            const historicData = Object.entries(property.market_value_historic).map(([year, value]) => ({
              year: +year,
              value: +value
            }));

            historicData.push({ year: 2025, value: property.market_value_2025, projected: true });
            
            createChart(historicData, "historic-value-chart");
          });

          suggestionBox.appendChild(listItem);
        });
      }
    } else {
      suggestionBox.innerHTML = '';
    }
  });

  clearButton.addEventListener('click', () => {
    resetWidget();
  });
});
