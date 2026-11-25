<script lang="ts">
	import { onMount } from 'svelte';
	import { apiClient } from '$lib/api/client';
	import type { Base } from '$lib/api/client';
	import { pageTitle } from '$lib/stores/pageStore';
	import { rm } from '$utils/reactiveMessages.svelte';
	import Section from '$components/Section.svelte';
	import Link from '$components/Link.svelte';
	import { onLanguageChange } from '$utils/languageDetection';
	import { getLocale } from '$lib/paraglide/runtime.js';
	import { buildRelativeUrl } from '$lib/utils/url';

	let bases = $state<Base[]>([]);
	let front_port = $state(2317);
	let loading = $state(true);
	let error = $state<string | null>(null);

	let lang: string = $state(getLocale());

	onLanguageChange(() => {
		lang = getLocale();
	});

	onMount(async () => {
		pageTitle.set(rm.databases());
		try {
			const response = await apiClient.listBases();
			bases = response.bases;
			front_port = response.port;
		} catch (e) {
			console.error('Failed to fetch bases:', e);
			error = rm.failed_load_databases();
		} finally {
			loading = false;
		}
	});

	function navigateToBase(baseName: string, port: number, lang: string): string {
		// Navigate to the genealogy tree for this base
		// Automatically uses the same protocol (http or https) as the current page
		return buildRelativeUrl(port, `/${baseName}`, { lang });
	}
</script>

<svelte:head>
	<title>{rm.databases()}</title>
</svelte:head>

<Section>
	{#snippet main()}
		<p class="mb-4">
			{rm.db_consult_info()}
			(<Link href="/gwsetup?v=gwd_info.htm" title={rm.gwd_info()} />)
		</p>

		<p></p>

		{#if loading}
			<p>{rm.loading_databases()}</p>
		{:else if error}
			<p style="color: red;">{error}</p>
		{:else}
			<ul>
				{#if bases.length > 0}
					{#each bases as base (base.name)}
						<li>
							<Link href={navigateToBase(base.name, front_port, lang)} title={base.name} />
						</li>
					{/each}
				{:else}
					<li>{rm.no_database()}</li>
				{/if}
			</ul>
		{/if}

		<p></p>

		<p class="mt-4">
			{rm.back_to_menu()} (<Link href="/" title={rm.welcome()} />)
		</p>
	{/snippet}
</Section>
