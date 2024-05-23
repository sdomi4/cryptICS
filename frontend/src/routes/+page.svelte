<script>
    export let data;
    import logo from '../images/hslulogo.svg'
    import Footer from './Footer.svelte'

    import '../style/globalStyle.css'

    console.log(data);
    const plugins = data?.body || []

    import de from './locales/de.json'
    import en from './locales/en.json'
    import { language } from '$lib/language';
    let translation;
    $: translation = $language === 'en' ? en : de;

    function toggleLanguage() {
        language.update(lang => lang === 'en' ? 'de' : 'en');
    }
</script>

<head>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
</head>

<header>
    <div class="language-toggle">
        <input type="checkbox" id="lang-toggle" 
               checked={language === 'de'} 
               on:change={toggleLanguage}>
        <label for="lang-toggle">
            <span class="toggle-track"></span>
        </label>
    </div>
</header>
<body>
<h1><img src={logo} alt="HSLU Logo" class="logo"/>CryptICS</h1>
<p class="textdiv">
    {translation.welcometext}
</p>
<div class="pluginContainer">
    {#each plugins as plugin}
        <a href={plugin.uri}>
            <div class="plugin">
                {#if $language === 'en'}
                    <h2>{plugin.description.en}</h2>
                {:else}
                    <h2>{plugin.description.de}</h2>
                {/if}
            </div>
        </a>
    {/each}
</div>
<p class="textdiv">
    {translation.creatortext}
</p>
</body>

<footer>
    <Footer />
</footer>
