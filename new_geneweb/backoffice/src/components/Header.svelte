<script lang="ts">
    import "$/app.css"
    import { onMount } from 'svelte';
    import { pageTitle } from '$lib/stores/pageStore';
    import ClickableImage from './ClickableImage.svelte';
	import { page } from "$app/state";


    let headerRef: HTMLElement | undefined;
    let logoRef: HTMLElement | undefined;
    let titleRef: HTMLElement | undefined = $state(undefined);
    let isStacked = $state(false);

    const checkOverlap = () => {
        if (headerRef && logoRef && titleRef) {
            const headerWidth = headerRef.clientWidth;
            const logoWidth = logoRef.clientWidth;
            const titleWidth = titleRef.clientWidth; // Use scrollWidth to get full text width
            isStacked = (logoWidth + titleWidth / 2) * 2.1 >= headerWidth;
        }
    };

    $effect(() => {
        if (titleRef && $pageTitle) {
            checkOverlap();
        }
    });

    onMount(() => {

        // Initial check
        checkOverlap();

        // Also listen for window resize as backup
        window.addEventListener('resize', checkOverlap);

        // Cleanup
        return () => {
            window.removeEventListener('resize', checkOverlap);
        };
    });
</script>

<header bind:this={headerRef} class={"flex " +
(isStacked ? "flex-col justify-between" : "flex-row items-center")}>
    <div bind:this={logoRef} class="w-fit">
        <ClickableImage
            href="/"
            aria_label="Go back to homepage"
            src="images/gwlogo.png"
            alt="GeneWeb logo"
        />
    </div>
    <h1 bind:this={titleRef}
     class={"text-lime-800 w-fit " +
     (isStacked ? "mx-auto" : "absolute left-1/2 transform -translate-x-1/2 whitespace-nowrap")
     }>{$pageTitle}</h1>
</header>