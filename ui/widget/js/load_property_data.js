async function loadPropertyData(url) {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error("Failed to fetch property data");
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error loading property data:", error);
    return {};
  }
}

export { loadPropertyData };