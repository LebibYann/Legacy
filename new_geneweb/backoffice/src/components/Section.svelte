<script lang="ts">
	import type { Snippet } from 'svelte';

	interface SectionProps {
		main: Snippet<[]>;
	}

	const { main }: SectionProps = $props();
</script>

<section class="flex flex-col pt-5">
	{@render main?.()}
	<hr class="mt-2" />
</section>
