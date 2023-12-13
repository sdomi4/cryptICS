<script>
    export let data;
    import logo from '../images/hslulogo.svg'
    import Footer from './Footer.svelte'
    
    import de from './locales/de.json'
    import en from './locales/en.json'
    console.log(data);
    const plugins = data?.body || []

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

<style>
    body {
        font-family: 'Roboto', sans-serif;
        background-color: #f4f4f4;
        color: #333;
        margin: 0;
        padding: 0;
        flex-grow: 1;
        max-width: 100%;
        overflow-x: hidden;
    }

    h1 {
        font-size: 2.5em;
        text-align: center;
        color: #333;
        margin-top: 20px;
    }

    .pluginContainer {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        padding: 20px;
        min-height: 65vh;
    }

    .plugin {
        background: #ffffff;
        padding: 20px;
        text-align: center;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin: 10px;
        width: 200px;
    }

    .plugin:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }

    a {
        text-decoration: none;
        color: #333;
    }

    a:hover {
        color: #007bff;
    }

    .logo {
        width: 200px;
        height: auto;
        display: block;
        margin: 0 auto 20px;
    }

    .language-toggle {
        position: relative;
        float: right;
        margin: 10px;
        width: 50px;
        height: 25px;
    }
    .language-toggle input[type="checkbox"] {
        opacity: 0;
        width: 0;
        height: 0;
    }

    .language-toggle label {
        position: absolute;
        cursor: pointer;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0px;
        background-image: url('../images/uk_flag.svg');
        background-size: cover;
        -webkit-transition: .4s;
        transition: .4s;
        border-radius: 25px;
    }

    .language-toggle label:before {
        position: absolute;
        content: "";
        height: 25px;
        width: 25px;
        left: -0.5px;
        bottom: 0px;
        background-color: white;
        -webkit-transition: .4s;
        transition: .4s;
        border-radius: 50%;
    }

    input:checked + label {
        background-image: url('../images/de_flag.svg');
    }

    input:checked + label:before {
        -webkit-transform: translateX(26px);
        -ms-transform: translateX(26px);
        transform: translateX(26px);
    }

    .textdiv {
        display: flex;
        align-items: center;
        justify-content: center;
    }



</style>
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
                <h2>{plugin.description}</h2>
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
