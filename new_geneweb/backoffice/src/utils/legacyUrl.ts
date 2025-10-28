import { browser } from '$app/environment';

const LEGACY_BASE_URL: string = '/gwsetup';

export function makeLegacyUrl(
	queryParams: Record<string, string>,
	url: string = LEGACY_BASE_URL
): string {
	const queryString = new URLSearchParams(queryParams).toString();
	const rootUrl = browser ? window.location.origin : '';
	return `${rootUrl}${url}?${queryString}`;
}
