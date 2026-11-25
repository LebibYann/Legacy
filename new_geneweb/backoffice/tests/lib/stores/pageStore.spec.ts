import { describe, it, expect, beforeEach } from 'vitest';
import { get } from 'svelte/store';
import { pageTitle, pageSubtitle, showBackButton } from '$stores/pageStore';

describe('pageStore', () => {
	beforeEach(() => {
		// Reset stores to their default values before each test
		pageTitle.set('Management and creation');
		pageSubtitle.set('');
		showBackButton.set(false);
	});

	describe('pageTitle store', () => {
		it('should have default value', () => {
			expect(get(pageTitle)).toBe('Management and creation');
		});

		it('should update value when set', () => {
			const newTitle = 'Test Page Title';
			pageTitle.set(newTitle);
			expect(get(pageTitle)).toBe(newTitle);
		});

		it('should update value when using update function', () => {
			pageTitle.update((current) => current + ' - Updated');
			expect(get(pageTitle)).toBe('Management and creation - Updated');
		});

		it('should notify subscribers when value changes', () => {
			let notifiedValue = '';
			const unsubscribe = pageTitle.subscribe((value) => {
				notifiedValue = value;
			});

			pageTitle.set('New Title');
			expect(notifiedValue).toBe('New Title');

			unsubscribe();
		});
	});

	describe('pageSubtitle store', () => {
		it('should have empty string as default value', () => {
			expect(get(pageSubtitle)).toBe('');
		});

		it('should update value when set', () => {
			const newSubtitle = 'Test Subtitle';
			pageSubtitle.set(newSubtitle);
			expect(get(pageSubtitle)).toBe(newSubtitle);
		});
	});

	describe('showBackButton store', () => {
		it('should have false as default value', () => {
			expect(get(showBackButton)).toBe(false);
		});

		it('should update value when set', () => {
			showBackButton.set(true);
			expect(get(showBackButton)).toBe(true);
		});

		it('should toggle value correctly', () => {
			showBackButton.update((current) => !current);
			expect(get(showBackButton)).toBe(true);

			showBackButton.update((current) => !current);
			expect(get(showBackButton)).toBe(false);
		});
	});
});
