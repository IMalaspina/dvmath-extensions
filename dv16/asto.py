"""
ASTO (Adaptive STO) Implementation for DV¹⁶
============================================

This module implements ASTO₅ (Partial STO), the singularity
treatment operation for DV¹⁶ (Sedenions).

IMPORTANT CORRECTION (22.12.2025):
----------------------------------
The original claim that "ASTO₅ achieves 100% success on all 84 canonical
zero divisors when applied to A" was INCORRECT. The correct statistics are:

- ASTO₅ applied to A only: 72/84 (85.7%)
- ASTO₅ applied to B only: 48/84 (57.1%)
- **Adaptive ASTO₅ (A or B): 84/84 (100%)**

The adaptive strategy tries ASTO on A first, and if that fails,
applies ASTO to B instead. This achieves 100% success.

Author: Ivano Franco Malaspina
Version: 2.2.0 (Corrected)

ASTO Variants History:
- ASTO₁: Standard STO (e₁ × x) - fails on some zero divisors
- ASTO₂: Double rotation - fails on some zero divisors
- ASTO₃: Conjugate + STO - fails on some zero divisors
- ASTO₄: Inverse direction - fails on some zero divisors
- ASTO₅: Partial STO - 85.7% on A, 100% with adaptive strategy ✓
"""

from dv16 import DV16, Octonion, e


def asto5(v: DV16) -> DV16:
    """
    ASTO₅ (Partial STO): Apply STO to first Octonion only.
    
    Applies STO only to the first Octonion component:
    ASTO₅(a, b) = (e₁ × a, b)
    
    WARNING: This function alone achieves only 85.7% success rate
    on the 84 canonical zero divisors. Use `asto5_adaptive` for 100%.
    
    Mathematical Basis:
    - Zero divisors require: ac = d*b (destructive interference)
    - ASTO₅ transforms: a → e₁ × a
    - For most pairs: (e₁ × a)c ≠ ac due to non-associativity
    - But 12 pairs require ASTO on B instead of A
    
    Args:
        v: DV16 vector
    
    Returns:
        Transformed DV16 vector with first octonion rotated
    """
    e1_oct = Octonion([0, 1, 0, 0, 0, 0, 0, 0])
    a_prime = e1_oct * v.a  # Left multiplication (canonical)
    return DV16(a_prime.to_list() + v.b.to_list())


def asto5_right(v: DV16) -> DV16:
    """
    ASTO₅ Right variant: a × e₁ instead of e₁ × a.
    
    Also achieves 85.7% success rate (same as left variant).
    
    Args:
        v: DV16 vector
    
    Returns:
        Transformed DV16 vector with first octonion rotated (right)
    """
    e1_oct = Octonion([0, 1, 0, 0, 0, 0, 0, 0])
    a_prime = v.a * e1_oct  # Right multiplication
    return DV16(a_prime.to_list() + v.b.to_list())


def asto5_adaptive(A: DV16, B: DV16, tol: float = 1e-10) -> tuple:
    """
    Adaptive ASTO₅: The CORRECT way to achieve 100% success.
    
    Algorithm:
    1. Try ASTO₅(A) × B
    2. If result ≠ 0, return (ASTO₅(A), B, "A")
    3. Else try A × ASTO₅(B)
    4. If result ≠ 0, return (A, ASTO₅(B), "B")
    5. Else return failure (should never happen for canonical pairs)
    
    Statistics on 84 canonical zero divisors:
    - 72 pairs: ASTO on A works
    - 12 pairs: ASTO on B works (these all contain e₉)
    - 0 pairs: Both fail
    
    Args:
        A: First factor of the zero divisor pair
        B: Second factor of the zero divisor pair
        tol: Tolerance for zero detection
    
    Returns:
        Tuple of (A', B', which) where:
        - A' × B' ≠ 0
        - which is "A" if ASTO was applied to A, "B" if applied to B
        - Returns (None, None, "FAIL") if no solution found
    
    Example:
        >>> A = e(1) + e(10)
        >>> B = e(5) + e(14)
        >>> assert (A * B).is_zero()  # Zero divisor
        >>> A_new, B_new, which = asto5_adaptive(A, B)
        >>> assert not (A_new * B_new).is_zero()  # Resolved!
    """
    # Try ASTO on A
    A_transformed = asto5(A)
    result_A = A_transformed * B
    
    if result_A.norm() > tol:
        return A_transformed, B, "A"
    
    # Try ASTO on B
    B_transformed = asto5(B)
    result_B = A * B_transformed
    
    if result_B.norm() > tol:
        return A, B_transformed, "B"
    
    # Both failed (should not happen for canonical pairs)
    return None, None, "FAIL"


