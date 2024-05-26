<script>
    import { title } from '$lib/title';
    import { backLink } from '$lib/title'
    import { pageTitle } from '$lib/stores.js';
    import { writable, derived } from 'svelte/store';
    import { slide } from 'svelte/transition';
    import { quintOut } from 'svelte/easing';

    import '../../../../style/globalStyle.css';
  
    import de from './locales/de.json';
    import en from './locales/en.json';
  
    import { language } from '$lib/language';

    let translation;
    $: {
        translation = $language === 'en' ? en : de;
        title.set(translation.title);
        backLink.set('/plugins/ecc');
        pageTitle.set(translation.subpagetitle);
    }

    export let data;

    let p = data.body.p;
    let a = data.body.a;
    let b = data.body.b;

    let m = data.body.practice_points[0]
    let n = data.body.practice_points[1]
    let o = data.body.practice_points[2]

    let m_coords = data.body.m;
    let n_coords = data.body.k;
    let P_coords = data.body.point_P;
    let T_coords = data.body.point_T;

    let nonsingularity = data.body.nonsingularity;

    let inverses = data.body.inverse_table;
    let inverseTableRows = chunkArray(inverses, 10);

    let currentStep = writable(1);

    let stepDetails = derived(currentStep, $currentStep => {
        return {
            showCurveCheck: $currentStep >=2,
            showPointCheck: $currentStep >=3,
            showCalculation: $currentStep >=4,
            showInversion: $currentStep >= 5,
            showEstimation: $currentStep >= 6
        };
    });

    function nextStep() {
        currentStep.update(i => i+1)
    }

    function chunkArray(array, chunkSize) {
        const chunks = [];
        for (let i = 0; i < array.length; i += chunkSize) {
            chunks.push(array.slice(i, i + chunkSize));
        }
        return chunks;
    }

    function checkSingleInput(event, field) {
        let correct = false;
        console.log(event.target.value, field);
        event.target.classList.remove("correct", "incorrect");
        switch(field) {
            case "curvecheck":
                const curveCheckAnswer = parseInt(event.target.value);
                if (curveCheckAnswer === nonsingularity) {
                    correct = true;
                }
                break;
            case "pointcheck":
                const pointCheckAnswer = parseInt(event.target.value);
                if (pointCheckAnswer === data.body.check_point[0]) {
                    correct = true;
                }
                break;
            case "calculation_x":
                const calculationXAnswer = parseInt(event.target.value);
                if (calculationXAnswer === data.body.q[0]) {
                    correct = true;
                }
                break;
            case "calculation_y":
                const calculationYAnswer = parseInt(event.target.value);
                if (calculationYAnswer === data.body.q[1]) {
                    correct = true;
                }
                break;
                case "inversion_x":
                const inversionXAnswer = parseInt(event.target.value);
                if (inversionXAnswer === data.body.point_U[0]) {
                    correct = true;
                }
                break;
            case "inversion_y":
                const inversionYAnswer = parseInt(event.target.value);
                if (inversionYAnswer === data.body.point_U[1]) {
                    correct = true;
                }
                break;
            // kind of unsure how the result is rounded or not, so giving the benefit of the doubt
            case "estimationLower":
                const estimationLowerAnswer = parseInt(event.target.value);
                if (estimationLowerAnswer >= data.body.hasse_bounds[0]-1 || estimationLowerAnswer <= data.body.hasse_bounds[0]+1) {
                    correct = true;
                }
                break;
            case "estimationUpper":
                const estimationUpperAnswer = parseInt(event.target.value);
                if (estimationUpperAnswer >= data.body.hasse_bounds[1]-1 || estimationUpperAnswer <= data.body.hasse_bounds[1]+1) {
                    correct = true;
                }
                break;
        }
        if (correct) {
            event.target.classList.add("correct");
        } else {
            event.target.classList.add("incorrect");
        }
    }

</script>

