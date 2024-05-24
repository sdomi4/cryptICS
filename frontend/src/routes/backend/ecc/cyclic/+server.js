import { API_BASE_URL } from '$lib/config';

export async function GET({ }) {
    // Assuming the necessary parameters are passed as query parameters
    

    const response = await fetch(`${API_BASE_URL}/plugins/ecc/cyclic`, {
        method: 'GET',
        headers: {
            'accept': 'application/json'
        }
    });
    const data = await response.json();
    return new Response(JSON.stringify(data), {
        headers: { 'Content-Type': 'application/json' }
    });
}