# Alias for backward compatibility
asto_variant5 = asto5


def ASTO(v: DV16) -> DV16:
    """
    Main ASTO function - uses ASTO₅.
    
    WARNING: For zero divisor resolution, use asto5_adaptive instead.
    
    Args:
        v: DV16 vector
    
    Returns:
        Transformed DV16 vector
    """
    return asto5(v)


# ============================================================
# STATISTICS
# ============================================================

ASTO5_STATS = {
    "asto5_on_A": {
        "success_rate": 85.7,
        "successes": 72,
        "total": 84,
        "description": "ASTO₅ applied to first factor A only"
    },
    "asto5_on_B": {
        "success_rate": 57.1,
        "successes": 48,
        "total": 84,
        "description": "ASTO₅ applied to second factor B only"
    },
    "asto5_adaptive": {
        "success_rate": 100.0,
        "successes": 84,
        "total": 84,
        "description": "Adaptive ASTO₅: try A first, then B if needed"
    }
}

# The 12 pairs where ASTO on A fails (all contain e₉ in B)
ASTO5_A_FAILURES = [
    "(e2 + e12) × (e7 + e9)",
    "(e2 + e13) × (e6 - e9)",
    "(e2 + e14) × (e5 + e9)",
    "(e2 + e15) × (e4 - e9)",
    "(e3 + e12) × (e6 - e9)",
    "(e3 + e14) × (e4 + e9)",
    "(e3 + e15) × (e5 + e9)",
    "(e3 + e13) × (e7 - e9)",
    "(e4 + e10) × (e7 - e9)",
    "(e4 + e11) × (e6 + e9)",
    "(e5 + e10) × (e6 + e9)",
    "(e5 + e11) × (e7 + e9)",
]


# ============================================================
# LEGACY VARIANTS (kept for reference, not recommended)
# ============================================================

def asto_variant_1(v: DV16) -> DV16:
    """ASTO Variant 1: Standard STO. NOT UNIVERSAL."""
    return v.STO()


def asto_variant_2(v: DV16) -> DV16:
    """ASTO Variant 2: Double rotation. NOT UNIVERSAL."""
    return v.STO().STO()


def asto_variant_3(v: DV16) -> DV16:
    """ASTO Variant 3: Conjugate + STO. NOT UNIVERSAL."""
    return v.conjugate().STO()


def asto_variant_4(v: DV16) -> DV16:
    """ASTO Variant 4: Inverse STO direction. NOT UNIVERSAL."""
    sto = v.STO()
    components = list(sto.components)
    for i in range(8, 16):
        components[i] = -components[i]
    return DV16(components)


# ============================================================
# VALIDATION
# ============================================================

def test_asto5_on_pair(A: DV16, B: DV16) -> dict:
    """
    Test ASTO₅ on a zero divisor pair.
    
    Returns:
        dict with test results
    """
    product = A * B
    is_zero_divisor = product.is_zero()
    
    if not is_zero_divisor:
        return {
            'is_zero_divisor': False,
            'asto_A_works': None,
            'asto_B_works': None,
            'adaptive_works': None
        }
    
    # Test ASTO on A: ASTO₅(A) × B
    result_A = asto5(A) * B
    asto_A_works = not result_A.is_zero()
    
    # Test ASTO on B: A × ASTO₅(B)
    result_B = A * asto5(B)
    asto_B_works = not result_B.is_zero()
    
    # Adaptive works if either works
    adaptive_works = asto_A_works or asto_B_works
    
    return {
        'is_zero_divisor': True,
        'asto_A_works': asto_A_works,
        'asto_B_works': asto_B_works,
        'adaptive_works': adaptive_works,
        'result_A_norm': result_A.norm(),
        'result_B_norm': result_B.norm()
    }


if __name__ == "__main__":
    print("=" * 70)
    print("ASTO₅ (Partial STO) - CORRECTED Implementation v2.2.0")
    print("=" * 70)
    
    print("\nIMPORTANT: ASTO₅ on A alone achieves 85.7%, not 100%!")
    print("Use asto5_adaptive() for 100% success rate.\n")
    
    print("Statistics on 84 canonical zero divisors:")
    for key, stats in ASTO5_STATS.items():
        print(f"  {key}: {stats['successes']}/{stats['total']} ({stats['success_rate']}%)")
    
    print("\n" + "=" * 70)
    print("The 12 pairs where ASTO on A fails (all contain e₉):")
    print("=" * 70)
    for pair in ASTO5_A_FAILURES:
        print(f"  {pair}")
    
    print("\n" + "=" * 70)
