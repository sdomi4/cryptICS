<script>
    import '../../../../style/globalStyle.css'
    
    import { title } from '$lib/title';
    import { backLink } from '$lib/title'
    import { pageTitle } from '$lib/stores.js';
  
    import de from './locales/de.json';
    import en from './locales/en.json';
  
    import { language } from '$lib/language';
	import ClickableBlockViewer from '../../../../lib/ClickableBlockViewer.svelte';
    import ComparisonBlockViewer from '../../../../lib/ComparisonBlockViewer.svelte';
    import EncryptionViewer from '../../../../lib/EncryptionViewer.svelte';

    export let data;

    let cleartext = data.body.cleartext;
    let key = data.body.key;
    let ciphertext = data.body.ciphertext;
    let original_ciphertext = data.body.ciphertext;

    $: keyFaultIndexes = [];
    $: clearTextFaultIndexes = {
        0: [],
        1: []
    }
    $: keyfaults = 0;
    $: clearfaults_0 = 0;
    $: clearfaults_1 = 0;

    let hamming = 0;

    let translation;
    $: {
        translation = $language === 'en' ? en : de;
        title.set(translation.pagetitle);
        backLink.set('/plugins/blockciphers');
        pageTitle.set(translation.diffconftitle);
    }

    async function handleKeyClick(letter, index) {
        if (index in keyFaultIndexes) {
            keyfaults--;
            keyFaultIndexes= keyFaultIndexes.filter(e => e !== index);
        } else {
            keyfaults++;
            keyFaultIndexes.push(index);
        }
        await updateCiphertext();
    }

    async function handleCleartextClick(letter, index, block) {
        if (index in clearTextFaultIndexes[block]) {
            if (block === 0) {
                clearfaults_0--;
            } else {
                clearfaults_1--;
            }
            clearTextFaultIndexes[block] = clearTextFaultIndexes[block].filter(e => e !== index);
        } else {
            if (block === 0) {
                clearfaults_0++;
            } else {
                clearfaults_1++;
            }
            clearTextFaultIndexes[block].push(index);
        }
        await updateCiphertext();
    }

    async function updateCiphertext() {
        const payload = JSON.stringify({
            flipped_key_bits: keyFaultIndexes,
            flipped_cleartext_bits: clearTextFaultIndexes,
            cleartext: cleartext,
            key: key
        });
        const response = await fetch('/backend/avalanche', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: payload
        })

        const modifiedCiphertext = await response.json();
        ciphertext = modifiedCiphertext.ciphertext;
        hamming = modifiedCiphertext.hamming;
    }
</script>

<body>
    <div class="bodycontainer">
        <div class="textcontainer">
            <p>{translation.diffconfintro}</p>
            
        </div>
        <div class="visualisation">
            <div class="key">
                <div class="keytext">
                    <span class="keyintro"> {translation.keyintro} </span>
                </div>
                <ClickableBlockViewer binaryblocks={[key]} onLetterClick={handleKeyClick}/>
            </div>
            <div class="encryption">
                <div class="cleartext">
                    <ClickableBlockViewer binaryblocks={cleartext} onLetterClick={handleCleartextClick}/>
                </div>
                <div class="encryption">
                    <EncryptionViewer key="K" blocknumber=2/>
                </div>
                <div class="ciphertext">
                    <ComparisonBlockViewer original={original_ciphertext} modified={ciphertext}/>
                </div>
            </div>
            <div class="analysis">
                {#if hamming != 0}
                {translation.hamming1} {hamming} {translation.hamming2} ({(hamming/128*100).toFixed(2)}% {translation.hamming3}, {(hamming/256*100).toFixed(2)}% {translation.hamming4}).
                {/if}
            </div>
        </div>
    </div>
</body>

<style>
    .bodycontainer {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: flex-start;
        margin-top: 60px;
    }

    .visualisation {
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        align-items: center;
    }

    .keytext {
        width: 20ch;
    }

    .key {
        margin-right: 50px;
    }

    .analysis {
        width: 35ch;
    }
</style>