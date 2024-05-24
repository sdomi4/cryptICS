import { API_BASE_URL } from '$lib/config';

export async function GET({ }) {
    const response = await fetch(`${API_BASE_URL}/plugins/ecc/random`, {
        method: 'GET',
        headers: {
            'accept': 'application/json'
        }
    });
    const data = await response.json();
    console.log(data);
    return new Response(JSON.stringify(data), {
        headers: { 'Content-Type': 'application/json' }
    });
}