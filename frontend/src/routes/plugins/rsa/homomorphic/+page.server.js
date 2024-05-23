// onMount function to load random cipher data to show confusion and diffusion
import { API_BASE_URL } from '$lib/config';
export async function load({ }) {
    const apiResponse = await fetch(`${API_BASE_URL}/plugins/rsa/homomorphic`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'accept': 'application/json'
        },
        body: JSON.stringify({
            initial_data: 42,
            modifier: 2
        })
    });
    const response = await apiResponse.json();
    console.log(response)
    return {
        status: 200,
        body: response
    };
}