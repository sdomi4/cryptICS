<script>
    import '../../../../style/globalStyle.css'
    
    import { title } from '$lib/title';
    import { navLinks } from '$lib/stores.js'
    import { onMount } from 'svelte';
    import { writable } from 'svelte/store';
  
    import de from './locales/de.json';
    import en from './locales/en.json';
  
    import { language } from '$lib/language';
	import Blockviewer from '../../../../lib/CryptICSVisualizer.svelte';
    import { savedHashData } from '$lib/stores.js';

    export let form;
    export let data;
    let allOptions = data.body;
    let options = ["MD5", "SHA256", "SHA512"];
    let selectedOption;
    let showAllAlgorithms = false;
    let savedData = false;

    let showDiff = false;

    function toggleShowAll() {
        showAllAlgorithms = !showAllAlgorithms;
    }

    function toggleShowDiff() {
        showDiff = !showDiff;
    }

    let hashData = form?.body || [];
    if (hashData && !savedData) {
        savedHashData.set(hashData);
    }

    console.log(hashData);
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
                <Blockviewer hexdata={$savedHashData.data}, binarydata={$savedHashData.binary} />
                <button on:click={toggleShowDiff}>
                    {showDiff ? 'Hide' : 'Modify'}
                </button>
            {/if}
        </div>
        {#if showDiff}
            <div class="diffcontainer">
                <form method="POST">
                    <input name="data" type="text" placeholder="Input to be hashed">
                    <select name="algorithm" bind:value={selectedOption}>
                        {#each (showAllAlgorithms ? allOptions : options) as option}
                            <option value="{option}">{option}</option>
                        {/each}
                    </select>
                    <button type="submit">Submit</button>
                </form>

            </div>
        {/if}
        
    </div>
</body>