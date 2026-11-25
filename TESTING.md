# TESTING.md - GeneWeb Project Testing Strategy & Plan

## Table of Contents
1. [Overview](#overview)
2. [Test-Driven Development (TDD) Approach](#test-driven-development-tdd-approach)
3. [Testing Strategy](#testing-strategy)
4. [Test Plan](#test-plan)
5. [CI/CD Integration](#cicd-integration)
6. [Conclusion](#conclusion)

---

## Overview

This document outlines the comprehensive testing strategy and plan for the GeneWeb project, a genealogy management system. The project consists of:

- **GeneWeb Core** (OCaml backend) - genealogy processing, GEDCOM import/export, database management
- **GWD Frontend** (TypeScript/UI) - web interface for setup, configuration, and data management
- **New GeneWeb** (Next.js/React) - modern frontend implementation
- **CLI Tools** - various binaries for data processing and maintenance

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
| IMP-002 | Export to GEDCOM format | E2E | Data integrity |

#### 2. Genealogy Management (HIGH PRIORITY)

| Test ID | Scenario | Type | Coverage |
|---------|----------|------|----------|
| GEN-001 | Create new genealogy from scratch | E2E | Happy path |
| GEN-002 | Delete genealogy with confirmation | E2E | Data safety |

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

---

## CI/CD Integration

### Pipeline Structure

```yaml
# Complete CI/CD Pipeline
stages:
  - lint
  - unit-test
  - integration-test
  - e2e-test
```

---

## Conclusion

This testing strategy provides a comprehensive framework for ensuring the quality, reliability, and maintainability of the GeneWeb project. By adopting TDD practices and maintaining high standards for test coverage and automation, we can deliver a robust genealogy management system that meets user needs and business requirements.

### Continuous Improvement
- **Weekly test reviews**: Assess flaky tests, coverage gaps
- **Monthly strategy updates**: Incorporate new tools, practices
- **Quarterly retrospectives**: Team feedback, process optimization
- **Annual strategy review**: Align with business objectives

For questions or suggestions regarding this testing strategy, please contact the QA Lead or create an issue in the project repository.