<script>
    import Footer from '../Footer.svelte';
    import logo from '../../images/hslulogo.svg';
    import deFlag from '../../images/de_flag.svg';
    import ukFlag from '../../images/uk_flag.svg';

    import { title } from '$lib/title'
    import { backLink } from '$lib/title'
    import { pageTitle } from '$lib/stores.js';

    import { language } from '$lib/language'

    // jank to properly persist language toggle
    let isGerman;
    $: isGerman = $language === 'de';

    function toggleLanguage() {
        language.update(lang => lang === 'en' ? 'de' : 'en');
    }
</script>

<head>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
</head>

<div class ="pagecontainer">
<header>
    <div class="logo" href="/">
       <img src={logo} alt="HSLU Logo"/> 
    </div>
    <div class = "navcontainer">
        <nav>
            <div class = "homediv">
                <a class="home" href="/">Home</a>
            </div>
            <div class="navseparator"></div>
            
            <div class = "navdiv">
                <div class="pagename">
                    <a href={$backLink}>{$title}</a>:
                </div>
                <div class = "navlinkcontainer">
                    <span class="navlink">{$pageTitle}</span>
                </div>
            </div> 
        </nav>
        <div class="navrighthalf">
            <div class="cryptics">
                CryptICS
            </div>
            <div class="language-toggle">
                <input type="checkbox" id="lang-toggle" 
                    bind:checked={isGerman} 
                    on:change={toggleLanguage}>
                <label for="lang-toggle" style="background-image: url({$language === 'en' ? ukFlag : deFlag});">
                    <span class="toggle-track"></span>
                </label>
            </div>
        </div>
    </div>
</header>

<body>
<slot />
</body>

</div>

<footer>
 <Footer />
</footer>

<style>
    body {
        max-width: 100%;
        overflow-x: hidden;
    }
    .pagecontainer {
    display: flex;
    flex-direction: column;
    min-height: 80vh;
    width: 100%;
    }
    header {
        background-color: #fff;
        display: flex;
        padding: 10px;
        position: fixed;
        top: 0;
        height: 60px;
        width: 100%;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        z-index: 1000;
    }
    .cryptics {
        font-family: "Roboto", sans-serif;
        font-size: 35px;
    }
    .logo {
        float: left;
        padding-top: 10px;
    }
    nav {
        display: flex;
        padding-top: 15px;
    }

    .navseparator {
        width: 3px;
        background-color: darkgrey;
        height: 32px;
        margin-left: 24px;
        margin-right: 48px;
    }

    .pagename {
        font-family: "Roboto", sans-serif;
        font-size: 26px;
        margin-right: 10px;
    }

    .navcontainer {
        display: flex;
        justify-content: space-between;
        width: 100%;
        align-items: center;
    }

    .navdiv {
        display: flex;
        align-items: center;
        background-color: #dedcdc;
        border-radius: 5px;
        padding: 15px;
        margin-top: -10px;
        white-space: nowrap;
    }
    .navlink {
        margin: 5px;
    }

    .navrighthalf {
        display: flex;
        align-items: center;
        margin-right: 5%;
    }

    .home {
        padding-top: 8px;
        font-size: 26px;
        margin-left: 25px;
    }

    a {
        font-family: "Roboto", sans-serif;
        font-size: 22px;
        text-decoration: none;
        color: #333;
    }

    nav .navlink {
        padding: 10px;
        font-family: "Roboto", sans-serif;
        font-size: 22px;

        text-decoration: none;
        color: #333;

        background-color: lightgray;
        border-radius: 5px;
    }
    nav a:hover {
        color: black;
        background-color: #8f8f8f;
    }

    .language-toggle {
        position: relative;
        display: block;
        margin: 10px;
        width: 50px;
        height: 25px;
    }
    .language-toggle input[type="checkbox"] {
        opacity: 0;
        width: 0;
        height: 0;
        display: block;
    }

    .language-toggle label {
        position: absolute;
        cursor: pointer;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0px;
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

    input:checked + label:before {
        -webkit-transform: translateX(26px);
        -ms-transform: translateX(26px);
        transform: translateX(26px);
    }    
</style>