"""
Comprehensive Test of ASTO Variant 5 (Partial STO) on 50 Zero Divisors
=======================================================================

This script generates 50 diverse zero divisor pairs and tests
ASTO Variant 5 systematically on all of them.
"""

import sys
sys.path.append('/home/ubuntu/dvmath/research/dv8')
sys.path.append('/home/ubuntu/dvmath-extensions/dv16')
from dv8 import DV8
from dv16 import DV16, basis_vector
import numpy as np
import itertools


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


def generate_zero_divisor_candidates():
    """
    Generate candidate zero divisor pairs.
    
    Strategy: Systematically try all combinations of basis vectors
    that cross the octonion boundary (indices 0-7 and 8-15).
    """
    candidates = []
    
    print("Generating zero divisor candidates...")
    
    # Try all combinations where indices cross the boundary
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
                    
                    A = basis_vector(i) + basis_vector(j)
                    B = basis_vector(k) - basis_vector(l)
                    
                    product = A * B
                    if product.is_zero():
                        candidates.append({
                            'indices': (i, j, k, l),
                            'A': A,
                            'B': B,
                        })
    
    return candidates


def get_pattern_signature(indices):
    """Get a unique signature for a zero divisor pattern."""
    i, j, k, l = indices
    mod8 = (i % 8, j % 8, k % 8, l % 8)
    return mod8


def select_diverse_zero_divisors(candidates, target_count=50):
    """
    Select diverse zero divisors from candidates.
    Prioritize diversity in modulo-8 patterns.
    """
    selected = []
    patterns_seen = set()
    
    # First pass: select unique patterns
    for candidate in candidates:
        if len(selected) >= target_count:
            break
        
        signature = get_pattern_signature(candidate['indices'])
        if signature not in patterns_seen:
            selected.append(candidate)
            patterns_seen.add(signature)
    
    # Second pass: if we need more, add duplicates with different indices
    if len(selected) < target_count:
        for candidate in candidates:
            if len(selected) >= target_count:
                break
            
            # Check if this exact index combination is already in selected
            already_selected = any(
                s['indices'] == candidate['indices'] for s in selected
            )
            
            if not already_selected:
                selected.append(candidate)
    
    return selected


def test_variant_5_on_zero_divisor(A, B):
    """
    Test ASTO Variant 5 on a zero divisor pair.
    Returns success status and norms.
    """
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
        'works_left': works_left,
        'works_right': works_right,
        'fully_works': fully_works,
        'norm_left': norm_left,
        'norm_right': norm_right,
    }


