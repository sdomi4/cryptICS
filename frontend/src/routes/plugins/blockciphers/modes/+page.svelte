<script>
    import '../../../../style/globalStyle.css'
    
    import { title } from '$lib/title';
    import { navLinks } from '$lib/stores.js'
    import { onMount } from 'svelte';
  
    import de from './locales/de.json';
    import en from './locales/en.json';
  
    import { language } from '$lib/language';

    export let data;
    console.log(data);

    let translation;
    $: {
        translation = $language === 'en' ? en : de;
        navLinks.set([
            { description: translation.diffconftitle, uri: "/plugins/blockciphers/diffusion-confusion" },
            { description: translation.ciphermodetitle, uri: "/plugins/blockciphers/ciphermodes"},
            { description: translation.mixmodetitle, uri: "/plugins/blockciphers/mixmode"}
        ]);
    }
  
    onMount(() => {
        title.set('Block Ciphers');
    });
</script>