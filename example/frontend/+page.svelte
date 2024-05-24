<script>
    import { title } from '$lib/title';
    import { backLink } from '$lib/title'
    import { pageTitle } from '$lib/stores.js';

    import '../../../style/globalStyle.css'
  
    import de from './locales/de.json';
    import en from './locales/en.json';
  
    import { language } from '$lib/language';
    let translation;
    $: {
        translation = $language === 'en' ? en : de;
        title.set(translation.pagetitle);
        backLink.set('/plugins/example');
        pageTitle.set(translation.subpagetitle);
    }

    export let data;
  </script>

<body>
    {#each data.body as element}
        <div class = "container">
            <p class="data">{element.description}</p>
        </div>
    {/each}
</body>