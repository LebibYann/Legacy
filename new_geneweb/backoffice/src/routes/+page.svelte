<script lang="ts">
	import { onMount } from 'svelte';
	import { pageTitle } from '$lib/stores/pageStore';
	import DefaultList from '$components/DefaultList.svelte';
	import Section from '$components/Section.svelte';
	import LanguageSelector from '$components/LanguageSelector.svelte';
	import { rm } from '$utils/reactiveMessages.svelte';
	import Link from '$components/Link.svelte';
	import { makeLegacyUrl } from '$utils/legacyUrl';
	import { onLanguageChange } from '$utils/languageDetection';
	import { getLocale } from '$lib/paraglide/runtime.js';

	let lang: string = $state(getLocale());

	onLanguageChange(() => {
		lang = getLocale();
	});

	// Set the page title when this component mounts
	$effect(() => {
		pageTitle.set(rm.homepage_title());
	});
	onMount(() => {
		pageTitle.set(rm.homepage_title());
	});
</script>

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
							<li>
								{rm.consult_list()} (<Link href="/list" title="list" />)
							</li>
							<li>
								{rm.consult_errors()} (<Link
									href={makeLegacyUrl({ lang: lang, v: 'traces.htm' })}
									title="errors"
								/>)
							</li>
						{/snippet}
					</DefaultList>
					<DefaultList title={rm.list_save()}>
						{#snippet main()}
							<li>
								{rm.save_gedcom()} (<Link
									href={makeLegacyUrl({ lang: lang, v: 'gwb2ged.htm' })}
									title="gwb2ged"
								/>)
							</li>
							<li>
								{rm.save_gwb_start()}
								<text class="font-bold text-lime-800">GeneWeb</text>
								{rm.save_gwb_end()} (<Link
									href={makeLegacyUrl({ lang: lang, v: 'gwu.htm' })}
									title="gwu"
								/>)
							</li>
						{/snippet}
					</DefaultList>
				</div>
				<div>
					<DefaultList title={rm.list_create()}>
						{#snippet main()}
							<li>
								{rm.create_gedcom()} (<Link
									href={makeLegacyUrl({ lang: lang, v: 'ged2gwb.htm' })}
									title="ged2gwb"
								/>)
							</li>
							<li>
								{rm.create_gwb_start()}
								<text class="font-bold text-lime-800">GeneWeb</text>
								{rm.create_gwb_end()} (<Link
									href={makeLegacyUrl({ lang: lang, v: 'gwc.htm' })}
									title="gwc"
								/>)
							</li>
							<li>
								{rm.create_empty()} (<Link
									href={makeLegacyUrl({ lang: lang, v: 'simple.htm' })}
									title="gwc"
								/>)
							</li>
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
						<li>
							{rm.ao_cleanup()} (<Link
								href={makeLegacyUrl({ lang: lang, v: 'cleanup.htm' })}
								title="cleanup"
							/>)
						</li>
						<li>
							{rm.ao_rename()} (<Link
								href={makeLegacyUrl({ lang: lang, v: 'rename.htm' })}
								title="rename"
							/>)
						</li>
						<li>
							{rm.ao_delete()} (<Link
								href={makeLegacyUrl({ lang: lang, v: 'delete.htm' })}
								title="delete"
							/>)
						</li>
						<li>
							{rm.ao_merge()} (<Link
								href={makeLegacyUrl({ lang: lang, v: 'merge.htm' })}
								title="merge"
							/>)
						</li>
						<li>
							{rm.ao_restore()} (<Link
								href={makeLegacyUrl({ lang: lang, v: 'save.htm' })}
								title="gwu"
							/>)
						</li>
						<li>
							{rm.ao_consang()} (<Link
								href={makeLegacyUrl({ lang: lang, v: 'consang.htm' })}
								title="consang"
							/>)
						</li>
						<li>
							{rm.ao_update()} (<Link
								href={makeLegacyUrl({ lang: lang, v: 'update_nldb.htm' })}
								title="update_nldb"
							/>)
						</li>
						<li>
							{rm.ao_compute()} (<Link
								href={makeLegacyUrl({ lang: lang, v: 'connex.htm' })}
								title="connex"
							/>)
						</li>
						<li>
							{rm.ao_compute_diff()} (<Link
								href={makeLegacyUrl({ lang: lang, v: 'gwdiff.htm' })}
								title="gwdiff"
							/>)
						</li>
						<li>
							{rm.ao_fix()} (<Link
								href={makeLegacyUrl({ lang: lang, v: 'gwfix.htm' })}
								title="gwfixbase"
							/>)
						</li>
					{/snippet}
				</DefaultList>
				<ul></ul>
			</div>
			<div style="float:left;">
				<DefaultList title={rm.list_configure()}>
					{#snippet main()}
						<li>
							{rm.config_db_param()} (<Link
								href={makeLegacyUrl({ lang: lang, v: 'gwf.htm' })}
								title=".gwf"
							/>)
						</li>
						<li>
							{rm.config_front_param()} (<Link
								href={makeLegacyUrl({ lang: lang, v: 'gwd.htm' })}
								title="gwd"
							/>)
						</li>
						<li>
							{rm.config_cache()} (<Link
								href={makeLegacyUrl({ lang: lang, v: 'cache_files.htm' })}
								title="cache_files"
							/>)
						</li>
					{/snippet}
				</DefaultList>
			</div>
		</div>
		<p style="clear:both"></p>
		<p>
			{rm.doc()}
			<text class="font-bold text-lime-800">GeneWeb</text>. (<a
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
