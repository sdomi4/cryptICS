<script>
    import { get } from 'svelte/store';
    export let binaryblocks = '';
    // click handler passed to the component
    export let onLetterClick = (letter, index, block) => {};

    function handleClick(event) {
        const target = event.target;
        if (target.classList.contains('letter')) {
            const blockIndex = target.dataset.blockIndex;
            const index = target.dataset.index;
            const letter = target.textContent;

            // Toggle highlight class
            target.classList.toggle('highlight');

            // Call the passed event handler
            onLetterClick(letter, index, blockIndex);
        }
    }
</script>


<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div class="blockviewer" on:click={handleClick}>
    {#each binaryblocks as block, blockIndex}
        <div class="blockcontainer">
            {#each block.split('') as letter, index}
                <span 
                    class="letter" 
                    data-block-index={blockIndex} 
                    data-index={index}
                >
                    {letter}
                </span>
            {/each}
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
        max-width: 17ch;
        padding: 10px;
        border: 1px solid #666;
        border-radius: 4px;
        background-color: #fff;
        display: grid;
        grid-template-columns: repeat(16, 1ch);
        word-wrap: break-word;
        text-align: center;
        font-family: 'Courier New', Courier, monospace;
        user-select: none;
    }

    .letter {
        cursor: pointer;
    }

    :global(.highlight) {
        background: #ffea4d;
    }
</style>