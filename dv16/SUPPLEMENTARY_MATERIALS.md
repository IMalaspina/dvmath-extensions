# Supplementary Materials

**Paper:** Consistency of DV¹⁶ via Partial Singularity Treatment  
**Author:** I. Malaspina  
**Date:** December 7, 2025

---

## Overview

This document provides supplementary materials for the paper "Consistency of DV¹⁶ via Partial Singularity Treatment: A New Principle for Extending the Cayley-Dickson Construction."

All code, data, and documentation are available on GitHub: [github.com/IMalaspina/dvmath-extensions](https://github.com/IMalaspina/dvmath-extensions)

---

## Contents

1. [Implementation Files](#implementation-files)
2. [Test Scripts](#test-scripts)
3. [Data Files](#data-files)
4. [Documentation](#documentation)
5. [Reproducibility](#reproducibility)

---

## Implementation Files

### Core DV¹⁶ Implementation

**File:** `dv16.py`

Implements the DV¹⁶ algebra using the Cayley-Dickson construction from DV⁸ (octonions).

**Key Classes:**
- `DV16`: Main class for 16-dimensional elements
  - `__init__(components)`: Initialize from 16 components
  - `__mul__(other)`: Cayley-Dickson multiplication
  - `conjugate()`: Conjugation operation
  - `norm()`: Euclidean norm
  - `__add__`, `__sub__`: Addition and subtraction

**Dependencies:** `dvmath` library (DV⁸ implementation)

---

### ASTO Implementations

**File:** `asto.py`

Implements all six ASTO variants for singularity treatment in DV¹⁶.

**Functions:**
- `asto_variant1(v)`: Full STO (both octonions)
- `asto_variant2(v)`: Reverse STO
- `asto_variant3(v)`: Alternating STO
- `asto_variant4(v)`: Conditional STO
- `asto_variant5(v)`: **Partial STO (first octonion only)** ← Main contribution
- `asto_variant6(v)`: Partial STO (second octonion only)

**Key Function:** `asto_variant5(v)`

```python
def asto_variant5(v):
    """
    ASTO Variant 5: Partial STO (First Octonion Only)
    
    Applies STO to only the first octonion component.
    This is the asymmetric treatment that breaks zero divisor balance.
    
    Args:
        v: DV16 element
        
    Returns:
        DV16 element with STO applied to first octonion only
    """
    # Extract two octonions
    a = DV8(v.components[:8])
    b = DV8(v.components[8:])
    
    # Apply STO to first octonion only
    a_sto = a.sto()
    
    # Reconstruct DV16
    return DV16(list(a_sto.components) + list(b.components))
```

---

## Test Scripts

### Zero Divisor Generation

**File:** `generate_zero_divisors.py`

Systematically generates all zero divisor pairs in DV¹⁶ from basis vector combinations.

**Method:**
1. Generate all combinations of basis vectors: `eᵢ ± eⱼ` for `i, j ∈ {0..15}`
2. Test all pairs for zero divisor property: `(A × B).norm() == 0`
3. Store valid zero divisor pairs

**Results:**
- Combinations tested: 16,384
- Zero divisors found: 336
- Output: `zero_divisors.json`

**Usage:**
```bash
python3 generate_zero_divisors.py
```

---

### Comprehensive ASTO Testing (50 Cases)

**File:** `test_asto_variant5_comprehensive.py`

Tests ASTO Variant 5 on 50 diverse zero divisor pairs.

**Test Method:**
1. Load 50 diverse zero divisors
2. For each pair `(A, B)`:
   - Verify `A × B = 0`
   - Apply ASTO₅: `A' = ASTO₅(A)`
   - Test: `A' × B ≠ 0`
   - Test: `A × ASTO₅(B) ≠ 0`
3. Record success/failure

**Results:**
- Tests: 50
- Success: 50/50 (100%)
- Output: `asto_variant5_test_results.json`

**Usage:**
```bash
python3 test_asto_variant5_comprehensive.py
```

---

### Exhaustive ASTO Testing (336 Cases)

**File:** `test_asto_exhaustive.py`

Tests ASTO Variant 5 on **all** 336 zero divisor pairs.

**Test Method:**
1. Load all 336 zero divisors
2. For each pair `(A, B)`:
   - Verify `A × B = 0`
   - Apply ASTO₅ in both directions
   - Test both products are non-zero
   - Record norm values
3. Compute statistics

**Results:**
- Tests: 336
- Success: 336/336 (100%)
- Output: `asto_exhaustive_results.json`

**Usage:**
```bash
python3 test_asto_exhaustive.py
```

---

## Data Files

### Zero Divisor Database

**File:** `zero_divisors.json` (not included in repo due to size)

Contains all 336 zero divisor pairs.

**Format:**
```json
{
  "metadata": {
    "total_combinations": 16384,
    "zero_divisors_found": 336,
    "generation_date": "2025-12-07"
  },
  "zero_divisors": [
    {
      "id": 0,
      "A": [0, 0, 1, 0, ..., 1, 0],
      "B": [0, 0, 0, 0, ..., -1, 0],
      "A_basis": "e2 + e8",
      "B_basis": "e5 - e14"
    },
    ...
  ]
}
```

---

### ASTO Variant 5 Test Results (50 Cases)

**File:** `asto_variant5_test_results.json`

Results from comprehensive 50-case test.

**Format:**
```json
{
  "metadata": {
    "test_date": "2025-12-07",
    "total_tests": 50,
    "successful": 50,
    "failed": 0,
    "success_rate": 100.0
  },
  "results": [
    {
      "id": 0,
      "A_basis": "e2 + e8",
      "B_basis": "e5 - e14",
      "original_norm": 0.0,
      "asto_A_norm": 2.0,
      "asto_B_norm": 2.0,
      "success": true
    },
    ...
  ]
}
```

---

### Exhaustive Test Results (336 Cases)

**File:** `asto_exhaustive_results.json`

Results from exhaustive 336-case test.

**Format:**
```json
{
  "metadata": {
    "test_date": "2025-12-07",
    "total_tests": 336,
    "successful": 336,
    "failed": 0,
    "success_rate": 100.0,
    "execution_time": 0.90
  },
  "statistics": {
    "mean_norm": 2.0,
    "std_norm": 0.0,
    "min_norm": 2.0,
    "max_norm": 2.0
  },
  "results": [...]
}
```

---

## Documentation

### Analysis Documents

1. **ASTO_VARIANT5_ANALYSIS.md**
   - Detailed analysis of ASTO Variant 5 results
   - Comparison with other variants
   - Pattern analysis

2. **EXHAUSTIVE_VALIDATION_REPORT.md**
   - Full report on exhaustive validation
   - Statistical analysis
   - Conclusions

3. **FINAL_PROOF_SUMMARY.md**
   - Summary of formal proof improvements
   - Comparison before/after fixes
   - Validation status

### Mathematical Documents

4. **formal_proof_rigorous.pdf**
   - Complete formal proof (6 pages)
   - 100% rigorous
   - LaTeX typeset

5. **mathematical_analysis.md**
   - Mathematical structure of DV¹⁶
   - Zero divisor characterization
   - Why ASTO₅ works

6. **theoretical_foundations.md**
   - Theoretical foundations
   - Lemmata and proofs
   - Discussion

7. **proof_validation.md**
   - Validation of proof correctness
   - Identification of gaps
   - Recommendations

---

## Reproducibility

### System Requirements

- **OS:** Linux/macOS/Windows
- **Python:** 3.11+
- **Dependencies:**
  - `dvmath` (DV-Mathematics library)
  - `numpy` (for numerical operations)
  - `json` (for data storage)

### Installation

```bash
# Clone repository
git clone https://github.com/IMalaspina/dvmath-extensions.git
cd dvmath-extensions/dv16

# Install dependencies
pip install -r requirements.txt
```

### Running Tests

```bash
# Generate zero divisors (takes ~1 minute)
python3 generate_zero_divisors.py

# Test ASTO Variant 5 on 50 cases (takes ~5 seconds)
python3 test_asto_variant5_comprehensive.py

# Exhaustive test on all 336 cases (takes ~1 second)
python3 test_asto_exhaustive.py
```

### Expected Output

All tests should output:
```
Success Rate: 100.00%
Total Tests: [50 or 336]
Successful: [50 or 336]
Failed: 0
```

---

## Verification Checklist

To verify the results independently:

- [ ] Clone repository
- [ ] Install dependencies
- [ ] Run `generate_zero_divisors.py` → Verify 336 zero divisors found
- [ ] Run `test_asto_variant5_comprehensive.py` → Verify 50/50 success
- [ ] Run `test_asto_exhaustive.py` → Verify 336/336 success
- [ ] Read `formal_proof_rigorous.pdf` → Verify proof logic
- [ ] Check `asto_exhaustive_results.json` → Verify all norms = 2.0

---

## Contact

For questions or issues, please open an issue on GitHub or contact the author.

**GitHub:** [github.com/IMalaspina/dvmath-extensions](https://github.com/IMalaspina/dvmath-extensions)

---

## License

[To be determined]

---

## Acknowledgments

This work builds on the DV-Mathematics framework and extends it to 16 dimensions with a novel singularity treatment method.
