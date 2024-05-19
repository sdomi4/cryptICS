<script>
    import { fade } from 'svelte/transition';

    export let original = [];
    export let modified = [];

    function highlighter(original, modified) {
        let highlightedArray = [];

        for (let i = 0; i < original.length; i++) {
            let originalString = original[i];
            let modifiedString = modified[i];
            let highlightedLetters = [];

            for (let j = 0; j < originalString.length; j++) {
                if (j > 0 && j % 16 === 0) {
                    highlightedLetters.push({ letter: '<br>', isHighlighted: false, isBreak: true });
                }
                highlightedLetters.push({
                    letter: modifiedString[j],
                    isHighlighted: originalString[j] !== modifiedString[j],
                    isBreak: false
                });
            }
            highlightedArray.push(highlightedLetters);
        }
        return highlightedArray;
    }

    $: highlightedDifferences = highlighter(original, modified);
</script>

<div class="blockviewer">
    {#each highlightedDifferences as block, i}
        <div class="blockcontainer">
            {#each block as { letter, isHighlighted, isBreak }, j}
                {#if isBreak}
                    <br>
                {:else}
                    <span class:highlight={isHighlighted} transition:fade>
                        {letter}
                    </span>
                {/if}
            {/each}
        </div>
    {/each}
</div>

<style>
    :global(.highlight) {
        background: #ffea4d;
    }

    .blockviewer {
        display: flex;
        flex-wrap: nowrap;
        gap: 10px; 
    }

    .blockcontainer {
        width: fit-content;
        padding: 10px;
        border: 1px solid #666;
        border-radius: 4px;
        background-color: #ffffff;
        display: block;
        word-wrap: break-word;
        text-align: center;
        font-family: 'Courier New', Courier, monospace;
    }
</style>
