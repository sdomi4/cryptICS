<script>
    import { onMount } from 'svelte';
    import FaultViewer from '$lib/FaultViewer.svelte';
    // load relevant data from backend api

    let data;
    let loading = true;

    async function fetchData() {
    const response = await fetch('/backend/faults', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ mode: 'CBC' })
    });

    data = await response.json();
    loading = false;
  }

  onMount(() => {
    fetchData();
  });
</script>

<body>
    <!-- generic fault viewer component with loaded data -->
    {#if loading}
        <p>Loading...</p>
    {:else}
        <FaultViewer {data} />
    {/if}
</body>

