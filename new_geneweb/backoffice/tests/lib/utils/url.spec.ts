import { describe, it, expect, afterEach } from 'vitest';
import { getProtocol, buildUrl, buildRelativeUrl, isHttps, getBaseUrl } from '$lib/utils/url';

describe('URL Utilities', () => {
	// Store original window
	const originalWindow = global.window;

	// Mock window.location for testing
	const mockLocation = (protocol: string, hostname: string, port: string) => {
		global.window = {
			location: {
				protocol,
				hostname,
				port
			}
		} as Window & typeof globalThis;
	};

	afterEach(() => {
		// Restore original window
		global.window = originalWindow;
	});

	describe('getProtocol', () => {
		it('should return https: when on HTTPS', () => {
			mockLocation('https:', 'localhost', '2316');
			expect(getProtocol()).toBe('https:');
		});

		it('should return http: when on HTTP', () => {
			mockLocation('http:', 'localhost', '2316');
			expect(getProtocol()).toBe('http:');
		});
	});

	describe('isHttps', () => {
		it('should return true when on HTTPS', () => {
			mockLocation('https:', 'localhost', '2316');
			expect(isHttps()).toBe(true);
		});

		it('should return false when on HTTP', () => {
			mockLocation('http:', 'localhost', '2316');
			expect(isHttps()).toBe(false);
		});
	});

	describe('buildUrl', () => {
		it('should build URL with HTTPS protocol', () => {
			mockLocation('https:', 'localhost', '2316');
			const url = buildUrl('example.com', 8080, '/api/test');
			expect(url).toBe('https://example.com:8080/api/test');
		});

		it('should build URL with HTTP protocol', () => {
			mockLocation('http:', 'localhost', '2316');
			const url = buildUrl('example.com', 8080, '/api/test');
			expect(url).toBe('http://example.com:8080/api/test');
		});

		it('should build URL with query parameters', () => {
			mockLocation('https:', 'localhost', '2316');
			const url = buildUrl('example.com', 8080, '/api/test', { foo: 'bar', baz: 'qux' });
			expect(url).toBe('https://example.com:8080/api/test?foo=bar&baz=qux');
		});

		it('should handle empty query parameters', () => {
			mockLocation('https:', 'localhost', '2316');
			const url = buildUrl('example.com', 8080, '/api/test', {});
			expect(url).toBe('https://example.com:8080/api/test');
		});
	});

	describe('buildRelativeUrl', () => {
		it('should build URL relative to current page on HTTPS', () => {
			mockLocation('https:', 'localhost', '2316');
			const url = buildRelativeUrl(2317, '/base1', { lang: 'en' });
			expect(url).toBe('https://localhost:2317/base1?lang=en');
		});

		it('should build URL relative to current page on HTTP', () => {
			mockLocation('http:', 'localhost', '2316');
			const url = buildRelativeUrl(2317, '/base1', { lang: 'en' });
			expect(url).toBe('http://localhost:2317/base1?lang=en');
		});

		it('should use current hostname', () => {
			mockLocation('https:', '192.168.1.100', '2316');
			const url = buildRelativeUrl(2317, '/api/bases');
			expect(url).toBe('https://192.168.1.100:2317/api/bases');
		});
	});

	describe('getBaseUrl', () => {
		it('should get base URL with HTTPS', () => {
			mockLocation('https:', 'localhost', '2316');
			const url = getBaseUrl();
			expect(url).toBe('https://localhost:2316');
		});

		it('should get base URL with HTTP', () => {
			mockLocation('http:', 'localhost', '2316');
			const url = getBaseUrl();
			expect(url).toBe('http://localhost:2316');
		});

		it('should get base URL with path', () => {
			mockLocation('https:', 'localhost', '2316');
			const url = getBaseUrl('/api/bases');
			expect(url).toBe('https://localhost:2316/api/bases');
		});

		it('should handle empty port', () => {
			mockLocation('https:', 'example.com', '');
			const url = getBaseUrl('/api');
			expect(url).toBe('https://example.com/api');
		});
	});
});
