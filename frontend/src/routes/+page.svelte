<script>
    export let data;
    console.log(data);
    const plugins = data?.body || []
</script>

<style>
    .plugin {
        background: lightsalmon;
        padding: 20px;
        text-align: center;
        border-radius: 5px;
        color: black;
        margin: 5px;
    }

    a {
        text-decoration: none;
    }

    .pluginContainer {
        display: flex;
    }
</style>

<h1>cryptICS</h1>
<div class="pluginContainer">
    {#each plugins as plugin}
        <a href={plugin.uri}>
            <div class="plugin">
                <h2>{plugin.description}</h2>
            </div>
        </a>
    {/each}
</div>