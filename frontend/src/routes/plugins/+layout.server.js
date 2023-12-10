/** @type {import('./$types').PageServerLoad} */
export async function load({ route }) {
    console.log(route.id)
    let dings = route.id.split('/')
    console.log(dings)
    const apiResponse = await fetch(`http://localhost:8000/plugins/navbar/${dings[2]}`);
    const navbar = await apiResponse.json()
    console.log(navbar)
    return {
        status: 200,
        body: navbar
    };
}