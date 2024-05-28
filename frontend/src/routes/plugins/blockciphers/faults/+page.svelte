<script>
    import '../../../../style/globalStyle.css';
    import { title } from '$lib/title';
    import { backLink } from '$lib/title';
    import { pageTitle } from '$lib/stores.js';
    import { onMount } from 'svelte';
  
    import de from './locales/de.json';
    import en from './locales/en.json';
  
    import { language } from '$lib/language';
    import ClickableBlockViewer from '$lib/ClickableBlockViewer.svelte';
    import ComparisonBlockViewer from '$lib/ComparisonBlockViewer.svelte';

    export let data;

    // use CBC as stand-in for all modes
    let ciphertext = data.body.ciphertext.CBC;
    let originalCleartextHex = data.body.cleartext.hex;
    let originalCleartextBinary = data.body.cleartext.binary;
    let key = data.body.key;
    let iv = data.body.iv;
    let nonce = data.body.nonce;
    let clear;

    let loading = false;
    let showFaults = false;
    let faultindexes = {
        0: [],
        1: [],
        2: [],
        3: []
    };
    let cleartexts = {};
    let clearHex = {
        ECB: originalCleartextHex,
        CBC: originalCleartextHex,
        OFB: originalCleartextHex,
        CFB: originalCleartextHex,
        CTR: originalCleartextHex
    };
    let clearBinary = {
        ECB: originalCleartextBinary,
        CBC: originalCleartextBinary,
        OFB: originalCleartextBinary,
        CFB: originalCleartextBinary,
        CTR: originalCleartextBinary
    };
    let showBinary = {
        ECB: false,
        CBC: false,
        OFB: false,
        CFB: true, // Default to binary
        CTR: true  // Default to binary
    };

    $: {
        clearHex.ECB = cleartexts.cleartext?.ECB.hex || originalCleartextHex;
        clearHex.CBC = cleartexts.cleartext?.CBC.hex || originalCleartextHex;
        clearHex.OFB = cleartexts.cleartext?.OFB.hex || originalCleartextHex;
        clearHex.CFB = cleartexts.cleartext?.CFB.hex || originalCleartextHex;
        clearHex.CTR = cleartexts.cleartext?.CTR.hex || originalCleartextHex;

        clearBinary.ECB = cleartexts.cleartext?.ECB.binary || originalCleartextBinary;
        clearBinary.CBC = cleartexts.cleartext?.CBC.binary || originalCleartextBinary;
        clearBinary.OFB = cleartexts.cleartext?.OFB.binary || originalCleartextBinary;
        clearBinary.CFB = cleartexts.cleartext?.CFB.binary || originalCleartextBinary;
        clearBinary.CTR = cleartexts.cleartext?.CTR.binary || originalCleartextBinary;
    }

    let translation;
    $: {
        translation = $language === 'en' ? en : de;
        title.set(translation.pagetitle);
        backLink.set('/plugins/blockciphers');
        pageTitle.set(translation.faulttitle);
    }

    async function handleLetterClick(letter, index, block) {
        loading = true;
        // check if letter is being checked or unchecked
        if (index in faultindexes[block]) {
            faultindexes[block] = faultindexes[block].filter(e => e !== index);
        } else {
            faultindexes[block].push(index);
        }
        const payload = JSON.stringify({
            key: key,
            ciphertext: {
                ECB: data.body.ciphertext.ECB,
                CBC: data.body.ciphertext.CBC,
                OFB: data.body.ciphertext.OFB,
                CFB: data.body.ciphertext.CFB,
                CTR: data.body.ciphertext.CTR
            },
            fault_indexes: faultindexes,
            iv: iv,
            nonce: nonce
        });
        // call backend to decrypt with introduced faults
        const response = await fetch('/backend/faults', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: payload
        });

        cleartexts = await response.json();
        loading = false;
        showFaults = true;
    }
  
    function toggleBinaryView(mode) {
        showBinary[mode] = !showBinary[mode];
    }
  
    onMount(() => {
    });
</script>

