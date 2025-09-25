# TESTING.md - GeneWeb Project Testing Strategy & Plan

## Table of Contents
1. [Overview](#overview)
2. [Test-Driven Development (TDD) Approach](#test-driven-development-tdd-approach)
3. [Testing Strategy](#testing-strategy)
4. [Test Plan](#test-plan)
5. [Test Environments](#test-environments)
6. [Tools & Frameworks](#tools--frameworks)
7. [Coverage & Quality Metrics](#coverage--quality-metrics)
8. [CI/CD Integration](#cicd-integration)
9. [Test Execution Guidelines](#test-execution-guidelines)
10. [Risk Management](#risk-management)

---

## Overview

This document outlines the comprehensive testing strategy and plan for the GeneWeb project, a genealogy management system. The project consists of:

- **GeneWeb Core** (OCaml backend) - genealogy processing, GEDCOM import/export, database management
- **GWD Frontend** (TypeScript/UI) - web interface for setup, configuration, and data management
- **New GeneWeb** (Next.js/React) - modern frontend implementation
- **CLI Tools** - various binaries for data processing and maintenance

### Project Structure
```
├── geneweb/           # OCaml core with legacy frontend
├── new_geneweb/       # Modern Next.js frontend
├── tests/             # E2E and functional tests
│   ├── e2e/          # Playwright end-to-end tests
│   └── functional/   # Python functional tests for binaries
└── docs/             # Documentation
```

---

## Test-Driven Development (TDD) Approach

### TDD Principles
We adopt TDD as our primary development methodology to ensure:
- **High code quality** through design-first thinking
- **Comprehensive test coverage** as a natural byproduct
- **Reduced debugging time** through early defect detection
- **Better system design** through testable code architecture

### TDD Cycle (Red-Green-Refactor)

#### 1. RED Phase - Write Failing Tests
- Write the minimum test that fails
- Focus on behavior and expected outcomes
- Define clear acceptance criteria

#### 2. GREEN Phase - Make Tests Pass
- Write the minimum code to make tests pass
- Don't optimize yet - focus on functionality
- Ensure all existing tests continue to pass

#### 3. REFACTOR Phase - Improve Code Quality
- Refactor code while keeping tests green
- Improve design, remove duplication
- Enhance performance and maintainability

### TDD Implementation by Component

#### Frontend (TypeScript/React)
```typescript
// Example: Component test-first approach
describe('GenealogyImportForm', () => {
  it('should validate GEDCOM file format before upload', async () => {
    // RED: Test fails initially
    const form = render(<GenealogyImportForm />);
    const file = new File(['invalid'], 'test.txt', { type: 'text/plain' });

    await userEvent.upload(form.getByRole('button', { name: /upload/i }), file);

    expect(form.getByText(/invalid file format/i)).toBeInTheDocument();
  });
});
```

#### Backend (OCaml)
```ocaml
(* Example: Function test-first approach *)
let test_gedcom_parser () =
  let invalid_gedcom = "INVALID GEDCOM CONTENT" in
  let result = Gedcom.parse invalid_gedcom in
  Alcotest.(check (result string string)) "should reject invalid GEDCOM"
    (Error "Invalid GEDCOM format") result
```

#### Binary Tools (Python Tests)
```python
def test_ged2gwb_invalid_input(tmp_path):
    """RED: Test should fail when invalid GEDCOM is provided"""
    invalid_ged = tmp_path / "invalid.ged"
    invalid_ged.write_text("NOT A VALID GEDCOM")

    with pytest.raises(subprocess.CalledProcessError):
        run([BIN_DIR / "ged2gwb", invalid_ged, "-o", "test"], cwd=tmp_path)
```

---

## Testing Strategy

### 1. Testing Pyramid

```
    /\     E2E Tests (5-10%)
   /  \    ├─ Critical user journeys
  /____\   ├─ Cross-browser compatibility
 /      \  └─ Performance validation
/________\
Integration Tests (20-30%)
├─ API endpoints
├─ Database operations
└─ Service interactions

Unit Tests (60-70%)
├─ Pure functions
├─ Business logic
├─ Component behavior
└─ Error handling
```

### 2. Testing Techniques

#### Behavior-Driven Development (BDD)
- **Gherkin scenarios** for critical user journeys
- **Given-When-Then** format for clarity
- **Living documentation** that stays current

```gherkin
Feature: GEDCOM Import
  Scenario: Import valid GEDCOM file
    Given I am on the genealogy import page
    When I upload a valid GEDCOM file
    Then the genealogy should be created successfully
    And I should see a confirmation message
```

#### Risk-Based Testing
- **High-risk areas**: Data import/export, genealogy merges, large datasets
- **Exploratory testing sessions**: 60-90 minute charters
- **Edge case focus**: Malformed data, memory limits, concurrent users

#### Property-Based Testing
- **QuickCheck-style testing** for OCaml functions
- **Hypothesis testing** for Python utilities
- **Random data generation** for robustness

### 3. Test Types & Scope

| Test Type | Framework | Coverage | Execution |
|-----------|-----------|----------|-----------|
| **Unit Tests** | Vitest (TS), Alcotest (OCaml), pytest (Python) | ≥85% statements | Every commit |
| **Integration** | Playwright, pytest | API/DB interactions | PR validation |
| **E2E** | Playwright | Critical user flows | Nightly + releases |
| **Performance** | Lighthouse, k6 | SLA compliance | Weekly + releases |
| **Security** | OWASP ZAP, Snyk | Vulnerability scans | Nightly |
| **Accessibility** | axe-core | WCAG 2.1 AA | PR validation |

---

## Test Plan

### Test Scenarios by Feature Area

#### 1. Data Import/Export (HIGH PRIORITY)

| Test ID | Scenario | Type | Coverage |
|---------|----------|------|----------|
| IMP-001 | Import valid GEDCOM file | E2E | Happy path |
| IMP-002 | Import large GEDCOM (>10MB) | Performance | Stress testing |
| IMP-003 | Import malformed GEDCOM | Integration | Error handling |
| IMP-004 | Export to GEDCOM format | E2E | Data integrity |
| IMP-005 | Export with filtering options | Integration | Feature completeness |
| IMP-006 | Concurrent import operations | Load | System limits |

#### 2. Genealogy Management (HIGH PRIORITY)

| Test ID | Scenario | Type | Coverage |
|---------|----------|------|----------|
| GEN-001 | Create new genealogy from scratch | E2E | Happy path |
| GEN-002 | Merge two genealogies | Integration | Complex operations |
| GEN-003 | Delete genealogy with confirmation | E2E | Data safety |
| GEN-004 | Rename genealogy database | Integration | Metadata updates |
| GEN-005 | View genealogy statistics | Unit | Calculation accuracy |

#### 3. User Interface (MEDIUM PRIORITY)

| Test ID | Scenario | Type | Coverage |
|---------|----------|------|----------|
| UI-001 | Navigate between setup pages | E2E | User workflow |
| UI-002 | Form validation and error display | Integration | Input handling |
| UI-003 | Responsive design across devices | Visual | Layout consistency |
| UI-004 | Internationalization (FR/EN) | E2E | Localization |
| UI-005 | Accessibility compliance | Automated | WCAG standards |

#### 4. System Operations (MEDIUM PRIORITY)

| Test ID | Scenario | Type | Coverage |
|---------|----------|------|----------|
| SYS-001 | Database consistency checks | Integration | Data integrity |
| SYS-002 | Cache management operations | Unit | Performance optimization |
| SYS-003 | Backup and restore procedures | E2E | Disaster recovery |
| SYS-004 | System configuration updates | Integration | Admin functions |

#### 5. Binary Tools (LOW PRIORITY)

| Test ID | Scenario | Type | Coverage |
|---------|----------|------|----------|
| BIN-001 | ged2gwb conversion accuracy | Functional | Data transformation |
| BIN-002 | gwb2ged round-trip consistency | Functional | Data preservation |
| BIN-003 | Database cleanup operations | Functional | Maintenance tools |
| BIN-004 | Consanguinity calculations | Unit | Algorithm correctness |

### Test Data Strategy

#### Test Datasets
- **Small dataset**: 50 persons, 3 generations (development/quick tests)
- **Medium dataset**: 1,000 persons, 8 generations (integration tests)
- **Large dataset**: 10,000+ persons, 15+ generations (performance tests)
- **Edge cases**: Malformed data, special characters, circular references

#### Data Management
- **Version controlled fixtures** in `tests/functional/samples/`
- **Generated test data** for performance and stress testing
- **Anonymized production data** for staging environment
- **Cleanup procedures** for test isolation

---

## Test Environments

### 1. Local Development
```yaml
# docker-compose.test.yml
services:
  geneweb-test:
    build:
      context: ./geneweb
      dockerfile: Dockerfile
    environment:
      - NODE_ENV=test
    volumes:
      - ./tests:/tests
    ports:
      - "2316:2316"
      - "2317:2317"
```

**Characteristics:**
- Fast feedback loop
- Individual developer control
- Seeded test data
- Docker-based consistency

### 2. CI/CD Pipeline
```yaml
# .github/workflows/test.yml
name: Test Suite
on: [push, pull_request]
jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - name: Run OCaml unit tests
        run: dune exec -- test/util_test.exe
      - name: Run TypeScript unit tests
        run: npm test -- --coverage
```

**Characteristics:**
- Ephemeral environments
- Parallel execution
- Artifact collection
- Quality gates

### 3. Staging Environment
```dockerfile
# Staging deployment
FROM ubuntu:24.04
COPY --from=builder /app/distribution /opt/geneweb
EXPOSE 2316 2317
CMD ["/opt/geneweb/gwd.sh"]
```

**Characteristics:**
- Production-like configuration
- Large anonymized datasets
- Performance baselines
- Security scanning

### 4. Pre-Production
**Characteristics:**
- Exact production mirrors
- Limited destructive testing
- Release candidate validation
- Final smoke tests

---

## Tools & Frameworks

### Testing Frameworks

#### Frontend (TypeScript/React/Next.js)
```json
{
  "devDependencies": {
    "@testing-library/react": "^13.4.0",
    "@testing-library/jest-dom": "^5.16.5",
    "@testing-library/user-event": "^14.4.3",
    "vitest": "^0.34.0",
    "@vitest/ui": "^0.34.0",
    "jsdom": "^22.1.0"
  }
}
```

#### Backend (OCaml)
```ocaml
(* dune-project *)
(package
 (name geneweb)
 (depends
  ocaml
  dune
  (alcotest :with-test)
  (ounit2 :with-test)
  (bisect_ppx :with-test)))
```

#### E2E Testing (Playwright)
```json
{
  "devDependencies": {
    "@playwright/test": "^1.47.0",
    "typescript": "^5.5.0"
  }
}
```

#### Functional Testing (Python)
```requirements.txt
pytest>=7.0.0
pytest-xdist>=3.0.0
pytest-html>=3.0.0
```

### Quality & Coverage Tools

#### Code Coverage
- **TypeScript**: c8/istanbul via Vitest
- **OCaml**: bisect_ppx
- **Python**: pytest-cov

#### Static Analysis
- **TypeScript**: ESLint, TypeScript strict mode
- **OCaml**: ocaml-lsp, dune warnings
- **Python**: flake8, mypy

#### Security Scanning
- **Dependencies**: npm audit, Snyk
- **Container**: Docker Bench, Trivy
- **Web App**: OWASP ZAP

### Performance Testing
- **Client-side**: Lighthouse via Playwright
- **API Load**: k6 or Artillery
- **Database**: Custom OCaml profiling

---

## Coverage & Quality Metrics

### Coverage Targets

| Component | Statements | Branches | Functions | Lines |
|-----------|------------|----------|-----------|-------|
| **TypeScript** | ≥85% | ≥80% | ≥85% | ≥85% |
| **OCaml** | ≥80% | ≥75% | ≥80% | ≥80% |
| **Python** | ≥90% | ≥85% | ≥90% | ≥90% |

### Quality Gates

#### Pull Request Requirements
- [ ] All unit tests pass
- [ ] Coverage thresholds met
- [ ] E2E smoke tests pass (Chromium)
- [ ] No critical security vulnerabilities
- [ ] Performance benchmarks within 10% of baseline

#### Release Requirements
- [ ] Full E2E test suite passes (all browsers)
- [ ] Performance SLAs met
- [ ] Security scan clean
- [ ] Accessibility compliance verified
- [ ] Documentation updated

### Service Level Agreements (SLAs)

| Metric | Target (p95) | Measurement |
|--------|--------------|-------------|
| **Home page load** | <1.5s | Lighthouse |
| **GEDCOM import (10MB)** | <90s | Custom timing |
| **Export genealogy** | <120s | Custom timing |
| **Page navigation** | <1.0s | Navigation API |
| **Search results** | <2.0s | Custom timing |

### Mutation Testing
```json
{
  "stryker": {
    "mutationScore": {
      "thresholds": {
        "high": 80,
        "low": 70,
        "break": 60
      }
    }
  }
}
```

---

## CI/CD Integration

### Pipeline Structure

```yaml
# Complete CI/CD Pipeline
stages:
  - lint
  - unit-test
  - integration-test
  - security-scan
  - performance-test
  - deploy-staging
  - e2e-test
  - deploy-production
```

### Quality Gates by Stage

#### Stage 1: Static Analysis & Unit Tests
```yaml
lint-and-unit:
  parallel:
    matrix:
      - COMPONENT: [frontend, backend, tests]
  script:
    - make lint-${COMPONENT}
    - make test-unit-${COMPONENT}
    - make coverage-${COMPONENT}
  coverage: '/Coverage: \d+\.\d+%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
```

#### Stage 2: Integration & E2E Tests
```yaml
integration-test:
  services:
    - docker:dind
  script:
    - docker-compose -f docker-compose.test.yml up -d
    - npm run test:integration
    - docker-compose down
  artifacts:
    when: always
    paths:
      - test-results/
      - playwright-report/
```

#### Stage 3: Performance & Security
```yaml
performance-security:
  parallel:
    - script: npm run test:performance
    - script: npm run security:scan
  artifacts:
    reports:
      performance: performance-report.json
      sast: security-report.json
```

### Artifact Management
- **Test Reports**: HTML, JUnit XML, coverage reports
- **Performance Data**: Lighthouse scores, timing metrics
- **Security Scans**: SARIF format for GitHub integration
- **Screenshots/Videos**: Playwright test failures
- **Container Images**: Tagged with commit SHA

---

## Test Execution Guidelines

### Local Development Workflow

#### TDD Development Cycle
```bash
# 1. Write failing test (RED)
npm run test:watch  # Continuous test running

# 2. Implement feature (GREEN)
# Write minimal code to pass test

# 3. Refactor (REFACTOR)
npm run test        # Ensure all tests pass
npm run lint:fix    # Code quality
```

#### Pre-Commit Checklist
```bash
# Run before every commit
make pre-commit-check
# Includes:
# - Unit tests
# - Linting
# - Type checking
# - Coverage validation
```

### Continuous Integration

#### Pull Request Validation
```yaml
pr-validation:
  strategy:
    matrix:
      os: [ubuntu-latest, windows-latest, macos-latest]
      node: [18, 20]
  steps:
    - name: Install dependencies
      run: npm ci
    - name: Run tests
      run: npm run test:ci
    - name: E2E smoke tests
      run: npm run test:e2e:smoke
```

#### Nightly Builds
```yaml
nightly:
  schedule:
    - cron: '0 2 * * *'  # 2 AM daily
  steps:
    - name: Full test suite
      run: npm run test:all
    - name: Performance benchmarks
      run: npm run test:performance
    - name: Mutation testing
      run: npm run test:mutation
```

### Test Environment Management

#### Environment Provisioning
```bash
#!/bin/bash
# scripts/setup-test-env.sh

# Start services
docker-compose -f docker-compose.test.yml up -d

# Wait for services
./scripts/wait-for-services.sh

# Seed test data
./scripts/seed-test-data.sh

# Run health checks
./scripts/health-check.sh
```

#### Cleanup Procedures
```bash
#!/bin/bash
# scripts/cleanup-test-env.sh

# Remove test databases
rm -rf /tmp/geneweb-test-*

# Stop containers
docker-compose -f docker-compose.test.yml down -v

# Clean artifacts
rm -rf test-results/ playwright-report/
```

---

## Risk Management

### Risk Assessment Matrix

| Risk | Probability | Impact | Mitigation |
|------|-------------|---------|------------|
| **Large GEDCOM import failure** | Medium | High | Performance tests, timeout handling, progress indicators |
| **Data corruption during merge** | Low | Critical | Backup procedures, rollback mechanisms, integrity checks |
| **Cross-browser compatibility** | High | Medium | Multi-browser E2E testing, progressive enhancement |
| **Security vulnerability** | Medium | High | Regular security scans, dependency updates, OWASP compliance |
| **Performance regression** | High | Medium | Continuous performance monitoring, SLA alerts |

### Test Data Security

#### Sensitive Data Handling
- **No production data** in development/CI environments
- **Anonymization scripts** for staging data
- **Data retention policies** for test artifacts
- **Access controls** for test environments

#### Privacy Compliance
- **GDPR compliance** for EU data subjects
- **Data minimization** in test datasets
- **Consent management** in test scenarios
- **Right to erasure** implementation testing

### Flaky Test Management

#### Detection & Analysis
```yaml
# Flaky test detection
flaky-test-detection:
  script:
    - npm run test:repeat -- --times=10
    - npm run analyze:flaky-tests
  artifacts:
    reports:
      junit: flaky-test-report.xml
```

#### Remediation Process
1. **Immediate**: Skip flaky tests with issue links
2. **Short-term**: Root cause analysis within 48 hours
3. **Long-term**: Fix or remove chronically flaky tests

### Disaster Recovery Testing
- **Backup verification**: Regular restore tests
- **Database recovery**: Point-in-time restoration
- **Service resilience**: Chaos engineering practices
- **Documentation**: Runbooks for common scenarios

---

## Conclusion

This testing strategy provides a comprehensive framework for ensuring the quality, reliability, and maintainability of the GeneWeb project. By adopting TDD practices and maintaining high standards for test coverage and automation, we can deliver a robust genealogy management system that meets user needs and business requirements.

### Key Success Metrics
- **Test Coverage**: Maintain >85% across all components
- **Build Success Rate**: >95% for all CI/CD pipelines
- **Performance SLAs**: Meet all defined targets consistently
- **Security**: Zero critical vulnerabilities in production
- **User Satisfaction**: Minimal production defects

### Continuous Improvement
- **Weekly test reviews**: Assess flaky tests, coverage gaps
- **Monthly strategy updates**: Incorporate new tools, practices
- **Quarterly retrospectives**: Team feedback, process optimization
- **Annual strategy review**: Align with business objectives

For questions or suggestions regarding this testing strategy, please contact the QA Lead or create an issue in the project repository.