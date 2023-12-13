<script>
    import { onMount } from 'svelte';
    import de from './locales/de.json';

    let slides = de;
    let refs = [];

    onMount(() => {
        console.log(slides.length)
    });

    function scrollToSlide({ target }) {
        const el = document.querySelector(target.getAttribute('href'));
		if (!el) return;
        el.scrollIntoView({
            behavior: 'smooth'
        });
    }
</script>

<body>
    {#each slides as slide}
        <section id="slide-{slide.id}">
            <h2>{slide.title}</h2>
            <div>{@html slide.content}</div>
            {#if slide.id < slides.length}
                <a href="#slide-{slide.id+1}" on:click|preventDefault={scrollToSlide}>Next</a>
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