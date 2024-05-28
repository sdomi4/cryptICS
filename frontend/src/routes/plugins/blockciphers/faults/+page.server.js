// onMount function to load random cipher data
import { API_BASE_URL } from '$lib/config';
export async function load({ }) {
    const apiResponse = await fetch(`${API_BASE_URL}/plugins/blockciphers/faults`);
    const response = await apiResponse.json();
    return {
        status: 200,
        body: response
    };
}