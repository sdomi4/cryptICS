<script>
    export let points = [];
    export let translation;
    export let infinity;
</script>

<body>
    {#each points as point, index}
        {translation.pointlabel} {index+1}: ({point[0]}, {point[1]})<br>
    {/each}
    {#if infinity != null}
        {translation.pointlabel} &#120134;: (-, &infin;)
    {/if}
</body>