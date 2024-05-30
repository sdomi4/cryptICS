/** @type {import('./$types').PageServerLoad} */
import { API_BASE_URL } from '$lib/config';
export async function load({ fetch }) {
  let primes = [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97];
  let nonPrimes = [];
  for (let i = 10; i < 100; i++) {
      if (!primes.includes(i)) nonPrimes.push(i);
  }
  const n = nonPrimes[Math.floor(Math.random() * nonPrimes.length)];
  const groupData = {
    n: n
  };

  const apiResponse = await fetch(`${API_BASE_URL}/plugins/rsa/carmichael`, {
    method: 'post',
    headers: {
      'Content-Type': 'application/json',
      'accept': 'application/json'
    },
    body: JSON.stringify(groupData)
  });

  if (apiResponse.ok) {
    const result = await apiResponse.json();
    return result
  } else {
    console.error('Failed to fetch API:', apiResponse);
    return {
      status: apiResponse.status,
      error: await apiResponse.text()
    }
  }
}
