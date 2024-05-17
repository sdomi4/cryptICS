<style>
    body {
        flex-grow: 1;
        padding-top: 100px;
    }

    .correct {
        background-color: #c8e6c9;
    }
    .incorrect {
        background-color: #ffcdd2;
    }
    .highlight {
        background-color: cadetblue;
    }
    table {
        border-collapse: collapse;
        margin: 20px 0;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: center;
    }
    input {
        width: 50px;
        text-align: center;
    }
    /* hiding the input arrows https://www.w3schools.com/howto/howto_css_hide_arrow_number.asp*/
    /* Chrome, Safari, Edge, Opera */
    input::-webkit-outer-spin-button,
    input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
    }

    /* Firefox */
    input[type=number] {
        -moz-appearance: textfield;
        appearance: textfield;
    }

    /* formatting the group info dings https://stackoverflow.com/questions/3742975/subscript-and-superscript-for-the-same-element */
    .supsub {
        display: inline-block;
    }

    .supsub sup,
    .supsub sub {
        position: relative;
        display: block;
        font-size: .5em;
        line-height: 1.2;
    }

    .supsub sub {
        top: .3em;
    }

    .tablestyle {
        border-collapse: collapse;
        table-layout: fixed;
    }

    .tablestyle th, .tablestyle td {
        width: 50px;
        height: 30px;
        padding: 4px 8px;
        border: 1px solid black;
        text-align: center;
        font-size: 16px;
        line-height: 22px;
    }

    .tablestyle input[type="number"] {
        width: 100%;
        box-sizing: border-box;
    }
</style>
<script>
    import { writable, derived } from 'svelte/store';
    import { navLinks } from '$lib/stores';
    import '../../../../style/globalStyle.css'
    // import data from page load server side
    export let data;
    export let error = null;

    if (error) {
        console.log(error);
    } else {
        console.log(data);
    }

    import de from './locales/de.json'
    import en from './locales/en.json'
    import { language } from '$lib/language';
    let translation;
    $: {
        translation = $language === 'en' ? en : de;
        navLinks.set([
            { description: translation.practice, uri: "/plugins/subgroups/practice"},
            { description: translation.calculate, uri: "/plugins/subgroups/calculate"}
        ]);
    }

    let elements = data.props.data.elements;
    let operation = data.props.data.operation;
    let mod = data.props.data.mod;
    let order = elements.length;
    let rowOrders = data.props.data.roworders;

    $: if ($stepDetails.showColorTable) {
    queueMicrotask(() => {
    const table = document.querySelector('.colortable');

    table.addEventListener('click', function(e) {
      const clickedCell = e.target;
      if (clickedCell.tagName === 'TD') {
        const row = clickedCell.parentNode;
        const rowOrder = rowOrders[row.firstElementChild.textContent.trim()];
        const colorValue = getColorFromValue(rowOrder);

        const clickedNumber = clickedCell.textContent.trim();
        const cellsInRow = row.querySelectorAll('td:not(:last-child)');

        cellsInRow.forEach(cell => {
            if (cell.textContent.trim() === clickedNumber) {
                if (cell === clickedCell) {
                    cell.style.backgroundColor = colorValue;
                } else {
                    cell.style.backgroundColor = `hsl(234, 0%, 50%)`;
                }
            }});
        }});
    })};

    function getColorFromValue(value) {
        const hue = parseInt(value, 10) * 36 % 360;
        return `hsl(${hue}, 100%, 80%)`;
    }

    let currentStep = writable(1);


    let stepDetails = derived(currentStep, $currentStep => {
        return {
            showOrder: $currentStep >=2,
            showSubgroups: $currentStep >=3,
            showPrimitives: $currentStep >=4,
            showTable: $currentStep >= 5,
            showColorTable: $currentStep >= 6
        };
    });

    function nextStep() {
        currentStep.update(i => i+1)
    }

    function operationSymbol(operation) {
        const symbols = {
            add: "+",
            sub: "-",
            mul: "*",
            div: "÷",
            exp: "^"
        };
        return symbols[operation] || "?";
    }

    $: formattedOperation = formattedOperation(operation);

    function formattedOperation(operation) {
        switch(operation) {
            case "exp":
                return `a<sup>b</sup>`;
            default:
                return `a ${operationSymbol(operation)} b`;
        }
    }

    function checkInput(event, x, y) {
        console.log(event);
        const userAnswer = parseInt(event.target.value);
        console.log(x, y)
        const correctAnswer = data.props.data.exponenttable[x][y];
        console.log(correctAnswer);
        event.target.classList.remove("correct", "incorrect");
        if (userAnswer === correctAnswer) {
            event.target.classList.add("correct");
        } else if (!isNaN(userAnswer)) {
            event.target.classList.add("incorrect");
        }
    }

    function parseList(listString) {
        let stringArray = listString.split(',');
        let intArray = stringArray.map(function(item) {
            return parseInt(item, 10);
        }).filter(function(item) {
            return !isNaN(item);
        });
        // sort number array to allow any order of input to be compared with sorted backend output
        intArray.sort(function(a, b) {
            return a - b;
        });
        return intArray;
    }

    function checkSingleInput(event, field) {
        let correct = false;
        event.target.classList.remove("correct", "incorrect");
        switch(field) {
            case "order":
                const orderAnswer = parseInt(event.target.value);
                if (orderAnswer === order) {
                    correct = true;
                }
                break;
            case "subgroupnumber":
                const numberAnswer = parseInt(event.target.value);
                if (numberAnswer === data.props.data.possiblesubgroups.length) {
                    correct = true;
                }
                break;
            case "subgrouporders":
                const ordersAnswer = parseList(event.target.value);
                // js can't compare arrays apparently, so turning into string for comparison
                if (JSON.stringify(ordersAnswer) === JSON.stringify(data.props.data.possiblesubgroups)) {
                    correct = true;
                }
                break;
            case "primitives":
                const primitivesAnswer = parseInt(event.target.value);
                if (primitivesAnswer === data.props.data.possibleprimitives) {
                    correct = true;
                }
                break;
            case "rowOrder":
                const rowOrderAnswer = parseInt(event.target.value);
                if (rowOrderAnswer === rowOrders[event.target.parentNode.parentNode.firstElementChild.textContent.trim()]) {
                    correct = true;
                }
        }
        if (correct) {
            event.target.classList.add("correct");
        } else {
            event.target.classList.add("incorrect");
        }
    }

