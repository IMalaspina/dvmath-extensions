"""
Analysis: Why does STO work for some zero divisors but not others?
===================================================================

This script performs a deep mathematical analysis of the STO behavior
on different zero divisor patterns in DV¹⁶.
"""

import sys
sys.path.append('/home/ubuntu/dvmath-extensions/dv16')
from dv16 import DV16, basis_vector


def analyze_zero_divisor_structure(i, j, k, l):
    """
    Analyze the structure of a zero divisor pattern (eᵢ + eⱼ) * (eₖ - eₗ).
    
    Returns detailed information about:
    - Index relationships
    - Cayley-Dickson structure
    - STO behavior
    """
    A = basis_vector(i) + basis_vector(j)
    B = basis_vector(k) - basis_vector(l)
    
    # Check if it's a zero divisor
    product = A * B
    is_zero_divisor = product.is_zero()
    
    if not is_zero_divisor:
        return None
    
    # Apply STO
    sto_a = A.STO()
    sto_b = B.STO()
    
    sto_a_times_b = sto_a * B
    a_times_sto_b = A * sto_b
    
    # Analyze index structure
    # In DV16, indices 0-7 are the "first octonion", 8-15 are the "second octonion"
    first_oct_a = (i < 8, j < 8)
    first_oct_b = (k < 8, l < 8)
    
    # Check if indices cross the octonion boundary
    crosses_boundary_a = first_oct_a[0] != first_oct_a[1]
    crosses_boundary_b = first_oct_b[0] != first_oct_b[1]
    
    # Calculate index differences
    diff_a = abs(i - j)
    diff_b = abs(k - l)
    
    return {
        'pattern': f"(e{i} + e{j}) * (e{k} - e{l})",
        'indices': (i, j, k, l),
        'is_zero_divisor': is_zero_divisor,
        'sto_a_times_b_works': not sto_a_times_b.is_zero(),
        'a_times_sto_b_works': not a_times_sto_b.is_zero(),
        'sto_fully_works': not sto_a_times_b.is_zero() and not a_times_sto_b.is_zero(),
        'crosses_boundary_a': crosses_boundary_a,
        'crosses_boundary_b': crosses_boundary_b,
        'diff_a': diff_a,
        'diff_b': diff_b,
        'sto_a_times_b_norm': sto_a_times_b.norm(),
        'a_times_sto_b_norm': a_times_sto_b.norm(),
    }


