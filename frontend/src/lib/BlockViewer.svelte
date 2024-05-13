<script>
    // data contains plaintext, key, and ciphertext
    export let cleartext = '';
</script>

<div class="blockviewer">
    {#each cleartext as block}
        <div class="blockcontainer">
            {block}
        </div>
    {/each}
</div>

<style>
    .blockviewer {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .blockcontainer {
        display: flex;
        flex-direction: row;
        align-items: center;
    }
</style>