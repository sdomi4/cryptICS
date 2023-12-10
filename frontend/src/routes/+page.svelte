<script>
    export let data;
    import logo from '../images/hslulogo.svg'
    import Footer from './Footer.svelte'
    console.log(data);
    const plugins = data?.body || []
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
</style>
<body>
<h1><img src={logo} alt="HSLU Logo" class="logo"/>CryptICS</h1>
<div class="pluginContainer">
    {#each plugins as plugin}
        <a href={plugin.uri}>
            <div class="plugin">
                <h2>{plugin.description}</h2>
            </div>
        </a>
    {/each}
</div>
</body>

<footer>
    <Footer />
</footer>
