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

<Section>
  {#snippet main()}
  <div class="max-w-4xl mx-auto p-2 mb-7 \
  border-2 border-blue-300 rounded-md \
  text-align-left overflow-auto \
  flex justify-between flex-col md:flex-row">
    <div>
      <DefaultList title="Consult">
        {#snippet main()}
        <li>family Trees (<a href="gwsetup?lang=en;v=list.htm">list</a>)</li>
        <li>the error history and statistics (<a href="gwsetup?lang=en;v=traces.htm">errors</a>)</li>
        {/snippet}
      </DefaultList>
      <DefaultList title="Save">
        {#snippet main()}
        <li>a GEDCOM source file (<a href="gwsetup?lang=en;v=gwb2ged.htm">gwb2ged</a>)</li>
        <li>a <b><font color="#2f6400">GeneWeb</font></b> source file (<a href="gwsetup?lang=en;v=gwu.htm">gwu</a>)</li>
        {/snippet}
      </DefaultList>
    </div>
    <div class="pr-5">
      <DefaultList title="Create Family Tree">
        {#snippet main()}
        <li>from a GEDCOM source file (<a href="gwsetup?lang=en;v=ged2gwb.htm">ged2gwb</a>)</li>
        <li>from a GeneWeb source file (<a href="gwsetup?lang=en;v=gwc.htm">gwc</a>)</li>
        <li>from an empty file (<a href="gwsetup?lang=en;v=simple.htm">gwc</a>)</li>
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
      <DefaultList title="Advanced Options">
        {#snippet main()}
        <li>Clean up (<a href="gwsetup?lang=en;v=cleanup.htm">cleanup</a>)</li>
        <li>Renaming (<a href="gwsetup?lang=en;v=rename.htm">rename</a>)</li>
        <li>Deletion (<a href="gwsetup?lang=en;v=delete.htm">delete</a>)</li>
        <li>Merging with other databases (<a href="gwsetup?lang=en;v=merge.htm">merge</a>)</li>
        <li>Saving and restoring (<a href="gwsetup?lang=en;v=save.htm">gwu</a>)</li>
        <li>initialisation of consanguinities (<a href="gwsetup?lang=en;v=consang.htm">consang</a>)</li>
        <li>Update links page / family chronicle (<a href="gwsetup?lang=en;v=update_nldb.htm">update_nldb</a>)</li>
        <li>Compute connected componants (<a href="gwsetup?lang=en;v=connex.htm">connex</a>)</li>
        <li>Compute the difference between two bases (<a href="gwsetup?lang=en;v=gwdiff.htm">gwdiff</a>)</li>
        <li>Fixes problems in a base (<a href="gwsetup?lang=en;v=gwfix.htm">gwfixbase</a>)</li>
        {/snippet}
      </DefaultList>
      <ul>
        </ul>
    </div>
    <div style="float:left;">
      <DefaultList title="Configure">
        {#snippet main()}
        <li>The parameters of a database (<a href="gwsetup?lang=en;v=gwf.htm">.gwf</a>)</li>
        <li>The parameters of the gwd service (<a href="gwd?lang=en;v=gwd.htm">gwd</a>)</li>
        <li>Name and places cache files for auto completion. (<a href="gwsetup?lang=en;v=cache_files.htm">cache_files</a>)</li>
        {/snippet}
      </DefaultList>
    </div>
  </div>
  <p style="clear:both"></p>
  <p>You can also consult the complete documentation of <b><font color="#2f6400">GeneWeb</font></b>. (<a href="http://geneweb.tuxfamily.org/wiki/manual" target="_blank">doc</a>)
  <br><br></p>
  <LanguageSelector />
  <br>
  {/snippet}
</Section>