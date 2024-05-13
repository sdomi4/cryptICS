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
        <div class="blockcontainer">

        </div>
        <div class="textfield">
            {translation.introtext}
            {randomInput}
        </div>
        <div class="textfield">
            {translation.blocktext}
        </div>
        <div class="blockcontainer">
            <Blockviewer {data} />
        </div>
        <div class="textfield">
            {translation.blocktext}
        </div>
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