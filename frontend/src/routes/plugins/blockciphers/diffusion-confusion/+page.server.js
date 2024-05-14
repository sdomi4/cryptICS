// onMount function to load random cipher data to show confusion and diffusion
export async function load({ }) {
    const apiResponse = await fetch(`http://localhost:8000/plugins/blockciphers/confusion-diffusion`);
    const response = await apiResponse.json();
    console.log(response)
    return {
        status: 200,
        body: response
    };
}