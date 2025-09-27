<script lang="ts">

  import Footer from "$components/Footer.svelte"
</script>

<style>
* {
  font-family:-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif, Apple Color Emoji, Segoe UI Emoji, Segoe UI Symbol;
}

pre {
  font-family: monospace;
}

a.j {
  font-family: monospace;
}

table.setup {
  border:1px solid;
  border-radius:4px;
  border-color:#5bc0de;
}

div.welcome {
  width: 830px;
  border: solid 2px #5bc0de;
  border-radius:6px;
  text-align: left;
  overflow: auto;
  margin-left: auto;
  margin-right: auto;
  padding:5px;
}
</style>


<div style="background:url('images/gwlogo.png') no-repeat left top;
  text-align:center; height:95px; line-height:95px; color:#2f6400;">
<h1 style="margin:0;">Management and creation</h1>
</div>
<p>
</p><div class="welcome">
  <div style="float:left; width:50%">
    <div>
      <span style="font-weight:bold">Consult</span>
      <ul>
        <li>family Trees (<a href="gwsetup?lang=en;v=list.htm">list</a>)
        </li><li>the error history and statistics (<a href="gwsetup?lang=en;v=traces.htm">errors</a>)
      </li></ul>
    </div>
    <div>
      <span style="font-weight:bold">Save</span>
      <ul>
        <li>a GEDCOM source file (<a href="gwsetup?lang=en;v=gwb2ged.htm">gwb2ged</a>)
        </li><li>a <b><font color="#2f6400">GeneWeb</font></b> source file (<a href="gwsetup?lang=en;v=gwu.htm">gwu</a>)
      </li></ul>
    </div>
  </div>
  <div style="float:left; width:50%;">
    <span style="font-weight:bold;">Create Family Tree</span>
    <ul>
      <li>from a GEDCOM source file (<a href="gwsetup?lang=en;v=ged2gwb.htm">ged2gwb</a>)
      </li><li>from a GeneWeb source file (<a href="gwsetup?lang=en;v=gwc.htm">gwc</a>)
      </li><li>from an empty file (<a href="gwsetup?lang=en;v=simple.htm">gwc</a>)
    </li></ul>
  </div>
</div>
<br><hr><br>
<div>
  <div style="float:left;">
    <span><b>Advanced Options</b></span>
    <ul>
      <li>Clean up (<a href="gwsetup?lang=en;v=cleanup.htm">cleanup</a>)
      </li><li>Renaming (<a href="gwsetup?lang=en;v=rename.htm">rename</a>)
      </li><li>Deletion (<a href="gwsetup?lang=en;v=delete.htm">delete</a>)
      </li><li>Merging with other databases (<a href="gwsetup?lang=en;v=merge.htm">merge</a>)
      </li><li>Saving and restoring (<a href="gwsetup?lang=en;v=save.htm">gwu</a>)
      </li><li>initialisation of consanguinities (<a href="gwsetup?lang=en;v=consang.htm">consang</a>)
      </li><li>Update links page / family chronicle (<a href="gwsetup?lang=en;v=update_nldb.htm">update_nldb</a>)
      </li><li>Compute connected componants (<a href="gwsetup?lang=en;v=connex.htm">connex</a>)
      </li><li>Compute the difference between two bases (<a href="gwsetup?lang=en;v=gwdiff.htm">gwdiff</a>)
      </li><li>Fixes problems in a base (<a href="gwsetup?lang=en;v=gwfix.htm">gwfixbase</a>)
    </li></ul>
  </div>
  <div style="float:left;">
    <span><b>Configure</b></span>
    <ul>
      <li>The parameters of a database (<a href="gwsetup?lang=en;v=gwf.htm">.gwf</a>)
      </li><li>The parameters of the gwd service (<a href="gwd?lang=en;v=gwd.htm">gwd</a>)
      </li><li>Name and places cache files for auto completion. (<a href="gwsetup?lang=en;v=cache_files.htm">cache_files</a>)
    </li></ul>
  </div>
</div>
<p style="clear:both">
</p><p>
You can also consult the complete documentation of <b><font color="#2f6400">GeneWeb</font></b>. (<a href="http://geneweb.tuxfamily.org/wiki/manual" target="_blank">doc</a>)
<br><br>
</p><div style="float: left; align: center;">
  <span>Display in:</span>
  <a href="co">Corsu</a>
  <a href="de">Deutsch</a>
  <a href="en">English</a>
  <a href="es">Español</a>
  <a href="fr">Français</a>
  <a href="it">Italiano</a>
  <a href="lv">Latviesu</a>
  <a href="sv">Svenska</a>
</div>
<br>