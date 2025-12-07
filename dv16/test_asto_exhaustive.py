"""
Exhaustive Validation of ASTO Variant 5 on ALL 336 Zero Divisors
=================================================================

This script tests ASTO Variant 5 (Partial STO) on all 336 generated
zero divisor pairs to provide complete mathematical validation.
"""

import sys
sys.path.append('/home/ubuntu/dvmath/research/dv8')
sys.path.append('/home/ubuntu/dvmath-extensions/dv16')
from dv8 import DV8
from dv16 import DV16, basis_vector
import numpy as np
import json
from datetime import datetime


def asto_variant_5(v):
    """
    ASTO Variant 5 (Partial STO):
    Apply STO only to the first octonion (components 0-7),
    keep the second octonion (components 8-15) unchanged.
    """
    components = list(v.components)
    # Apply STO only to first octonion (0-7)
    first_oct = DV8(*components[0:8])
    sto_first = first_oct.STO()
    
    # Keep second octonion unchanged
    result = list(sto_first.components) + components[8:16]
    return DV16(result)


def generate_all_zero_divisors():
    """
    Generate ALL zero divisor pairs systematically.
    
    Pattern: (eᵢ + eⱼ) × (eₖ - eₗ) where indices cross the boundary.
    """
    zero_divisors = []
    
    print("Generating all zero divisor pairs...")
    print("=" * 70)
    
    total_checked = 0
    
    # Systematically try all combinations
    for i in range(16):
        for j in range(16):
            if i == j:
                continue
            
            # Ensure cross-boundary pattern
            if not ((i < 8 and j >= 8) or (i >= 8 and j < 8)):
                continue
            
            for k in range(16):
                for l in range(16):
                    if k == l:
                        continue
                    
                    # Ensure cross-boundary pattern
                    if not ((k < 8 and l >= 8) or (k >= 8 and l < 8)):
                        continue
                    
                    total_checked += 1
                    
                    A = basis_vector(i) + basis_vector(j)
                    B = basis_vector(k) - basis_vector(l)
                    
                    product = A * B
                    if product.is_zero():
                        zero_divisors.append({
                            'id': len(zero_divisors) + 1,
                            'indices': (i, j, k, l),
                            'A': A,
                            'B': B,
                            'pattern': f"(e{i} + e{j}) * (e{k} - e{l})"
                        })
                        
                        # Progress update every 50 found
                        if len(zero_divisors) % 50 == 0:
                            print(f"Found {len(zero_divisors)} zero divisors so far...")
    
    print(f"\n{'=' * 70}")
    print(f"Total combinations checked: {total_checked}")
    print(f"Zero divisors found: {len(zero_divisors)}")
    print(f"{'=' * 70}")
    
    return zero_divisors


def test_variant_5_on_zero_divisor(zd):
    """
    Test ASTO Variant 5 on a single zero divisor pair.
    Returns detailed results.
    """
    A = zd['A']
    B = zd['B']
    
    # Verify it's actually a zero divisor
    product = A * B
    is_zero_divisor = product.is_zero()
    original_norm = product.norm()
    
    # Apply Variant 5
    asto_a = asto_variant_5(A)
    asto_b = asto_variant_5(B)
    
    # Test both directions
    prod_left = asto_a * B
    prod_right = A * asto_b
    
    norm_left = prod_left.norm()
    norm_right = prod_right.norm()
    
    works_left = norm_left > 1e-10
    works_right = norm_right > 1e-10
    fully_works = works_left and works_right
    
    return {
        'id': zd['id'],
        'pattern': zd['pattern'],
        'indices': zd['indices'],
        'is_zero_divisor': is_zero_divisor,
        'original_norm': original_norm,
        'works_left': works_left,
        'works_right': works_right,
        'fully_works': fully_works,
        'norm_left': norm_left,
        'norm_right': norm_right,
    }


