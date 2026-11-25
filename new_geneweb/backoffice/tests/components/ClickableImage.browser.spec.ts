import { describe, it, expect } from 'vitest';
import { render } from 'vitest-browser-svelte';
import ClickableImage from '$components/ClickableImage.svelte';

describe('ClickableImage.svelte', () => {
	const defaultProps = {
		href: '/test-link',
		aria_label: 'Test aria label',
		src: '/test-image.jpg',
		alt: 'Test image'
	};

	it('renders with correct props', async () => {
		const { container } = render(ClickableImage, defaultProps);

		const link = container.querySelector('a');
		const image = container.querySelector('img');

		expect(link).toBeTruthy();
		expect(image).toBeTruthy();
		expect(link?.getAttribute('href')).toBe(defaultProps.href);
		expect(link?.getAttribute('aria-label')).toBe(defaultProps.aria_label);
		expect(image?.getAttribute('src')).toBe(defaultProps.src);
		expect(image?.getAttribute('alt')).toBe(defaultProps.alt);
		expect(image?.getAttribute('style')).toBe('border:0');
	});

	it('renders image inside link', async () => {
		const { container } = render(ClickableImage, defaultProps);

		const link = container.querySelector('a');
		const image = container.querySelector('img');

		expect(link).toBeTruthy();
		expect(image).toBeTruthy();
		expect(link).toContain(image);
	});

	it('handles different href values', async () => {
		const externalHref = 'https://example.com';
		const { container } = render(ClickableImage, {
			...defaultProps,
			href: externalHref
		});

		const link = container.querySelector('a');
		expect(link?.getAttribute('href')).toBe(externalHref);
	});

	it('handles different aria-label values', async () => {
		const customAriaLabel = 'Custom accessibility label';
		const { container } = render(ClickableImage, {
			...defaultProps,
			aria_label: customAriaLabel
		});

		const link = container.querySelector('a');
		expect(link?.getAttribute('aria-label')).toBe(customAriaLabel);
	});

	it('handles different image sources and alt text', async () => {
		const customProps = {
			...defaultProps,
			src: '/custom-image.png',
			alt: 'Custom alt text'
		};

		const { container } = render(ClickableImage, customProps);

		const image = container.querySelector('img');
		expect(image?.getAttribute('src')).toBe(customProps.src);
		expect(image?.getAttribute('alt')).toBe(customProps.alt);
	});

	it('is accessible with screen reader', async () => {
		const { container } = render(ClickableImage, defaultProps);

		const link = container.querySelector(`a[aria-label="${defaultProps.aria_label}"]`);
		expect(link).toBeTruthy();
	});

	it('can be clicked', async () => {
		const { container } = render(ClickableImage, defaultProps);

		const link = container.querySelector('a');
		expect(link).toBeTruthy();

		// Test that the link is clickable (has proper href)
		expect(link?.getAttribute('href')).toBe(defaultProps.href);
		expect(link?.tagName.toLowerCase()).toBe('a');
	});
});
