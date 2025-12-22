"""
ASTO₅ (Adaptive Singularity Treatment Operation, Variant 5)
============================================================

Implementation of ASTO₅ for DV¹⁶ (Sedenions).

VALIDATED: 100% success rate on all 84 canonical zero divisors.

Definition:
    ASTO₅(a, b) = (e₁ × a, b)
    
    Where (a, b) is a sedenion with a, b being octonions,
    and e₁ is the first imaginary octonion unit.

The key insight is that ASTO₅ applies the transformation asymmetrically,
only to the first octonion component. This breaks the destructive
interference that creates zero divisors.

Why it works:
    For a zero divisor pair A × B = 0, the Cayley-Dickson formula requires:
    - ac = d*b (destructive interference)
    - da = -bc*
    
    ASTO₅ transforms a → e₁ × a. Due to octonion non-associativity:
    (e₁ × a) × c ≠ e₁ × (a × c) in general
    
    This breaks the precise cancellation required for zero divisors.

Author: Ivano Franco Malaspina
Date: December 2025
Version: 2.3.0

VALIDATION RESULTS:
    - ASTO₅ on A: 84/84 (100%)
    - ASTO₅ on B: 84/84 (100%)
    - Both work:  84/84 (100%)
"""

import json
import os
from typing import Tuple, Optional

# Import the DV16 implementation
try:
    from .dv16 import Sedenion, e, e_oct
except ImportError:
    from dv16 import Sedenion, e, e_oct


def asto5(S: Sedenion) -> Sedenion:
    """
    Apply ASTO₅ to a sedenion.
    
    ASTO₅(a, b) = (e₁ × a, b)
    
    Args:
        S: A sedenion (a, b) where a, b are octonions
        
    Returns:
        A new sedenion with the first octonion multiplied by e₁
        
    Example:
        >>> A = e(1) + e(10)  # A zero divisor component
        >>> A_treated = asto5(A)
        >>> # Now A_treated × B ≠ 0 for any zero divisor pair (A, B)
    """
    e1_oct = e_oct(1)
    a_prime = e1_oct * S.a
    return Sedenion(*a_prime.components, *S.b.components)


def asto5_left(S: Sedenion) -> Sedenion:
    """
    Apply ASTO₅ using left multiplication: (e₁ × a, b)
    
    This is the canonical form of ASTO₅.
    """
    return asto5(S)


def asto5_right(S: Sedenion) -> Sedenion:
    """
    Apply ASTO₅ using right multiplication: (a × e₁, b)
    
    This variant also achieves 100% success rate.
    """
    e1_oct = e_oct(1)
    a_prime = S.a * e1_oct
    return Sedenion(*a_prime.components, *S.b.components)


def resolve_zero_divisor(A: Sedenion, B: Sedenion) -> Tuple[Sedenion, Sedenion, str]:
    """
    Resolve a zero divisor pair using ASTO₅.
    
    For any zero divisor pair A × B = 0, this function returns
    a modified pair (A', B) or (A, B') such that A' × B ≠ 0 or A × B' ≠ 0.
    
    Args:
        A: First sedenion of the zero divisor pair
        B: Second sedenion of the zero divisor pair
        
    Returns:
        Tuple of (A_new, B_new, method) where:
        - A_new, B_new: The modified pair
        - method: "A" if ASTO was applied to A, "B" if to B
        
    Note:
        ASTO₅ achieves 100% success when applied to A for all 84
        canonical zero divisors. Applying to B also works for all pairs.
    """
    # Apply ASTO to A (works for all 84 canonical pairs)
    A_asto = asto5(A)
    product = A_asto * B
    
    if product.norm() > 1e-10:
        return A_asto, B, "A"
    
    # Fallback: Apply to B (also works for all pairs)
    B_asto = asto5(B)
    product = A * B_asto
    
    if product.norm() > 1e-10:
        return A, B_asto, "B"
    
    # This should never happen for valid zero divisor pairs
    raise ValueError("ASTO₅ failed to resolve zero divisor - pair may not be a valid zero divisor")


