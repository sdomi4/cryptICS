<script>
    import { title } from '$lib/title';
    import { backLink } from '$lib/title'
    import { pageTitle } from '$lib/stores.js';

    import '../../../../style/globalStyle.css';
  
    import de from './locales/de.json';
    import en from './locales/en.json';
  
    import { language } from '$lib/language';
    let translation;
    $: {
        translation = $language === 'en' ? en : de;
        title.set(translation.pagetitle);
        backLink.set('/plugins/rsa');
        pageTitle.set(translation.subpagetitle);
    }

    export let data;
    console.log(data);
  </script>

<body>
    <div class="bodycontainer">
        <div class="introtext">
            {JSON.stringify(data)}
        </div>
    </div>
</body>

<style>
    .bodycontainer {
        margin-top: 80px;
    }
</style>