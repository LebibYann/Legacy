import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import {
	detectAndSetBrowserLanguage,
	getCurrentLocale,
	switchLanguage,
	onLanguageChange
} from '$utils/languageDetection';

// Mock the paraglide runtime
vi.mock('$lib/paraglide/runtime.js', () => ({
	getLocale: vi.fn(() => 'en'),
	setLocale: vi.fn(),
	locales: ['co', 'de', 'en', 'es', 'fr', 'it', 'lv', 'sv']
}));

describe('languageDetection', () => {
	beforeEach(() => {
		vi.clearAllMocks();

		// Mock global objects for browser environment

		global.window = {
			localStorage: {
				getItem: vi.fn(),
				setItem: vi.fn(),
				removeItem: vi.fn(),
				clear: vi.fn()
			},
			navigator: {
				language: 'en-US',
				languages: ['en-US', 'en']
			}
			// eslint-disable-next-line @typescript-eslint/no-explicit-any
		} as any;

		global.localStorage = global.window.localStorage;
		// Use Object.defineProperty to avoid read-only property issues
		Object.defineProperty(global, 'navigator', {
			value: global.window.navigator,
			writable: true,
			configurable: true
		});
	});

	afterEach(() => {
		// Clean up global mocks
		// eslint-disable-next-line @typescript-eslint/no-explicit-any
		delete (global as any).window;
		// eslint-disable-next-line @typescript-eslint/no-explicit-any
		delete (global as any).localStorage;
		// Reset navigator property
		Object.defineProperty(global, 'navigator', {
			value: undefined,
			writable: true,
			configurable: true
		});
	});

	describe('getCurrentLocale', () => {
		it('should return current locale from paraglide', async () => {
			const { getLocale } = await import('$lib/paraglide/runtime.js');
			vi.mocked(getLocale).mockReturnValue('fr');

			const result = getCurrentLocale();
			expect(result).toBe('fr');
		});

		it('should return fallback locale when getLocale throws', async () => {
			const { getLocale } = await import('$lib/paraglide/runtime.js');
			vi.mocked(getLocale).mockImplementation(() => {
				throw new Error('No locale set');
			});

			const result = getCurrentLocale();
			expect(result).toBe('en');
		});
	});

	describe('switchLanguage', () => {
		it('should switch to supported language', async () => {
			const { setLocale } = await import('$lib/paraglide/runtime.js');

			switchLanguage('fr');

			expect(setLocale).toHaveBeenCalledWith('fr', { reload: false });
			expect(global.localStorage.setItem).toHaveBeenCalledWith('user-language-preference', 'fr');
		});

		it('should not switch to unsupported language', async () => {
			const { setLocale } = await import('$lib/paraglide/runtime.js');

			// @ts-expect-error - testing with invalid locale
			switchLanguage('invalid');

			expect(setLocale).not.toHaveBeenCalled();
			expect(global.localStorage.setItem).not.toHaveBeenCalled();
		});
	});

	describe('onLanguageChange', () => {
		it('should register and call language change callback', () => {
			const callback = vi.fn();
			const unsubscribe = onLanguageChange(callback);

			// Trigger a language change
			switchLanguage('de');

			expect(callback).toHaveBeenCalledWith('de');

			// Test unsubscribe
			unsubscribe();
			callback.mockClear();

			switchLanguage('fr');
			expect(callback).not.toHaveBeenCalled();
		});

		it('should handle multiple subscribers', () => {
			const callback1 = vi.fn();
			const callback2 = vi.fn();

			onLanguageChange(callback1);
			onLanguageChange(callback2);

			switchLanguage('es');

			expect(callback1).toHaveBeenCalledWith('es');
			expect(callback2).toHaveBeenCalledWith('es');
		});
	});

	describe('detectAndSetBrowserLanguage', () => {
		it('should use stored language preference', async () => {
			const { setLocale } = await import('$lib/paraglide/runtime.js');
			vi.mocked(global.localStorage.getItem).mockReturnValue('de');

			detectAndSetBrowserLanguage();

			expect(setLocale).toHaveBeenCalledWith('de', { reload: false });
		});

		it('should detect browser language when no stored preference', async () => {
			const { setLocale } = await import('$lib/paraglide/runtime.js');
			vi.mocked(global.localStorage.getItem).mockReturnValue(null);

			// Update the navigator mock using Object.defineProperty
			Object.defineProperty(global, 'navigator', {
				value: {
					...global.navigator,
					languages: ['fr-FR', 'en-US']
				},
				writable: true,
				configurable: true
			});

			detectAndSetBrowserLanguage();

			expect(setLocale).toHaveBeenCalledWith('fr', { reload: false });
		});

		it('should handle exact language match', async () => {
			const { setLocale } = await import('$lib/paraglide/runtime.js');
			vi.mocked(global.localStorage.getItem).mockReturnValue(null);

			// Update the navigator mock using Object.defineProperty
			Object.defineProperty(global, 'navigator', {
				value: {
					...global.navigator,
					languages: ['en'] // Exact match
				},
				writable: true,
				configurable: true
			});

			detectAndSetBrowserLanguage();

			expect(setLocale).toHaveBeenCalledWith('en', { reload: false });
		});

		it('should handle language code extraction', async () => {
			const { setLocale } = await import('$lib/paraglide/runtime.js');
			vi.mocked(global.localStorage.getItem).mockReturnValue(null);

			// Update the navigator mock using Object.defineProperty
			Object.defineProperty(global, 'navigator', {
				value: {
					...global.navigator,
					languages: ['es-MX'] // Should extract 'es'
				},
				writable: true,
				configurable: true
			});

			detectAndSetBrowserLanguage();

			expect(setLocale).toHaveBeenCalledWith('es', { reload: false });
		});

		it('should not set locale for unsupported languages', async () => {
			const { setLocale } = await import('$lib/paraglide/runtime.js');
			vi.mocked(global.localStorage.getItem).mockReturnValue(null);

			// Update the navigator mock using Object.defineProperty
			Object.defineProperty(global, 'navigator', {
				value: {
					...global.navigator,
					languages: ['zh-CN', 'ja'] // Unsupported languages
				},
				writable: true,
				configurable: true
			});

			detectAndSetBrowserLanguage();

			expect(setLocale).not.toHaveBeenCalled();
		});

		it('should handle server-side environment gracefully', () => {
			// Remove window to simulate server environment
			// eslint-disable-next-line @typescript-eslint/no-explicit-any
			delete (global as any).window;

			// Should not throw
			expect(() => detectAndSetBrowserLanguage()).not.toThrow();
		});
	});
});
