<script lang="ts">
	interface ClickableImageProps {
		href: string;
		aria_label: string;
		src: string;
		alt: string;
	}

	const { href, aria_label, src, alt }: ClickableImageProps = $props();
</script>

<a {href} aria-label={aria_label}>
	<img {src} style="border:0" {alt} />
</a>