def main():
    """Main test routine."""
    print("=" * 70)
    print("COMPREHENSIVE TEST: ASTO VARIANT 5 ON 50 ZERO DIVISORS")
    print("=" * 70)
    
    # Step 1: Generate candidates
    print("\nStep 1: Generating zero divisor candidates...")
    candidates = generate_zero_divisor_candidates()
    print(f"Found {len(candidates)} zero divisor pairs")
    
    if len(candidates) == 0:
        print("\n⚠️  ERROR: No zero divisors found!")
        print("   This is unexpected. Check the generation logic.")
        return
    
    # Step 2: Select diverse subset
    print(f"\nStep 2: Selecting 50 diverse zero divisors...")
    target_count = min(50, len(candidates))
    selected = select_diverse_zero_divisors(candidates, target_count)
    print(f"Selected {len(selected)} zero divisors")
    
    # Step 3: Test Variant 5 on all
    print(f"\nStep 3: Testing ASTO Variant 5 on all {len(selected)} zero divisors...")
    print("=" * 70)
    
    results = []
    success_count = 0
    
    for idx, zd in enumerate(selected):
        i, j, k, l = zd['indices']
        A = zd['A']
        B = zd['B']
        
        result = test_variant_5_on_zero_divisor(A, B)
        result['id'] = idx + 1
        result['indices'] = (i, j, k, l)
        result['pattern'] = f"(e{i} + e{j}) * (e{k} - e{l})"
        
        results.append(result)
        
        if result['fully_works']:
            success_count += 1
        
        # Print progress every 10 tests
        if (idx + 1) % 10 == 0:
            print(f"Tested {idx + 1}/{len(selected)} zero divisors... "
                  f"Success rate so far: {success_count}/{idx + 1} "
                  f"({success_count/(idx+1)*100:.1f}%)")
    
    # Step 4: Analyze results
    print("\n" + "=" * 70)
    print("DETAILED RESULTS")
    print("=" * 70)
    
    # Show first 10 and any failures
    print("\nFirst 10 test cases:")
    for r in results[:10]:
        status = "✓" if r['fully_works'] else "✗"
        print(f"{status} #{r['id']:2d}: {r['pattern']:30s} "
              f"Left: {r['norm_left']:8.4f}, Right: {r['norm_right']:8.4f}")
    
    # Show failures
    failures = [r for r in results if not r['fully_works']]
    if failures:
        print(f"\n⚠️  FAILURES ({len(failures)} cases):")
        for r in failures:
            print(f"✗ #{r['id']:2d}: {r['pattern']:30s} "
                  f"Left: {r['norm_left']:8.4f}, Right: {r['norm_right']:8.4f}")
    
    # Step 5: Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    total = len(results)
    success_rate = success_count / total * 100 if total > 0 else 0
    
    print(f"\nTotal zero divisors tested: {total}")
    print(f"Successful (both directions work): {success_count}")
    print(f"Failed (at least one direction fails): {len(failures)}")
    print(f"Success rate: {success_rate:.1f}%")
    
    # Analyze failure patterns
    if failures:
        print(f"\nFailure analysis:")
        left_failures = sum(1 for r in failures if not r['works_left'])
        right_failures = sum(1 for r in failures if not r['works_right'])
        both_failures = sum(1 for r in failures if not r['works_left'] and not r['works_right'])
        
        print(f"  Left direction fails: {left_failures}")
        print(f"  Right direction fails: {right_failures}")
        print(f"  Both directions fail: {both_failures}")
    
    # Pattern analysis
    print(f"\nPattern distribution:")
    pattern_signatures = {}
    for r in results:
        sig = get_pattern_signature(r['indices'])
        if sig not in pattern_signatures:
            pattern_signatures[sig] = {'total': 0, 'success': 0}
        pattern_signatures[sig]['total'] += 1
        if r['fully_works']:
            pattern_signatures[sig]['success'] += 1
    
    print(f"  Unique modulo-8 patterns: {len(pattern_signatures)}")
    
    # Show pattern-specific success rates
    print(f"\n  Pattern-specific success rates:")
    for sig, counts in sorted(pattern_signatures.items(), 
                              key=lambda x: x[1]['success']/x[1]['total'], 
                              reverse=True)[:10]:
        rate = counts['success'] / counts['total'] * 100
        print(f"    {sig}: {counts['success']}/{counts['total']} ({rate:.0f}%)")
    
    # Final verdict
    print("\n" + "=" * 70)
    print("VERDICT")
    print("=" * 70)
    
    if success_rate == 100:
        print("\n✓✓✓ ASTO VARIANT 5 IS UNIVERSALLY SUCCESSFUL!")
        print("    All 50 zero divisors were successfully handled.")
        print("    DV¹⁶ with ASTO Variant 5 appears to be CONSISTENT!")
        print("\n    This is a MAJOR breakthrough for DV-Mathematics!")
    elif success_rate >= 95:
        print(f"\n✓✓ ASTO Variant 5 is HIGHLY SUCCESSFUL ({success_rate:.1f}%)")
        print("   Only minor edge cases fail.")
        print("   Further refinement may achieve 100% success.")
    elif success_rate >= 80:
        print(f"\n✓ ASTO Variant 5 shows PROMISE ({success_rate:.1f}%)")
        print("  Majority of cases work, but significant failures exist.")
        print("  Pattern-specific adaptations may be needed.")
    else:
        print(f"\n⚠️  ASTO Variant 5 has LIMITATIONS ({success_rate:.1f}%)")
        print("   Success rate is too low for universal application.")
        print("   Alternative approaches should be explored.")
    
    # Save results
    print(f"\n{'=' * 70}")
    print("Saving results...")
    
    import json
    output_data = {
        'total_tested': total,
        'success_count': success_count,
        'success_rate': success_rate,
        'results': [
            {
                'id': r['id'],
                'pattern': r['pattern'],
                'indices': r['indices'],
                'fully_works': r['fully_works'],
                'norm_left': r['norm_left'],
                'norm_right': r['norm_right'],
            }
            for r in results
        ]
    }
    
    with open('/home/ubuntu/dvmath-extensions/dv16/asto_variant5_test_results.json', 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print("Results saved to: /home/ubuntu/dvmath-extensions/dv16/asto_variant5_test_results.json")
    
    return results


if __name__ == "__main__":
    results = main()
