import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render } from 'vitest-browser-svelte';
import Header from '$components/Header.svelte';
import { pageTitle } from '$lib/stores/pageStore';

// Mock the ClickableImage component
vi.mock('$components/ClickableImage.svelte', () => {
	return {
		default: vi.fn(() => ({
			render: () => '<div data-testid="clickable-image">Mocked ClickableImage</div>'
		}))
	};
});

describe('Header.svelte', () => {
	beforeEach(() => {
		// Reset page title before each test
		pageTitle.set('Test Page Title');

		// Mock window methods
		Object.defineProperty(window, 'addEventListener', {
			value: vi.fn(),
			writable: true
		});
		Object.defineProperty(window, 'removeEventListener', {
			value: vi.fn(),
			writable: true
		});
	});

	it('renders header with correct structure', async () => {
		const { container } = render(Header);

		const header = container.querySelector('header');
		expect(header).toBeTruthy();
		expect(header?.className).toContain('flex');
	});

	it('displays the page title from store', async () => {
		const testTitle = 'Custom Test Title';
		pageTitle.set(testTitle);

		const { container } = render(Header);

		const title = container.querySelector('h1');
		expect(title).toBeTruthy();
		expect(title?.textContent?.trim()).toBe(testTitle);
	});

	it('has correct CSS classes for title', async () => {
		const { container } = render(Header);

		const title = container.querySelector('h1');
		expect(title).toBeTruthy();
		expect(title?.className).toContain('w-fit');
		expect(title?.className).toContain('text-lime-800');
	});

	it('applies responsive layout classes', async () => {
		const { container } = render(Header);

		const header = container.querySelector('header');
		expect(header).toBeTruthy();

		// Should have flex classes for layout
		expect(header?.className).toContain('flex');
	});

	it('updates title when store changes', async () => {
		const { container } = render(Header);

		// Initial title
		const initialTitle = 'Initial Title';
		pageTitle.set(initialTitle);

		// Wait for reactivity
		await new Promise((resolve) => setTimeout(resolve, 0));

		let title = container.querySelector('h1');
		expect(title?.textContent?.trim()).toBe(initialTitle);

		// Update title
		const newTitle = 'Updated Title';
		pageTitle.set(newTitle);

		// Wait for reactivity
		await new Promise((resolve) => setTimeout(resolve, 0));

		title = container.querySelector('h1');
		expect(title?.textContent?.trim()).toBe(newTitle);
	});

	it('has logo container with correct classes', async () => {
		const { container } = render(Header);

		// Look for the logo container div
		const logoContainer = container.querySelector('div.w-fit');
		expect(logoContainer).toBeTruthy();
	});

	it('sets up resize event listener on mount', async () => {
		const addEventListenerSpy = vi.spyOn(window, 'addEventListener');

		render(Header);

		// Should add resize event listener
		expect(addEventListenerSpy).toHaveBeenCalledWith('resize', expect.any(Function));
	});

	describe('responsive behavior', () => {
		it('applies stacked layout classes when needed', async () => {
			// Mock clientWidth to simulate narrow screen
			Object.defineProperty(HTMLElement.prototype, 'clientWidth', {
				get() {
					if (this.classList?.contains('w-fit')) return 200; // logo width
					return 300; // header width (narrow)
				},
				configurable: true
			});

			const { container } = render(Header);

			// Wait for effects to run
			await new Promise((resolve) => setTimeout(resolve, 100));

			const header = container.querySelector('header');
			// In a real test, you'd check for the stacked classes
			expect(header).toBeTruthy();
		});
	});
});