def main():
    """Analyze all known zero divisor patterns."""
    print("=" * 70)
    print("ANALYSIS: STO BEHAVIOR ON ZERO DIVISORS")
    print("=" * 70)
    
    # Known zero divisor patterns
    patterns = [
        (3, 10, 6, 15),  # Works
        (2, 9, 5, 14),   # Fails
        (1, 9, 4, 12),   # Unknown
        (1, 9, 5, 13),   # Unknown
        (1, 9, 6, 14),   # Unknown
        (1, 9, 7, 15),   # Unknown
        (2, 10, 4, 12),  # Unknown
        (2, 10, 5, 13),  # Unknown
        (2, 10, 6, 14),  # Unknown
        (2, 10, 7, 15),  # Unknown
        (3, 11, 4, 12),  # Unknown
        (3, 11, 5, 13),  # Unknown
        (3, 11, 6, 14),  # Unknown
        (3, 11, 7, 15),  # Unknown
    ]
    
    results = []
    for pattern in patterns:
        result = analyze_zero_divisor_structure(*pattern)
        if result:
            results.append(result)
    
    # Print detailed results
    print("\nDetailed Analysis:")
    print("-" * 70)
    
    for r in results:
        print(f"\n{r['pattern']}")
        print(f"  Indices: {r['indices']}")
        print(f"  Crosses boundary A: {r['crosses_boundary_a']}")
        print(f"  Crosses boundary B: {r['crosses_boundary_b']}")
        print(f"  Index diff A: {r['diff_a']}")
        print(f"  Index diff B: {r['diff_b']}")
        print(f"  STO(A) * B works: {r['sto_a_times_b_works']} (norm: {r['sto_a_times_b_norm']:.6f})")
        print(f"  A * STO(B) works: {r['a_times_sto_b_works']} (norm: {r['a_times_sto_b_norm']:.6f})")
        print(f"  STO fully works: {'✓' if r['sto_fully_works'] else '✗'}")
    
    # Analyze patterns
    print("\n" + "=" * 70)
    print("PATTERN ANALYSIS")
    print("=" * 70)
    
    # Group by success/failure
    successes = [r for r in results if r['sto_fully_works']]
    failures = [r for r in results if not r['sto_fully_works']]
    
    print(f"\nSuccesses: {len(successes)}")
    print(f"Failures: {len(failures)}")
    
    # Analyze index differences
    print("\n--- Index Difference Analysis ---")
    
    if successes:
        print("\nSuccessful patterns:")
        for r in successes:
            print(f"  {r['pattern']}: diff_a={r['diff_a']}, diff_b={r['diff_b']}")
    
    if failures:
        print("\nFailed patterns:")
        for r in failures:
            print(f"  {r['pattern']}: diff_a={r['diff_a']}, diff_b={r['diff_b']}")
    
    # Analyze boundary crossing
    print("\n--- Boundary Crossing Analysis ---")
    
    success_cross_a = sum(1 for r in successes if r['crosses_boundary_a'])
    success_cross_b = sum(1 for r in successes if r['crosses_boundary_b'])
    
    failure_cross_a = sum(1 for r in failures if r['crosses_boundary_a'])
    failure_cross_b = sum(1 for r in failures if r['crosses_boundary_b'])
    
    print(f"\nSuccesses crossing boundary A: {success_cross_a}/{len(successes)}")
    print(f"Successes crossing boundary B: {success_cross_b}/{len(successes)}")
    print(f"Failures crossing boundary A: {failure_cross_a}/{len(failures)}")
    print(f"Failures crossing boundary B: {failure_cross_b}/{len(failures)}")
    
    # Hypothesis testing
    print("\n" + "=" * 70)
    print("HYPOTHESIS TESTING")
    print("=" * 70)
    
    print("\nHypothesis 1: Index difference matters")
    print("  Observation:")
    if successes and failures:
        success_diffs = [(r['diff_a'], r['diff_b']) for r in successes]
        failure_diffs = [(r['diff_a'], r['diff_b']) for r in failures]
        print(f"    Success diffs: {success_diffs}")
        print(f"    Failure diffs: {failure_diffs}")
        
        # Check if there's a pattern
        if all(d[0] == 7 for d in success_diffs):
            print("  ✓ All successes have diff_a = 7")
        if all(d[0] == 7 for d in failure_diffs):
            print("  ✓ All failures have diff_a = 7")
    
    print("\nHypothesis 2: Boundary crossing matters")
    print("  Observation:")
    print(f"    All successes cross boundary: {all(r['crosses_boundary_a'] and r['crosses_boundary_b'] for r in successes)}")
    print(f"    All failures cross boundary: {all(r['crosses_boundary_a'] and r['crosses_boundary_b'] for r in failures)}")
    
    print("\nHypothesis 3: Specific index patterns")
    print("  Observation:")
    if successes and failures:
        # Check if there's a modulo pattern
        success_mods = [((r['indices'][0] % 8), (r['indices'][1] % 8), 
                        (r['indices'][2] % 8), (r['indices'][3] % 8)) for r in successes]
        failure_mods = [((r['indices'][0] % 8), (r['indices'][1] % 8), 
                        (r['indices'][2] % 8), (r['indices'][3] % 8)) for r in failures]
        
        print(f"    Success patterns (mod 8): {success_mods}")
        print(f"    Failure patterns (mod 8): {failure_mods}")
    
    # Final conclusion
    print("\n" + "=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    
    if len(successes) > 0 and len(failures) > 0:
        print("\n⚠️  STO behavior is INDEX-DEPENDENT in DV¹⁶")
        print("   Certain index patterns allow STO to work, others don't.")
        print("   This suggests a deep structural limitation related to")
        print("   the Cayley-Dickson construction beyond octonions.")
    elif len(successes) == len(results):
        print("\n✓ STO works for all tested patterns!")
    else:
        print("\n✗ STO fails for all tested patterns")
    
    return results


if __name__ == "__main__":
    results = main()
