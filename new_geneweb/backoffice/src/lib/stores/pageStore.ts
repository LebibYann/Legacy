import { writable } from 'svelte/store';

// Create a writable store for the page title
export const pageTitle = writable<string>('Management and creation');

// You can also create other page-related stores here
export const pageSubtitle = writable<string>('');
export const showBackButton = writable<boolean>(false);