// onMount function to load random cipher data to show confusion and diffusion
import { API_BASE_URL } from '$lib/config';
export async function load({ }) {
    const apiResponse = await fetch(`${API_BASE_URL}/plugins/blockciphers/avalanche`);
    const response = await apiResponse.json();
    console.log(response)
    return {
        status: 200,
        body: response
    };
}