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
        display: flex; /* Flex container to hold blocks inline */
        flex-wrap: wrap; /* Allows blocks to wrap onto the next line */
        gap: 10px; /* Spacing between blocks */
    }

    .binaryblock {
        width: 8ch; /* Fixed width for each block */
        padding: 10px; /* Padding inside each block */
        border: 1px solid #666; /* Solid border for blocks */
        border-radius: 4px;
        background-color: #fff; /* White background for contrast */
        display: block; /* Grid layout to split the block into lines */
        grid-template-columns: 1fr; /* One column grid */
        word-wrap: break-word; /* Ensures content breaks to avoid overflow */
        text-align: center; /* Centers text in the block */
    }
    .binaryblock > div {
        line-height: 1.5;
    }
    .highlight {
      background-color: yellow;
    }
  </style>
  