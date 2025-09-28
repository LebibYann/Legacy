<script lang="ts">
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';
	import type { Route } from './$types';

	interface AProps {
		title: string;
		href: string;
	}

	const { title, href }: AProps = $props();
</script>

<a {href} onclick={() => goto(resolve(href as Route))}>{title}</a>
