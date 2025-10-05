// API helper functions for communicating with the backend.
// The API prefix is fixed to /api as per user instruction.
// Coordinates are sent as lat (coordinate_x) and lon (coordinate_y) due to a known swap issue.

const API_BASE = '/api';

/**
 * Create a new calculation for a given coordinate.
 * The backend expects coordinate_x = latitude and coordinate_y = longitude.
 * @param {number} lat Latitude
 * @param {number} lon Longitude
 * @returns {Promise<string>} calculation_id
 */
export async function createCalculation(lat, lon) {
  // The backend expects coordinate_x = longitude and coordinate_y = latitude.
  const res = await fetch(`${API_BASE}/calculation/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      coordinate_x: lon,
      coordinate_y: lat,
    }),
  });
  if (!res.ok) {
    throw new Error(`API error: ${res.status}`);
  }
  const data = await res.json();
  return data.calculation_id;
}

/**
 * Poll the calculation until a result object is available.
 * The result is an object containing a "score" field and additional integer fields.
 * @param {string} calculationId
 * @returns {Promise<Object>} result object
 */
export async function pollCalculation(calculationId) {
  while (true) {
    const res = await fetch(`${API_BASE}/calculation/${calculationId}`);
    if (!res.ok) throw new Error('Failed to get calculation');
    const data = await res.json();
    if (data.result !== null && data.result !== undefined) {
      return data.result;
    }
    // wait 1 second before next poll
    await new Promise((resolve) => setTimeout(resolve, 1000));
  }
}

/**
 * Fetch address for a given coordinate from 2GIS Catalog API.
 * Uses the same API key as the map key.
 * @param {number} lat Latitude
 * @param {number} lon Longitude
 * @param {string} key MapGL API key (2GIS)
 * @returns {Promise<string>} full address or empty string on failure
 */
export async function fetchAddress(lat, lon, key) {
  const url = `https://catalog.api.2gis.com/3.0/items/geocode?q=${lat},${lon}&key=${key}`;
  try {
    const res = await fetch(url);
    if (!res.ok) return '';
    const json = await res.json();
    const items = json?.result?.items;
    if (items && items.length > 0) {
      return items[0].full_name || '';
    }
    return '';
  } catch (err) {
    return '';
  }
}