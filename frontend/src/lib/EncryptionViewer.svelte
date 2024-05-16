<script>
    export let key = '';
    export let blocknumber = 1;
    // different visuals per cipher mode
    // export let mode = '';
</script>

<div>
    <div class="cipherviewer">
        {#each {length: blocknumber} as _, i}
        <div class="ciphersymbol">
            <svg width="130" height="150" xmlns="http://www.w3.org/2000/svg">
              
              <path d="M 65,75 L 45,50 L 85,50 L 45,100 L 85,100 Z" fill="transparent" stroke="black" stroke-width="2"/>
              <text x="5" y="51.5%" dominant-baseline="middle" text-anchor="left" fill="black" font-size="20">{key}</text>
              <text x="85" y="51.5%" dominant-baseline="middle" text-anchor="left" fill="black" font-size="20">E</text>
              <path d="M 25,75 L 45,75 L 42,72 L 42,78 L 45,75" fill="black" stroke="black" stroke-width="1"/>
              <path d="M 65,5 L 65,40 L 62,37 L 68,37 L 65,40" fill="black" stroke="black" stroke-width="1"/>
              <path d="M 65,110 L 65,145 L 62,142 L 68,142 L 65,145" fill="black" stroke="black" stroke-width="1"/>
            </svg>
          </div>
        {/each}
    </div>
</div>

<style>
    .cipherviewer {
        display: flex;
        flex-direction: row;
        justify-content: left;
        align-items: center;
        margin-left: 18px;
        gap: 45px;
    }
</style>