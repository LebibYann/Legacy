<script lang="ts">
    import "$/app.css"
    import { pageTitle } from '$lib/stores/pageStore';
    import ClickableImage from './ClickableImage.svelte';
</script>

<header class="flex flex-col justify-between lg:flex-row lg:items-center">
    <ClickableImage
        href="/"
        aria_label="Go back to homepage"
        src="images/gwlogo.png"
        alt="GeneWeb logo"
    />
    <h1 class="text-lime-800 mx-auto">{$pageTitle}</h1>
    <div></div>
</header>