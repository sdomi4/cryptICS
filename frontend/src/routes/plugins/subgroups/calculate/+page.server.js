/** @type {import('./$types').PageServerLoad} */
import { API_BASE_URL } from '$lib/config';
export const actions = {
  default: async ({ request }) => {
    console.log(request);
    const data = await request.formData()
    console.log("===================")
    console.log(data);
    const apiResponse = await fetch(`${API_BASE_URL}/plugins/groups/subgroups`, {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
        'accept': 'application/json'
      },
      body: JSON.stringify({
        "elements": data.get("elements").split(','),
        "operation": data.get("op"),
        "mod": parseInt(data.get("mod"))
      })
    });
  
    const result = await apiResponse.json();
    console.log(result);
    return {
      status: 200,
      body: result
    };
  }
};

