<script>
    import '../../../../style/globalStyle.css'
    
    import { title } from '$lib/title';
    import { navLinks } from '$lib/stores.js'
    import { onMount } from 'svelte';
  
    import de from './locales/de.json';
    import en from './locales/en.json';
  
    import { language } from '$lib/language';
    let translation;
    $: {
        translation = $language === 'en' ? en : de;
        navLinks.set([
            { description: translation.diffusiontitle, uri: "/plugins/hashing/diffusion" },
            { description: translation.experimenttitle, uri: "/plugins/hashing/experiment"}
        ]);
    }
  
  
    onMount(() => {
        title.set('Hashing');
    });
</script>