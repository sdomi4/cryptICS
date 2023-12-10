<script>
    import logo from '../../images/hslulogo.svg';
    import {page} from '$app/stores'
    export let data;
    let title = $page.url.pathname.split('/')[2];
    let parent = $page.url.pathname.slice(0, $page.url.pathname.lastIndexOf('/'))
</script>

<head>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
</head>

<div class ="pagecontainer">
<header>
    <div class="logo" href="/">
       <img src={logo} alt="HSLU Logo"/> 
    </div>
    <nav>
        <div class = "homediv">
            <a class="home" href="/">Home</a>
        </div>
        <div class="navseparator"></div>
        
        <div class = "navdiv">
            <div class="pagename">{title.charAt(0).toUpperCase() + title.slice(1)}:</div>
            {#each data.body as link}
                <div class = "navlinkcontainer">
                    <a class="navlink" href={link.uri}>{link.description}</a>
                </div>
            {/each}
        </div> 
    </nav>
    <div class="cryptics">
        CryptICS
    </div>
</header>
  
<style>
    html, body {
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
        margin-top: 8px;
        margin-left: 30%;
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
        margin-top: -15px;
        margin-right: 10px;
    }

    .navdiv {
        display: flex;
        background-color: #dedcdc;
        border-radius: 5px;
        padding: 25px;
        margin-top: -8px;
    }

    .navlinkcontainer {
        margin-top: -12px;
    }

    .navlink {
        margin: 15px;
        padding-top: 5px;
        padding-bottom: 5px;
    }

    .home {
        padding-top: 8px;
        font-size: 26px;
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

    footer {
        background-color: #f9f9f9;
        padding: 20px;
        text-align: center;
        position: relative;
        bottom: 0;
        width: 100%;
        box-shadow: 0 -2px 4px rgba(0,0,0,0.1);
        }
</style>

<slot />

</div>

<footer>

</footer>