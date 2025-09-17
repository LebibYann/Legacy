import { execSync } from 'child_process';

const tests = ['@oc1', '@oc2', '@oc3'];

for (const tag of tests) {
  console.log(`\n➡️ Running tests with ${tag}`);
  execSync(`npx playwright test --grep "${tag}"`, { stdio: 'inherit' });
}