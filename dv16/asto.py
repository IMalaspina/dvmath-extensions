"""
ASTO (Adaptive STO) Implementation for DV¹⁶
============================================

This module implements an index-adaptive STO variant that adjusts
based on the modulo-8 pattern of the vector indices.

Goal: Achieve consistent STO behavior for all zero divisors.
"""

import sys
sys.path.append('/home/ubuntu/dvmath/research/dv8')
sys.path.append('/home/ubuntu/dvmath-extensions/dv16')
from dv8 import DV8
from dv16 import DV16
import numpy as np


def get_dominant_indices(v):
    """
    Get the indices of the dominant (non-zero) components.
    Returns indices sorted by magnitude.
    """
    components = v.components
    indexed = [(i, abs(c)) for i, c in enumerate(components) if abs(c) > 1e-10]
    indexed.sort(key=lambda x: x[1], reverse=True)
    return [i for i, _ in indexed]


def get_pattern_signature(v):
    """
    Get the modulo-8 pattern signature of a vector.
    Returns a tuple of (mod_values, crosses_boundary).
    """
    indices = get_dominant_indices(v)
    if not indices:
        return (tuple(), False)
    
    mod_values = tuple(sorted([i % 8 for i in indices]))
    crosses_boundary = any(i < 8 for i in indices) and any(i >= 8 for i in indices)
    
    return (mod_values, crosses_boundary)


def asto_variant_1(v):
    """
    ASTO Variant 1: Standard STO (rotation to depth dimension).
    This is the original STO from DV⁸.
    """
    return v.STO()


def asto_variant_2(v):
    """
    ASTO Variant 2: Double rotation.
    Apply STO twice to reach a different position in the rotation cycle.
    """
    return v.STO().STO()


def asto_variant_3(v):
    """
    ASTO Variant 3: Conjugate + STO.
    Combine conjugation with STO for a different transformation.
    """
    return v.conjugate().STO()


def asto_variant_4(v):
    """
    ASTO Variant 4: Inverse STO direction.
    Rotate in the opposite direction (negate after STO).
    """
    sto = v.STO()
    # Negate the depth components (8-15)
    components = list(sto.components)
    for i in range(8, 16):
        components[i] = -components[i]
    return DV16(components)


def asto_variant_5(v):
    """
    ASTO Variant 5: Partial STO.
    Only rotate half of the components.
    """
    components = list(v.components)
    # Apply STO logic only to first octonion (0-7)
    first_oct = DV8(*components[0:8])
    sto_first = first_oct.STO()
    
    # Keep second octonion unchanged
    result = list(sto_first.components) + components[8:16]
    return DV16(result)


def asto_variant_6(v):
    """
    ASTO Variant 6: Cross-octonion STO.
    Swap the octonions and then apply STO.
    """
    components = list(v.components)
    # Swap first and second octonion
    swapped = components[8:16] + components[0:8]
    v_swapped = DV16(swapped)
    return v_swapped.STO()


# Pattern-to-variant mapping
# This will be determined empirically through testing
PATTERN_MAP = {
    # Default: use variant 1 (standard STO)
    'default': asto_variant_1,
    
    # Specific patterns (to be filled based on test results)
    # Format: (mod_values, crosses_boundary): variant_function
}


def ASTO(v, context=None):
    """
    Adaptive STO: Choose the appropriate STO variant based on the vector's pattern.
    
    Args:
        v: DV16 vector
        context: Optional context (e.g., the other vector in a multiplication)
    
    Returns:
        Transformed DV16 vector
    """
    signature = get_pattern_signature(v)
    
    # Look up the appropriate variant
    variant_func = PATTERN_MAP.get(signature, PATTERN_MAP['default'])
    
    return variant_func(v)


def test_asto_on_zero_divisor(A, B, pattern_name):
    """
    Test all ASTO variants on a zero divisor pair.
    Returns the best variant (if any).
    """
    variants = [
        ('Variant 1 (Standard)', asto_variant_1),
        ('Variant 2 (Double)', asto_variant_2),
        ('Variant 3 (Conjugate)', asto_variant_3),
        ('Variant 4 (Inverse)', asto_variant_4),
        ('Variant 5 (Partial)', asto_variant_5),
        ('Variant 6 (Cross)', asto_variant_6),
    ]
    
    results = []
    
    for variant_name, variant_func in variants:
        # Test both directions
        asto_a = variant_func(A)
        asto_b = variant_func(B)
        
        prod_left = asto_a * B
        prod_right = A * asto_b
        
        works_left = not prod_left.is_zero()
        works_right = not prod_right.is_zero()
        fully_works = works_left and works_right
        
        results.append({
            'variant': variant_name,
            'works_left': works_left,
            'works_right': works_right,
            'fully_works': fully_works,
            'norm_left': prod_left.norm(),
            'norm_right': prod_right.norm(),
        })
    
    return results


