import { vi, expect } from 'vitest';

/**
 * Mock navigator object for testing language detection
 */
export function mockNavigator(language: string, languages?: string[]) {
	Object.defineProperty(window, 'navigator', {
		value: {
			language,
			languages: languages || [language]
		},
		writable: true,
		configurable: true
	});
}

/**
 * Mock localStorage for testing
 */
export function mockLocalStorage() {
	const storage = new Map<string, string>();

	return {
		getItem: vi.fn((key: string) => storage.get(key) || null),
		setItem: vi.fn((key: string, value: string) => storage.set(key, value)),
		removeItem: vi.fn((key: string) => storage.delete(key)),
		clear: vi.fn(() => storage.clear()),
		key: vi.fn((index: number) => Array.from(storage.keys())[index] || null),
		get length() {
			return storage.size;
		}
	};
}

/**
 * Mock window.addEventListener and removeEventListener
 */
export function mockWindowEvents() {
	const eventListeners = new Map<string, Array<(event?: unknown) => void>>();

	const addEventListener = vi.fn((event: string, handler: (event?: unknown) => void) => {
		if (!eventListeners.has(event)) {
			eventListeners.set(event, []);
		}
		eventListeners.get(event)!.push(handler);
	});

	const removeEventListener = vi.fn((event: string, handler: (event?: unknown) => void) => {
		const handlers = eventListeners.get(event);
		if (handlers) {
			const index = handlers.indexOf(handler);
			if (index > -1) {
				handlers.splice(index, 1);
			}
		}
	});

	const dispatchEvent = (event: string, data?: unknown) => {
		const handlers = eventListeners.get(event);
		if (handlers) {
			handlers.forEach((handler) => handler(data));
		}
	};

	Object.defineProperty(window, 'addEventListener', {
		value: addEventListener,
		writable: true
	});

	Object.defineProperty(window, 'removeEventListener', {
		value: removeEventListener,
		writable: true
	});

	return {
		addEventListener,
		removeEventListener,
		dispatchEvent,
		getListeners: (event: string) => eventListeners.get(event) || []
	};
}

/**
 * Mock DOM element dimensions for testing responsive behavior
 */
export function mockElementDimensions(
	elementSelector: string,
	dimensions: { width?: number; height?: number }
) {
	const originalGetComputedStyle = window.getComputedStyle;

	window.getComputedStyle = vi.fn((element: Element) => {
		if (element.matches && element.matches(elementSelector)) {
			return {
				...originalGetComputedStyle(element),
				width: `${dimensions.width || 0}px`,
				height: `${dimensions.height || 0}px`
			} as CSSStyleDeclaration;
		}
		return originalGetComputedStyle(element);
	});

	// Mock clientWidth and clientHeight properties
	Object.defineProperty(HTMLElement.prototype, 'clientWidth', {
		get() {
			if (this.matches && this.matches(elementSelector)) {
				return dimensions.width || 0;
			}
			return 0;
		},
		configurable: true
	});

	Object.defineProperty(HTMLElement.prototype, 'clientHeight', {
		get() {
			if (this.matches && this.matches(elementSelector)) {
				return dimensions.height || 0;
			}
			return 0;
		},
		configurable: true
	});
}

/**
 * Wait for Svelte reactivity to complete
 */
export function waitForReactivity(): Promise<void> {
	return new Promise((resolve) => setTimeout(resolve, 0));
}

/**
 * Create a test wrapper for Svelte stores
 */
export function createStoreTestWrapper<T>(initialValue: T) {
	let value = initialValue;
	const subscribers = new Set<(value: T) => void>();

	return {
		subscribe: (callback: (value: T) => void) => {
			subscribers.add(callback);
			callback(value);
			return () => subscribers.delete(callback);
		},
		set: (newValue: T) => {
			value = newValue;
			subscribers.forEach((callback) => callback(value));
		},
		update: (updater: (value: T) => T) => {
			value = updater(value);
			subscribers.forEach((callback) => callback(value));
		},
		get: () => value
	};
}

/**
 * Assert that an element has specific accessibility attributes
 */
export function assertAccessibility(
	element: Element | null,
	expectedAttributes: Record<string, string>
) {
	expect(element).toBeTruthy();

	Object.entries(expectedAttributes).forEach(([attribute, expectedValue]) => {
		expect(element?.getAttribute(attribute)).toBe(expectedValue);
	});
}

/**
 * Mock paraglide runtime for testing
 */
export function mockParaglideRuntime(currentLocale = 'en') {
	return {
		getLocale: vi.fn(() => currentLocale),
		setLocale: vi.fn(),
		locales: ['co', 'de', 'en', 'es', 'fr', 'it', 'lv', 'sv']
	};
}

/**
 * Test data factories
 */
export const testDataFactory = {
	clickableImageProps: (
		overrides?: Partial<{
			href: string;
			aria_label: string;
			src: string;
			alt: string;
		}>
	) => ({
		href: '/test-link',
		aria_label: 'Test aria label',
		src: '/test-image.jpg',
		alt: 'Test image',
		...overrides
	})
};
