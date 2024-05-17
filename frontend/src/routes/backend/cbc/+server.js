import { API_BASE_URL } from '$lib/config';

export async function POST() {

    const response = await fetch(`${API_BASE_URL}/plugins/blockciphers/faults`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'accept': 'application/json'
        },
        body: JSON.stringify({
            "mode": "CBC"
        })
    });
    const data = await response.json();
    return new Response(JSON.stringify(data), {
      headers: { 'Content-Type': 'application/json' }
    });
}