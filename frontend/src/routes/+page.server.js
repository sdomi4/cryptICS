/** @type {import('./$types').PageServerLoad} */
import { API_BASE_URL } from '$lib/config';
export async function load({ params }) {
    const apiResponse = await fetch(`${API_BASE_URL}/plugins/homepage`);
    const homepageInfo = await apiResponse.json()

    return {
        status: 200,
        body: homepageInfo
    };
}