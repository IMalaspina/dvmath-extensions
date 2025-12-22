# DV-Mathematics Extensions

**Extensions and advanced research for the DV-Mathematics framework**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**Author:** Ivano Franco Malaspina  
**Date:** December 2025  
**Version:** 2.3.0

---

## 🎉 VALIDATED: ASTO₅ Achieves 100% Success Rate

**December 22, 2025:** ASTO₅ has been rigorously validated on all 84 canonical zero divisors.

**Results:**

| Strategy | Success Rate |
|----------|--------------|
| ASTO₅ on A | **84/84 (100%)** ✅ |
| ASTO₅ on B | **84/84 (100%)** ✅ |
| Both work | **84/84 (100%)** ✅ |

**What is ASTO₅?**

ASTO₅ (Adaptive STO Variant 5) applies the Singularity Treatment Operation asymmetrically to only the first octonion component:

```
ASTO₅(a, b) = (e₁ × a, b)
```

This breaks the destructive interference that creates zero divisors.

---

## Repository Structure

### `/dv16/` — DV¹⁶ (Sedenions) ✅ VALIDATED

**Status:** ✅ **VALIDATED** — 84/84 canonical zero divisors (100%)

The 16-dimensional extension of DV-Mathematics, implementing sedenions with ASTO₅.

**Key Files:**
| File | Description |
|------|-------------|
| `dv16.py` | Main DV¹⁶ implementation (Cayley-Dickson) |
| `asto.py` | ASTO₅ implementation (100% validated) |
| `canonical_zero_divisors.py` | All 84 canonical zero divisor pairs |
| `literature_84_pairs.json` | JSON data of all 84 pairs |

**Quick Start:**

```python
from dv16.dv16 import Sedenion, e
from dv16.asto import asto5, resolve_zero_divisor

# Create a zero divisor pair
A = e(1) + e(10)  # e₁ + e₁₀
B = e(5) + e(14)  # e₅ + e₁₄

# Verify it's a zero divisor
print((A * B).norm())  # Output: 0.0

# Apply ASTO₅
A_treated = asto5(A)

# Verify treatment works
print((A_treated * B).norm())  # Output: 2.0 (non-zero!)

# Or use the convenience function
A_new, B_new, method = resolve_zero_divisor(A, B)
print(f"Applied ASTO to: {method}")  # Output: "A"
print((A_new * B_new).norm())  # Output: 2.0
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

**Full list:** See `dv16/canonical_zero_divisors.py` or `dv16/literature_84_pairs.json`

**Source:** Wikipedia Sedenion article, Reggiani (2024) arXiv:2411.18881v1

---

## Why ASTO₅ Works

### The Zero Divisor Condition

For a zero divisor pair `(a, b) × (c, d) = 0`, the Cayley-Dickson formula requires:
- `ac = d*b` (destructive interference)
- `da = -bc*`

### How ASTO₅ Breaks It

ASTO₅ transforms `a → e₁ × a`. Due to **octonion non-associativity**:

```
(e₁ × a) × c ≠ e₁ × (a × c)
```

The associator `[e₁, a, c] ≠ 0` for the relevant octonion triplets, so:

```
(e₁ × a) × c ≠ a × c = d*b
```

Therefore, the zero divisor condition is broken.

### Formal Proof

See `docs/ASTO5_UNIVERSAL_PROOF_PAPER_EN.pdf` for the complete mathematical proof.

---

## S-Algebra (Singularity Algebra)

DV¹⁶ with ASTO₅ forms the first non-trivial **S-Algebra**:

**Definition:** An S-Algebra is an algebra `(A, +, ×, σ)` where:
1. `(A, +, ×)` is a (possibly non-associative) algebra
2. `σ: A → A` is a singularity treatment operation
3. For any zero divisor pair `(x, y)`: `σ(x) × y ≠ 0` or `x × σ(y) ≠ 0`

**S¹⁶ = (DV¹⁶, +, ×, ASTO₅)** satisfies all conditions with 100% success.

---

## Validation Results

### DV¹⁶ Validation Summary

| Test | Result | Details |
|------|--------|---------|
| **Cayley-Dickson** | ✅ PASS | Correct multiplication formula |
| **84 Zero Divisors** | ✅ PASS | All confirmed from literature |
| **ASTO₅ on A** | ✅ PASS | 84/84 (100%) |
| **ASTO₅ on B** | ✅ PASS | 84/84 (100%) |
| **Both work** | ✅ PASS | 84/84 (100%) |
| **Norm Preservation** | ✅ PASS | ASTO₅ preserves norms |
| **Numerical Stability** | ✅ PASS | 50-digit precision available |

### Running Tests

```bash
cd dv16
python3 dv16.py                    # Basic validation
python3 asto.py                    # ASTO₅ validation (100% success)
python3 canonical_zero_divisors.py # Full 84-pair test
```

---

## Future Work

### Immediate
- [x] ~~Validate ASTO₅ on 84 canonical zero divisors~~ ✅ 100%
- [ ] Publish formal paper on ASTO₅
- [ ] Integrate into main `dvmath` library

### Short-term
- [ ] Extend to DV³² (32 dimensions, 1260 zero divisors)
- [ ] Investigate G₂ manifold structure further
- [ ] Develop formal proof for higher dimensions

### Long-term
- [ ] Establish general principle for DV^n
- [ ] Explore Lie algebra connections (F₄, E₆, E₇, E₈)
- [ ] Investigate physics applications

---

## Open Questions

1. **DV³²:** Can ASTO₅ be extended to 32 dimensions? (1260 zero divisors)
2. **General Principle:** Is there a universal ASTO for all DV^n?
3. **Physics:** What are the physical implications of S-Algebras?

---

## Citation

```bibtex
@misc{malaspina2025dv16,
  author = {Malaspina, Ivano Franco},
  title = {DV¹⁶ Validation with ASTO₅: A Universal Solution for Sedenion Zero Divisors},
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

### v2.3.0 (December 22, 2025) — **Current**
- **CORRECTION:** ASTO₅ achieves 100% success on ALL 84 pairs
- **Fixed:** `canonical_zero_divisors.py` now correctly uses `literature_84_pairs.json`
- **Clarified:** The "12 failing pairs" in v2.2.0 were an artifact of incorrect data
- **Verified:** Both ASTO on A and ASTO on B work for all 84 pairs

### v2.2.0 (December 22, 2025)
- **RETRACTED:** Claimed 12 pairs failed - this was due to data error
- Added analysis scripts (still useful for verification)

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
