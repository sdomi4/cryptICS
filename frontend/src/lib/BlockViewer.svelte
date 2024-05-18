<script>
    export let binaryblocks = '';
    console.log(binaryblocks);
</script>

<div class="blockviewer">
    {#each binaryblocks as block}
        <div class="blockcontainer">
            {block}
        </div>
    {/each}
</div>

<style>
    .blockviewer {
        display: flex;
        flex-wrap: nowrap;
        gap: 10px; 
    }

    .blockcontainer {
        width: 16ch;
        padding: 10px;
        border: 1px solid #666;
        border-radius: 4px;
        background-color: #fff;
        display: block;
        word-wrap: break-word;
        text-align: center;
        font-family: 'Courier New', Courier, monospace;
    }
</style>