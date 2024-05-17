<script>
    import '../../../style/globalStyle.css'
        
    import { title } from '$lib/title';
    import { navLinks } from '$lib/stores.js'
    import { onMount } from 'svelte';

    import de from './locales/de.json';
    import en from './locales/en.json';

    import { language } from '$lib/language';

    export let data;
    console.log(data);

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
    <h1 class="title">
      {translation.title}
    </h1>
    <div class="sectioncontainer">
        {translation.introtext}
    </div>
    <div class="sections">
    <div class="sectioncontainer">
      {translation.diffconf}
      <div class="sectionlink">
        <a href='/plugins/blockciphers/diffusion-confusion'>{translation.diffconftitle}</a>  
      </div>
    </div>
    <div class="sectioncontainer">
      {translation.modes}
      <div class="sectionlink">
        <a href='/plugins/blockciphers/modes'>{translation.ciphermodetitle}</a>  
      </div>
    </div>
  </div>
  </body>
  
  <style>
      body {
      flex-grow: 1;
      padding-top: 200px;
      display: flex;
      align-items: center;
      flex-direction: column;
      justify-content: center;
    }
  
    h1 {
      font-family: "Roboto", sans-serif;
      font-size: xx-large;
    }
  
    .sections {
      display: flex;
      align-items: center;
      justify-content: center;
      flex-direction: column;
    }
  
    .sectioncontainer {
      width: 60%;
      margin: 25px;
      font-family: "Roboto", sans-serif;
      font-size: large;
    }
  
    .sectionlink {
      padding: 10px;
      font-family: "Roboto", sans-serif;
      font-size: 22px;
      text-align: center;
      
      color: #333;
  
      background-color: lightgray;
      border-radius: 5px;
    }
  
    .sectioncontainer a:hover {
      background-color: #8f8f8f;
    }
  
    a {
      text-decoration: none;
      color: black;
    }
  </style>
