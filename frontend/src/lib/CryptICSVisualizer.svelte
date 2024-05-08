<script>
    export let hexdata = '';
    export let binarydata = '';
    export let blockSize = 32; // Default block size
  
    // split data into blocks
    function formatData(data) {
      let formatted = '';
      for (let i = 0; i < data.length; i += blockSize) {
        formatted += data.slice(i, i + blockSize) + ' ';
      }
      return formatted.trim();
    }

    let binaryBlocks = formatData(binarydata);
    console.log(binaryBlocks);
  </script>
  
  <div class="datacontainer">
    <div class="hexdata">
        {hexdata}
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
    .data-box > div {
      display: inline-block;
      vertical-align: top;
      padding: 10px;
      margin-right: 10px;
      border: 1px solid #ccc;
      background-color: #f9f9f9;
    }
    .highlight {
      background-color: yellow;
    }
  </style>
  