export const actions = {
    default: async ({ request }) => {
      const data = await request.formData()
      const hashResponse = await fetch('http://localhost:8000/plugins/hash', {
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
      // api call to convert hexdigest to binary for display
      const binaryResponse = await fetch('http://localhost:8000/plugins/hexToBinary', {
        method: 'post',
        headers: {
          'Content-Type': 'application/json',
          'accept': 'application/json'
        },
        body: JSON.stringify({
          "data": HashResult.hash
        })
      });
      const binaryResult = await binaryResponse.json();
      return {
        status: 200,
        body: binaryResult
      };
    }
  };

// onMount function to load available hash algorithms
export async function load({ }) {
    const apiResponse = await fetch(`http://localhost:8000/plugins/hash`);
    const algorithms = await apiResponse.json();
    return {
        status: 200,
        body: algorithms
    };
}