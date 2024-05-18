<script>
    import '../../../../style/globalStyle.css'
    
    import { title } from '$lib/title';
    import { navLinks } from '$lib/stores.js'
    import { onMount } from 'svelte';
  
    import de from './locales/de.json';
    import en from './locales/en.json';
  
    import { language } from '$lib/language';
    import ClickableBlockViewer from '$lib/ClickableBlockViewer.svelte';
    import ComparisonBlockViewer from '$lib/ComparisonBlockViewer.svelte';

    export let data;

    // use CBC as standin for all modes
    let ciphertext = data.body.ciphertext.CBC;
    let originalCleartext = data.body.cleartext;
    let key = data.body.key;
    let iv = data.body.iv;
    let nonce = data.body.nonce;

    let loading = false;
    let showFaults = false;
    let faultindexes = {
        0: [],
        1: [],
        2: [],
        3: []
    };
    let cleartexts = {};
    let clear = {
        ECB: originalCleartext,
        CBC: originalCleartext,
        OFB: originalCleartext,
        CFB: originalCleartext,
        CTR: originalCleartext
    };
    $: {
        clear = cleartexts?.cleartext || clear;
    }

    let translation;
    $: {
        translation = $language === 'en' ? en : de;
        navLinks.set([
            { description: translation.diffconftitle, uri: "/plugins/blockciphers/diffusion-confusion" },
            { description: translation.ciphermodetitle, uri: "/plugins/blockciphers/faults"}
        ]);
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
        })

        cleartexts = await response.json();
        //console.log(cleartexts.cleartext);
        loading = false;
        showFaults = true;
    }
  
    onMount(() => {
        title.set('Block Ciphers');
    });
</script>

<body>
    <div class="bodycontainer">
        
        <div class="introcontainer">

        </div>
        <div class="visualisationcontainer">
        <div class="ciphertextcontainer">
            <ClickableBlockViewer binaryblocks={ciphertext} onLetterClick={handleLetterClick}/>
        </div>
        <div>
            <div class="decryptionspace">

            </div>
            <div class="faultcontainer">
                <div id="ECB" class="cleartextcontainer">
                    <h1>ECB</h1>
                    <ComparisonBlockViewer original={originalCleartext} modified={clear.ECB}/>
                </div>
                <div id="CBC" class="cleartextcontainer">
                    <h1>CBC</h1>
                    <ComparisonBlockViewer original={originalCleartext} modified={clear.CBC}/>
                </div>
                <div id="OFB" class="cleartextcontainer">
                    <h1>OFB</h1>
                    <ComparisonBlockViewer original={originalCleartext} modified={clear.OFB}/>
                </div>
                <div id="CFB" class="cleartextcontainer">
                    <h1>CFB</h1>
                    <ComparisonBlockViewer original={originalCleartext} modified={clear.CFB}/>
                </div>
                <div id="CTR" class="cleartextcontainer">
                    <h1>CTR</h1>
                    <ComparisonBlockViewer original={originalCleartext} modified={clear.CTR}/>
                </div>
            </div>
        </div>
    </div>
</body>
