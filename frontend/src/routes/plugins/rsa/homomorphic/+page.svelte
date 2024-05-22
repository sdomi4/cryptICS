<script>
    import '../../../../style/globalStyle.css'
    
    import { writable, derived } from 'svelte/store';
    import { title } from '$lib/title';
    import { backLink } from '$lib/title'
    import { pageTitle } from '$lib/stores.js';
    import { onMount } from 'svelte';
    import { fade } from 'svelte/transition';

    import de from './locales/de.json';
    import en from './locales/en.json';
  
    import { language } from '$lib/language';
	import BlockViewer from '$lib/BlockViewer.svelte';

    export let data;

    // reactive declarations so the components hopefully update with changes
    $: initialData = data.body.initial_data;
    $: modifier = data.body.modifier;
    $: encryptedData = data.body.encrypted_data.slice(2, 126).concat("...");
    $: modifiedData = data.body.modified_data.slice(2, 126).concat("...");
    $: homomorphicData = data.body.homomorphic_data.slice(2, 126).concat("...");
    $: decryptedData = data.body.decrypted_data;

    console.log(data.body);

    let translation;
    $: {
        translation = $language === 'en' ? en : de;
        title.set(translation.pagetitle);
        backLink.set('/plugins/rsa');
        pageTitle.set(translation.homomorphictitle);
    }

    let isOpen = true;

    function toggleExplainer() {
        isOpen = !isOpen;
    }

    let currentStep = writable(1);
    let stepDetails = derived(currentStep, $currentStep => {
        return {
            showEnc: $currentStep >=2,
            showMod: $currentStep >=3,
            showModEnc: $currentStep >=4,
            showModMult: $currentStep >= 5,
            showDec: $currentStep >= 6
        };
    });

    $: currentStepText = translation.steps[$currentStep-1];

    function incrementStep() {
        currentStep.update(i => i+1)
    }

    function decrementStep() {
        currentStep.update(i => i-1)
    }
</script>

