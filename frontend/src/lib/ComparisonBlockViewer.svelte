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

    let highlightedDifferences = highlighter(original, modified);
    console.log(highlightedDifferences);
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
        width: 16ch;
        padding: 10px;
        border: 1px solid #666;
        border-radius: 4px;
        background-color: #ffffff;
        display: block;
        grid-template-columns: 1fr;
        word-wrap: break-word;
        text-align: center;
    }
</style>