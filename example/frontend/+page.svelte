<script>
    import { title } from '$lib/title';
    import { onMount } from 'svelte';
  
    import de from './locales/de.json';
    import en from './locales/en.json';
  
    import { language } from '$lib/language';
    let translation;
    $: translation = $language === 'en' ? en : de;
 
    onMount(() => {
        title.set('New Module');
    });

    export let data;
  </script>

<body>
    {#each data.body as element}
        <div class = "container">
            <p class="data">{element.description}</p>
        </div>
    {/each}
</body>