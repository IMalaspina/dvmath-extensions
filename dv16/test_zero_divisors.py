"""
Comprehensive Zero Divisor Tests for DV¹⁶
==========================================
This script systematically tests the STO functionality with zero divisors in DV¹⁶.

Test Categories:
1. Known zero divisors from literature
2. Systematic search for new zero divisors
3. STO application on zero divisors
4. Norm preservation analysis
5. Paradox resolution verification
"""

import sys
import random
sys.path.append('/home/ubuntu/dvmath-extensions/dv16')
from dv16 import DV16, basis_vector, known_zero_divisor


def test_known_zero_divisors():
    """Test 1: Verify known zero divisors from literature."""
    print("=" * 70)
    print("TEST 1: Known Zero Divisors")
    print("=" * 70)
    
    # Known zero divisor: (e₃ + e₁₀) * (e₆ - e₁₅) = 0
    A, B = known_zero_divisor()
    product = A * B
    
    print(f"\nKnown Zero Divisor Pair:")
    print(f"  A = e₃ + e₁₀")
    print(f"  B = e₆ - e₁₅")
    print(f"  A * B = {product}")
    print(f"  norm(A * B) = {product.norm():.15f}")
    print(f"  Is zero? {product.is_zero()}")
    
    # Additional known patterns
    # Pattern: (eᵢ + eⱼ) * (eₖ - eₗ) where specific indices create zero divisors
    test_pairs = [
        (3, 10, 6, 15),  # Original
        (2, 9, 5, 14),   # Similar pattern
        (1, 8, 4, 13),   # Similar pattern
    ]
    
    zero_divisors_found = 0
    for i, j, k, l in test_pairs:
        A = basis_vector(i) + basis_vector(j)
        B = basis_vector(k) - basis_vector(l)
        product = A * B
        is_zero = product.is_zero()
        
        print(f"\n  Test: (e{i} + e{j}) * (e{k} - e{l})")
        print(f"    norm(product) = {product.norm():.15f}")
        print(f"    Is zero? {is_zero}")
        
        if is_zero:
            zero_divisors_found += 1
    
    print(f"\n  Summary: {zero_divisors_found}/{len(test_pairs)} patterns are zero divisors")
    return zero_divisors_found > 0


def test_systematic_search():
    """Test 2: Systematic search for zero divisors."""
    print("\n" + "=" * 70)
    print("TEST 2: Systematic Search for Zero Divisors")
    print("=" * 70)
    
    print("\nSearching for zero divisors in random vectors...")
    print("(Testing 10,000 random pairs)")
    
    zero_divisors = []
    tests = 10000
    
    for _ in range(tests):
        # Generate random DV16 vectors
        components_a = [random.uniform(-10, 10) for _ in range(16)]
        components_b = [random.uniform(-10, 10) for _ in range(16)]
        
        A = DV16(components_a)
        B = DV16(components_b)
        product = A * B
        
        # Check if it's a zero divisor
        if product.norm() < 1e-8 and A.norm() > 0.1 and B.norm() > 0.1:
            zero_divisors.append((A, B, product))
            if len(zero_divisors) <= 5:  # Print first 5
                print(f"\n  Zero Divisor #{len(zero_divisors)} found!")
                print(f"    norm(A) = {A.norm():.6f}")
                print(f"    norm(B) = {B.norm():.6f}")
                print(f"    norm(A*B) = {product.norm():.15f}")
    
    print(f"\n  Summary: Found {len(zero_divisors)} zero divisors in {tests} tests")
    print(f"  Frequency: {len(zero_divisors)/tests * 100:.4f}%")
    
    return zero_divisors


def test_sto_on_zero_divisors(zero_divisors):
    """Test 3: Apply STO to zero divisors and verify it breaks the zero-divisor property."""
    print("\n" + "=" * 70)
    print("TEST 3: STO Application on Zero Divisors")
    print("=" * 70)
    
    if not zero_divisors:
        print("\n  No zero divisors to test. Using known zero divisor.")
        A, B = known_zero_divisor()
        zero_divisors = [(A, B, A * B)]
    
    success_count = 0
    total_tests = min(len(zero_divisors), 10)  # Test up to 10 zero divisors
    
    for i, (A, B, _) in enumerate(zero_divisors[:total_tests]):
        print(f"\n  Test {i+1}/{total_tests}:")
        
        # Original product (should be zero)
        original_product = A * B
        print(f"    A * B norm: {original_product.norm():.15f}")
        
        # Apply STO to A
        sto_a = A.STO()
        product_sto_a = sto_a * B
        print(f"    STO(A) * B norm: {product_sto_a.norm():.15f}")
        
        # Apply STO to B
        sto_b = B.STO()
        product_sto_b = A * sto_b
        print(f"    A * STO(B) norm: {product_sto_b.norm():.15f}")
        
        # Check if STO broke the zero-divisor property
        if not product_sto_a.is_zero() and not product_sto_b.is_zero():
            print(f"    ✓ STO successfully broke the zero-divisor property")
            success_count += 1
        else:
            print(f"    ✗ STO failed to break the zero-divisor property")
    
    print(f"\n  Summary: STO succeeded in {success_count}/{total_tests} cases")
    print(f"  Success rate: {success_count/total_tests * 100:.1f}%")
    
    return success_count == total_tests


