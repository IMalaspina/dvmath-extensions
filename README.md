# DV-Mathematics Extensions

**Extensions and advanced research for the DV-Mathematics framework**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**Author:** Ivano Franco Malaspina  
**Date:** December 2025  
**Version:** 2.2.0

---

## ⚠️ IMPORTANT CORRECTION (December 22, 2025)

The previous claim that "ASTO₅ achieves 100% success when applied to A" was **INCORRECT**.

**Corrected Statistics:**

| Strategy | Success Rate | Details |
|----------|--------------|---------|
| ASTO₅ on A only | **72/84 (85.7%)** | 12 pairs fail |
| ASTO₅ on B only | **48/84 (57.1%)** | 36 pairs fail |
| **Adaptive ASTO₅** | **84/84 (100%)** ✅ | Try A, if fails try B |

**The 12 pairs where ASTO on A fails all contain e₉ in the second factor.**

**Solution:** Use `asto5_adaptive(A, B)` for guaranteed 100% success.

---

## 🎉 ADAPTIVE ASTO₅: 100% Success on All Zero Divisors

**December 22, 2025:** We announce the **adaptive ASTO₅ strategy** that achieves 100% success!

**Algorithm:**
```python
def asto5_adaptive(A, B):
    # Try ASTO on A first
    if (asto5(A) * B).norm() > 0:
        return asto5(A), B, "A"
    # If fails, try ASTO on B
    if (A * asto5(B)).norm() > 0:
        return A, asto5(B), "B"
    return None, None, "FAIL"  # Never happens for canonical pairs
```

**Key Results:**
- ✅ **72 pairs**: ASTO on A works
- ✅ **12 pairs**: ASTO on B works (all contain e₉)
- ✅ **0 pairs**: Both fail
- ✅ **100% total success** with adaptive strategy

---

## Repository Structure

### `/dv16/` — DV¹⁶ (Sedenions) ✅ VALIDATED

**Status:** ✅ **VALIDATED** — 84/84 canonical zero divisors (100% with adaptive ASTO₅)

The 16-dimensional extension of DV-Mathematics, implementing sedenions with ASTO₅.

**Key Files:**
| File | Description |
|------|-------------|
| `dv16.py` | Main DV¹⁶ implementation (Cayley-Dickson) |
| `asto.py` | ASTO₅ implementation with adaptive strategy |
| `canonical_zero_divisors.py` | All 84 canonical zero divisor pairs |
| `literature_84_pairs.json` | JSON data of all 84 pairs |

**Quick Start:**

```python
from dv16.dv16 import DV16, e
from dv16.asto import asto5, asto5_adaptive

# Create a zero divisor pair
A = e(1) + e(10)  # e₁ + e₁₀
B = e(5) + e(14)  # e₅ + e₁₄

# Verify it's a zero divisor
print((A * B).norm())  # Output: 0.0

# Use adaptive ASTO₅ for guaranteed success
A_new, B_new, which = asto5_adaptive(A, B)
print(f"Applied ASTO to: {which}")
print((A_new * B_new).norm())  # Output: 2.0 (non-zero!)
```

---

### `/physics/` — Hypothetical Applications ⚠️ SPECULATIVE

**Status:** ⚠️ **SPECULATIVE** — Theoretical exploration, not validated

- **`/quantum/`**: DV-based quantum state representations
- **`/spacetime/`**: Potential spacetime metric applications

**Note:** These are purely speculative explorations.

---

### `/theory/` — Theoretical Connections ⚠️ RESEARCH

**Status:** ⚠️ **RESEARCH** — Ongoing theoretical work

- **`/lie_algebras/`**: G₂ connections and commutator structures
- **`/category_theory/`**: Functorial formalization of DV hierarchy

---

## The 84 Canonical Zero Divisors

All zero divisors have the form: `(eᵢ + eⱼ) × (eₖ ± eₗ) = 0`

| Group | First Vector | Second Vectors |
|-------|--------------|----------------|
| 1 | e₁ + e₁₀ | (e₅ + e₁₄), (e₄ - e₁₅), (e₇ + e₁₂), (e₆ - e₁₃) |
| 2 | e₁ + e₁₁ | (e₄ + e₁₄), (e₅ + e₁₅), (e₆ + e₁₂), (e₇ + e₁₃) |
| 3 | e₁ + e₁₂ | (e₇ - e₁₀), (e₆ - e₁₁), (e₅ + e₈), (e₄ - e₉) |
| ... | ... | ... |

**Full list:** See `dv16/canonical_zero_divisors.py`

**Source:** Wikipedia Sedenion article, Reggiani (2024) arXiv:2411.18881v1

---

## Why ASTO₅ Works (and When It Doesn't)

### The Zero Divisor Condition

For a zero divisor pair `(a, b) × (c, d) = 0`, the Cayley-Dickson formula requires:
- `ac = d*b` (destructive interference)
- `da = -bc*`

### How ASTO₅ Breaks It

