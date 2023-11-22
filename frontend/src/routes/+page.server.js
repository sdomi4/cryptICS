export async function load({ params }) {
    const apiResponse = await fetch('http://localhost:8000/plugins/homepage');
    const homepageInfo = await apiResponse.json()

    return {
        status: 200,
        body: homepageInfo
    };
}