import { defineConfig, loadEnv } from 'vite';
import { paraglideVitePlugin } from '@inlang/paraglide-js';
import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';

export default defineConfig(({ mode }) => {
	// Charge les variables .env selon le mode (development, production, etc.)
	const env = loadEnv(mode, process.cwd(), '');

	return {
		plugins: [
			paraglideVitePlugin({ project: './project.inlang', outdir: './src/lib/paraglide' }),
			tailwindcss(),
			sveltekit()
		],
		server: {
			allowedHosts: [process.env.BACKOFFICE_DNS ?? env.BACKOFFICE_DNS ?? 'backoffice'],
			port: Number(process.env.NEW_BACKOFFICE_PORT ?? env.NEW_BACKOFFICE_PORT ?? 5173),
			hmr: {
				protocol: 'ws',
				host: 'localhost',
				port: Number(process.env.OLD_BACKOFFICE_PORT ?? env.OLD_BACKOFFICE_PORT ?? 2316)
			}
		},
		test: {
			expect: { requireAssertions: true },
			environment: 'node',
			include: ['tests/**/*.{test,spec}.ts'],
			exclude: ['tests/**/*.svelte.{test,spec}.ts', 'tests/**/*.browser.{test,spec}.ts']
		}
	};
});
