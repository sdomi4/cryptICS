/** @type {import('./$types').PageServerLoad} */

export async function load({ fetch }) {
  // static data for now, dynamically generate random groups later
  const groupData = {
    elements: [1, 2, 3, 4, 5, 6],
    operation: "mul",
    mod: 7
  };

  const apiResponse = await fetch("http://localhost:8000/plugins/groups/subgroups", {
    method: 'post',
    headers: {
      'Content-Type': 'application/json',
      'accept': 'application/json'
    },
    body: JSON.stringify(groupData)
  });

  if (apiResponse.ok) {
    const result = await apiResponse.json();
    return {
      props: { data: result },
      error: null
    };
  } else {
    return {
      data: null,
      props: { error: "Unable to calculate group" }
    }
  }
}