<body>
    <div class="bodycontainer">
        <div class="introcontainer">
            <h1>{translation.faulttitle}</h1>
            <p>{translation.faultdescription}</p>
        </div>
        <div class="visualisationcontainer">
            <h2>{translation.ciphertext}</h2>
            <div class="ciphertextcontainer">
                <ClickableBlockViewer binaryblocks={ciphertext} onLetterClick={handleLetterClick}/>
            </div>
            <div>
                <div class="decryptionspace">
                    <h2>{translation.decrypted}</h2>
                </div>
                <div class="faultcontainer">
                    <div id="ECB" class="cleartextcontainer">
                        <span class="modetitle">ECB</span>
                        {#if showBinary.ECB}
                            <ComparisonBlockViewer original={originalCleartextBinary} modified={clearBinary.ECB}/>
                        {:else}
                            <ComparisonBlockViewer original={originalCleartextHex} modified={clearHex.ECB}/>
                        {/if}
                        <label class="switch">
                            <input type="checkbox" on:change={() => toggleBinaryView('ECB')}>
                            <span class="slider">
                                {#if showBinary.ECB}
                                    <span class="text text-right">Binary</span>
                                {:else}
                                    <span class="text text-left">Hex</span>
                                {/if}
                            </span>
                        </label>
                    </div>
                    <div id="CBC" class="cleartextcontainer">
                        <span class="modetitle">CBC</span>
                        {#if showBinary.CBC}
                            <ComparisonBlockViewer original={originalCleartextBinary} modified={clearBinary.CBC}/>
                        {:else}
                            <ComparisonBlockViewer original={originalCleartextHex} modified={clearHex.CBC}/>
                        {/if}
                        <label class="switch">
                            <input type="checkbox" on:change={() => toggleBinaryView('CBC')}>
                            <span class="slider">
                                {#if showBinary.CBC}
                                    <span class="text text-right">Binary</span>
                                {:else}
                                    <span class="text text-left">Hex</span>
                                {/if}
                            </span>
                        </label>
                    </div>
                    <div id="OFB" class="cleartextcontainer">
                        <span class="modetitle">OFB</span>
                        {#if showBinary.OFB}
                            <ComparisonBlockViewer original={originalCleartextBinary} modified={clearBinary.OFB}/>
                        {:else}
                            <ComparisonBlockViewer original={originalCleartextHex} modified={clearHex.OFB}/>
                        {/if}
                        <label class="switch">
                            <input type="checkbox" on:change={() => toggleBinaryView('OFB')}>
                            <span class="slider">
                                {#if showBinary.OFB}
                                    <span class="text text-right">Binary</span>
                                {:else}
                                    <span class="text text-left">Hex</span>
                                {/if}
                            </span>
                        </label>
                    </div>
                    <div id="CFB" class="cleartextcontainer">
                        <span class="modetitle">CFB</span>
                        {#if showBinary.CFB}
                            <ComparisonBlockViewer original={originalCleartextBinary} modified={clearBinary.CFB}/>
                        {:else}
                            <ComparisonBlockViewer original={originalCleartextHex} modified={clearHex.CFB}/>
                        {/if}
                        <label class="switch">
                            <input type="checkbox" on:change={() => toggleBinaryView('CFB')}>
                            <span class="slider">
                                {#if showBinary.CFB}
                                    <span class="text text-left">Binary</span>
                                {:else}
                                    <span class="text text-right">Hex</span>
                                {/if}
                            </span>
                        </label>
                    </div>
                    <div id="CTR" class="cleartextcontainer">
                        <span class="modetitle">CTR</span>
                        {#if showBinary.CTR}
                            <ComparisonBlockViewer original={originalCleartextBinary} modified={clearBinary.CTR}/>
                        {:else}
                            <ComparisonBlockViewer original={originalCleartextHex} modified={clearHex.CTR}/>
                        {/if}
                        <label class="switch">
                            <input type="checkbox" on:change={() => toggleBinaryView('CTR')}>
                            <span class="slider">
                                {#if showBinary.CTR}
                                    <span class="text text-left">Binary</span>
                                {:else}
                                    <span class="text text-right">Hex</span>
                                {/if}
                            </span>
                        </label>
                    </div>
                </div>
                <div class="foottext">
                    {translation.faultdetails}
                </div>
            </div>
        </div>
    </div>
</body>

<style>
    .cleartextcontainer {
        display: flex;
        flex-direction: row;
        gap: 10px;
        align-items: center;
    }

    .faultcontainer {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .decryptionspace {
        height: 40px;
    }

    .foottext {
        font-size: 0.8em;
        margin-top: 30px;
        width: 80%;
    }

    .introcontainer {
        width: 80%;
    }

    .ciphertextcontainer {
        display: flex;
        flex-direction: row;
        gap: 10px;
        margin-left: 44px;
    }

    .modetitle {
        font-size: 1.2em;
        font-weight: bold;
    }

    .switch {
        position: relative;
        display: inline-block;
        width: 100px; /* Adjusted width for text */
        height: 34px;
    }

    .switch input {
        opacity: 0;
        width: 0;
        height: 0;
    }

    .slider {
        position: absolute;
        cursor: pointer;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: #ccc;
        -webkit-transition: .4s;
        transition: .4s;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .slider:before {
        position: absolute;
        content: "";
        height: 26px;
        width: 26px;
        left: 4px;
        bottom: 4px;
        background-color: white;
        -webkit-transition: .4s;
        transition: .4s;
    }

    input:checked + .slider {
        background-color: #2196F3;
    }

    input:focus + .slider {
        box-shadow: 0 0 1px #2196F3;
    }

    input:checked + .slider:before {
        -webkit-transform: translateX(66px); /* Adjusted transform for text */
        -ms-transform: translateX(66px); /* Adjusted transform for text */
        transform: translateX(66px); /* Adjusted transform for text */
    }

    .slider .text {
        position: absolute;
        width: 100%;
        text-align: center;
    }

    .slider .text-left {
        right: 10px;
        text-align: right;
    }

    .slider .text-right {
        left: 10px;
        text-align: left;
    }
</style>
