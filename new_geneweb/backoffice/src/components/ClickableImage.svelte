<script lang="ts">
    interface ClickableImageProps {
        href: string;
        aria_label: string;
        src: string;
        alt: string;
    }

    const {
        href,
        aria_label,
        src,
        alt
    }: ClickableImageProps = $props();
</script>

<a href={href} aria-label={aria_label}>
    <img src={src} style="border:0" alt={alt}>
</a>