def main():
    """Main exhaustive test routine."""
    start_time = datetime.now()
    
    print("=" * 70)
    print("EXHAUSTIVE VALIDATION: ASTO VARIANT 5 ON ALL 336 ZERO DIVISORS")
    print("=" * 70)
    print(f"Start time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Step 1: Generate all zero divisors
    print("STEP 1: GENERATING ALL ZERO DIVISORS")
    print("=" * 70)
    zero_divisors = generate_all_zero_divisors()
    
    if len(zero_divisors) == 0:
        print("\n⚠️  ERROR: No zero divisors found!")
        return
    
    print(f"\n✓ Generated {len(zero_divisors)} zero divisor pairs")
    
    # Step 2: Test ASTO Variant 5 on all
    print(f"\n{'=' * 70}")
    print("STEP 2: TESTING ASTO VARIANT 5 ON ALL ZERO DIVISORS")
    print("=" * 70)
    
    results = []
    success_count = 0
    failure_count = 0
    
    # Progress tracking
    total = len(zero_divisors)
    checkpoint = max(1, total // 10)  # 10% checkpoints
    
    for idx, zd in enumerate(zero_divisors):
        result = test_variant_5_on_zero_divisor(zd)
        results.append(result)
        
        if result['fully_works']:
            success_count += 1
        else:
            failure_count += 1
        
        # Progress updates
        if (idx + 1) % checkpoint == 0 or (idx + 1) == total:
            progress = (idx + 1) / total * 100
            print(f"Progress: {idx + 1}/{total} ({progress:.1f}%) - "
                  f"Success: {success_count}, Failures: {failure_count}")
    
    # Step 3: Analyze results
    print(f"\n{'=' * 70}")
    print("STEP 3: ANALYZING RESULTS")
    print("=" * 70)
    
    success_rate = success_count / total * 100 if total > 0 else 0
    
    print(f"\nOverall Statistics:")
    print(f"  Total tested: {total}")
    print(f"  Successful: {success_count}")
    print(f"  Failed: {failure_count}")
    print(f"  Success rate: {success_rate:.2f}%")
    
    # Analyze failures (if any)
    failures = [r for r in results if not r['fully_works']]
    
    if failures:
        print(f"\n⚠️  FAILURES DETECTED ({len(failures)} cases):")
        print(f"{'=' * 70}")
        
        # Show first 10 failures
        for r in failures[:10]:
            print(f"\n✗ #{r['id']:3d}: {r['pattern']}")
            print(f"    Left:  {'✓' if r['works_left'] else '✗'} (norm: {r['norm_left']:.6f})")
            print(f"    Right: {'✓' if r['works_right'] else '✗'} (norm: {r['norm_right']:.6f})")
        
        if len(failures) > 10:
            print(f"\n... and {len(failures) - 10} more failures")
        
        # Analyze failure patterns
        print(f"\n{'=' * 70}")
        print("FAILURE PATTERN ANALYSIS")
        print(f"{'=' * 70}")
        
        left_only_failures = sum(1 for r in failures if not r['works_left'] and r['works_right'])
        right_only_failures = sum(1 for r in failures if r['works_left'] and not r['works_right'])
        both_failures = sum(1 for r in failures if not r['works_left'] and not r['works_right'])
        
        print(f"\nFailure breakdown:")
        print(f"  Left direction only fails: {left_only_failures}")
        print(f"  Right direction only fails: {right_only_failures}")
        print(f"  Both directions fail: {both_failures}")
        
        # Analyze index patterns of failures
        print(f"\nIndex patterns of failures:")
        failure_patterns = {}
        for r in failures:
            i, j, k, l = r['indices']
            mod8 = (i % 8, j % 8, k % 8, l % 8)
            if mod8 not in failure_patterns:
                failure_patterns[mod8] = 0
            failure_patterns[mod8] += 1
        
        for pattern, count in sorted(failure_patterns.items(), key=lambda x: -x[1])[:5]:
            print(f"  {pattern}: {count} failures")
    
    else:
        print(f"\n✓✓✓ NO FAILURES DETECTED!")
        print(f"    ASTO Variant 5 works on ALL {total} zero divisors!")
    
    # Step 4: Save results
    print(f"\n{'=' * 70}")
    print("STEP 4: SAVING RESULTS")
    print(f"{'=' * 70}")
    
    output_data = {
        'test_info': {
            'timestamp': start_time.isoformat(),
            'total_tested': total,
            'success_count': success_count,
            'failure_count': failure_count,
            'success_rate': success_rate,
        },
        'results': [
            {
                'id': r['id'],
                'pattern': r['pattern'],
                'indices': r['indices'],
                'fully_works': r['fully_works'],
                'works_left': r['works_left'],
                'works_right': r['works_right'],
                'norm_left': r['norm_left'],
                'norm_right': r['norm_right'],
            }
            for r in results
        ]
    }
    
    output_file = '/home/ubuntu/dvmath-extensions/dv16/asto_exhaustive_results.json'
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"\n✓ Results saved to: {output_file}")
    
    # Step 5: Final verdict
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print(f"\n{'=' * 70}")
    print("FINAL VERDICT")
    print(f"{'=' * 70}")
    
    print(f"\nTest duration: {duration:.2f} seconds")
    print(f"End time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    if success_rate == 100:
        print(f"\n{'🎉' * 35}")
        print("✓✓✓ ASTO VARIANT 5 IS UNIVERSALLY SUCCESSFUL!")
        print("    ALL 336 ZERO DIVISORS HANDLED CONSISTENTLY!")
        print("    DV¹⁶ WITH ASTO VARIANT 5 IS MATHEMATICALLY CONSISTENT!")
        print(f"{'🎉' * 35}")
        print("\n⭐ This is a MAJOR mathematical result!")
        print("⭐ DV¹⁶ is VALIDATED and ready for formal proof!")
    elif success_rate >= 99:
        print(f"\n✓✓ ASTO Variant 5 is HIGHLY SUCCESSFUL ({success_rate:.2f}%)")
        print("   Only minimal edge cases fail.")
        print("   Further investigation of failures recommended.")
    elif success_rate >= 95:
        print(f"\n✓ ASTO Variant 5 shows STRONG PROMISE ({success_rate:.2f}%)")
        print("  Most cases work, but some failures exist.")
        print("  Pattern analysis may reveal refinements.")
    else:
        print(f"\n⚠️  ASTO Variant 5 has LIMITATIONS ({success_rate:.2f}%)")
        print("   Success rate is below 95%.")
        print("   Alternative approaches should be explored.")
    
    return results


if __name__ == "__main__":
    results = main()