def test_norm_preservation():
    """Test 4: Analyze norm preservation in DV16."""
    print("\n" + "=" * 70)
    print("TEST 4: Norm Preservation Analysis")
    print("=" * 70)
    
    print("\nTesting norm preservation: ||A * B|| = ||A|| * ||B||")
    print("(Testing 1,000 random pairs)")
    
    preserved_count = 0
    tests = 1000
    max_error = 0.0
    
    for _ in range(tests):
        components_a = [random.uniform(-5, 5) for _ in range(16)]
        components_b = [random.uniform(-5, 5) for _ in range(16)]
        
        A = DV16(components_a)
        B = DV16(components_b)
        product = A * B
        
        norm_product = product.norm()
        norm_a_times_b = A.norm() * B.norm()
        
        error = abs(norm_product - norm_a_times_b)
        max_error = max(max_error, error)
        
        if error < 1e-6:
            preserved_count += 1
    
    print(f"\n  Norm preserved in: {preserved_count}/{tests} cases")
    print(f"  Preservation rate: {preserved_count/tests * 100:.1f}%")
    print(f"  Maximum error observed: {max_error:.10f}")
    
    if preserved_count == tests:
        print(f"\n  ⚠️  UNEXPECTED: Norm is preserved in ALL cases!")
        print(f"      This contradicts the literature on Sedenions.")
    else:
        print(f"\n  ✓ Norm preservation is lost (as expected for Sedenions)")
    
    return preserved_count / tests


def test_paradox_resolution():
    """Test 5: Verify that the paradox 1/0 ≠ 2/0 is resolved."""
    print("\n" + "=" * 70)
    print("TEST 5: Paradox Resolution Verification")
    print("=" * 70)
    
    print("\nTesting: 1/0 ≠ 2/0 (via STO)")
    
    one = DV16(1)
    two = DV16(2)
    zero = DV16([0] * 16)
    
    # Division by zero triggers STO
    result_1 = one / zero
    result_2 = two / zero
    
    print(f"\n  1 / 0 = STO(1) = {result_1}")
    print(f"  2 / 0 = STO(2) = {result_2}")
    print(f"  norm(STO(1)) = {result_1.norm():.6f}")
    print(f"  norm(STO(2)) = {result_2.norm():.6f}")
    
    # Check if they are different
    are_different = not (result_1 == result_2)
    print(f"\n  Are they different? {are_different}")
    
    # Check if they are proportional
    ratio = result_2.norm() / result_1.norm()
    print(f"  Ratio of norms: {ratio:.6f}")
    print(f"  Expected ratio: 2.0")
    
    is_proportional = abs(ratio - 2.0) < 1e-6
    print(f"  Are they proportional? {is_proportional}")
    
    if are_different and is_proportional:
        print(f"\n  ✓ Paradox resolved: 1/0 ≠ 2/0, and results are proportional")
        return True
    else:
        print(f"\n  ✗ Paradox resolution failed")
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("DV¹⁶ ZERO DIVISOR TESTS - COMPREHENSIVE SUITE")
    print("=" * 70)
    print("\nObjective: Systematically test STO functionality with zero divisors")
    print("Expected outcome: Determine if DV-Mathematics can extend to DV¹⁶")
    
    # Run all tests
    test1_pass = test_known_zero_divisors()
    zero_divisors = test_systematic_search()
    test3_pass = test_sto_on_zero_divisors(zero_divisors)
    norm_preservation_rate = test_norm_preservation()
    test5_pass = test_paradox_resolution()
    
    # Final summary
    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    
    print(f"\n  Test 1 (Known Zero Divisors): {'✓ PASS' if test1_pass else '✗ FAIL'}")
    print(f"  Test 2 (Systematic Search): {len(zero_divisors)} zero divisors found")
    print(f"  Test 3 (STO on Zero Divisors): {'✓ PASS' if test3_pass else '✗ FAIL'}")
    print(f"  Test 4 (Norm Preservation): {norm_preservation_rate * 100:.1f}% preserved")
    print(f"  Test 5 (Paradox Resolution): {'✓ PASS' if test5_pass else '✗ FAIL'}")
    
    # Overall conclusion
    print("\n" + "=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    
    if test3_pass and test5_pass:
        print("\n  ✓✓✓ STO IS CONSISTENT IN DV¹⁶!")
        print("      DV-Mathematics can be extended to Sedenions.")
        print("      This is a significant finding.")
    else:
        print("\n  ✗ STO has limitations in DV¹⁶")
        print("    DV⁸ (Octonions) is the natural limit of the framework.")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    random.seed(42)  # For reproducibility
    main()
