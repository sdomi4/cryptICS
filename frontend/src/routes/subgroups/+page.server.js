/** @type {import('./$types').PageServerLoad} */
export async function load({ params }) {
	return {
		post: await get(params.slug)
	};
}
async function load() {
    const data = request.body;
  
    const apiResponse = await fetch('http://localhost:8000/plugins/groups/subgroups', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'accept': 'application/json'
      },
      body: JSON.stringify(data)
    });
  
    const result = await apiResponse.json();
    return {
      status: 200,
      body: result
    };
  }