<script>
        import '../../../../style/globalStyle.css'
    
    import { title } from '$lib/title';
    import { backLink } from '$lib/title'
    import { pageTitle } from '$lib/stores.js';
    import { onMount } from 'svelte';
  
    import de from './locales/de.json';
    import en from './locales/en.json';

    import { fly } from 'svelte/transition';
	import { expoOut } from 'svelte/easing';
  
    import { language } from '$lib/language';
	import BlockViewer from '$lib/BlockViewer.svelte';

    export let data;

    // reactive declarations so the components hopefully update with changes
    $: initialData = data.body.initial_data;
    $: modifier = data.body.modifier;
    $: encryptedData = data.body.encrypted_data.slice(2, 126).concat("...");
    $: modifiedData = data.body.modified_data;
    $: homomorphicData = data.body.homomorphic_data;
    $: decryptedData = data.body.decrypted_data;

    console.log(data.body);

    let translation;
    $: {
        translation = $language === 'en' ? en : de;
        title.set(translation.pagetitle);
        backLink.set('/plugins/rsa');
        pageTitle.set(translation.homomorphictitle);
    }
</script>

<body>
<div class="bodycontainer">
    <div class="visualisation">
        <div class="explainer">
            
        </div>
        <div class="gridcontainer">
            <div class="griditem input" id="1">
                <BlockViewer binaryblocks={[initialData]} />
            </div>
            <div class="griditem encrypt" id="2">

            </div>
            <div class="griditem cipher" id="3">
                <BlockViewer binaryblocks={[encryptedData]} />
            </div>
            <div class="griditem spacer" id="4">

            </div>
            <div class="griditem spacer" id="5">

            </div>
            <div class="griditem multiplicator" id="6">
                
            </div>
            <div class="griditem modifier" id="7">
                <BlockViewer binaryblocks={[modifier]} />
            </div>
            <div class="griditem encrypt" id="8">

            </div>
            <div class="griditem cipher" id="9">
                <BlockViewer binaryblocks={[modifiedData]} />
            </div>
            <div class="griditem spacer" id="10">
            
            </div>
            <div class="griditem spacer" id="11">
            
            </div>
            <div class="griditem modified" id="12">
                <BlockViewer binaryblocks={[homomorphicData]} />
            </div> 
            <div class="griditem decrypt" id="13">

            </div>
            <div class="griditem cipherModified" id="14">
                <BlockViewer binaryblocks={[decryptedData]} />
            </div>
        </div>
    </div>
</div>
</body>

<style>
    .bodycontainer {
        margin-top: 80px;
    }

    .gridcontainer {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        grid-template-rows: repeat(3, 1fr);
        gap: 10px;
    }

    #1, #4, #7, #10, #13 {
        grid-row: 1 / span 1;
    }

    #2, #5, #8, #11, #14 {
        grid-row: 2 / span 1;
    }

    #3, #6, #9, #12, #15 {
        grid-row: 3 / span 1;
    }

    #1, #2, #3 {
        grid-column: 1 / span 1;
    }

    #4, #5, #6 {
        grid-column: 2 / span 1;
    }

    #7, #8, #9 {
        grid-column: 3 / span 1;
    }

    #10, #11, #12 {
        grid-column: 4 / span 1;
    }

    #13, #14, #15 {
        grid-column: 5 / span 1;
    }
</style>