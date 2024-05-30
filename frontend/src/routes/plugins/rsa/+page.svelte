<script>
    import '../../../style/globalStyle.css'
        
    import { title } from '$lib/title';
    import { backLink } from '$lib/title'
    import { pageTitle } from '$lib/stores.js';
    import { onMount } from 'svelte';

    import de from './locales/de.json';
    import en from './locales/en.json';

    import { language } from '$lib/language';

    export let data;
    console.log(data);

    let translation;
    $: {
        translation = $language === 'en' ? en : de;
        title.set(translation.title);
        backLink.set('/plugins/rsa');
        pageTitle.set(translation.overviewtitle);
    }

    onMount(() => {

    });
</script>

<body>
  <div class="bodycontainer">
      <h1 class="title">
        {translation.title}
      </h1>
      <div class="sectioncontainer">
          {translation.introtext}
      </div>
      <div class="sections">
      <div class="sectioncontainer">
        {translation.homomorphic}
        <div class="sectionlink">
          <a href='/plugins/rsa/homomorphic'>{translation.homomorphictitle}</a>  
        </div>
      </div>
      <div class="sectioncontainer">
        {translation.carmichael}
        <div class="sectionlink">
          <a href='/plugins/rsa/carmichael'>{translation.carmichaeltitle}</a>  
        </div>
      </div>
    </div>
</div>
  </body>
  
  <style>
    .bodycontainer {
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
