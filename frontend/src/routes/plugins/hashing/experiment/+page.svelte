<script>
    import '../../../../style/globalStyle.css'
    
    import { title } from '$lib/title';
    import { navLinks } from '$lib/stores.js'
    import { onMount } from 'svelte';
    import { slide } from 'svelte/transition';
    import { quintOut } from 'svelte/easing';
  
    import de from './locales/de.json';
    import en from './locales/en.json';
  
    import { language } from '$lib/language';
	import Blockviewer from '../../../../lib/CryptICSVisualizer.svelte';

    export let form;
    export let data;
    let allOptions = data.body.algorithms;
    console.log(allOptions);
    let options = ["MD5", "SHA256", "SHA512"];
    console.log(options);
    let selectedOption;
    let showAllAlgorithms = false;
    let showDiff = false;

    function toggleShowAll() {
        showAllAlgorithms = !showAllAlgorithms;
    }

    function toggleShowDiff() {
        showDiff = !showDiff;
    }

    let hashData = form?.body || [];

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

<body>
    <div class="bodycontainer">
        <div class="hashcontainer">
            {#if !hashData.data}
            <form method="POST">
                <input name="data" type="text" placeholder="Input to be hashed">
                <select name="algorithm" bind:value={selectedOption}>
                    {#each (showAllAlgorithms ? allOptions : options) as option}
                    <option value="{option}">{option}</option>
                    {/each}
                </select>
                <button type="submit">Submit</button>
            </form>
            <button on:click={toggleShowAll}>
                {showAllAlgorithms ? 'Show Less' : 'Show More'}
            </button>
            {/if}
            {#if hashData.data}
            <div class="blockviewer">
                <Blockviewer hexdata={hashData.data}, binarydata={hashData.binary} />
            </div>
            <button on:click={toggleShowDiff}>
                {showAllAlgorithms ? 'Hide Diffusion' : 'Show Diffusion'}
            </button>
            {/if}
        </div>
        {#if showDiff}
            <div class="diffviewer" transition:slide={{ delay: 500, duration: 300, easing: quintOut, axis: 'x' }}>

            </div>
        {/if}
    </div>
</body>