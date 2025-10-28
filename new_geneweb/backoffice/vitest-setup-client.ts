/// <reference types="@vitest/browser/matchers" />

import { beforeEach } from 'vitest';
import { vi } from 'vitest';

// Mock DOM methods that might not be available in the test environment
beforeEach(() => {
	// Mock ResizeObserver if it's not available
	if (!global.ResizeObserver) {
		global.ResizeObserver = vi.fn().mockImplementation(() => ({
			observe: vi.fn(),
			unobserve: vi.fn(),
			disconnect: vi.fn()
		}));
	}

	// Mock IntersectionObserver if it's not available
	if (!global.IntersectionObserver) {
		global.IntersectionObserver = vi.fn().mockImplementation(() => ({
			observe: vi.fn(),
			unobserve: vi.fn(),
			disconnect: vi.fn()
		}));
	}

	// Reset all mocks before each test
	vi.clearAllMocks();
});
