import { loadPropertyData } from "./load_property_data.js";
import { searchForAddress } from "./address_search.js";
import { updatePropertyInfo } from "./update_property_info.js";
import { drawHistoricChart } from "./draw_chart.js";
import { resetWidget } from "./reset_widget.js";

const propertyDataUrl = "https://storage.googleapis.com/musa5090s25-team5-public/configs/chart_historic_year_property.json";
let propertyData = {};

document.addEventListener("DOMContentLoaded", async () => {
  propertyData = await loadPropertyData(propertyDataUrl);

  console.log(propertyData);

  searchForAddress(propertyData, (propertyId) => {
    const selectedProperty = propertyData[propertyId];
    if (selectedProperty) {
      updatePropertyInfo(propertyId, selectedProperty);
      drawHistoricChart(selectedProperty);
    }
  });

  const clearButton = document.getElementById('clear-button');
  clearButton.addEventListener('click', () => {
    resetWidget();
  });
});
