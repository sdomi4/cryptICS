<script>
    import '../../../../style/globalStyle.css'
    
    import { title } from '$lib/title';
    import { navLinks } from '$lib/stores.js'
    import { onMount } from 'svelte';
  
    import de from './locales/de.json';
    import en from './locales/en.json';

    import { fly } from 'svelte/transition';
	import { expoOut } from 'svelte/easing';
  
    import { language } from '$lib/language';
	import BlockViewer from '../../../../lib/BlockViewer.svelte';
    import ComparisonBlockViewer from '../../../../lib/ComparisonBlockViewer.svelte';
    import EncryptionViewer from '../../../../lib/EncryptionViewer.svelte';

    export let data;
    console.log(data);

    let cleartext = data.body.cleartext;
    let key = data.body.key;
    let ciphertext = data.body.ciphertext;
    console.log(cleartext);
    console.log(ciphertext);

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
            { description: translation.ciphermodetitle, uri: "/plugins/blockciphers/faults"}
        ]);
    }
  
    onMount(() => {
        title.set('Block Ciphers');
    });
</script>

<body>
    <div class="bodycontainer">
        <p>{translation.diffconfintro}</p>
        <div class="textcontainer">
            <div class="textbox">
                <span class="keyintro"> {translation.keyintro} </span><span class="key"><BlockViewer binaryblocks={[key]} /></span>
            </div>
            <div class="buffer"></div>
            <div class="textbox">
                {#if showDiffusion}
                    {translation.diffusion}
                {:else if showConfusion}
                    <span class="keyintro">{translation.confusion}</span> <span class="key"><ComparisonBlockViewer original={[key]} modified={[confusionKey]}/></span>
                {/if}
            </div>
        </div>
        <div class="visualisation">
        <div class="blockcontainer">
            <div class="cleartext">
                <BlockViewer binaryblocks={cleartext} />
            </div>
            <div class="encryption">
                <EncryptionViewer key="K" blocknumber=2/>
            </div>
            <div class="ciphertext">
                <BlockViewer binaryblocks={ciphertext} />
            </div>
        </div>
        <div class="buttoncontainer">
            <button on:click={toggleShowConfusion}>{translation.showConf}</button>
            <button on:click={toggleShowDiffusion}>{translation.showDiff}</button>
        </div>
        <div class="blockcontainer">
            <div class="cleartext">
                {#if showDiffusion}
                <div in:fly={{ delay: 50, duration: 700, x: -200, y: 0, opacity: 0.1, easing: expoOut }}>
                    <ComparisonBlockViewer original={cleartext} modified={diffusionCleartext} />
                </div>
                {:else if showConfusion}
                <div
                    in:fly={{ delay: 50, duration: 700, x: -200, y: 0, opacity: 0.1, easing: expoOut }}>
                    <ComparisonBlockViewer original={cleartext} modified={cleartext} />
                </div>
                {/if}
            </div>
            <div class="encryption">
                {#if showDiffusion}
                <div in:fly={{ delay: 50, duration: 700, x: -200, y: 0, opacity: 0.1, easing: expoOut }}>
                    <EncryptionViewer key="K" blocknumber=2 />
                </div>
                {:else if showConfusion}
                <div in:fly={{ delay: 50, duration: 700, x: -200, y: 0, opacity: 0.1, easing: expoOut }}>
                    <EncryptionViewer key="K'" blocknumber=2 />
                </div>
                {/if}
            </div>
            <div class="ciphertext">
                {#if showDiffusion}
                <div in:fly={{ delay: 50, duration: 700, x: -200, y: 0, opacity: 0.1, easing: expoOut }}>
                    <ComparisonBlockViewer original={ciphertext} modified={diffusionCiphertext} />
                </div>
                {:else if showConfusion}
                <div in:fly={{ delay: 50, duration: 700, x: -200, y: 0, opacity: 0.1, easing: expoOut }}>
                    <ComparisonBlockViewer original={ciphertext} modified={confusionCiphertext} />
                </div>
                {/if}
            </div>
        </div>
    </div>
</body>

<style>
    .highlight {
        background: #ffcccb;
    }

    .buffer {
        width: 150px;
    }

    .keyintro {
        width: 16ch;
        padding-right: 20px;
    }

    .textcontainer {
        display: flex;
        flex-direction: row;
    }

    .textbox {
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        align-items: center;
        gap: 10px;
    }

    .bodycontainer {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        gap: 20px;
        width: 60%;
    }

    .visualisation {
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
    }

    .buttoncontainer {
        display: flex;
        flex-direction: column;
        justify-content: center;
        gap: 20px;
        align-items: center;
        margin: 20px;
    }

    button {
    background-color: #007BFF; /* Vibrant blue background */
    color: white; /* White text for high contrast */
    border: none; /* No border for a cleaner look */
    width: 110px; /* Control the width to not span the entire parent container */
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
</style>