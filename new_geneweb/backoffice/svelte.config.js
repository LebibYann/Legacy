import adapter from '@sveltejs/adapter-node';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	// Consult https://svelte.dev/docs/kit/integrations
	// for more information about preprocessors
	preprocess: vitePreprocess(),

	kit: {
		// adapter-auto only supports some environments, see https://svelte.dev/docs/kit/adapter-auto for a list.
		// If your environment is not supported, or you settled on a specific environment, switch out the adapter.
		// See https://svelte.dev/docs/kit/adapters for more information about adapters.
		adapter: adapter(),
		alias: {
			// $lib is natively mapped to src/lib
			$components: 'src/components',
			$assets: 'src/assets',
			$stores: 'src/lib/stores',
			$utils: 'src/utils',
			$routes: 'src/routes',
			$: 'src', // Adding alias for root folder
			$test: 'tests' // If ever needed
		}
	}
};

export default config;
