<script>
    export let key = '';
    // different visuals per cipher mode
    // export let mode = '';
</script>

<div>
    <div class="cipherviewer">
        <div class="ciphersymbol">
            <svg width="100" height="200" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                <path d="M 30,10 L 90,10 L 30,80 L 90,80 Z" fill="transparent" stroke="black" stroke-width="3"/>
                <text x="50%" y="60%" dominant-baseline="middle" text-anchor="left" fill="black" font-size="20">{key}</text>
            </svg>
        </div>
        <div class="key">
            {key}
        </div>
    </div>
</div>