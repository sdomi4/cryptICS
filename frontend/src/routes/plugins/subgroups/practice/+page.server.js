/** @type {import('./$types').PageServerLoad} */
import { API_BASE_URL } from '$lib/config';
export async function load({ fetch }) {
  // static data for now, dynamically generate random groups later
  const primes = [5, 7, 11, 13, 17];
  const randomIndex = Math.floor(Math.random() * primes.length);
  const selectedPrime = primes[randomIndex];
  const elementsArray = Array.from({ length: selectedPrime - 1 }, (_, i) => i + 1);

  const groupData = {
    elements: elementsArray,
    operation: "mul",
    mod: selectedPrime
  };

  const apiResponse = await fetch(`${API_BASE_URL}/plugins/groups/subgroups`, {
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
