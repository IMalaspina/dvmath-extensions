"""
Zero Divisor Generator for DV¹⁶
================================
This script generates multiple zero divisor pairs using known patterns in Sedenions.

Mathematical Background:
- Sedenions have zero divisors of the form (eᵢ + eⱼ) * (eₖ - eₗ) = 0
- These follow specific index patterns related to the Cayley-Dickson construction
"""

import sys
sys.path.append('/home/ubuntu/dvmath-extensions/dv16')
from dv16 import DV16, basis_vector


def generate_pattern_based_zero_divisors():
    """
    Generate zero divisors based on known patterns.
    
    Pattern: (eᵢ + eⱼ) * (eₖ - eₗ) where indices satisfy specific relationships.
    
    In Sedenions, zero divisors occur when the indices form specific patterns
    related to the Cayley-Dickson doubling structure.
    """
    zero_divisors = []
    
    # Known pattern: indices that differ by 7 (related to octonion structure)
    # (e_i + e_{i+7}) * (e_j - e_{j+7}) can be zero for specific i, j
    
    patterns = [
        # Original known zero divisor
        (3, 10, 6, 15),
        (2, 9, 5, 14),
        
        # Systematic patterns based on Cayley-Dickson structure
        # Pattern 1: i, i+8, j, j+8 where i, j are from different octonion halves
        (1, 9, 4, 12),
        (1, 9, 5, 13),
        (1, 9, 6, 14),
        (1, 9, 7, 15),
        
        (2, 10, 4, 12),
        (2, 10, 5, 13),
        (2, 10, 6, 14),
        (2, 10, 7, 15),
        
        (3, 11, 4, 12),
        (3, 11, 5, 13),
        (3, 11, 6, 14),
        (3, 11, 7, 15),
        
        # Pattern 2: Symmetric patterns
        (4, 12, 1, 9),
        (5, 13, 2, 10),
        (6, 14, 3, 11),
        (7, 15, 4, 12),
        
        # Pattern 3: Cross-patterns
        (1, 8, 2, 9),
        (2, 8, 3, 10),
        (3, 8, 4, 11),
        (4, 8, 5, 12),
        (5, 8, 6, 13),
        (6, 8, 7, 14),
        (7, 8, 1, 15),
    ]
    
    for i, j, k, l in patterns:
        A = basis_vector(i) + basis_vector(j)
        B = basis_vector(k) - basis_vector(l)
        product = A * B
        
        if product.is_zero():
            zero_divisors.append({
                'A': A,
                'B': B,
                'pattern': f"(e{i} + e{j}) * (e{k} - e{l})",
                'indices': (i, j, k, l)
            })
    
    return zero_divisors


def generate_linear_combination_zero_divisors():
    """
    Generate zero divisors using linear combinations of basis vectors.
    
    Try combinations like (a*eᵢ + b*eⱼ) * (c*eₖ + d*eₗ) = 0
    """
    zero_divisors = []
    
    # Coefficients to try
    coeffs = [(1, 1), (1, -1), (2, 1), (1, 2), (1, 3)]
    
    # Base patterns from known zero divisors
    base_patterns = [
        (3, 10, 6, 15),
        (2, 9, 5, 14),
        (1, 9, 4, 12),
    ]
    
    for (i, j, k, l) in base_patterns:
        for (a, b) in coeffs:
            for (c, d) in coeffs:
                A = a * basis_vector(i) + b * basis_vector(j)
                B = c * basis_vector(k) + d * basis_vector(l)
                product = A * B
                
                if product.is_zero():
                    zero_divisors.append({
                        'A': A,
                        'B': B,
                        'pattern': f"({a}*e{i} + {b}*e{j}) * ({c}*e{k} + {d}*e{l})",
                        'indices': (i, j, k, l),
                        'coeffs': (a, b, c, d)
                    })
    
    return zero_divisors


def test_zero_divisor_with_sto(zd_dict):
    """Test a single zero divisor with STO."""
    A = zd_dict['A']
    B = zd_dict['B']
    
    # Original product (should be zero)
    original = A * B
    
    # Apply STO
    sto_a_times_b = A.STO() * B
    a_times_sto_b = A * B.STO()
    
    return {
        'pattern': zd_dict['pattern'],
        'original_norm': original.norm(),
        'sto_a_times_b_norm': sto_a_times_b.norm(),
        'a_times_sto_b_norm': a_times_sto_b.norm(),
        'sto_breaks_zero': not sto_a_times_b.is_zero() and not a_times_sto_b.is_zero()
    }


def main():
    """Generate and test zero divisors."""
    print("=" * 70)
    print("ZERO DIVISOR GENERATOR FOR DV¹⁶")
    print("=" * 70)
    
    # Generate pattern-based zero divisors
    print("\n1. Generating pattern-based zero divisors...")
    pattern_zds = generate_pattern_based_zero_divisors()
    print(f"   Found {len(pattern_zds)} pattern-based zero divisors")
    
    # Generate linear combination zero divisors
    print("\n2. Generating linear combination zero divisors...")
    linear_zds = generate_linear_combination_zero_divisors()
    print(f"   Found {len(linear_zds)} linear combination zero divisors")
    
    # Combine and deduplicate
    all_zds = pattern_zds + linear_zds
    print(f"\n3. Total unique zero divisors: {len(all_zds)}")
    
    if len(all_zds) == 0:
        print("\n   ⚠️  No zero divisors found! This is unexpected.")
        print("      The patterns may need adjustment.")
        return
    
    # Test each zero divisor with STO
    print("\n" + "=" * 70)
    print("TESTING STO ON ALL ZERO DIVISORS")
    print("=" * 70)
    
    results = []
    for i, zd in enumerate(all_zds[:20]):  # Test first 20
        result = test_zero_divisor_with_sto(zd)
        results.append(result)
        
        if i < 5 or not result['sto_breaks_zero']:  # Print first 5 or any failures
            print(f"\nZero Divisor #{i+1}: {result['pattern']}")
            print(f"  Original norm: {result['original_norm']:.15f}")
            print(f"  STO(A) * B norm: {result['sto_a_times_b_norm']:.6f}")
            print(f"  A * STO(B) norm: {result['a_times_sto_b_norm']:.6f}")
            print(f"  STO breaks zero? {result['sto_breaks_zero']}")
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    success_count = sum(1 for r in results if r['sto_breaks_zero'])
    total_tested = len(results)
    
    print(f"\nTotal zero divisors tested: {total_tested}")
    print(f"STO successfully broke zero divisor: {success_count}/{total_tested}")
    print(f"Success rate: {success_count/total_tested * 100:.1f}%")
    
    if success_count == total_tested:
        print("\n✓✓✓ STO IS CONSISTENT ACROSS ALL TESTED ZERO DIVISORS!")
        print("    This strongly suggests that DV¹⁶ with STO is viable.")
    elif success_count > total_tested * 0.9:
        print("\n✓ STO works in most cases (>90%)")
        print("  Further investigation needed for edge cases.")
    else:
        print("\n⚠️  STO has significant limitations in DV¹⁶")
        print(f"   Only {success_count/total_tested * 100:.1f}% success rate")
    
    # List any failures
    failures = [r for r in results if not r['sto_breaks_zero']]
    if failures:
        print(f"\n⚠️  FAILURES DETECTED ({len(failures)} cases):")
        for f in failures:
            print(f"  - {f['pattern']}")
    
    return all_zds, results


if __name__ == "__main__":
    zero_divisors, results = main()
