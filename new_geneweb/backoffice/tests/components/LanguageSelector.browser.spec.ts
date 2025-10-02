import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render } from 'vitest-browser-svelte';
import LanguageSelector from '$components/LanguageSelector.svelte';

// Mock the dependencies
vi.mock('$utils/languageDetection', () => ({
	switchLanguage: vi.fn()
}));

vi.mock('$utils/reactiveMessages.svelte', () => ({
	rm: {
		display_in: vi.fn(() => 'Display in:')
	}
}));

describe('LanguageSelector.svelte', () => {
	beforeEach(() => {
		vi.clearAllMocks();
	});

	it('renders all language buttons', async () => {
		const { container } = render(LanguageSelector);

		const buttons = container.querySelectorAll('button');
		expect(buttons).toHaveLength(8);

		// Check that all expected languages are present
		const languageTexts = Array.from(buttons).map((button) => button.textContent?.trim());
		expect(languageTexts).toEqual([
			'Corsu',
			'Deutsch',
			'English',
			'Español',
			'Français',
			'Italiano',
			'Latviesu',
			'Svenska'
		]);
	});

	it('displays the "Display in" message', async () => {
		const { container } = render(LanguageSelector);

		const displayText = container.querySelector('span');
		expect(displayText).toBeTruthy();
		expect(displayText?.textContent).toBe('Display in:');
	});

	it('has correct container styling', async () => {
		const { container } = render(LanguageSelector);

		const containerDiv = container.querySelector('div');
		expect(containerDiv).toBeTruthy();
		expect(containerDiv?.getAttribute('style')).toBe('float: left; align: center;');
	});

	describe('language switching', () => {
		it('calls switchLanguage with correct locale when Corsu button is clicked', async () => {
			const { switchLanguage } = await import('$utils/languageDetection');
			const { container } = render(LanguageSelector);

			const corsuButton = Array.from(container.querySelectorAll('button')).find(
				(btn) => btn.textContent?.trim() === 'Corsu'
			);

			expect(corsuButton).toBeTruthy();
			corsuButton?.click();

			expect(switchLanguage).toHaveBeenCalledWith('co');
		});

		it('calls switchLanguage with correct locale when Deutsch button is clicked', async () => {
			const { switchLanguage } = await import('$utils/languageDetection');
			const { container } = render(LanguageSelector);

			const deutschButton = Array.from(container.querySelectorAll('button')).find(
				(btn) => btn.textContent?.trim() === 'Deutsch'
			);

			expect(deutschButton).toBeTruthy();
			deutschButton?.click();

			expect(switchLanguage).toHaveBeenCalledWith('de');
		});

		it('calls switchLanguage with correct locale when English button is clicked', async () => {
			const { switchLanguage } = await import('$utils/languageDetection');
			const { container } = render(LanguageSelector);

			const englishButton = Array.from(container.querySelectorAll('button')).find(
				(btn) => btn.textContent?.trim() === 'English'
			);

			expect(englishButton).toBeTruthy();
			englishButton?.click();

			expect(switchLanguage).toHaveBeenCalledWith('en');
		});

		it('calls switchLanguage with correct locale when Español button is clicked', async () => {
			const { switchLanguage } = await import('$utils/languageDetection');
			const { container } = render(LanguageSelector);

			const espanolButton = Array.from(container.querySelectorAll('button')).find(
				(btn) => btn.textContent?.trim() === 'Español'
			);

			expect(espanolButton).toBeTruthy();
			espanolButton?.click();

			expect(switchLanguage).toHaveBeenCalledWith('es');
		});

		it('calls switchLanguage with correct locale when Français button is clicked', async () => {
			const { switchLanguage } = await import('$utils/languageDetection');
			const { container } = render(LanguageSelector);

			const francaisButton = Array.from(container.querySelectorAll('button')).find(
				(btn) => btn.textContent?.trim() === 'Français'
			);

			expect(francaisButton).toBeTruthy();
			francaisButton?.click();

			expect(switchLanguage).toHaveBeenCalledWith('fr');
		});

		it('calls switchLanguage with correct locale when Italiano button is clicked', async () => {
			const { switchLanguage } = await import('$utils/languageDetection');
			const { container } = render(LanguageSelector);

			const italianoButton = Array.from(container.querySelectorAll('button')).find(
				(btn) => btn.textContent?.trim() === 'Italiano'
			);

			expect(italianoButton).toBeTruthy();
			italianoButton?.click();

			expect(switchLanguage).toHaveBeenCalledWith('it');
		});

		it('calls switchLanguage with correct locale when Latviesu button is clicked', async () => {
			const { switchLanguage } = await import('$utils/languageDetection');
			const { container } = render(LanguageSelector);

			const latviesuButton = Array.from(container.querySelectorAll('button')).find(
				(btn) => btn.textContent?.trim() === 'Latviesu'
			);

			expect(latviesuButton).toBeTruthy();
			latviesuButton?.click();

			expect(switchLanguage).toHaveBeenCalledWith('lv');
		});

		it('calls switchLanguage with correct locale when Svenska button is clicked', async () => {
			const { switchLanguage } = await import('$utils/languageDetection');
			const { container } = render(LanguageSelector);

			const svenskaButton = Array.from(container.querySelectorAll('button')).find(
				(btn) => btn.textContent?.trim() === 'Svenska'
			);

			expect(svenskaButton).toBeTruthy();
			svenskaButton?.click();

			expect(switchLanguage).toHaveBeenCalledWith('sv');
		});
	});

	describe('accessibility', () => {
		it('has clickable buttons for all languages', async () => {
			const { container } = render(LanguageSelector);

			const buttons = container.querySelectorAll('button');
			buttons.forEach((button) => {
				expect(button.tagName.toLowerCase()).toBe('button');
				expect(button.textContent?.trim()).toBeTruthy();
			});
		});

		it('buttons are keyboard accessible', async () => {
			const { container } = render(LanguageSelector);

			const buttons = container.querySelectorAll('button');
			buttons.forEach((button) => {
				// Buttons should be focusable (tabindex should not be -1)
				expect(button.getAttribute('tabindex')).not.toBe('-1');
			});
		});
	});

	describe('responsive messages integration', () => {
		it('updates display text when reactive messages change', async () => {
			const { rm } = await import('$utils/reactiveMessages.svelte');

			// Mock the message to return different values
			vi.mocked(rm.display_in).mockReturnValue('Afficher en:');

			const { container } = render(LanguageSelector);

			const displayText = container.querySelector('span');
			expect(displayText?.textContent).toBe('Afficher en:');
		});
	});

	describe('error handling', () => {
		it('handles switchLanguage errors gracefully', async () => {
			const { switchLanguage } = await import('$utils/languageDetection');
			vi.mocked(switchLanguage).mockImplementation(() => {
				throw new Error('Language switch failed');
			});

			const { container } = render(LanguageSelector);

			const englishButton = Array.from(container.querySelectorAll('button')).find(
				(btn) => btn.textContent?.trim() === 'English'
			);

			// Should not throw when clicking the button
			expect(() => englishButton?.click()).not.toThrow();
		});
	});
});