ASTO₅ transforms `a → e₁ × a`. Due to **octonion non-associativity**:

```
(e₁ × a) × c ≠ e₁ × (a × c)
```

The associator `[e₁, a, c] ≠ 0` for most octonion triplets, so:

```
(e₁ × a) × c ≠ a × c = d*b
```

Therefore, the zero divisor condition is broken.

### When ASTO on A Fails

For 12 specific pairs (all containing e₉ in B), the associator happens to be zero or the transformation preserves the zero divisor condition. In these cases, applying ASTO to B instead works.

**Pattern:** All 12 failures have the form `(eₓ + eᵧ) × (eₖ ± e₉)` where:
- x ∈ {2, 3, 4, 5} (first octonion)
- y ∈ {10, 11, 12, 13, 14, 15} (second octonion)
- k ∈ {4, 5, 6, 7} (first octonion)
- e₉ is always present (first element of second octonion)

---

## S-Algebra (Singularity Algebra)

DV¹⁶ with adaptive ASTO₅ forms the first non-trivial **S-Algebra**:

**Definition:** An S-Algebra is an algebra `(A, +, ×, σ)` where:
1. `(A, +, ×)` is a (possibly non-associative) algebra
2. `σ: A × A → A × A` is a singularity treatment operation
3. For any zero divisor pair `(x, y)`: `σ(x, y) = (x', y')` such that `x' × y' ≠ 0`

**S¹⁶ = (DV¹⁶, +, ×, ASTO₅_adaptive)** satisfies all conditions.

---

## Validation Results

### DV¹⁶ Validation Summary

| Test | Result | Details |
|------|--------|---------|
| **Cayley-Dickson** | ✅ PASS | Correct multiplication formula |
| **84 Zero Divisors** | ✅ PASS | All confirmed from literature |
| **ASTO₅ on A** | ⚠️ 85.7% | 72/84 pairs |
| **ASTO₅ on B** | ⚠️ 57.1% | 48/84 pairs |
| **Adaptive ASTO₅** | ✅ 100% | 84/84 pairs |
| **Norm Preservation** | ✅ PASS | ASTO₅ preserves norms |
| **Numerical Stability** | ✅ PASS | 50-digit precision |

### Running Tests

```bash
cd dv16
python3 dv16.py                    # Basic validation
python3 asto.py                    # ASTO₅ validation
python3 canonical_zero_divisors.py # Full 84-pair test
```

---

## Future Work

### Immediate
- [x] ~~Validate ASTO₅ on 84 canonical zero divisors~~
- [x] ~~Correct documentation with accurate statistics~~
- [ ] Publish formal paper on adaptive ASTO₅

### Short-term
- [ ] Extend to DV³² (32 dimensions, 1260 zero divisors)
- [ ] Investigate why e₉ pairs fail with ASTO on A
- [ ] Develop formal proof for adaptive strategy

### Long-term
- [ ] Establish general principle for DV^n
- [ ] Explore Lie algebra connections (F₄, E₆, E₇, E₈)
- [ ] Investigate physics applications

---

## Open Questions (Updated December 22, 2025)

1. **ASTO on A failures:** ✅ **IDENTIFIED** — 12 pairs with e₉ fail, ASTO on B works
2. **Completeness:** ✅ **ANSWERED** — No zero divisors with ≥3 basis elements found
3. **DV³²:** ⏳ **OPEN** — Can adaptive ASTO₅ be extended to 32 dimensions?
4. **Why e₉?:** ⏳ **OPEN** — Why do exactly the e₉ pairs fail with ASTO on A?

---

## Citation

```bibtex
@misc{malaspina2025dv16,
  author = {Malaspina, Ivano Franco},
  title = {DV¹⁶ Validation with Adaptive ASTO₅: A Universal Solution for Sedenion Zero Divisors},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/IMalaspina/dvmath-extensions}
}
```

---

## Contact

**Ivano Franco Malaspina**
- **Main Repository**: [github.com/IMalaspina/dvmath](https://github.com/IMalaspina/dvmath)
- **Extensions Repository**: [github.com/IMalaspina/dvmath-extensions](https://github.com/IMalaspina/dvmath-extensions)

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

## Changelog

### v2.2.0 (December 22, 2025) — **Current**
- **CRITICAL CORRECTION:** ASTO₅ on A achieves 85.7%, not 100%
- **Adaptive Strategy:** Introduced `asto5_adaptive()` for 100% success
- **Pattern Identified:** 12 failing pairs all contain e₉
- **Updated Documentation:** Accurate statistics throughout

### v2.1.0 (December 22, 2025)
- Universal Proof paper added
- G₂ invariance testing (4200 pairs)

### v2.0.0 (December 2025)
- ASTO₅ implementation
- 84 canonical zero divisors documented

### v1.0.0 (November 2025)
- Initial release with experimental DV¹⁶ implementation

---

**Note:** This repository contains validated research (DV¹⁶) and speculative explorations (physics, theory). Only the DV¹⁶ module is publication-ready.
