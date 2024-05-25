<script>
    import { title } from '$lib/title';
    import { backLink } from '$lib/title'
    import { pageTitle } from '$lib/stores.js';
    import { writable, derived } from 'svelte/store';

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
    console.log(data);

    let p = data.body.p;
    let a = data.body.a;
    let b = data.body.b;

    let m = data.body.practice_points[0]
    let n = data.body.practice_points[1]
    let o = data.body.practice_points[2]

    let inverses = data.body.inverse_table;
    let inverseTableRows = chunkArray(inverses, 10);

    console.log(inverseTableRows);




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

</script>

<body>
    <div class="bodycontainer">
        <div class="questions">
        <p>{@html translation.given}{a}{@html translation.given2}{b} {translation.given3} <span class="zdings">&#8484;</span><sub>{p}</sub></p>
        {#if $stepDetails.showCurveCheck}
            <div class="questioncontainer">
                <p>{translation.curvecheck}</p>
                {translation.curvecheckresult} <input class="answerinput" type="number">
            </div>
        {/if}
        {#if $stepDetails.showPointCheck}
            <div class="questioncontainer">
                <p>{translation.pointcheck}(x, y) {translation.pointcheck2}</p>
                {translation.pointcheckresult} <input class="answerinput" type="number">
            </div>
        {/if}
        {#if $stepDetails.showCalculation}
            <div class="questioncontainer">
                <p>{translation.calculation} {m}{translation.calculation2}(x, y) {translation.calculation3} {n}{translation.calculation4}(x, y) {translation.calculation5} {o}{translation.calculation6}</p>
                S(<input class="answerinput" type="number">, <input class="answerinput" type="number">)
            </div>
        {/if}
        {#if $stepDetails.showInversion}
            <div class="questioncontainer">
                <p>{translation.inversion}(x,y) {translation.inversion2}</p>
                U(<input class="answerinput" type="number">, <input class="answerinput" type="number">)
            </div>
        {/if}
        {#if $stepDetails.showEstimation}
            <div class="questioncontainer">
                {translation.estimation}
            </div>
        {/if}
        <button on:click={nextStep}>{translation.next}</button>
        </div>
        <div class="inversiontable">
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
    .bodycontainer {
        margin-top: 80px;
        display: flex;
        flex-direction: row;
    }

    .questions {
        display: flex;
        flex-direction: column;
        gap: 20px;
        width: 250px;
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
        max-width: 500px; /* adjust this value as needed */
    }

    table {
        border-collapse: collapse;
    }

    th, td {
        border: 1px solid #ccc;
        padding: 5px;
        text-align: center;
        min-width: 40px; /* adjust this value as needed */
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
</style>
