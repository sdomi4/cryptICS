<script>
    export let original = '';
    export let modified = '';

    // function to highlight differences between two strings
    function highlightDifferences(original, modified) {
        let differences = [];

        // find differences between original and modified strings
        for (let i = 0; i < original.length; i++) {
            if (original[i] !== modified[i]) {
                differences.push(i);
            }
        }

        // highlight differences in modified string
        let highlighted = modified.split('').map((letter, index) => {
            if (differences.includes(index)) {
                return `<span class="highlight">${letter}</span>`;
            } else {
                return letter;
            }
        });

        return highlighted.join('');
    }
</script>

<div class="blockviewer">
    {#each modified as block, i}
        <div class="blockcontainer">
            {#if original[i] === block}
                {block}
            {:else}
                {@html highlightDifferences(original, modified)}
            {/if}
        </div>
    {/each}
</div>