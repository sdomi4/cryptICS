<!-- Form.svelte -->
<script>
    let elements = '';
    let operation = '';
    let mod = '';
    let subgroups = [];
  
    async function handleSubmit() {
      const response = await fetch('/subgroups', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        elements: elements.split(',').map(Number),
        operation,
        mod
      })
    });
    const data = await response.json();
    
    subgroups = data.subgroups;
    }
  </script>
  
  <form on:submit|preventDefault={handleSubmit}>
    <input type="text" bind:value={elements} placeholder="Elements (comma-separated)">
    <input type="text" bind:value={operation} placeholder="Operation">
    <input type="number" bind:value={mod} placeholder="Mod">
    <button type="submit">Submit</button>
  </form>


  
  {#each subgroups as subgroup, i (i)}
    <div>
      <h2>Subgroup {i + 1}</h2>
      <table>
        <thead>
          <tr>
            {#each Object.keys(subgroup) as key}
              <th>{key}</th>
            {/each}
          </tr>
        </thead>
        <tbody>
          {#each Object.keys(subgroup) as outerKey}
            <tr>
              {#each Object.keys(subgroup[outerKey]) as innerKey}
                <td>{innerKey}</td>
                {#each Object.keys(subgroup[outerKey][innerKey]) as innerMostKey}
                  <td>{subgroup[outerKey][innerKey][innerMostKey]}</td>
                {/each}
              {/each}
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  {/each}