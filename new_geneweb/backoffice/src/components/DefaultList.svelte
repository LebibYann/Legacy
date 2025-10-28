<script lang="ts">
	import type { Snippet } from 'svelte';

	interface DefaultListProps {
		main: Snippet<[]>;
		title: string;
	}

	const { main, title }: DefaultListProps = $props();
</script>

<div class="pb-3">
	<span class="font-bold">{title}</span>
	<ul class="pt-3">
		{@render main?.()}
	</ul>
</div>
