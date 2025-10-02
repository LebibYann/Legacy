# Testing Guide for Svelte + TypeScript Project

This guide explains how to write and run tests for your Svelte components and TypeScript code using Vitest.

## Test Setup Overview

The project is configured with:

- **Vitest** for test runner and assertions
- **@vitest/browser** with Playwright for browser-based component testing
- **vitest-browser-svelte** for Svelte component rendering
- Separate test projects for client-side and server-side code

## Running Tests

```bash
# Run all tests
npm run test:unit

# Run tests in watch mode
npm run test:unit -- --watch

# Run tests with coverage
npm run test:unit -- --coverage

# Run specific test file
npm run test:unit -- src/components/ClickableImage.svelte.spec.ts

# Run tests for a specific pattern
npm run test:unit -- --grep "LanguageSelector"
```

## Test File Naming Conventions

- **Component tests**: `ComponentName.svelte.spec.ts`
- **TypeScript utility tests**: `fileName.spec.ts`
- **Integration tests**: `fileName.integration.spec.ts`

## Writing Component Tests

### Basic Component Test Structure

```typescript
import { describe, it, expect } from 'vitest';
import { render } from 'vitest-browser-svelte';
import MyComponent from './MyComponent.svelte';

describe('MyComponent.svelte', () => {
	it('renders correctly', async () => {
		const { container } = render(MyComponent, {
			prop1: 'value1',
			prop2: 'value2'
		});

		const element = container.querySelector('.my-element');
		expect(element).toBeTruthy();
		expect(element?.textContent).toBe('Expected text');
	});
});
```

### Testing Props

```typescript
it('renders with custom props', async () => {
	const props = {
		title: 'Custom Title',
		isActive: true
	};

	const { container } = render(MyComponent, props);

	expect(container.querySelector('h1')?.textContent).toBe('Custom Title');
	expect(container.querySelector('.active')).toBeTruthy();
});
```

### Testing Events

```typescript
import { vi } from 'vitest';

it('handles click events', async () => {
	const { container } = render(MyComponent);

	const button = container.querySelector('button');
	expect(button).toBeTruthy();

	button?.click();

	// Check for expected side effects
	expect(container.querySelector('.clicked')).toBeTruthy();
});
```

### Testing with Mocks

```typescript
import { vi } from 'vitest';

// Mock external dependencies
vi.mock('$utils/someUtility', () => ({
	utilityFunction: vi.fn(() => 'mocked result')
}));

describe('ComponentWithDependencies', () => {
	beforeEach(() => {
		vi.clearAllMocks();
	});

	it('uses mocked dependency', async () => {
		const { utilityFunction } = await import('$utils/someUtility');
		const { container } = render(ComponentWithDependencies);

		expect(utilityFunction).toHaveBeenCalled();
	});
});
```

## Writing TypeScript Tests

### Testing Utility Functions

```typescript
import { describe, it, expect } from 'vitest';
import { myUtilityFunction } from './myUtility';

describe('myUtilityFunction', () => {
	it('returns expected result', () => {
		const result = myUtilityFunction('input');
		expect(result).toBe('expected output');
	});

	it('handles edge cases', () => {
		expect(myUtilityFunction('')).toBe('');
		expect(myUtilityFunction(null)).toBe(null);
	});
});
```

### Testing Svelte Stores

```typescript
import { describe, it, expect, beforeEach } from 'vitest';
import { get } from 'svelte/store';
import { myStore } from './myStore';

describe('myStore', () => {
	beforeEach(() => {
		myStore.set('initial value');
	});

	it('has correct initial value', () => {
		expect(get(myStore)).toBe('initial value');
	});

	it('updates value correctly', () => {
		myStore.set('new value');
		expect(get(myStore)).toBe('new value');
	});

	it('notifies subscribers', () => {
		let notifiedValue = '';
		const unsubscribe = myStore.subscribe((value) => {
			notifiedValue = value;
		});

		myStore.set('subscribed value');
		expect(notifiedValue).toBe('subscribed value');

		unsubscribe();
	});
});
```

## Testing Patterns and Best Practices

### 1. Use Test Helpers