def main():
    """Test ASTO on all known zero divisors."""
    print("=" * 70)
    print("ASTO (ADAPTIVE STO) IMPLEMENTATION TEST")
    print("=" * 70)
    
    # Known zero divisor patterns
    from dv16 import basis_vector
    
    test_cases = [
        {
            'name': 'Success Case: (e3 + e10) * (e6 - e15)',
            'A': basis_vector(3) + basis_vector(10),
            'B': basis_vector(6) - basis_vector(15),
        },
        {
            'name': 'Failure Case: (e2 + e9) * (e5 - e14)',
            'A': basis_vector(2) + basis_vector(9),
            'B': basis_vector(5) - basis_vector(14),
        },
    ]
    
    all_results = {}
    
    for test_case in test_cases:
        print(f"\n{'=' * 70}")
        print(f"Testing: {test_case['name']}")
        print(f"{'=' * 70}")
        
        A = test_case['A']
        B = test_case['B']
        
        # Verify it's a zero divisor
        product = A * B
        print(f"\nOriginal product norm: {product.norm():.15f}")
        print(f"Is zero divisor: {product.is_zero()}")
        
        # Test all variants
        results = test_asto_on_zero_divisor(A, B, test_case['name'])
        all_results[test_case['name']] = results
        
        # Print results
        print(f"\nASTO Variant Results:")
        print(f"{'-' * 70}")
        
        for r in results:
            status = "✓ WORKS" if r['fully_works'] else "✗ FAILS"
            print(f"\n{r['variant']}: {status}")
            print(f"  ASTO(A) * B: {'✓' if r['works_left'] else '✗'} (norm: {r['norm_left']:.6f})")
            print(f"  A * ASTO(B): {'✓' if r['works_right'] else '✗'} (norm: {r['norm_right']:.6f})")
    
    # Summary
    print(f"\n{'=' * 70}")
    print("SUMMARY")
    print(f"{'=' * 70}")
    
    for test_name, results in all_results.items():
        working_variants = [r for r in results if r['fully_works']]
        print(f"\n{test_name}")
        print(f"  Working variants: {len(working_variants)}/6")
        
        if working_variants:
            print(f"  Best variants:")
            for r in working_variants:
                print(f"    - {r['variant']}")
    
    # Check if there's a universal solution
    print(f"\n{'=' * 70}")
    print("UNIVERSAL SOLUTION CHECK")
    print(f"{'=' * 70}")
    
    # Find variants that work for ALL test cases
    variant_names = [r['variant'] for r in all_results[test_cases[0]['name']]]
    
    for variant_name in variant_names:
        works_for_all = True
        for test_name, results in all_results.items():
            variant_result = next(r for r in results if r['variant'] == variant_name)
            if not variant_result['fully_works']:
                works_for_all = False
                break
        
        if works_for_all:
            print(f"\n✓✓✓ {variant_name} works for ALL test cases!")
            print(f"    This could be the universal ASTO solution!")
        else:
            print(f"\n✗ {variant_name} does NOT work for all cases")
    
    # Conclusion
    print(f"\n{'=' * 70}")
    print("CONCLUSION")
    print(f"{'=' * 70}")
    
    # Check if any variant works universally
    universal_found = False
    for variant_name in variant_names:
        works_for_all = all(
            any(r['variant'] == variant_name and r['fully_works'] for r in results)
            for results in all_results.values()
        )
        if works_for_all:
            universal_found = True
            print(f"\n✓ ASTO is viable with {variant_name}")
            print(f"  DV¹⁶ can be made consistent with this adaptive approach!")
            break
    
    if not universal_found:
        print(f"\n⚠️  No single ASTO variant works for all cases")
        print(f"   A pattern-specific mapping may be required")
        print(f"   OR we need to develop new variants")


if __name__ == "__main__":
    main()
