import { paraglideVitePlugin } from '@inlang/paraglide-js';
import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [
		paraglideVitePlugin({ project: './project.inlang', outdir: './src/lib/paraglide' }),
		tailwindcss(),
		sveltekit()
	],
	test: {
		expect: { requireAssertions: true },
		environment: 'node',
		include: ['tests/**/*.{test,spec}.ts'],
		exclude: ['tests/**/*.svelte.{test,spec}.ts', 'tests/**/*.browser.{test,spec}.ts']
	}
});
