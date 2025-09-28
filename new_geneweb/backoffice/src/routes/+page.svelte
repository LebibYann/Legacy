<script lang="ts">
	import { onMount } from 'svelte';
	import { pageTitle } from '$lib/stores/pageStore';
	import DefaultList from '$components/DefaultList.svelte';
	import Section from '$components/Section.svelte';
	import LanguageSelector from '$components/LanguageSelector.svelte';
	import { rm } from '$utils/reactiveMessages.svelte';
	import Link from '$components/Link.svelte';

	// Set the page title when this component mounts
	$effect(() => {
		pageTitle.set(rm.homepage_title());
	});
	onMount(() => {
		pageTitle.set(rm.homepage_title());
	});
</script>

{#snippet geneweb()}
	<text class="font-bold text-lime-800">GeneWeb</text>
{/snippet}

<Section>
	{#snippet main()}
		<div class="flex justify-center">
			<div
				class="\ \ text-align-left \ mb-7
    flex max-w-4xl flex-2 flex-col
    overflow-auto rounded-md border-2
    border-blue-300 p-2 lg:flex-row"
			>
				<div class="lg:pr-35">
					<DefaultList title={rm.list_consult()}>
						{#snippet main()}
							<li>{rm.consult_list()} (<Link href="/list" title="list" />)</li>
							<li>{rm.consult_errors()} (<Link href="/errors" title="errors" />)</li>
						{/snippet}
					</DefaultList>
					<DefaultList title={rm.list_save()}>
						{#snippet main()}
							<li>
								{rm.save_gedcom()} (<Link href="/export/gedcom" title="gwb2ged" />)
							</li>
							<li>
								{rm.save_gwb_start()}
								{@render geneweb()}
								{rm.save_gwb_end()} (<Link href="/export/gwb" title="gwu" />
							</li>
						{/snippet}
					</DefaultList>
				</div>
				<div>
					<DefaultList title={rm.list_create()}>
						{#snippet main()}
							<li>
								{rm.create_gedcom()} (<Link href="/import/gedcom" title="ged2gwb" />)
							</li>
							<li>
								{rm.create_gwb_start()}
								{@render geneweb()}
								{rm.create_gwb_end()} (<Link href="/import/gwb" title="gwc" />
							</li>
							<li>{rm.create_empty()} (<Link href="/new-db" title="gwc" /></li>
						{/snippet}
					</DefaultList>
				</div>
			</div>
		</div>
	{/snippet}
</Section>
<Section>
	{#snippet main()}
		<div>
			<div style="float:left;">
				<DefaultList title={rm.list_advanced_options()}>
					{#snippet main()}
						<li>{rm.ao_cleanup()} (<Link href="/cleanup" title="cleanup" /></li>
						<li>{rm.ao_rename()} (<Link href="/rename" title="rename" /></li>
						<li>{rm.ao_delete()} (<Link href="/delete" title="delete" /></li>
						<li>{rm.ao_merge()} (<Link href="/merge" title="merge" /></li>
						<li>{rm.ao_restore()} (<Link href="/save" title="gwu" /></li>
						<li>{rm.ao_consang()} (<Link href="/consang" title="consang" /></li>
						<li>{rm.ao_update()} (<Link href="/update-nldb" title="update_nldb" /></li>
						<li>{rm.ao_compute()} (<Link href="/connex" title="connex" /></li>
						<li>{rm.ao_compute_diff()} (<Link href="/gwdiff" title="gwdiff" /></li>
						<li>{rm.ao_fix()} (<Link href="/gwfix" title="gwfixbase" /></li>
					{/snippet}
				</DefaultList>
				<ul></ul>
			</div>
			<div style="float:left;">
				<DefaultList title={rm.list_configure()}>
					{#snippet main()}
						<li>{rm.config_db_param()} (<Link href="/gwf" title=".gwf" /></li>
						<li>{rm.config_front_param()} (<Link href="/gwd" title="gwd" /></li>
						<li>{rm.config_cache()} (<Link href="/cache-files" title="cache_files" /></li>
					{/snippet}
				</DefaultList>
			</div>
		</div>
		<p style="clear:both"></p>
		<p>
			{rm.doc()}
			{@render geneweb()}. (<a
				href="http://geneweb.tuxfamily.org/wiki/manual"
				target="_blank"
				rel="external">doc</a
			>)
			<br /><br />
		</p>
		<LanguageSelector />
		<br />
	{/snippet}
</Section>
