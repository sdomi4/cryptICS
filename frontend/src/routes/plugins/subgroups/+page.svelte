<script>
  import { title } from '$lib/title';
  import { onMount } from 'svelte';

  import de from './locales/de.json';
  import en from './locales/en.json';

  import { language } from '$lib/language';
  let translation;
  $: translation = $language === 'en' ? en : de;


  onMount(() => {
      title.set('Group Theory');
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
    {translation.learntext}
    <div class="sectionlink">
      <a href='/plugins/subgroups/learn'>Learn</a>  
    </div>
  </div>
  <div class="sectioncontainer">
    {translation.practicetext}
    <div class="sectionlink">
      <a href='/plugins/subgroups/practice'>Practice</a>  
    </div>
  </div>
  <div class="sectioncontainer">
    {translation.calculatetext}
    <div class="sectionlink">
      <a href='/plugins/subgroups/calculate'>Calculate</a>  
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