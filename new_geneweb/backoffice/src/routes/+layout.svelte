<script lang="ts">
	import '$/app.css';
	import { onMount } from "svelte";
	import favicon from '$lib/assets/favicon.svg';
	import Footer from '$components/Footer.svelte';
	import Header from '$components/Header.svelte';
	import { detectAndSetBrowserLanguage, switchLanguage, onLanguageChange } from "$utils/languageDetection";

    onMount(() => {
        detectAndSetBrowserLanguage();
    });

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<Header />
{@render children?.()}
<Footer />
