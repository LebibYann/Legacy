import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { createReactiveMessages } from '$utils/reactiveMessages.svelte';
// import { onLanguageChange } from "$utils/languageDetection"

// Mock the paraglide messages
vi.mock('$lib/paraglide/messages.js', () => ({
	homepage_title: vi.fn(() => 'Homepage Title'),
	create_empty: vi.fn(() => 'Create Empty Database'),
	list_configure: vi.fn(() => 'Configure')
}));

// Mock the language detection
vi.mock('$utils/languageDetection', () => ({
	onLanguageChange: vi.fn((callback) => {
		// Store the callback for later use
		(
			global as typeof globalThis & { __languageChangeCallback?: () => void }
		).__languageChangeCallback = callback;
		return () => {}; // Return unsubscribe function
	})
}));

describe('reactiveMessages', () => {
	beforeEach(() => {
		vi.clearAllMocks();
		// Mock browser environment
		// eslint-disable-next-line @typescript-eslint/no-explicit-any
		global.window = {} as any;
	});

	afterEach(() => {
		// eslint-disable-next-line @typescript-eslint/no-explicit-any
		delete (global as any).window;
		// eslint-disable-next-line @typescript-eslint/no-explicit-any
		delete (global as any).__languageChangeCallback;
	});

	describe('createReactiveMessages', () => {
		it('should create reactive wrapper for messages', async () => {
			const messages = createReactiveMessages();

			expect(messages.homepage_title).toBeDefined();
			expect(messages.create_empty).toBeDefined();
			expect(messages.list_configure).toBeDefined();
		});

		it('should call original message functions', async () => {
			const { homepage_title } = await import('$lib/paraglide/messages.js');
			const messages = createReactiveMessages();

			const result = messages.homepage_title();

			expect(homepage_title).toHaveBeenCalled();
			expect(result).toBe('Homepage Title');
		});

		it('should handle message functions correctly', async () => {
			const messages = createReactiveMessages();

			// Use an actual message from the messages module
			const result = messages.homepage_title();

			expect(result).toBe('Homepage Title');
		});

		it('should update when language changes', async () => {
			const messages = createReactiveMessages();
			const { onLanguageChange } = await import('$utils/languageDetection');

			// Get the registered callback
			const callback = vi.mocked(onLanguageChange).mock.calls[0][0];

			// Call the message initially
			messages.homepage_title();

			// Simulate language change
			callback('fr');

			// Call the message again - should reflect the language change
			messages.homepage_title();

			expect(onLanguageChange).toHaveBeenCalledWith(expect.any(Function));
		});

		it('should register language change listener only in browser environment', async () => {
			// Mock server environment by removing window
			// eslint-disable-next-line @typescript-eslint/no-explicit-any
			delete (global as any).window;

			createReactiveMessages();

			const { onLanguageChange } = await import('$utils/languageDetection');
			// In server environment, should not register listener
			expect(onLanguageChange).not.toHaveBeenCalled();
		});

		it('should handle multiple language changes', async () => {
			const messages = createReactiveMessages();
			const { onLanguageChange } = await import('$utils/languageDetection');

			const callback = vi.mocked(onLanguageChange).mock.calls[0][0];

			// Initial call
			messages.homepage_title();

			// Multiple language changes
			callback('fr');
			callback('de');
			callback('es');

			// Message should still work after multiple changes
			const result = messages.homepage_title();
			expect(result).toBe('Homepage Title');
		});

		it('should preserve function identity for non-function properties', async () => {
			const messages = createReactiveMessages();

			// If there are any non-function properties in the messages,
			// they should be preserved as-is
			Object.keys(messages).forEach((key) => {
				// eslint-disable-next-line @typescript-eslint/no-explicit-any
				const originalValue = (messages as any)[key];
				expect(originalValue).toBeDefined();
			});
		});
	});

	describe('integration with real usage patterns', () => {
		it('should work with common message patterns', async () => {
			const messages = createReactiveMessages();

			// Test different types of messages
			expect(typeof messages.homepage_title).toBe('function');
			expect(typeof messages.create_empty).toBe('function');
			expect(typeof messages.list_configure).toBe('function');

			// Test calling them
			const title = messages.homepage_title();
			const createEmpty = messages.create_empty();
			const configure = messages.list_configure();

			expect(typeof title).toBe('string');
			expect(typeof createEmpty).toBe('string');
			expect(typeof configure).toBe('string');
		});

		it('should handle edge cases', async () => {
			const messages = createReactiveMessages();

			// Should not throw when accessing undefined messages
			expect(() => {
				// @ts-expect-error - testing non-existent message
				messages.non_existent_message?.();
			}).not.toThrow();
		});
	});
});