<body>
    <div class="correct incorrect"></div>
    <div class="bodycontainer">
        <div class="questions">
        <p>{@html translation.given}{a}{@html translation.given2}{b} {translation.given3} <span class="zdings">&#8484;</span><sub>{p}</sub></p>
        {#if $stepDetails.showCurveCheck}
            <div class="questioncontainer" transition:slide={{ delay: 0, duration: 300, easing: quintOut, axis: 'y' }}>
                <p>{translation.curvecheck}</p>
                {translation.curvecheckresult} <input class="answerinput" type="number" on:input={(event) => checkSingleInput(event, "curvecheck")}>
            </div>
        {/if}
        {#if $stepDetails.showPointCheck}
            <div class="questioncontainer" transition:slide={{ delay: 0, duration: 300, easing: quintOut, axis: 'y' }}>
                <p>{translation.pointcheck}({P_coords}) {translation.pointcheck2}</p>
                {translation.pointcheckresult} <input class="answerinput" type="number" on:input={(event) => checkSingleInput(event, "pointcheck")}>
            </div>
        {/if}
        {#if $stepDetails.showCalculation}
            <div class="questioncontainer" transition:slide={{ delay: 0, duration: 300, easing: quintOut, axis: 'y' }}>
                <p>{translation.calculation} {m}{translation.calculation2}({m_coords}) {translation.calculation3} {n}{translation.calculation4}({n_coords}) {translation.calculation5} {o}{translation.calculation6}</p>
                S(<input class="answerinput coordinateinput" type="number" on:input={(event) => checkSingleInput(event, "calculation_x")}>, <input class="answerinput coordinateinput" type="number" on:input={(event) => checkSingleInput(event, "calculation_y")}>)
            </div>
        {/if}
        {#if $stepDetails.showInversion}
            <div class="questioncontainer" transition:slide={{ delay: 0, duration: 300, easing: quintOut, axis: 'y' }}>
                <p>{translation.inversion}({T_coords}) {translation.inversion2}</p>
                U(<input class="answerinput coordinateinput" type="number" on:input={(event) => checkSingleInput(event, "inversion_x")}>, <input class="answerinput coordinateinput" type="number" on:input={(event) => checkSingleInput(event, "inversion_y")}>)
            </div>
        {/if}
        {#if $stepDetails.showEstimation}
            <div class="questioncontainer" transition:slide={{ delay: 0, duration: 300, easing: quintOut, axis: 'y' }}>
                <p>{translation.estimation} {data.body.estimation_number} {translation.estimation2}</p>
                {translation.estimationresult} <input class="answerinput" type="number" on:input={(event) => checkSingleInput(event, "estimationLower")}> {translation.estimationresult2} <input class="answerinput" type="number" on:input={(event) => checkSingleInput(event, "estimationUpper")}> {translation.estimationresult3}
            </div>
        {/if}
        {#if !$stepDetails.showEstimation}
            <button on:click={nextStep} transition:slide={{ delay: 0, duration: 300, easing: quintOut, axis: 'y' }}>{translation.next}</button>
        {/if}
        </div>
        <div class="inversiontable">
            <div class="inversiontext">
                <b>{translation.inversetable}</b>
            </div>
            <div class="tablerows">
            {#each inverseTableRows as row, i}
                <div class="tablerow">
                    <table class="fixed-table">
                        <tr>
                            <th class="inverseheader">
                                x
                            </th>
                            {#each row as cell, j}
                                <td>
                                    {i*10 + j + 1}
                                </td>
                            {/each}
                        </tr>
                        <tr>
                            <th class ="inverseheader">
                                x<sup>-1</sup> mod {p}
                            </th>
                            {#each row as cell}
                                <td>
                                    {cell}
                                </td>
                            {/each}
                        </tr>
                    </table>
                </div>
            {/each}
        </div>
        </div>
    </div>
</body>

<style>
    .inversiontext {
        width: 250px;
        text-wrap: nowrap;
        margin-bottom: 10px;
        margin-top: 40px;
    }
    .correct {
        background-color: #c8e6c9;
    }
    .incorrect {
        background-color: #ffcdd2;
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

    input {
        width: 50px;
        text-align: center;
    }

    .answerinput.coordinateinput {
        width: 25px;
    }

    .bodycontainer {
        margin-top: 80px;
        display: flex;
        flex-direction: row;
    }

    .questions {
        display: flex;
        flex-direction: column;
        gap: 20px;
        width: 400px;
    }

    .zdings {
        font-size: 1.3em;
    }

    .inversiontable {
        display: flex;
        flex-wrap: wrap;
        width: 250px;
        margin-left: 200px;
    }

    .tablerows {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .fixed-table {
        max-width: 500px;
    }

    table {
        border-collapse: collapse;
    }

    th, td {
        border: 1px solid #ccc;
        padding: 5px;
        text-align: center;
        min-width: 40px;
        box-sizing: border-box;
    }

    th {
        background-color: yellow;
        text-wrap: nowrap;
    }

    th.inverseheader {
        position: -webkit-sticky; /* for Safari */
        position: sticky;
        left: 0;
        background: yellow;
        z-index: 2; /* make sure the header is on top */
    }
    button {
        background-color: #007BFF;
        color: white;
        border: none;
        width: fit-content;
        padding: 5px 10px;
        font-size: 16px;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    }

    button:hover {
        background-color: #0056b3;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        outline: none;
    }
</style>
