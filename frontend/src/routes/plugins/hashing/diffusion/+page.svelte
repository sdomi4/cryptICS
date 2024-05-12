<script>
    import '../../../../style/globalStyle.css'
    
    import { title } from '$lib/title';
    import { navLinks } from '$lib/stores.js'
    import { onMount } from 'svelte';
    import { fly } from 'svelte/transition';
    import { quintOut } from 'svelte/easing';
  
    import de from './locales/de.json';
    import en from './locales/en.json';
  
    import { language } from '$lib/language';
	import Blockviewer from '../../../../lib/CryptICSVisualizer.svelte';

    export let form;
    export let data;
    let allOptions = data.body.algorithms;
    let options = ["MD5", "SHA256", "SHA512"];
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
            {#if !hashData.hash}
            <div class="hashform">
                <form method="POST">
                    <input name="data" type="text" placeholder="Input to be hashed">
                    <select name="algorithm" bind:value={selectedOption}>
                        {#each (showAllAlgorithms ? allOptions : options) as option}
                        <option value="{option}">{option}</option>
                        {/each}
                    </select>
                    <div class="buttonrow">
                    <button type="button" on:click={toggleShowAll} class:active={showAllAlgorithms}>
                        {showAllAlgorithms ? 'Show Less' : 'Show More'}
                    </button>
                    <button type="submit">Submit</button>
                    </div>
                </form>
                
            </div>
            {/if}
            {#if hashData.hash}
            <div class="blockviewer">
                <Blockviewer input={hashData.input} text={translation.hashviewer} hexdata={hashData.hash} binarydata={hashData.hash_binary} />
            </div>
            <button on:click={toggleShowDiff}>
                {showDiff ? 'Hide Diffusion' : 'Show Diffusion'}
            </button>
            {/if}
        </div>
        {#if showDiff}
            <div class="diffviewer">
                <h1>Diffusion</h1>
            </div>
        {/if}
    </div>
</body>

<style>
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

    input, select {
        padding: 8px 10px;
        border: 2px solid #ccc;
        border-radius: 5px;
        font-size: 16px;
        color: #333;
        background-color: white;
        transition: border-color 0.3s ease-in-out;
    }

    input:focus, select:focus {
        border-color: #007BFF;
        outline: none;
    }

    .bodycontainer {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }

    .hashcontainer {
        display: flex;
        flex-direction: column;
        align-items: left;
    }

    .blockviewer {
        display: flex;
        margin-top: 20px;
        align-items: left;
    }

    .diffviewer {
        margin-top: 20px;
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