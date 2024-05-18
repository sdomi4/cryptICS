<script>
    export let original = [];
    export let modified = [];

    function highlighter(original, modified) {
        let highlightedArray = [];

        for (let i = 0; i < original.length; i++) {
            let originalString = original[i];
            let modifiedString = modified[i];
            let highlightedString = '';

            for (let j = 0; j < originalString.length; j++) {
                if (j > 0 && j % 16 === 0) {
                    highlightedString += '<br>';
                }
                if (originalString[j] === modifiedString[j]) {
                    highlightedString += modifiedString[j];
                } else {
                    highlightedString += `<span class="highlight">${modifiedString[j]}</span>`;
                }
            }
            highlightedArray.push(highlightedString);
        }
        return highlightedArray;
    }

    $: highlightedDifferences = highlighter(original, modified);
</script>

<div class="blockviewer">
    {#each modified as block, i}
        <div class="blockcontainer">
            {@html highlightedDifferences[i]}
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