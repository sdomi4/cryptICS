<script>
    import '../../../../style/globalStyle.css'
    
    import { title } from '$lib/title';
    import { backLink } from '$lib/title'
    import { pageTitle } from '$lib/stores.js';
  
    import de from './locales/de.json';
    import en from './locales/en.json';
  
    import { language } from '$lib/language';

    // import BlockViewer Components
    import BlockViewer from '$lib/BlockViewer.svelte';
    import ComparisonBlockViewer from '$lib/ComparisonBlockViewer.svelte';


    let translation;
    $: {
        translation = $language === 'en' ? en : de;
        title.set(translation.pagetitle);
        backLink.set('/plugins/hashing');
        pageTitle.set(translation.avalanchetitle);
    }

    $: input = "";
    $: hash = "";
    $: binaryBlocks = [];

    $: modifiedInput = "";
    $: modifiedHash = "";
    $: modifiedBlocks = [];

    function onInput(event) {
        if (event.target.value.length > 0) {
            // update things
            if (event.target.name === "original") {
                input = event.target.value;
                updateHash();
            } else {
                modifiedInput = event.target.value;
                updateModifiedHash();
            }
        }
    }

    async function updateHash() {
        const payload = JSON.stringify({
            data: input,
            algorithm: "MD5"
        });
        const response = await fetch('/backend/hash', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: payload
        });

        const modifiedHash = await response.json();
        hash = modifiedHash.hash;
        binaryBlocks = await updateBinary(hash);
    }

    async function updateModifiedHash() {
        const payload = JSON.stringify({
            data: modifiedInput,
            algorithm: "MD5"
        });
        const response = await fetch('/backend/hash', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: payload
        });

        const hashResponse = await response.json();
        modifiedHash = hashResponse.hash;
        modifiedBlocks = await updateBinary(modifiedHash);
    }

    async function updateBinary(hashValue) {
        const payload = JSON.stringify({ blocks: [hashValue] });
        const response = await fetch('/backend/hexToBinary', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: payload
        });

        const modifiedBinary = await response.json();
        console.log(modifiedBinary.blocks)
        return modifiedBinary.blocks;
    }

    
</script>

<body>
    <div class="bodycontainer">
        <div class="hashcontainer">
            <div class="inputform">
                <input name="original" type="text" placeholder="Input to be hashed" on:input={onInput} maxlength="32">
            </div>
            {#if input.length > 0}
            <div class="hash">
                <p>Hash: {hash}</p>
            </div>
            <div class="binary">
                <BlockViewer binaryblocks={binaryBlocks} />
            </div>
            {/if}
        </div>
        <div class="hashcontainer">
            <div class="inputform">
                <input name="modified" type="text" placeholder="Input to be hashed" on:input={onInput} maxlength="32">
            </div>
            {#if modifiedInput.length > 0}
            <div class="hash">
                <p>Hash: {modifiedHash}</p>
            </div>
            <div class="binary">
                <ComparisonBlockViewer original={binaryBlocks} modified={modifiedBlocks} />
            </div>
            {/if}
        </div>
    </div>
</body>

<style>

    input {
        padding: 8px 10px;
        border: 2px solid #ccc;
        border-radius: 5px;
        font-size: 16px;
        color: #333;
        background-color: white;
        transition: border-color 0.3s ease-in-out;
    }

    input:focus {
        border-color: #007BFF;
        outline: none;
    }

    .bodycontainer {
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        gap: 30px;
        margin-top: 80px;
    }

    .hashcontainer {
        display: flex;
        flex-direction: column;
        align-items: left;
    }
</style>