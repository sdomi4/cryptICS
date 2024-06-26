import { API_BASE_URL } from '$lib/config';

export async function POST({ request }) {
    const requestBody = await request.json();
    const response = await fetch(`${API_BASE_URL}/plugins/rsa/homomorphic`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'accept': 'application/json'
        },
        body: JSON.stringify(requestBody)
    });
    const data = await response.json();
    return new Response(JSON.stringify(data), {
      headers: { 'Content-Type': 'application/json' }
    });
}