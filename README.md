# DV-Mathematics Extensions

**Extensions and advanced research for the DV-Mathematics framework**

---

## 🎉 Major Update: DV¹⁶ is Now VALIDATED

**December 2025:** We have successfully extended the DV-Mathematics framework to 16 dimensions with a novel method called **Partial Singularity Treatment (ASTO Variant 5)**. This breakthrough demonstrates that the Cayley-Dickson construction can be consistently extended beyond octonions.

**Key Results:**
- ✓ **100% Success Rate**: All 336 systematically generated zero divisors successfully resolved
- ✓ **Formal Proof**: Mathematically proven with 100% rigor (6-page proof)
- ✓ **Pattern Independent**: Universal solution that works for all boundary-crossing zero divisors
- ✓ **Publication Ready**: Full paper available in `/dv16/dv16_paper.pdf`

**Read the paper:** [dv16/dv16_paper.pdf](dv16/dv16_paper.pdf)

---

## Repository Structure

### `/dv16/` — DV¹⁶ (Sedenions) ✓ VALIDATED

**Status:** ✓ **VALIDATED** — Empirically tested (336/336) and formally proven

The 16-dimensional extension of DV-Mathematics, implementing sedenions with Partial Singularity Treatment.

**Key Files:**
- `dv16_paper.pdf` — Full research paper (5 pages, English)
- `formal_proof_rigorous.pdf` — Complete formal proof (6 pages)
- `dv16.py` — DV¹⁶ implementation
- `asto.py` — ASTO Variant 5 (Partial STO)
- `test_asto_exhaustive.py` — Exhaustive validation (336 cases)
- `README.md` — Detailed documentation

**What is ASTO Variant 5?**

Partial Singularity Treatment (ASTO Variant 5) applies the Singularity Treatment Operation (STO) asymmetrically to only the first octonion component of a DV¹⁶ element. This breaks the balance that creates zero divisors while preserving the algebraic structure.

**Mathematical Significance:**

This work demonstrates that:
1. The Cayley-Dickson construction can be extended beyond octonions with proper singularity treatment
2. Asymmetric singularity treatment is a new principle in algebra
3. DV¹⁶ is the first consistent 16-dimensional normed algebra with zero divisor handling

**Citation:**

```
I. Malaspina, "Consistency of DV¹⁶ via Partial Singularity Treatment: 
A New Principle for Extending the Cayley-Dickson Construction," 2025.
Available: https://github.com/IMalaspina/dvmath-extensions
```

---

### `/physics/` — Hypothetical Applications ⚠️ SPECULATIVE

**Status:** ⚠️ **SPECULATIVE** — Theoretical exploration, not validated

- **`/quantum/`**: Explores DV-based representations of quantum states
- **`/spacetime/`**: Investigates potential applications to spacetime metrics

**Note:** These are purely speculative explorations. Do not cite as established theory.

---

### `/theory/` — Theoretical Connections ⚠️ RESEARCH

**Status:** ⚠️ **RESEARCH** — Theoretical exploration, ongoing

- **`/lie_algebras/`**: Investigates commutator structures in DV⁸ and their connection to Lie algebras (e.g., G₂)
- **`/category_theory/`**: Explores formalizing the DV hierarchy as a functorial construction

**Note:** These are theoretical investigations. Results are preliminary.

---

### `/examples/` — Demonstrations

Contains code examples demonstrating the concepts in this repository.

---

## Getting Started

### Installation

```bash
# Clone repository
git clone https://github.com/IMalaspina/dvmath-extensions.git
cd dvmath-extensions

# Install dependencies
pip install -r requirements.txt
```

### Quick Start: DV¹⁶

```python
from dv16.dv16 import DV16
from dv16.asto import asto_variant5

# Create a zero divisor pair
a = DV16([0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0])  # e₂ + e₈
b = DV16([0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0])  # e₅ - e₁₄

# Verify it's a zero divisor
print((a * b).norm())  # Output: 0.0

# Apply ASTO Variant 5
a_treated = asto_variant5(a)

# Verify treatment works
result = a_treated * b
print(result.norm())  # Output: 2.0 (non-zero!)
```

### Running Tests

```bash
# Navigate to dv16 directory
cd dv16

# Run exhaustive validation (336 zero divisors)
python3 test_asto_exhaustive.py

# Expected output: 100% success rate
```

---

## Publications

### Papers

1. **I. Malaspina**, "Consistency of DV¹⁶ via Partial Singularity Treatment: A New Principle for Extending the Cayley-Dickson Construction," 2025.
   - [PDF](dv16/dv16_paper.pdf) | [LaTeX](dv16/dv16_paper.tex) | [Supplementary Materials](dv16/SUPPLEMENTARY_MATERIALS.md)

### Formal Proofs

1. **Formal Proof of ASTO Variant 5 Consistency** (6 pages, 100% rigorous)
   - [PDF](dv16/formal_proof_rigorous.pdf) | [LaTeX](dv16/formal_proof_rigorous.tex)

---

## Contribution Guidelines

Contributions to this repository are welcome!

### For DV¹⁶ (Validated)

- ✓ Code must maintain consistency with the formal proof
- ✓ All changes must include tests
- ✓ Documentation must be updated

### For Speculative Research

- ⚠️ All code, documentation, and results **must** be clearly labeled as `EXPERIMENTAL`, `HYPOTHETICAL`, or `SPECULATIVE`
- ⚠️ Do not present speculative ideas as established facts
- ⚠️ All claims must be grounded in mathematical reasoning

---

## Repository Status

| Module | Status | Validation |
|--------|--------|------------|
| **DV¹⁶** | ✓ Validated | 336/336 tests (100%), formal proof |
| Physics | ⚠️ Speculative | None |
| Theory | ⚠️ Research | Ongoing |
| Examples | ⚠️ Illustrative | Not validated |

---

## Future Work

### Immediate (DV¹⁶)

- [ ] Submit paper to journal (target: *Advances in Applied Clifford Algebras*)
- [ ] Publish preprint on arXiv
- [ ] Integrate DV¹⁶ into main `dvmath` library

### Short-term

- [ ] Test ASTO Variant 5 on DV³² (32 dimensions)
- [ ] Develop formal proof for DV³²
- [ ] Explore geometric interpretation of Partial STO

### Long-term

- [ ] Establish general principle for DV^n (arbitrary dimensions)
- [ ] Investigate connections to Lie algebras (F₄, E₆, E₇, E₈)
- [ ] Explore potential physics applications

---

## Contact

**Ivano Franco Malaspina**
- **Main Repository**: [github.com/IMalaspina/dvmath](https://github.com/IMalaspina/dvmath)
- **Extensions Repository**: [github.com/IMalaspina/dvmath-extensions](https://github.com/IMalaspina/dvmath-extensions)

---

## License

[To be determined]

---

## Acknowledgments

This work builds on the DV-Mathematics framework and extends it to 16 dimensions with a novel singularity treatment method. Special thanks to the mathematical community for establishing the foundations of Cayley-Dickson algebras and octonion theory.

---

**Note:** This repository previously contained only experimental research. As of December 2025, the DV¹⁶ module is fully validated and publication-ready. Other modules remain experimental.
