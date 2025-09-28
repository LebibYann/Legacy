<script lang="ts">
    import { onMount } from "svelte";
    import { switchLanguage } from "$utils/languageDetection";
    import { rm } from '$utils/reactiveMessages.svelte';

</script>

<div style="float: left; align: center;">
    <span>{rm.display_in()}</span>
    <button on:click={() => {switchLanguage("co")}}>Corsu</button>
    <button on:click={() => {switchLanguage("de")}}>Deutsch</button>
    <button on:click={() => {switchLanguage("en")}}>English</button>
    <button on:click={() => {switchLanguage("es")}}>Español</button>
    <button on:click={() => {switchLanguage("fr")}}>Français</button>
    <button on:click={() => {switchLanguage("it")}}>Italiano</button>
    <button on:click={() => {switchLanguage("lv")}}>Latviesu</button>
    <button on:click={() => {switchLanguage("sv")}}>Svenska</button>
</div>