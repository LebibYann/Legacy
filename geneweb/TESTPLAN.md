# Test Plan: GWD Setup (GeneWeb Frontend)

## Overview

This test plan defines the testing strategy and scenarios for validating the GWD Setup frontend used to create, modify, and delete genealogy data in GeneWeb. The objective is to ensure that all workflows, functionality, and UI interactions work as expected.

---

## Scope

The following features and workflows will be tested:

1. **Create/Import a Genealogy**

   * Create based on a GEDCOM file (ged2gwb)
   * Create based on a GeneWeb file (gwc)
   * Create from scratch (empty database)
2. **Consult Data**

   * Consult genealogy list
   * Consult history of errors and statistics
3. **Export a Genealogy**

   * Export in GEDCOM format (gwb2ged)
   * Export in GeneWeb format (gwu)
4. **Change Configuration**

   * Parameters of database (gwf)
   * Service parameters (gwd)
   * Name and Places cache files (cache\_files)
5. **Advanced Editing Options**

   * Clean Up
   * Rename base
   * Delete base
   * Merge several bases
   * Save and Restore (gwu)
   * Consanguinity initialization
   * Update links page/family chronicle
   * Data capture
   * Compute connected components
   * Compute difference between two bases
   * Fix problems in a base

---

## Test Scenarios

### 1. Create/Import a Genealogy

| ID | Test Case                         | Precondition                | Steps                                              | Expected Result                              |
| -- | --------------------------------- | --------------------------- | -------------------------------------------------- | -------------------------------------------- |
| C1 | Create database from GEDCOM       | Valid GEDCOM file available | Upload GEDCOM → Select import option → Create base | New genealogy created with all data imported |
| C2 | Create database from GeneWeb file | Valid GWC file available    | Upload GWC → Select import option → Create base    | Genealogy imported successfully              |
| C3 | Create empty database             | None                        | Select "Create from nothing" option                | Empty base created                           |

### 2. Consult Data

| ID | Test Case           | Precondition                 | Steps                                    | Expected Result               |
| -- | ------------------- | ---------------------------- | ---------------------------------------- | ----------------------------- |
| D1 | View genealogy list | At least one database exists | Navigate to "Consult existing genealogy" | List of genealogies displayed |
| D2 | View error history  | Database with logged errors  | Navigate to "Consult history"            | Error log displayed           |

### 3. Export Genealogy

| ID | Test Case                | Precondition          | Steps                     | Expected Result        |
| -- | ------------------------ | --------------------- | ------------------------- | ---------------------- |
| E1 | Export in GEDCOM         | Valid database exists | Select "Export to GEDCOM" | Downloaded GEDCOM file |
| E2 | Export in GeneWeb format | Valid database exists | Select "Export to GWU"    | Downloaded GWU file    |

### 4. Change Configuration

| ID   | Test Case               | Precondition       | Steps                                      | Expected Result         |
| ---- | ----------------------- | ------------------ | ------------------------------------------ | ----------------------- |
| CFG1 | Edit DB parameters      | Database exists    | Access settings → Update parameters → Save | Changes saved           |
| CFG2 | Edit service parameters | Running GWD server | Update GWD config → Save                   | Server settings updated |
| CFG3 | Update cache files      | Names/places exist | Regenerate cache files                     | Cache updated           |

### 5. Advanced Editing Options

| ID    | Test Case                    | Precondition                    | Steps                     | Expected Result       |
| ----- | ---------------------------- | ------------------------------- | ------------------------- | --------------------- |
| ADV1  | Clean up base                | Base exists with redundant data | Run cleanup               | Database optimized    |
| ADV2  | Rename base                  | Base exists                     | Rename base → Confirm     | Base renamed          |
| ADV3  | Delete base                  | Base exists                     | Delete base → Confirm     | Base deleted          |
| ADV4  | Merge several bases          | Multiple bases                  | Select bases → Merge      | Unified base          |
| ADV5  | Save/Restore base            | Base exists                     | Export → Delete → Restore | Base restored         |
| ADV6  | Initialize consanguinity     | Base with data                  | Run consanguinity calc    | Relations initialized |
| ADV7  | Update family chronicle      | Base with families              | Update chronicle          | Updated links         |
| ADV8  | Data capture                 | Base exists                     | Run capture               | Captured data         |
| ADV9  | Compute connected components | Base exists                     | Run computation           | Displayed components  |
| ADV10 | Compare bases                | Two bases exist                 | Compute differences       | Differences report    |
| ADV11 | Fix problems                 | Base with errors                | Run fix                   | Errors resolved       |

---

## Test Environment

* **Frontend:** GWD Setup interface
* **Backend:** GeneWeb server (gwd)
* **Browsers:** Chrome, Firefox, Edge
* **Data:** Test GEDCOM and GWC files
* **OS:** Windows, macOS, Linux

---

## Entry and Exit Criteria

* **Entry:** All required test data prepared, server running, frontend deployed.
* **Exit:** All test cases executed; critical defects resolved.

---

## Deliverables

* Test Plan document
* Test Case documents
* Execution Report
* Bug/Defect Report

---

## Risks and Mitigations

* **Risk:** Large GEDCOM files may impact performance. **Mitigation:** Stress test with incremental data.
* **Risk:** Cache inconsistencies. **Mitigation:** Frequent cache rebuild tests.

---

## Approval

* QA Lead
* Development Lead
* Product Owner
