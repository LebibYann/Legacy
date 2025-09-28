<script lang="ts">
	import '$/app.css';
	import { onMount } from 'svelte';
	import { pageTitle } from '$lib/stores/pageStore';
	import ClickableImage from './ClickableImage.svelte';

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

<header
	bind:this={headerRef}
	class={'flex ' + (isStacked ? 'flex-col justify-between' : 'flex-row items-center')}
>
	<div bind:this={logoRef} class="w-fit">
		<ClickableImage
			href="/"
			aria_label="Go back to homepage"
			src="images/gwlogo.png"
			alt="GeneWeb logo"
		/>
	</div>
	<h1
		bind:this={titleRef}
		class={'w-fit text-lime-800 ' +
			(isStacked ? 'mx-auto' : 'absolute left-1/2 -translate-x-1/2 transform whitespace-nowrap')}
	>
		{$pageTitle}
	</h1>
</header>