<body>
<div class="bodycontainer">
    <div class="visualisation">
        <div class="explainercontainer">
        <div class="explainer {isOpen ? '' : 'hidden'}">
            <div class="textbox">
                {@html currentStepText}
            </div>
            <div class="buttonbox">
                <button class="step-button" on:click={decrementStep} disabled={$currentStep === 1}>{translation.back}</button>
                <button class="step-button" on:click={incrementStep} disabled={$currentStep === 6}>{translation.forward}</button>
            </div>
        </div>
    
        <div class="tabbutton {isOpen ? '' : 'hidden'}" on:click={toggleExplainer}>
            <div class="buttonarrow {isOpen ? '' : 'hidden'}"></div>
        </div>
    </div>
        <div class="gridcontainer {isOpen ? '' : 'hidden'}">
            <div class="griditem input">
                <BlockViewer binaryblocks={[initialData]} />
                {#if $stepDetails.showEnc || !isOpen}
                <svg width="100" height="120" transition:fade={{ delay: 250, duration: 300 }}>
                    <path d="M 50,0 L 50,118 L 42,108 L 58,108 L50,118 " fill="black" stroke-width="1" stroke="black" stroke-linejoin="round" />
                    <text x = "5" y = "25" font-size = "20">
                        <tspan x = "5" y = "60">
                            K<tspan dy="5" font-size="12">PUB</tspan>
                        </tspan>
                        <tspan x="60" y="60">
                            E
                        </tspan>
                    </text>
                </svg>
                {/if}
            </div>
            <div class="griditem spacer">

            </div>
            <div class="griditem modifier">
                {#if $stepDetails.showMod || !isOpen}
                <div transition:fade={{ delay: 250, duration: 300 }}>
                    <BlockViewer binaryblocks={[modifier]} />
                </div>
                {/if}
                {#if $stepDetails.showModEnc || !isOpen}
                <svg width="100" height="120" transition:fade={{ delay: 250, duration: 300 }}>
                    <path d="M 50,0 L 50,118 L 42,108 L 58,108 L50,118 " fill="black" stroke-width="1" stroke="black" stroke-linejoin="round" />
                    <text x = "5" y = "25" font-size = "20">
                        <tspan x = "5" y = "60">
                            K<tspan dy="5" font-size="12">PUB</tspan>
                        </tspan>
                        <tspan x="60" y="60">
                            E
                        </tspan>
                    </text>
                </svg>
                {/if}
            </div>
            <div class="griditem spacer"></div>
            <div class="griditem cipherModified">
                {#if $stepDetails.showDec || !isOpen}
                <div transition:fade={{ delay: 250, duration: 300 }}>
                    <BlockViewer binaryblocks={[decryptedData]} />
                </div>
                <svg width="100" height="120" transition:fade={{ delay: 250, duration: 300 }}>
                    <path d="M 50,120 L 50,2 L 42,10 L 58,10 L50,2 " fill="black" stroke-width="1" stroke="black" stroke-linejoin="round" />
                    <text x = "5" y = "25" font-size = "20">
                        <tspan x = "5" y = "60">
                            K<tspan dy="5" font-size="12">PRIV</tspan>
                        </tspan>
                        <tspan x="60" y="60">
                            D
                        </tspan>
                    </text>
                </svg>
                {/if}
            </div>
            {#if $stepDetails.showEnc || !isOpen}
            <div class="griditem cipher" transition:fade={{ delay: 250, duration: 300 }}>
                <BlockViewer binaryblocks={[encryptedData]} />
            </div>
            {/if}
            
            <div class="griditem multiplicator" >
                {#if $stepDetails.showModMult || !isOpen}
                <span transition:fade={{ delay: 250, duration: 300 }}>&times;</span>
                {/if}
            </div>
            
            {#if $stepDetails.showModEnc || !isOpen}
            <div class="griditem cipher" transition:fade={{ delay: 250, duration: 300 }}>
                <BlockViewer binaryblocks={[modifiedData]} />
            </div>
            {/if}
            {#if $stepDetails.showModMult || !isOpen}       
            <div class="griditem equals" transition:fade={{ delay: 250, duration: 300 }}>
                =
            </div>
            <div class="griditem modified" transition:fade={{ delay: 250, duration: 300 }}>
                <BlockViewer binaryblocks={[homomorphicData]} />
            </div>  
            {/if}
        </div>
    </div>
</div>
</body>

<style>
    .tabbutton {
        transition: transform 0.3s ease-in-out;
        transform: rotate(-90deg) translateX(-480px);
        transform-origin: top left;
        border: 1px solid black;
        border-top: none;
        border-radius: 0 0 5px 5px;
        height: 30px;
        width: 60px;
        display: flex;
        text-align: center;
        text-anchor: middle;
    }

    .buttonarrow {
        width: 0; 
        height: 0; 
        border-left: 12px solid transparent;
        border-right: 12px solid transparent;
        border-bottom: 12px solid black;
        transition: transform 0.3s ease-in-out;
        margin-left: 10px;
        margin-top: 8px;
    }

    .buttonarrow.hidden {
        transform: rotate(180deg);
    }

    button {
        background-color: #007BFF;
        color: white;
        border: none;
        width: fit-content;
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    }

    button:hover {
        background-color: #0056b3;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        outline: none;
    }

    button:disabled {
        background-color: #243d58;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        outline: none;
        color: grey;
    }

    .explainercontainer {
        display: flex;
        flex-direction: row;
    }

    .visualisation {
        display: flex;
        flex-direction: row;
    }
    .bodycontainer {
        margin-top: 80px;
        margin-left: 0px;
    }

    .gridcontainer {
        display: grid;
        grid-template-columns: 180px 50px 180px 50px 180px;
        grid-template-rows: repeat(3, 1fr);
        transition: transform 0.3s ease-in-out;
    }

    .gridcontainer.hidden{
        transform: translateX(-310px);
    }

    .spacer {
        width: 50px;
    }

    .griditem {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .multiplicator, .equals {
        display: flex;
        justify-content: center;
        font-size: 30px;
    }

    .explainer {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 250px;
        height: 460px;
        transition: transform 0.3s ease-in-out;
        transform: translateX(0);
        background-color: #e8e8e8;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid black;
    }

    .explainer.hidden {
        transform: translateX(-150%);
    }

    .tabbutton.hidden {
        transform: rotate(-90deg) translateX(-480px) translateY(-275px);
    }

    .buttonbox {
        display: flex;
        justify-content: space-around;
        margin-top: auto;
        gap: 25px;
    }
</style>