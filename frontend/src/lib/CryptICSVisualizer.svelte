<script>
    export let input = '';
    export let hexdata = '';
    export let binarydata = '';
    export let text = {};
    export let blockSize = 32; // Default block size

    console.log(hexdata);
  
    // split data into blocks
    function formatData(data) {
      let formatted = '';
      for (let i = 0; i < data.length; i += blockSize) {
        formatted += data.slice(i, i + blockSize) + ' ';
      }
      return formatted.trim();
    }

    let binaryBlocks = formatData(binarydata);
  </script>
  
  <div class="visualizer">
    <div class="textdiv">
        {text.inputtext}
        {input}
    </div>
    <div class="textdiv">
        {text.hextext}
    </div>
    <div class="hexdata">
        {hexdata}
    </div>
    <div class="textdiv">
        {text.binarytext}
    </div>
    <div class="binarydata">
        {#each binaryBlocks.split(' ') as block}
            <div class="binaryblock">
                {block}
            </div>
        {/each}
    </div>
  </div>
  
  <style>
    .textdiv {
        margin-bottom: 10px;
    }

    .visualizer {
        width: fit-content; /* Control the width to not span the entire parent container */
        padding: 20px; /* Padding inside the box */
        background-color: #f8f8f8; /* Light grey background for the box */
        border: 1px solid #ccc; /* Light grey border */
        border-radius: 10px; /* Slightly rounded corners */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow to make the box 'float' */
    }

    .hexdata {
        font-family: 'Courier New', monospace; /* Ensures hex data is evenly spaced */
        color: #333; /* Darker text color for better readability */
        margin-bottom: 20px; /* Space between hex data and binary blocks */
    }

    .binarydata {
        display: flex;
        flex-wrap: wrap;
        gap: 10px; 
    }

    .binaryblock {
        width: 8ch;
        padding: 10px;
        border: 1px solid #666;
        border-radius: 4px;
        background-color: #fff;
        display: block;
        grid-template-columns: 1fr;
        word-wrap: break-word;
        text-align: center;
    }
    .binaryblock > div {
        line-height: 1.5;
    }
    .highlight {
      background-color: yellow;
    }
  </style>
  