</script>

<head>

</head>

<body>
    <div class="bodycontainer">
        <div class="slideshowcontainer">
            <!-- dummy div so ide doesnt complain about unused css selectors -->
            <div class="correct incorrect highlight"></div>
            <!-- Slideshow Controls -->
            

            <!-- group info -->
            <p>{translation.given} &#8484;<span class="supsub"><sup>{operationSymbol(operation)}</sup><sub>{mod}</sub></span></p>

            <!-- order stuff -->
            {#if $stepDetails.showOrder}
                <p>{translation.order} <input type="number" on:input={(event) => checkSingleInput(event, "order")}></p>
            {/if}
            <!-- subgroup things -->
            {#if $stepDetails.showSubgroups}
                <p>
                    {translation.subgroups}
                    <input type="number" on:input={(event) => checkSingleInput(event, "subgroupnumber")}>
                    {translation.subgroups2}
                    <input on:input={(event) => checkSingleInput(event, "subgrouporders")}>
                </p>
            {/if}
            <!-- primitives -->
            {#if $stepDetails.showPrimitives}
                <p>
                    {translation.primitives} {order} {translation.primitives2}{order}{translation.primitives3}
                    <input type="number" on:input={(event) => checkSingleInput(event, "primitives")}>
                    {translation.primitives4}
                </p>
            {/if}
            <!-- exponent table to fill in -->
            {#if $stepDetails.showTable}
            {translation.table}
            <table class="tablestyle">
                <tr>
                    <th>a<sup>b</sup> mod {data.props.data.mod}</th>
                    {#each elements as element}
                        <th>{element}</th>
                    {/each}
                </tr>
                {#each elements as rowElement, i}
                    <tr>
                        <th>{rowElement}</th>
                        {#each elements as colElement, j}
                            <td>
                                <input type="number"
                                    aria-label={`${rowElement} ${operationSymbol(operation)} ${colElement}`}
                                    on:input={(event) => checkInput(event, rowElement, colElement)}
                                    min="0"
                                    max={data.props.data.mod}>
                            </td>
                        {/each}
                    </tr>
                {/each}
            </table>
            {/if}
            <!-- add subgroup orders and color it in -->
            {#if $stepDetails.showColorTable}
            {translation.coloring}
            <table class="tablestyle colortable">
                <tr>
                    <th>a<sup>b</sup> mod {data.props.data.mod}</th>
                    {#each elements as element}
                        <th>{element}</th>
                    {/each}
                    <th>ord</th>
                </tr>
                {#each elements as rowElement, i}
                    <tr>
                        <th>{rowElement}</th>
                        {#each elements as colElement, j}
                            <td>
                                {data.props.data.exponenttable[rowElement][colElement]}
                            </td>
                        {/each}
                        <td><input type="number" on:input={(event) => checkSingleInput(event, "rowOrder")}></td>
                    </tr>
                {/each}
            </table>
            {/if}
            {#if !$stepDetails.showColorTable}
                <button on:click={nextStep}>{translation.next}</button>
            {/if}
        </div>
    </div>
</body>