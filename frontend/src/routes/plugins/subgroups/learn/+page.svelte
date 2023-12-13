<script>
    import { onMount } from 'svelte';
    import de from './locales/de.json';

    let slides = de;
    let refs = [];

    onMount(() => {
        console.log(slides)
        refs = Array(slides.length).fill(slides);
        console.log(refs)
    });

    function scrollToSlide(index) {
        console.log(index)
        const element = refs[index];
        if (element) {
            element.scrollIntoView({ behavior: 'smooth' });
        }
    }
</script>

<body>
    {#each slides as slide, index (slide.id)}
        <section bind:this={refs[index]}>
            <h2>{slide.title}</h2>
            <div>{@html slide.content}</div>
            {#if index < slides.length - 1}
                <button on:click={() => scrollToSlide(index + 1)}>Next</button>
            {/if}
        </section>
    {/each}
</body>

<style>
    body {
        margin-top: 10%;
    }
    section {
        min-height: 100vh;
        padding: 20px;
        /* Add more styling as needed */
    }
</style>