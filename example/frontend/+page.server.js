/** @type {import('./$types').PageServerLoad} */
export async function load({ }) {
    const apiResponse = await fetch(`http://localhost:8000/plugins/new_module`);
    const response = await apiResponse.json()
    return {
        status: 200,
        body: response
    };
}