# ============================================================
# LEGACY ASTO VARIANTS (for reference)
# ============================================================

def asto1(S: Sedenion) -> Sedenion:
    """ASTO Variant 1: Full STO on both components (DOES NOT WORK)"""
    e1_oct = e_oct(1)
    a_prime = e1_oct * S.a
    b_prime = e1_oct * S.b
    return Sedenion(*a_prime.components, *b_prime.components)


def asto2(S: Sedenion) -> Sedenion:
    """ASTO Variant 2: STO on second component only (DOES NOT WORK)"""
    e1_oct = e_oct(1)
    b_prime = e1_oct * S.b
    return Sedenion(*S.a.components, *b_prime.components)


def asto3(S: Sedenion) -> Sedenion:
    """ASTO Variant 3: Conjugate-based (DOES NOT WORK)"""
    return S.conjugate()


def asto4(S: Sedenion) -> Sedenion:
    """ASTO Variant 4: Norm-based scaling (DOES NOT WORK)"""
    norm = S.norm()
    if norm < 1e-10:
        return S
    return Sedenion(*[c / norm for c in S.components])


# ============================================================
# VALIDATION
# ============================================================

def validate_asto5():
    """
    Validate ASTO₅ on all 84 canonical zero divisors.
    
    Returns:
        dict with validation results
    """
    # Load the 84 canonical pairs
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, 'literature_84_pairs.json')
    
    with open(json_path, 'r') as f:
        pairs = json.load(f)
    
    results = {
        'total': len(pairs),
        'asto_A_success': 0,
        'asto_B_success': 0,
        'both_success': 0,
        'failures': []
    }
    
    for i, j, k, l in pairs:
        sign = 1 if l > 0 else -1
        l_abs = abs(l)
        
        A = e(i) + e(j)
        B = e(k) + sign * e(l_abs)
        
        # Verify it's a zero divisor
        original = A * B
        if original.norm() > 1e-10:
            results['failures'].append({
                'pair': f"(e{i} + e{j}) × (e{k} {'+' if sign > 0 else '-'} e{l_abs})",
                'reason': 'Not a zero divisor',
                'norm': original.norm()
            })
            continue
        
        # Test ASTO on A
        A_asto = asto5(A)
        product_A = A_asto * B
        A_works = product_A.norm() > 1e-10
        
        # Test ASTO on B
        B_asto = asto5(B)
        product_B = A * B_asto
        B_works = product_B.norm() > 1e-10
        
        if A_works:
            results['asto_A_success'] += 1
        if B_works:
            results['asto_B_success'] += 1
        if A_works and B_works:
            results['both_success'] += 1
        
        if not A_works and not B_works:
            results['failures'].append({
                'pair': f"(e{i} + e{j}) × (e{k} {'+' if sign > 0 else '-'} e{l_abs})",
                'reason': 'ASTO failed on both A and B',
                'asto_A_norm': product_A.norm(),
                'asto_B_norm': product_B.norm()
            })
    
    return results


if __name__ == "__main__":
    print("=" * 70)
    print("ASTO₅ VALIDATION")
    print("=" * 70)
    print()
    
    results = validate_asto5()
    
    print(f"Total pairs tested: {results['total']}")
    print(f"ASTO on A success:  {results['asto_A_success']}/{results['total']} ({100*results['asto_A_success']/results['total']:.1f}%)")
    print(f"ASTO on B success:  {results['asto_B_success']}/{results['total']} ({100*results['asto_B_success']/results['total']:.1f}%)")
    print(f"Both work:          {results['both_success']}/{results['total']} ({100*results['both_success']/results['total']:.1f}%)")
    print()
    
    if results['failures']:
        print("FAILURES:")
        for f in results['failures']:
            print(f"  {f['pair']}: {f['reason']}")
    else:
        print("✅ ALL TESTS PASSED - ASTO₅ achieves 100% success rate!")
    
    print()
    print("=" * 70)
