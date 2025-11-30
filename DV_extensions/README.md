# DV_extensions

Extension of DV-Mathematics (Dimensions-Vectors) to DV4 (quaternions) and DV8 (octonions). This library implements the hierarchical expansion from DV2 (complex-like) to higher dimensions, with geometric handling of singularities like division by zero via depth rotations.

Born from a thought experiment on singularities (e.g., black holes, division by zero), DV-Space adds an orthogonal depth dimension to preserve information without loss. It maintains norms, avoids infinity, and is contradiction-free—unlike Riemann spheres or wheel algebras.

## Overview (from Scientific Report)

DV-Mathematics offers a fresh take on handling singularities in an algebraic framework. It expands real numbers with depth dimensions, shifting information via rotations at problematic points. Key features:
- **DV2**: Isomorphic to complex numbers (C), commutative, associative, with TR (depth rotation) for zero-division.
- **DV4**: Isomorphic to quaternions (H), non-commutative, associative, with GTR1-3 rotations, su(2) Lie algebra for spin.
- **DV8**: Isomorphic to octonions (O), non-commutative, non-associative, with GTR1-7 rotations (exceptional via Hurwitz theorem).
- Applications: Quantum mechanics (wave functions, spin), QFT (regularized propagators), numerics (stable division), geometry, and potential string theory links.

For the original DV foundations, see [IMalaspina](https://github.com/IMalaspina/dvmath).

## Installation

Prerequisites:
- Python 3.7+
- Install dependencies: `pip install -r requirements.txt`

Clone and use:
```bash
git clone https://github.com/your-username/DV_extensions.git
cd DV_extensions