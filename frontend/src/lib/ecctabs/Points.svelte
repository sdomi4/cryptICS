<script>
    export let points = [];
    export let translation;
</script>

<body>
    {#each points as point, index}
        {translation.pointlabel} {index+1}: ({point[0]}, {point[1]})<br>
    {/each}
</body>