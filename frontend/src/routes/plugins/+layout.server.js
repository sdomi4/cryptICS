/** @type {import('./$types').PageServerLoad} */
// export async function load({ route }) {
//     let dings = route.id.split('/')
//     const apiResponse = await fetch(`http://localhost:8000/plugins/navbar/${dings[2]}`);
//     const navbar = await apiResponse.json()
//     return {
//         status: 200,
//         body: navbar
//     };
// }