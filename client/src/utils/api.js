
/**
 * API functions for communicating with the RSA simulation backend
 */

// Base URL for the backend API (replace with your actual backend URL)
const API_BASE_URL = 'http://localhost:8000/rsa';

/**
 * Fetch initial simulation data from the backend
 * @param {string} stage - 'keyGeneration', 'encryption', or 'decryption'
 * @param {object} data - Input parameters for the simulation
 */
export const fetchInitialSimulation = async (stage, data) => {
  const endpoint = `${API_BASE_URL}/${stage}/`;
  
  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });
    
    if (!response.ok) {
      let err
      try {
        const resData = await response.json();
        err = resData.error
      } catch (error) {
        err = "Something Went wrong"
      }
      throw new Error(`Error fetching initial simulation: ${err}`);
    }
    
    return await response.json();
  } catch (error) {
    throw error;
  }
};

/**
 * api request - Fetch next chunk of simulation steps
 * @param {string} stage - 'keyGeneration', 'encryption', or 'decryption'
 */
export const fetchNextChunk = async (stage) => {
  const endpoint = `${API_BASE_URL}/${stage}/`;
  
  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ fetch_chunk: true })
    });
    
    if (!response.ok) {
      let err
      try {
        const resData = await response.json();
        err = resData.error
      } catch (error) {
        err = "Something Went wrong"
      }
      throw new Error(`Error fetching chunk: ${err}`);
    }
    
    return await response.json();
  } catch (error) {
    throw error;
  }
};
