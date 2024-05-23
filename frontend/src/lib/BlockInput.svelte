<script>
    import { createEventDispatcher } from 'svelte';
    export let inputValue = '';
    
    const dispatch = createEventDispatcher();

    function handleInput(event) {
        inputValue = event.target.value;
        dispatch('inputChange', inputValue);
    }
</script>

<div class="blockviewer">
        <div class="blockcontainer">
            <input type="number" bind:value={inputValue} on:input={handleInput} class="styledinput"/>
        </div>
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

    .styledinput {
        font-family: 'Courier New', Courier, monospace;
        text-align: center;
        border: none;
        outline: none;
        width: 100%;
        box-sizing: border-box;
        box-shadow: 0 0 15px 1px #007BFF;
    }
</style>