<script lang="ts">
    import type { Snippet } from "svelte";

    interface SectionProps {
        main: Snippet<[]>;
    }

    const {
        main
    }: SectionProps = $props();
</script>

<section class="pt-5 flex flex-col">
    {@render main?.() }
    <hr class="mt-2">
</section>