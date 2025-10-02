# Vitest Testing Setup for Svelte Backoffice

This document explains the comprehensive testing setup for the Svelte backoffice application using Vitest.

## Testing Architecture

### Test Focus

This setup is focused exclusively on **unit testing** for:

- TypeScript utilities and functions
- Svelte stores and reactive logic
- Business logic and API interactions
- Server-side code testing

### File Naming Conventions

- **Unit Tests**: `*.{test,spec}.{js,ts}`
- **Excluded**: `*.svelte.{test,spec}.{js,ts}` and `*.browser.{test,spec}.{js,ts}` (Svelte component tests)

## Available Test Scripts

```json
{
	"test:unit": "vitest",
	"test": "npm run test:unit -- --run && npm run test:e2e"
}
```

## Unit Tests (Server Environment)

Unit tests run in Node.js environment and are perfect for:

- Testing TypeScript utilities and functions
- Testing Svelte stores
- Testing business logic
- Testing API interactions
- Mocking browser APIs when needed

### Current Unit Test Coverage

1. **Store Tests** (`src/lib/stores/pageStore.spec.ts`)
   - Page title store functionality
   - Store subscriptions and updates
   - Multiple subscriber handling

2. **Language Detection** (`src/utils/languageDetection.spec.ts`)
   - Browser language detection
   - Locale switching
   - Language change callbacks
   - Server-side safety

3. **Reactive Messages** (`src/utils/reactiveMessages.spec.ts`)
   - Message reactivity system
   - Language change integration
   - Server/browser environment handling

4. **Integration Utilities** (`src/utils/integration.spec.ts`)
   - Form validation helpers
   - URL and navigation utilities
   - Data formatting functions
   - Array and object utilities

5. **Demo Test** (`src/demo.spec.ts`)
   - Basic example test

## Browser Tests (Browser Environment)

Browser tests run in real browser using Playwright and are perfect for:

- Testing Svelte components
- Testing DOM interactions
- Testing user events
- Testing browser-specific APIs

### Current Browser Test Coverage

1. **ClickableImage Component** (`src/components/ClickableImage.browser.spec.ts`)
   - Component rendering
   - Props handling
   - Accessibility features
   - Click interactions

2. **Header Component** (`src/components/Header.browser.spec.ts`)
   - Responsive layout
   - Page title integration
   - Event listener setup
   - DOM manipulation

3. **LanguageSelector Component** (`src/components/LanguageSelector.browser.spec.ts`)
   - Language button rendering
   - Language switching functionality
   - Accessibility compliance
   - Error handling

## Test Setup Files

### `vitest-setup-client.ts`

- Browser environment setup
- Mock ResizeObserver and IntersectionObserver
- Global mock cleanup

### `src/utils/testHelpers.ts`

- Comprehensive testing utilities
- Mock factories for common scenarios
- Accessibility testing helpers
- Store testing wrappers

## Running Tests

### Unit Tests

```bash
npm run test:unit
```

### Single Test File

```bash
npx vitest run src/utils/languageDetection.spec.ts
```

## Writing New Tests

### For TypeScript/Utility Functions (Unit Tests)

```typescript
import { describe, it, expect } from 'vitest';

describe('MyUtility', () => {
	it('should do something', () => {
		// Test implementation
		expect(true).toBe(true);
	});
});
```

### For Svelte Components (Browser Tests)

```typescript
import { describe, it, expect } from 'vitest';
import { render } from 'vitest-browser-svelte';
import MyComponent from './MyComponent.svelte';

describe('MyComponent.svelte', () => {
	it('should render correctly', async () => {
		const { container } = render(MyComponent, {
			prop1: 'value1',
			prop2: 'value2'
		});

		const element = container.querySelector('div');
		expect(element).toBeTruthy();
	});
});
```

### Testing Stores

```typescript
import { describe, it, expect } from 'vitest';
import { get } from 'svelte/store';
import { myStore } from './myStore';

describe('myStore', () => {
	it('should update value', () => {
		myStore.set('new value');
		expect(get(myStore)).toBe('new value');
	});
});
```

## Mocking Guidelines

### Mocking Modules

```typescript
vi.mock('$lib/paraglide/runtime.js', () => ({
	getLocale: vi.fn(() => 'en'),
	setLocale: vi.fn(),
	locales: ['en', 'fr', 'de']
}));
```

### Mocking Browser APIs

```typescript
beforeEach(() => {
	global.window = {
		localStorage: {
			getItem: vi.fn(),
			setItem: vi.fn()
		}
	} as any;
});
```

### Mocking Components

```typescript
vi.mock('./MyComponent.svelte', () => ({
	default: vi.fn(() => ({ render: () => '<div>Mocked</div>' }))
}));
```

## Best Practices

1. **Separate Concerns**: Keep unit tests for logic, browser tests for UI
2. **Mock External Dependencies**: Always mock external APIs and modules
3. **Test Edge Cases**: Include error scenarios and boundary conditions
4. **Use Descriptive Names**: Test names should clearly describe what they test
5. **Clean Up**: Always clean up mocks and global state in `afterEach`
6. **Accessibility**: Include accessibility tests for components
7. **Performance**: Use `--run` flag for CI/CD pipelines

## Configuration Details

### Vite Config (`vite.config.ts`)

- Single test configuration for unit tests only
- Node.js environment
- Excludes Svelte component tests
- No Playwright dependencies

### Package Dependencies

- `vitest`: Core testing framework
- `@vitest/browser`: Browser environment support
- `vitest-browser-svelte`: Svelte component testing
- `@playwright/test`: Browser automation

## Troubleshooting

### Common Issues

1. **"window is not defined"**: Use unit tests for server-side code
2. **"Cannot find module"**: Check import paths and mock setup
3. **Playwright errors**: Install browsers with `npx playwright install`
4. **Component test failures**: Ensure correct file naming (`.browser.spec.ts`)

### Debug Mode

```bash
npx vitest --project unit --reporter=verbose
```

This testing setup provides comprehensive coverage for both TypeScript business logic and Svelte component functionality while maintaining clear separation between server and browser environments.
