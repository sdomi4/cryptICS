<!-- Form.svelte -->
<script>
    export let form;
    console.log(form)
    let subgroups = form?.body.subgroups || []
    subgroups.sort(Object.keys);
</script>

<style>
  

  body {
    flex-grow: 1;
    padding-top: 100px;
  }

  table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
  }

  th {
    background-color: lightslategray;
  }

  th, td {
    padding: 5px;
    padding-left: 10px;
    padding-right: 10px;
  }

  .subgroupcontainer {
    display: flex;
  }

  .subgroup {
    background-color: blanchedalmond;
    border-radius: 5px;
    margin: 10px;
    padding: 5px;
  }
</style>

  <form method="POST">
    <input name="elements" type="text" placeholder="Elements (comma-separated)">
    <input name="op" type="text" placeholder="Operation">
    <input name="mod" type="number" placeholder="Modulus">
    <button type="submit">Submit</button>
  </form>

<body>
  <div class="subgroupcontainer">
  {#each subgroups as subgroup}
    {@const order = Object.keys(subgroup)}
    {@const elements = Object.keys(subgroup[order])}
    <div class="subgroup">
      <p>Order: {order}</p>
      <table class="subgrouptable">
        <!-- table header -->
        <tr>
          <th></th>
          {#each elements as element}
            <th>{element}</th>
          {/each}
        </tr>
        <!-- table rows -->
        {#each elements as element}
          <tr>
            <th>{element}</th>
            {#each Object.values(subgroup[order][element]) as value}
              <td>{value}</td>
            {/each}
          </tr>
        {/each}
      </table>
    </div>
    {/each}
  </div>
</body>
