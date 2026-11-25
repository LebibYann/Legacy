/**
 * Utility functions for handling URLs and protocols
 */

/**
 * Get the current protocol (http: or https:)
 * @returns The current protocol with colon (e.g., 'https:')
 */
export function getProtocol(): string {
	if (typeof window === 'undefined') {
		return 'https:'; // Default for SSR
	}
	return window.location.protocol;
}

/**
 * Build a URL with the same protocol as the current page
 * @param hostname - The hostname (e.g., 'localhost')
 * @param port - The port number
 * @param path - The path (should start with /)
 * @param params - Optional query parameters
 * @returns A complete URL string
 */
export function buildUrl(
	hostname: string,
	port: number,
	path: string,
	params?: Record<string, string>
): string {
	const protocol = getProtocol();
	let url = `${protocol}//${hostname}:${port}${path}`;

	if (params && Object.keys(params).length > 0) {
		const queryString = new URLSearchParams(params).toString();
		url += `?${queryString}`;
	}

	return url;
}

/**
 * Build a URL relative to the current page's protocol and hostname
 * @param port - The port number
 * @param path - The path (should start with /)
 * @param params - Optional query parameters
 * @returns A complete URL string
 */
export function buildRelativeUrl(
	port: number,
	path: string,
	params?: Record<string, string>
): string {
	if (typeof window === 'undefined') {
		throw new Error('buildRelativeUrl can only be used in the browser');
	}
	return buildUrl(window.location.hostname, port, path, params);
}

/**
 * Check if the current page is using HTTPS
 * @returns true if HTTPS, false if HTTP
 */
export function isHttps(): boolean {
	return getProtocol() === 'https:';
}

/**
 * Get the base URL for the current environment
 * Automatically detects protocol, hostname, and port
 * @param path - Optional path to append
 * @returns The base URL
 */
export function getBaseUrl(path: string = ''): string {
	if (typeof window === 'undefined') {
		return path; // For SSR, return relative path
	}
	const protocol = window.location.protocol;
	const hostname = window.location.hostname;
	const port = window.location.port ? `:${window.location.port}` : '';
	return `${protocol}//${hostname}${port}${path}`;
}
