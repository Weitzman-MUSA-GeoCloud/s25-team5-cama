async function searchPropertyFromAPI(apiUrl, query) {
  try {
    const response = await fetch(`${apiUrl}?address=${encodeURIComponent(query)}`);
    if (!response.ok) {
      throw new Error('Failed to fetch property suggestions');
    }
    const properties = await response.json();
    return properties;
  } catch (error) {
    console.error('Error fetching property suggestions:', error);
    return [];
  }
}

export { searchPropertyFromAPI };
