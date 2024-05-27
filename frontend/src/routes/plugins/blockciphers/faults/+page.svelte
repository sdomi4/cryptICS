<script>
    import '../../../../style/globalStyle.css'
    
    import { title } from '$lib/title';
    import { backLink } from '$lib/title';
    import { pageTitle } from '$lib/stores.js'
  
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

    let binary = {
        ECB: false,
        CBC: false,
        OFB: true,
        CFB: false,
        CTR: true
    }
    $: {
        clear = cleartexts?.cleartext || clear;

        // swap hex to binary for OFB and CTR by default
        for (let mode in binary) {
            if (binary[mode]) {
                handleToggle(clear[mode]);
            }
        }
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
        })

        cleartexts = await response.json();
        //console.log(cleartexts.cleartext);
        loading = false;
        showFaults = true;
    }
  
    async function handleToggle(mode) {
        switch (mode) {
            case 'ECB':
                if (binary.ECB) {
                    clear.ECB = await hexToBinary(clear.ECB);
                } else {
                    clear.ECB = await binaryToHex(clear.ECB);
                }
                break;
            case 'CBC':
                if (binary.CBC) {
                    clear.CBC = await hexToBinary(clear.CBC);
                } else {
                    clear.CBC = await binaryToHex(clear.CBC);
                }
                break;
            case 'OFB':
                if (binary.OFB) {
                    clear.OFB = await hexToBinary(clear.OFB);
                } else {
                    clear.OFB = await binaryToHex(clear.OFB);
                }
                break;
            case 'CFB':
                if (binary.CFB) {
                    clear.CFB = await hexToBinary(clear.CFB);
                } else {
                    clear.CFB = await binaryToHex(clear.CFB);
                }
                break;
            case 'CTR':
                if (binary.CTR) {
                    clear.CTR = await hexToBinary(clear.CTR);
                } else {
                    clear.CTR = await binaryToHex(clear.CTR);
                }
                break;    
        }
    }

    async function hexToBinary(hex) {
        const payload = JSON.stringify({
            blocks: hex
        });
        const response = await fetch('/backend/hexToBinary', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: payload
        });

        const converted = await response.json();
        return converted.blocks;
    }

    async function binaryToHex(binary) {
        const payload = JSON.stringify({
            blocks: binary
        });
        const response = await fetch('/backend/binaryToHex', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: payload
        });

        const converted = await response.json();
        return converted.blocks;
    }

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
                    <ComparisonBlockViewer original={originalCleartext} modified={clear.ECB}/>
                    <label class="switch">
                        <input type="checkbox">
                        <span class="slider"></span>
                    </label>
                </div>
                <div id="CBC" class="cleartextcontainer">
                    <span class="modetitle">CBC</span>
                    <ComparisonBlockViewer original={originalCleartext} modified={clear.CBC}/>
                    <label class="switch">
                        <input type="checkbox">
                        <span class="slider"></span>
                    </label>
                </div>
                <div id="OFB" class="cleartextcontainer">
                    <span class="modetitle">OFB</span>
                    <ComparisonBlockViewer original={originalCleartext} modified={clear.OFB}/>
                    <label class="switch" on:click={handleToggle("OFB")}>
                        <input type="checkbox">
                        <span class="slider"></span>
                    </label>
                </div>
                <div id="CFB" class="cleartextcontainer">
                    <span class="modetitle">CFB</span>
                    <ComparisonBlockViewer original={originalCleartext} modified={clear.CFB}/>
                    <label class="switch">
                        <input type="checkbox">
                        <span class="slider"></span>
                    </label>
                </div>
                <div id="CTR" class="cleartextcontainer">
                    <span class="modetitle">CTR</span>
                    <ComparisonBlockViewer original={originalCleartext} modified={clear.CTR}/>
                    <label class="switch">
                        <input type="checkbox">
                        <span class="slider"></span>
                    </label>
                </div>
            </div>
            <div class="foottext">
                {translation.faultdetails}
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
        width: 60px;
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
        -webkit-transform: translateX(26px);
        -ms-transform: translateX(26px);
        transform: translateX(26px);
    }
</style>