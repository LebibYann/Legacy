import * as m from '$lib/paraglide/messages.js';
import { onLanguageChange } from './languageDetection.js';

type Messages = typeof m;

/**
 * Creates a reactive wrapper around Paraglide messages that automatically
 * updates when the language changes, without needing to manually define each message.
 */
export function createReactiveMessages(): Messages {
	let updateTrigger = $state(0);

	if (typeof window !== 'undefined') {
		onLanguageChange(() => {
			updateTrigger++;
		});
	}

	const reactiveMessages: Partial<Messages> = {};

	for (const key of Object.keys(m) as Array<keyof Messages>) {
		const originalFunction = m[key];
		if (typeof originalFunction === 'function') {
			reactiveMessages[key] = ((...args: unknown[]) => {
				// eslint-disable-next-line @typescript-eslint/no-unused-expressions
				updateTrigger;
				return originalFunction(...args);
			}) as Messages[typeof key];
		} else {
			reactiveMessages[key] = originalFunction;
		}
	}

	return reactiveMessages as Messages;
}

/**
 * Reactive messages instance - ready to use!
 * This is a drop-in replacement for the regular Paraglide messages import.
 *
 * Usage:
 * Instead of: import * as m from '$lib/paraglide/messages.js'
 * Use: import { rm } from '$utils/reactiveMessages'
 */
export const rm = createReactiveMessages();
