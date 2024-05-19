<script>
    import { title } from '$lib/title';
    import { backLink } from '$lib/title'
    import { pageTitle } from '$lib/stores.js';

    import de from './locales/de.json';
    import en from './locales/en.json';

    import { language } from '$lib/language';
    let translation;
    $: {
        translation = $language === 'en' ? en : de;
        
        title.set(translation.pagetitle);
        backLink.set('/plugins/subgroups');
        pageTitle.set(translation.subgrouptitle);
    }

    export let form;
    let subgroups = form?.body.subgroups || []
    subgroups.sort(Object.keys);
</script>

<style>
  body {
    flex-grow: 1;
    padding-top: 100px;
    font-family: "Roboto", sans-serif;
  }

  .bodycontainer {
    margin-top: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  form {
        display: flex;
        flex-direction: column;
        width: fit-content;
        gap: 10px;
        padding: 20px;
        border: 2px solid #ccc;
        border-radius: 10px;
        background-color: #f8f8f8;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    input {
        padding: 8px 10px;
        border: 2px solid #ccc;
        border-radius: 5px;
        font-size: 16px;
        color: #333;
        background-color: white;
        transition: border-color 0.3s ease-in-out;
    }

    button {
    background-color: #007BFF; /* Vibrant blue background */
    color: white; /* White text for high contrast */
    border: none; /* No border for a cleaner look */
    width: fit-content; /* Control the width to not span the entire parent container */
    padding: 10px 20px; /* Appropriate padding for a comfortable click area */
    font-size: 16px; /* Readable text size */
    border-radius: 5px; /* Slightly rounded corners */
    cursor: pointer; /* Cursor changes to pointer to indicate it's clickable */
    transition: background-color 0.3s ease, box-shadow 0.3s ease; /* Smooth transition for visual effects */
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2); /* Subtle shadow for 3D effect */
  }

  button:hover {
    background-color: #0056b3; /* Darker shade of blue on hover/focus for feedback */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3); /* Slightly more pronounced shadow on hover/focus */
    outline: none; /* Remove outline to maintain the sleek look */
  }
  .subgroupcontainer {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
  }

  .subgroup {
    background-color: rgb(231, 231, 231);
    border-radius: 5px;
    padding: 10px;
    border: 1px solid #666;
  }

  .subgrouptable {
    border: 1px solid black;
    border-collapse: collapse;
    margin-top: 10px;
  }

  th, td {
    border: 1px solid black;
    padding: 5px;
    text-align: center;
  }

  th {
    background-color: lightslategray;
    color: white;
  }

  th, td {
    padding-left: 10px;
    padding-right: 10px;
  }
</style>

<body>
  <div class="bodycontainer">
  <form method="POST">
    <input name="elements" type="text" placeholder="Elements (comma-separated)">
    <input name="op" type="text" placeholder="Operation">
    <input name="mod" type="number" placeholder="Modulus">
    <button type="submit">Submit</button>
  </form>
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
  </div>
</body>
