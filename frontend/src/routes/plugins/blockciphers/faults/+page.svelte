<script>
    import '../../../../style/globalStyle.css'
    
    import { title } from '$lib/title';
    import { navLinks } from '$lib/stores.js'
    import { onMount } from 'svelte';
  
    import de from './locales/de.json';
    import en from './locales/en.json';
  
    import { language } from '$lib/language';
    import { API_BASE_URL } from '$lib/config';

    export let data;
    let faultData;
    let loading = true;

    let translation;
    $: {
        translation = $language === 'en' ? en : de;
        navLinks.set([
            { description: translation.diffconftitle, uri: "/plugins/blockciphers/diffusion-confusion" },
            { description: translation.ciphermodetitle, uri: "/plugins/blockciphers/ciphermodes"}
        ]);
    }

    async function fetchData() {
    const response = await fetch(`/backend/cbc`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
    });

    faultData = await response.json();
    console.log(faultData);
    loading = false;
  }
  
    onMount(() => {
        title.set('Block Ciphers');
        fetchData();
    });
</script>

<body>
    {#if loading}
        <p>Loading...</p>
    {:else}
        <div>
            <!-- Display your data here -->
            <pre>{faultData}</pre>
        </div>
    {/if}
</body>