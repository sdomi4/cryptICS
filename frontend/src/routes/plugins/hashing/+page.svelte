<script>
    import '../../../style/globalStyle.css'
    
    import { title } from '$lib/title';
    import { navLinks } from '$lib/stores.js'
    import { onMount } from 'svelte';
  
    import de from './locales/de.json';
    import en from './locales/en.json';
  
    import { language } from '$lib/language';
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
    <h1 class="title">
      {translation.title}
    </h1>
    <div class="sectioncontainer">
        {translation.introtext}
    </div>
    <div class="sections">
    <div class="sectioncontainer">
      {translation.diffusion}
      <div class="sectionlink">
        <a href='/plugins/hashing/diffusion'>{translation.diffusiontitle}</a>  
      </div>
    </div>
    <div class="sectioncontainer">
      {translation.experiment}
      <div class="sectionlink">
        <a href='/plugins/hashing/experiment'>{translation.experimenttitle}</a>  
      </div>
    </div>
  </div>
  </body>
  
  <style>
      body {
      flex-grow: 1;
      padding-top: 60px;
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