```typescript
import { mockNavigator, mockLocalStorage, waitForReactivity } from '../utils/testHelpers';

describe('LanguageDetection', () => {
	beforeEach(() => {
		mockNavigator('en-US');
		Object.defineProperty(window, 'localStorage', {
			value: mockLocalStorage()
		});
	});
});
```

### 2. Test Accessibility

```typescript
it('is accessible', async () => {
	const { container } = render(MyComponent);

	const button = container.querySelector('button');
	expect(button?.getAttribute('aria-label')).toBeTruthy();
	expect(button?.getAttribute('tabindex')).not.toBe('-1');
});
```

### 3. Test Responsive Behavior

```typescript
import { mockElementDimensions } from '../utils/testHelpers';

it('adapts to different screen sizes', async () => {
	mockElementDimensions('header', { width: 300 });

	const { container } = render(ResponsiveComponent);

	await waitForReactivity();

	expect(container.querySelector('header')?.className).toContain('stacked');
});
```

### 4. Test Error Handling

```typescript
it('handles errors gracefully', async () => {
	const { externalService } = await import('$lib/externalService');
	vi.mocked(externalService).mockRejectedValue(new Error('Service unavailable'));

	const { container } = render(ComponentWithErrorHandling);

	expect(container.querySelector('.error-message')).toBeTruthy();
});
```

### 5. Integration Tests

```typescript
describe('Feature Integration', () => {
	it('works end-to-end', async () => {
		// Test multiple components working together
		const { container } = render(ParentComponent);

		// Interact with one component
		container.querySelector('button')?.click();

		await waitForReactivity();

		// Verify effects in another component
		expect(container.querySelector('.updated-child')).toBeTruthy();
	});
});
```

## Common Testing Scenarios

### Testing Forms

```typescript
it('validates form input', async () => {
	const { container } = render(FormComponent);

	const input = container.querySelector('input[type="email"]') as HTMLInputElement;
	const submitButton = container.querySelector('button[type="submit"]');

	// Test invalid input
	input.value = 'invalid-email';
	input.dispatchEvent(new Event('input'));

	expect(container.querySelector('.error')).toBeTruthy();

	// Test valid input
	input.value = 'valid@email.com';
	input.dispatchEvent(new Event('input'));

	expect(container.querySelector('.error')).toBeFalsy();
});
```

### Testing Navigation

```typescript
it('navigates correctly', async () => {
	const { container } = render(NavigationComponent);

	const link = container.querySelector('a[href="/about"]');
	expect(link).toBeTruthy();
	expect(link?.getAttribute('href')).toBe('/about');
});
```

### Testing Conditional Rendering

```typescript
it('shows/hides content based on conditions', async () => {
	const { container } = render(ConditionalComponent, {
		isVisible: true
	});

	expect(container.querySelector('.conditional-content')).toBeTruthy();

	// Re-render with different props
	const { container: hiddenContainer } = render(ConditionalComponent, {
		isVisible: false
	});

	expect(hiddenContainer.querySelector('.conditional-content')).toBeFalsy();
});
```

## Debugging Tests

### View Rendered HTML

```typescript
it('debug test', async () => {
	const { container } = render(MyComponent);

	console.log(container.innerHTML);
	// Or use the debug helper
	screen.debug();
});
```

### Test with Real Browser

Run tests with `--browser.headless=false` to see tests running in a real browser:

```bash
npm run test:unit -- --browser.headless=false
```

## Configuration Files

### Key Test Configuration

- **vite.config.ts**: Main Vitest configuration with browser setup
- **vitest-setup-client.ts**: Client-side test setup and global mocks
- **testHelpers.ts**: Utility functions for testing

### Environment Variables

Tests run in browser environment with access to DOM APIs and browser globals.

## Troubleshooting

### Common Issues

1. **Component not rendering**: Check if all required props are provided
2. **Mocks not working**: Ensure mock is defined before import
3. **Async issues**: Use `await waitForReactivity()` for reactive updates
4. **CSS issues**: Mock CSS imports if they cause problems
5. **Store state**: Reset stores in `beforeEach` hooks

### Getting Help

- Check the Vitest documentation: https://vitest.dev/
- Check the Svelte testing library docs
- Look at existing test examples in the codebase
