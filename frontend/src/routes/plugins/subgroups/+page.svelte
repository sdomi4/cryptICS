<script>
  import { title } from '$lib/title';
  import { onMount } from 'svelte';

  onMount(() => {
      title.set('Group Theory');
  });
</script>


<body>

</body>

<style>
    body {
    flex-grow: 1;
    padding-top: 200px;
  }
</style>