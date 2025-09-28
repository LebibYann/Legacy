<script lang="ts">
    import ClickableImage from './ClickableImage.svelte';
</script>

<footer>
    <div class="flex flex-row gap-1">
        <ClickableImage
            href="https://github.com/geneweb/geneweb/"
            aria_label="Visit GeneWeb project on GitHub"
            src="images/logo_bas.png"
            alt="GeneWeb logo"
        />
        <div class="flex flex-col justify-end">
            <em>Version 0.1-beta 2025</em>
        </div>
    </div>
</footer>