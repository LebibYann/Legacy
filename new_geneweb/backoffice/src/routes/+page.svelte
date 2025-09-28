<script lang="ts">
  import { onMount } from 'svelte';
  import { pageTitle } from '$lib/stores/pageStore';
  import DefaultList from "$components/DefaultList.svelte";
  import Section from "$components/Section.svelte";
  import LanguageSelector from "$components/LanguageSelector.svelte";
	import { rm } from "$utils/reactiveMessages.svelte"

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
    <div class="max-w-4xl p-2 mb-7 flex-2 \
    border-2 border-blue-300 rounded-md \
    text-align-left overflow-auto \
    flex flex-col lg:flex-row">
      <div class="lg:pr-35">
        <DefaultList title={rm.list_consult()}>
          {#snippet main()}
          <li>{rm.consult_list()} (<a href="/list">list</a>)</li>
          <li>{rm.consult_errors()} (<a href="/errors">errors</a>)</li>
          {/snippet}
        </DefaultList>
        <DefaultList title={rm.list_save()}>
          {#snippet main()}
          <li>{rm.save_gedcom()} (<a href="/export/gedcom">gwb2ged</a>)</li>
          <li>{rm.save_gwb_start()} {@render geneweb()} {rm.save_gwb_end()} (<a href="/export/gwb">gwu</a>)</li>
          {/snippet}
        </DefaultList>
      </div>
      <div>
        <DefaultList title={rm.list_create()}>
          {#snippet main()}
          <li>{rm.create_gedcom()} (<a href="/import/gedcom">ged2gwb</a>)</li>
          <li>{rm.create_gwb_start()} {@render geneweb()} {rm.create_gwb_end()} (<a href="/import/gwb">gwc</a>)</li>
          <li>{rm.create_empty()} (<a href="/new_db">gwc</a>)</li>
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
        <li>{rm.ao_cleanup()} (<a href="/cleanup">cleanup</a>)</li>
        <li>{rm.ao_rename()} (<a href="/rename">rename</a>)</li>
        <li>{rm.ao_delete()} (<a href="/delete">delete</a>)</li>
        <li>{rm.ao_merge()} (<a href="/merge">merge</a>)</li>
        <li>{rm.ao_restore()} (<a href="/save">gwu</a>)</li>
        <li>{rm.ao_consang()} (<a href="/consang">consang</a>)</li>
        <li>{rm.ao_update()} (<a href="/update_nldb">update_nldb</a>)</li>
        <li>{rm.ao_compute()} (<a href="/connex">connex</a>)</li>
        <li>{rm.ao_compute_diff()} (<a href="/gwdiff">gwdiff</a>)</li>
        <li>{rm.ao_fix()} (<a href="/gwfix">gwfixbase</a>)</li>
        {/snippet}
      </DefaultList>
      <ul>
        </ul>
    </div>
    <div style="float:left;">
      <DefaultList title={rm.list_configure()}>
        {#snippet main()}
        <li>{rm.config_db_param()} (<a href="/gwf">.gwf</a>)</li>
        <li>{rm.config_front_param()} (<a href="/gwd">gwd</a>)</li>
        <li>{rm.config_cache()} (<a href="/cache_files">cache_files</a>)</li>
        {/snippet}
      </DefaultList>
    </div>
  </div>
  <p style="clear:both"></p>
  <p>{rm.doc()} {@render geneweb()}. (<a href="http://geneweb.tuxfamily.org/wiki/manual" target="_blank">doc</a>)
  <br><br></p>
  <LanguageSelector />
  <br>
  {/snippet}
</Section>