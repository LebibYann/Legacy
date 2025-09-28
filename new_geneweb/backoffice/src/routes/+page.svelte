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
  <div class="max-w-4xl mx-auto p-2 mb-7 \
  border-2 border-blue-300 rounded-md \
  text-align-left overflow-auto \
  flex justify-between flex-col md:flex-row">
    <div>
      <DefaultList title={rm.list_consult()}>
        {#snippet main()}
        <li>{rm.consult_list()} (<a href="gwsetup?lang=en;v=list.htm">list</a>)</li>
        <li>{rm.consult_errors()} (<a href="gwsetup?lang=en;v=traces.htm">errors</a>)</li>
        {/snippet}
      </DefaultList>
      <DefaultList title={rm.list_save()}>
        {#snippet main()}
        <li>{rm.save_gedcom()} (<a href="gwsetup?lang=en;v=gwb2ged.htm">gwb2ged</a>)</li>
        <li>{rm.save_gwb_start()} {@render geneweb()} {rm.save_gwb_end()} (<a href="gwsetup?lang=en;v=gwu.htm">gwu</a>)</li>
        {/snippet}
      </DefaultList>
    </div>
    <div class="pr-5">
      <DefaultList title={rm.list_create()}>
        {#snippet main()}
        <li>{rm.create_gedcom()} (<a href="gwsetup?lang=en;v=ged2gwb.htm">ged2gwb</a>)</li>
        <li>{rm.create_gwb_start()} {@render geneweb()} {rm.create_gwb_end()} (<a href="gwsetup?lang=en;v=gwc.htm">gwc</a>)</li>
        <li>{rm.create_empty()} (<a href="gwsetup?lang=en;v=simple.htm">gwc</a>)</li>
        {/snippet}
      </DefaultList>
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
        <li>{rm.ao_cleanup()} (<a href="gwsetup?lang=en;v=cleanup.htm">cleanup</a>)</li>
        <li>{rm.ao_rename()} (<a href="gwsetup?lang=en;v=rename.htm">rename</a>)</li>
        <li>{rm.ao_delete()} (<a href="gwsetup?lang=en;v=delete.htm">delete</a>)</li>
        <li>{rm.ao_merge()} (<a href="gwsetup?lang=en;v=merge.htm">merge</a>)</li>
        <li>{rm.ao_restore()} (<a href="gwsetup?lang=en;v=save.htm">gwu</a>)</li>
        <li>{rm.ao_consang()} (<a href="gwsetup?lang=en;v=consang.htm">consang</a>)</li>
        <li>{rm.ao_update()} (<a href="gwsetup?lang=en;v=update_nldb.htm">update_nldb</a>)</li>
        <li>{rm.ao_compute()} (<a href="gwsetup?lang=en;v=connex.htm">connex</a>)</li>
        <li>{rm.ao_compute_diff()} (<a href="gwsetup?lang=en;v=gwdiff.htm">gwdiff</a>)</li>
        <li>{rm.ao_fix()} (<a href="gwsetup?lang=en;v=gwfix.htm">gwfixbase</a>)</li>
        {/snippet}
      </DefaultList>
      <ul>
        </ul>
    </div>
    <div style="float:left;">
      <DefaultList title={rm.list_configure()}>
        {#snippet main()}
        <li>{rm.config_db_param()} (<a href="gwsetup?lang=en;v=gwf.htm">.gwf</a>)</li>
        <li>{rm.config_front_param()} (<a href="gwd?lang=en;v=gwd.htm">gwd</a>)</li>
        <li>{rm.config_cache()} (<a href="gwsetup?lang=en;v=cache_files.htm">cache_files</a>)</li>
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