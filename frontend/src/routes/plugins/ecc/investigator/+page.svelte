<script>
    import { title } from '$lib/title';
    import { backLink } from '$lib/title'
    import { pageTitle } from '$lib/stores.js';
    import { slide } from 'svelte/transition';
    import { quintOut } from 'svelte/easing';

    import '../../../../style/globalStyle.css';
  
    import de from './locales/de.json';
    import en from './locales/en.json';

    $: a = 'a';
    $: b = 'b';
    $: p = 'p';
  
    import { language } from '$lib/language';

	import Points from '$lib/ecctabs/Points.svelte';
    import Tabs from '$lib/Tabs.svelte';

    let translation;
    $: {
        translation = $language === 'en' ? en : de;
        title.set(translation.title);
        backLink.set('/plugins/ecc');
        pageTitle.set(translation.subpagetitle);
    }

    function handleInput(event) {
        const { name, value } = event.target;
        if (value === "") {
            // Reset to default if input is empty
            if (name === "a") a = 'a';
            if (name === "b") b = 'b';
            if (name === "p") p = 'p';
        } else {
            // Update variable with input value
            if (name === "a") a = value;
            if (name === "b") b = value;
            if (name === "p") p = value;
        }
        // if all are set, investigate curve
        if (a !== 'a' && b !== 'b' && p !== 'p') {
            investigate_curve(a, b, p);
        }
    }

    $: isElliptic = false;
    $: isCyclic = false;
    $: allPoints = [];
    $: allPositivePoints = [];
    $: allPrimitivePoints = [];
    $: curveOrder = 0;
    $: calculationdetails = {};
    $: detailsArray = [];
    $: notElliptic = "";
    $: ellipticReason = "";
    $: infinityX = 0;

    $: {
        if (!isElliptic) {
            if (notElliptic === "singular") {
                ellipticReason = translation.singular;
            }
            if (notElliptic === "nonprime") {
                ellipticReason = translation.nonprime;
            }
        }
    }
    
    let curveLoaded = false;

    let activeTab = 0;

    async function investigate_curve(a, b, p) {
        const payload = JSON.stringify({
                "a": a,
                "b": b,
                "p": p
            });
        const response = await fetch('/backend/ecc/investigate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: payload
        })

        const curve = await response.json();
        console.log(curve);
        isElliptic = curve.is_elliptic;
        isCyclic = curve.is_cyclic;
        allPoints = curve.all_points;
        allPositivePoints = curve.positive_points;
        allPrimitivePoints = curve.primitive_points;
        curveOrder = curve.order;
        calculationdetails = curve.calculation_info;
        notElliptic = curve.not_elliptic;
        infinityX = curve.infinity;
        // clear array first duh
        detailsArray = [];
        for (let key in calculationdetails) {
            const keyTuple = key.replace(/[()]/g, '').split(',').map(Number);
            detailsArray.push({ key: keyTuple, value: calculationdetails[key] });
        }
        curveLoaded = true;
    }

    async function get_random_curve() {
        const response = await fetch('/backend/ecc/random', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        });

        if (response.ok) {
            const curve = await response.json();
            a = curve.a;
            b = curve.b;
            p = curve.p;
            investigate_curve(a, b, p);
        } else {
            console.error('Failed to fetch random curve:', response.statusText);
        }
    }

    function get_cyclic_curve() {

    }
    
    $: tabs = [
    { label: translation.allpoints,
		 value: 1,
		 component: Points,
         props: {points: allPoints, infinity: infinityX, translation: translation}
		},
    { label: translation.positivepoints,
		 value: 2,
		 component: Points,
         props: {points: allPositivePoints, infinity: infinityX, translation: translation}
		},
    { label: translation.primitivepoints,
		 value: 3,
		 component: Points,
         props: {points: allPrimitivePoints, infinity: infinityX, translation: translation}
		}
  ];

    function handleTabChange(event) {
        activeTab = event.detail.tabValue;
    }
  </script>

<body>
    <div class="bodycontainer">
        <div class="formula">
            {translation.formula} <span class="zdings">&#8484;</span><sub>{p}</sub>:
            <br>
            y<sup>2</sup> mod {p} &equiv; x<sup>3</sup> + {a}x + {b} mod {p}
        </div>
        <div class="curveform">
            <div class="inputs">
                <div class="inputfields">
                    <div class="inputfield ecc-a">
                        <label for="a">a=</label>
                        <input type="number" id="a" name="a" on:input={handleInput} bind:value={a}>
                    </div>
                    <div class="inputfield ecc-b">
                        <label for="b">b=</label>
                        <input type="number" id="b" name="b" on:input={handleInput} bind:value={b}>
                    </div>
                    <div class="inputfield ecc-p">
                        <label for="p">p=</label>
                        <input type="number" id="p" name="p" on:input={handleInput} bind:value={p}>
                    </div>
                </div>
            </div>
            <div class="randombuttons">
                <button on:click={get_random_curve}>{translation.random}</button>
            </div>
        </div>
        {#if curveLoaded}
        <div class="investigator" transition:slide={{ delay: 250, duration: 1000, easing: quintOut, axis: 'y'}}>
            <div class="curveinfo">
                <div class="elliptic">
                    {@html isElliptic ? translation.elliptic_true : translation.elliptic_false}
                    {#if !isElliptic}
                        {ellipticReason}
                    {/if}
                </div>
                {#if isElliptic}
                <div class="order">
                    {translation.order}: {curveOrder}
                </div>
                {/if}
            </div>
            {#if isElliptic}
            <div class="tabscontainer">
                <div class="tabs" transition:slide={{ delay: 250, duration: 1000, easing: quintOut, axis: 'y'}}>
                    <Tabs {tabs} on:tabChange={handleTabChange}/>
                </div>
                {#if activeTab == 3}
                <div class="details" transition:slide={{ delay: 250, duration: 1000, easing: quintOut, axis: 'x'}}>
                    <div class="detailstitle">
                        {translation.calculationdetails}
                    </div>
                    <div class="calculationdetails scrollbox">
                        {#each detailsArray as detail}
                            <div class="detail-box">
                                <strong>{translation.details_one} ({detail.key[0]}, {detail.key[1]}){translation.details_two}:</strong><br>
                                {#each detail.value as point, pointIndex}
                                    {translation.steplabel} {pointIndex+1}: ({point[0]}, {point[1]})<br>
                                {/each}
                            </div>
                        {/each}
                    </div>
                </div>
                {/if}
            </div>
            {/if}
        </div>
        {/if}
    </div>
</body>

<style>
    .bodycontainer {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 60px;
        gap: 20px;
    }
    
    .tabscontainer {
        display: flex;
        flex-direction: row;
    }

    .calculationdetails {
        width: 240px;
        max-height: 300px;
        overflow-y: scroll;
        border: 1px solid #ccc;
        padding: 10px;
        box-sizing: border-box;
        border-radius: 0 8px 8px 0;
    }

    .detailstitle {
        font-weight: bold;
        margin-top: 85px;
        margin-left: 10px;
    }

    .detail-box {
        font-size: 0.7em;
    }

    .curveform {
        display: flex;
        flex-direction: row;
        gap: 20px;
    }

    .formula {
        text-align: center;
    }

    .zdings {
        font-size: 1.3em;
    }

    .inputfields {
        display: flex;
        flex-direction: row;
        gap: 20px;
    }

    input {
        width: 40px;
    }
</style>