<script>
    import '../../../../style/globalStyle.css'
    
    import { title } from '$lib/title';
    import { navLinks } from '$lib/stores.js'
    import { onMount } from 'svelte';
  
    import de from './locales/de.json';
    import en from './locales/en.json';
  
    import { language } from '$lib/language';
	import BlockViewer from '../../../../lib/BlockViewer.svelte';
    import ComparisonBlockViewer from '../../../../lib/ComparisonBlockViewer.svelte';
    import EncryptionViewer from '../../../../lib/EncryptionViewer.svelte';

    export let data;
    console.log(data);

    let cleartext = data.body.cleartext;
    let key = data.body.key;
    let ciphertext = data.body.ciphertext;

    let diffusionCleartext = data.body.diffusion.cleartext;
    let confusionKey = data.body.confusion.key;

    let diffusionCiphertext = data.body.diffusion.ciphertext;
    let confusionCiphertext = data.body.confusion.ciphertext;



    let showDiffusion = false;
    let showConfusion = false;

    function toggleShowConfusion() {
        showConfusion = !showConfusion;
        if (showDiffusion) {
            showDiffusion = false;
        }
    }

    function toggleShowDiffusion() {
        showDiffusion = !showDiffusion;
        if (showConfusion) {
            showConfusion = false;
        }
    }

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

<body>
    <div class="bodycontainer">
        <div class="blockcontainer">
            <div class="cleartext">
                <BlockViewer {cleartext} />
            </div>
            <div class="encryption">
                <EncryptionViewer {key} />
            </div>
            <div class="ciphertext">
                <BlockViewer {ciphertext} />
            </div>
        </div>
        <div class="buttoncontainer">
            <button on:click={toggleShowConfusion}>{translation.showConf}</button>
            <button on:click={toggleShowDiffusion}>{translation.showDiff}</button>
        </div>
        <div class="blockcontainer">
            <div class="cleartext">
                {#if showDiffusion}
                    <ComparisonBlockViewer original={cleartext}, modified={diffusionCleartext} />
                {:else if showConfusion}
                    <BlockViewer {cleartext} />
                {/if}
            </div>
            <div class="encryption">
                {#if showDiffusion}
                    <EncryptionViewer {key} />
                {:else if showConfusion}
                    <EncryptionViewer {confusionKey} />
                {/if}
            </div>
            <div class="ciphertext">
                {#if showDiffusion}
                    <ComparisonBlockViewer original={ciphertext}, modified={diffusionCiphertext} />
                {:else if showConfusion}
                    <ComparisonBlockViewer original={ciphertext}, modified={confusionCiphertext} />
                {/if}
            </div>
    </div>
</body>

<style>
    .bodycontainer {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
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

  .active {
    background-color: #03089f; /* Green background for active state */
    box-shadow: 0 2px 5px rgba(0, 128, 0, 0.4); /* Green shadow for a lifted effect */
  }
</style>