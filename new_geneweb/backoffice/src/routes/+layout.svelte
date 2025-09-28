<script lang="ts">
	import '$/app.css';
	import { onMount } from "svelte";
	import favicon from '$lib/assets/favicon_gwsetup.png';
	import Footer from '$components/Footer.svelte';
	import Header from '$components/Header.svelte';
	import { detectAndSetBrowserLanguage } from "$utils/languageDetection";

    onMount(() => {
        detectAndSetBrowserLanguage();
    });

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" type="image/png" href={favicon} />
</svelte:head>

<Header />
{@render children?.()}
<Footer />
