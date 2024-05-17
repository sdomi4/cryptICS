import { API_BASE_URL } from '$lib/config';
export const actions = {
    default: async ({ request }) => {
      const data = await request.formData()
      const hashResponse = await fetch(`${API_BASE_URL}/plugins/hash/diffusion`, {
        method: 'post',
        headers: {
          'Content-Type': 'application/json',
          'accept': 'application/json'
        },
        body: JSON.stringify({
          "algorithm": data.get("algorithm"),
          "data": data.get("data")
        })
      });
    
      const HashResult = await hashResponse.json();
      console.log(HashResult);

      return {
        status: 200,
        body: HashResult
      };
    }
  };

// onMount function to load available hash algorithms
export async function load({ }) {
    const apiResponse = await fetch(`${API_BASE_URL}/plugins/hash`);
    const algorithms = await apiResponse.json();
    return {
        status: 200,
        body: algorithms
    };
}