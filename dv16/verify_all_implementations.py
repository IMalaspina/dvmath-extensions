#!/usr/bin/env python3
"""
Comprehensive Verification of DV-Mathematics Implementations

This script verifies all mathematical implementations before GitHub upload.
It checks:
1. Octonion multiplication table correctness
2. Cayley-Dickson formula implementation
3. Zero divisor validation
4. ASTO₅ implementation (both variants)
5. G₂ automorphism properties

Author: Ivano Franco Malaspina
Date: December 22, 2025
"""

import numpy as np
from scipy.linalg import expm
import json
import sys

# =============================================================================
# OCTONION MULTIPLICATION TABLE (Standard Fano Plane Convention)
# =============================================================================

# Cayley multiplication table for octonions
# e_i * e_j where i,j in {1,...,7}
# Returns signed index: positive = +e_k, negative = -e_k, 0 = real

CAYLEY_TABLE = np.array([
    # e1  e2  e3  e4  e5  e6  e7
    [ 0,  3, -2,  5, -4, -7,  6],  # e1 *
    [-3,  0,  1,  6,  7, -4, -5],  # e2 *
    [ 2, -1,  0,  7, -6,  5, -4],  # e3 *
    [-5, -6, -7,  0,  1,  2,  3],  # e4 *
    [ 4, -7,  6, -1,  0, -3,  2],  # e5 *
    [ 7,  4, -5, -2,  3,  0, -1],  # e6 *
    [-6,  5,  4, -3, -2,  1,  0],  # e7 *
])


def octonion_mult(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Multiply two octonions using standard Cayley multiplication."""
    result = np.zeros(8)
    
    # Real * Real
    result[0] = a[0] * b[0]
    
    # Real * Imaginary and Imaginary * Real
    for i in range(1, 8):
        result[i] += a[0] * b[i]
        result[i] += a[i] * b[0]
    
    # Imaginary * Imaginary
    for i in range(1, 8):
        for j in range(1, 8):
            if i == j:
                result[0] -= a[i] * b[j]  # e_i * e_i = -1
            else:
                k = CAYLEY_TABLE[i-1, j-1]
                sign = 1 if k > 0 else -1
                idx = abs(k)
                result[idx] += sign * a[i] * b[j]
    
    return result


def octonion_conj(a: np.ndarray) -> np.ndarray:
    """Conjugate: a* = (a0, -a1, ..., -a7)"""
    result = a.copy()
    result[1:] = -result[1:]
    return result


# =============================================================================
# SEDENION (DV16) IMPLEMENTATION
# =============================================================================

def sedenion_mult(s1: np.ndarray, s2: np.ndarray) -> np.ndarray:
    """
    Cayley-Dickson multiplication for sedenions.
    S1 = (a, b), S2 = (c, d)
    S1 * S2 = (ac - d*b, da + bc*)
    """
    a, b = s1[:8], s1[8:]
    c, d = s2[:8], s2[8:]
    
    # ac - d*b
    ac = octonion_mult(a, c)
    d_conj = octonion_conj(d)
    d_conj_b = octonion_mult(d_conj, b)
    new_a = ac - d_conj_b
    
    # da + bc*
    da = octonion_mult(d, a)
    c_conj = octonion_conj(c)
    bc_conj = octonion_mult(b, c_conj)
    new_b = da + bc_conj
    
    return np.concatenate([new_a, new_b])


def sedenion_basis(i: int) -> np.ndarray:
    """Create basis sedenion e_i"""
    s = np.zeros(16)
    s[i] = 1.0
    return s


# =============================================================================
# ASTO₅ IMPLEMENTATION
# =============================================================================

def sto_octonion_left(a: np.ndarray) -> np.ndarray:
    """STO(a) = e_1 * a (left multiplication)"""
    e1 = np.zeros(8)
    e1[1] = 1.0
    return octonion_mult(e1, a)


def sto_octonion_right(a: np.ndarray) -> np.ndarray:
    """STO(a) = a * e_1 (right multiplication)"""
    e1 = np.zeros(8)
    e1[1] = 1.0
    return octonion_mult(a, e1)


def asto5_left(s: np.ndarray) -> np.ndarray:
    """ASTO₅ left: (a, b) -> (e_1 * a, b)"""
    a, b = s[:8], s[8:]
    return np.concatenate([sto_octonion_left(a), b])


def asto5_right(s: np.ndarray) -> np.ndarray:
    """ASTO₅ right: (a, b) -> (a * e_1, b)"""
    a, b = s[:8], s[8:]
    return np.concatenate([sto_octonion_right(a), b])


# =============================================================================
# G₂ IMPLEMENTATION
# =============================================================================

def g2_basis_matrices():
    """Construct the 14 basis matrices of the G₂ Lie algebra."""
    sqrt3_6 = np.sqrt(3) / 6
    
    def E(i, j):
        M = np.zeros((8, 8))
        M[i, j] = 1
        M[j, i] = -1
        return M
    
    X0 = 0.5 * (E(4, 5) + E(6, 7))
    X1 = 0.5 * (E(4, 6) - E(5, 7))
    X2 = 0.5 * (E(4, 7) + E(5, 6))
    X3 = -sqrt3_6 * (2*E(2, 3) - E(4, 5) + E(6, 7))
    X4 = sqrt3_6 * (2*E(1, 3) + E(4, 6) + E(5, 7))
    X5 = -sqrt3_6 * (2*E(1, 2) - E(4, 7) + E(5, 6))
    X6 = -0.5 * (E(1, 7) - E(2, 4))
    X7 = 0.5 * (E(1, 6) + E(2, 5))
    X8 = -0.5 * (E(1, 5) - E(2, 6))
    X9 = 0.5 * (E(1, 4) + E(2, 7))
    X10 = sqrt3_6 * (E(1, 6) - E(2, 5) + 2*E(3, 4))
    X11 = sqrt3_6 * (E(1, 7) + E(2, 4) + 2*E(3, 5))
    X12 = -sqrt3_6 * (E(1, 4) - E(2, 7) - 2*E(3, 6))
    X13 = -sqrt3_6 * (E(1, 5) + E(2, 6) - 2*E(3, 7))
    
    return [X0, X1, X2, X3, X4, X5, X6, X7, X8, X9, X10, X11, X12, X13]


def random_g2_element(scale: float = 0.5) -> np.ndarray:
    """Generate random G₂ element via exponential map."""
    basis = g2_basis_matrices()
    t = np.random.randn(14) * scale
    generator = sum(t[i] * basis[i] for i in range(14))
    return expm(generator)


def apply_g2_to_octonion(g: np.ndarray, a: np.ndarray) -> np.ndarray:
    """Apply G₂ transformation to octonion."""
    result = np.zeros(8)
    result[0] = a[0]
    result[1:8] = g[1:8, 1:8] @ a[1:8]
    return result


def apply_g2_to_sedenion(g: np.ndarray, s: np.ndarray) -> np.ndarray:
    """Apply G₂ to both octonion components of sedenion."""
    a, b = s[:8], s[8:]
    new_a = apply_g2_to_octonion(g, a)
    new_b = apply_g2_to_octonion(g, b)
    return np.concatenate([new_a, new_b])


# =============================================================================
# VERIFICATION TESTS
# =============================================================================

def test_octonion_multiplication():
    """Verify octonion multiplication table."""
    print("=" * 60)
    print("TEST 1: Octonion Multiplication Table")
    print("=" * 60)
    
    errors = []
    
    # Test e_i * e_i = -1 for i = 1..7
    for i in range(1, 8):
        ei = np.zeros(8)
        ei[i] = 1.0
        result = octonion_mult(ei, ei)
        expected = np.zeros(8)
        expected[0] = -1.0
        
        if not np.allclose(result, expected):
            errors.append(f"e_{i} * e_{i} != -1")
    
    # Test some known products from Fano plane
    # e_1 * e_2 = e_3
    e1, e2, e3 = np.zeros(8), np.zeros(8), np.zeros(8)
    e1[1], e2[2], e3[3] = 1, 1, 1
    result = octonion_mult(e1, e2)
    if not np.allclose(result, e3):
        errors.append("e_1 * e_2 != e_3")
    
    # e_2 * e_1 = -e_3 (anti-commutativity)
    result = octonion_mult(e2, e1)
    if not np.allclose(result, -e3):
        errors.append("e_2 * e_1 != -e_3")
    
    if errors:
        print(f"  ✗ FAILED: {len(errors)} errors")
        for e in errors:
            print(f"    - {e}")
        return False
    else:
        print("  ✓ PASSED: All octonion products correct")
        return True


def test_cayley_dickson_formula():
    """Verify Cayley-Dickson formula for sedenions."""
    print("\n" + "=" * 60)
    print("TEST 2: Cayley-Dickson Formula")
    print("=" * 60)
    
    # Test (a, 0) * (c, 0) = (ac, 0)
    a = np.random.randn(8)
    c = np.random.randn(8)
    
    s1 = np.concatenate([a, np.zeros(8)])
    s2 = np.concatenate([c, np.zeros(8)])
    
    result = sedenion_mult(s1, s2)
    expected_a = octonion_mult(a, c)
    expected = np.concatenate([expected_a, np.zeros(8)])
    
    if np.allclose(result, expected, atol=1e-10):
        print("  ✓ PASSED: (a, 0) * (c, 0) = (ac, 0)")
        return True
    else:
        print("  ✗ FAILED: Cayley-Dickson formula incorrect")
        return False


def test_zero_divisors():
    """Verify all 84 canonical zero divisors."""
    print("\n" + "=" * 60)
    print("TEST 3: 84 Canonical Zero Divisors")
    print("=" * 60)
    
    with open('/home/ubuntu/literature_84_pairs.json', 'r') as f:
        raw_pairs = json.load(f)
    
    valid = 0
    invalid = 0
    
    for entry in raw_pairs:
        i, j, k, l = entry
        
        A = sedenion_basis(i) + sedenion_basis(j)
        
        if l > 0:
            B = sedenion_basis(k) + sedenion_basis(l)
        else:
            B = sedenion_basis(k) - sedenion_basis(abs(l))
        
        product = sedenion_mult(A, B)
        norm = np.linalg.norm(product)
        
        if norm < 1e-10:
            valid += 1
        else:
            invalid += 1
    
    print(f"  Valid zero divisors: {valid}/84")
    print(f"  Invalid pairs: {invalid}/84")
    
    if valid == 84:
        print("  ✓ PASSED: All 84 canonical zero divisors verified")
        return True
    else:
        print("  ✗ FAILED: Some pairs are not zero divisors")
        return False


def test_asto5_on_zero_divisors():
    """Verify ASTO₅ breaks zero divisor condition."""
    print("\n" + "=" * 60)
    print("TEST 4: ASTO₅ on Zero Divisors")
    print("=" * 60)
    
    with open('/home/ubuntu/literature_84_pairs.json', 'r') as f:
        raw_pairs = json.load(f)
    
    left_success = 0
    right_success = 0
    
    for entry in raw_pairs:
        i, j, k, l = entry
        
        A = sedenion_basis(i) + sedenion_basis(j)
        
        if l > 0:
            B = sedenion_basis(k) + sedenion_basis(l)
        else:
            B = sedenion_basis(k) - sedenion_basis(abs(l))
        
        # Test left variant
        A_left = asto5_left(A)
        prod_left = sedenion_mult(A_left, B)
        if np.linalg.norm(prod_left) > 1e-8:
            left_success += 1
        
        # Test right variant
        A_right = asto5_right(A)
        prod_right = sedenion_mult(A_right, B)
        if np.linalg.norm(prod_right) > 1e-8:
            right_success += 1
    
    print(f"  ASTO₅ (left) success: {left_success}/84 ({100*left_success/84:.1f}%)")
    print(f"  ASTO₅ (right) success: {right_success}/84 ({100*right_success/84:.1f}%)")
    
    if left_success == 84 and right_success == 84:
        print("  ✓ PASSED: ASTO₅ breaks all 84 zero divisors")
        return True
    else:
        print("  ✗ FAILED: ASTO₅ does not break all zero divisors")
        return False


def test_g2_automorphism():
    """Verify G₂ is an automorphism of octonion multiplication."""
    print("\n" + "=" * 60)
    print("TEST 5: G₂ Automorphism Property")
    print("=" * 60)
    
    max_error = 0.0
    
    for _ in range(100):
        g = random_g2_element(scale=0.3)
        a = np.random.randn(8)
        b = np.random.randn(8)
        
        # g(a*b) vs g(a)*g(b)
        ab = octonion_mult(a, b)
        g_ab = apply_g2_to_octonion(g, ab)
        
        ga = apply_g2_to_octonion(g, a)
        gb = apply_g2_to_octonion(g, b)
        ga_gb = octonion_mult(ga, gb)
        
        error = np.linalg.norm(g_ab - ga_gb)
        max_error = max(max_error, error)
    
    print(f"  Max error: {max_error:.2e}")
    
    if max_error < 1e-10:
        print("  ✓ PASSED: G₂ preserves octonion multiplication")
        return True
    else:
        print("  ✗ FAILED: G₂ does not preserve multiplication")
        return False


def test_g2_preserves_zero_divisors():
    """Verify G₂ transformations preserve zero divisors."""
    print("\n" + "=" * 60)
    print("TEST 6: G₂ Preserves Zero Divisors")
    print("=" * 60)
    
    with open('/home/ubuntu/literature_84_pairs.json', 'r') as f:
        raw_pairs = json.load(f)
    
    preserved = 0
    total = 0
    
    # Test first 20 pairs with 10 G₂ samples each
    for entry in raw_pairs[:20]:
        i, j, k, l = entry
        
        A = sedenion_basis(i) + sedenion_basis(j)
        if l > 0:
            B = sedenion_basis(k) + sedenion_basis(l)
        else:
            B = sedenion_basis(k) - sedenion_basis(abs(l))
        
        for _ in range(10):
            total += 1
            g = random_g2_element(0.5)
            
            A_g = apply_g2_to_sedenion(g, A)
            B_g = apply_g2_to_sedenion(g, B)
            
            product = sedenion_mult(A_g, B_g)
            if np.linalg.norm(product) < 1e-8:
                preserved += 1
    
    print(f"  Zero divisors preserved: {preserved}/{total} ({100*preserved/total:.1f}%)")
    
    if preserved == total:
        print("  ✓ PASSED: G₂ preserves all zero divisors")
        return True
    else:
        print("  ✗ FAILED: G₂ does not preserve all zero divisors")
        return False


def test_asto5_on_g2_transformed():
    """Verify ASTO₅ works on G₂-transformed zero divisors."""
    print("\n" + "=" * 60)
    print("TEST 7: ASTO₅ on G₂-Transformed Zero Divisors")
    print("=" * 60)
    
    with open('/home/ubuntu/literature_84_pairs.json', 'r') as f:
        raw_pairs = json.load(f)
    
    success = 0
    total = 0
    
    # Test first 20 pairs with 10 G₂ samples each
    for entry in raw_pairs[:20]:
        i, j, k, l = entry
        
        A = sedenion_basis(i) + sedenion_basis(j)
        if l > 0:
            B = sedenion_basis(k) + sedenion_basis(l)
        else:
            B = sedenion_basis(k) - sedenion_basis(abs(l))
        
        for _ in range(10):
            g = random_g2_element(0.5)
            
            A_g = apply_g2_to_sedenion(g, A)
            B_g = apply_g2_to_sedenion(g, B)
            
            # Only test if still zero divisor
            if np.linalg.norm(sedenion_mult(A_g, B_g)) < 1e-8:
                total += 1
                
                A_asto = asto5_left(A_g)
                product = sedenion_mult(A_asto, B_g)
                
                if np.linalg.norm(product) > 1e-8:
                    success += 1
    
    print(f"  ASTO₅ success on G₂-transformed: {success}/{total} ({100*success/total:.1f}%)")
    
    if success == total:
        print("  ✓ PASSED: ASTO₅ works on all G₂-transformed zero divisors")
        return True
    else:
        print("  ✗ FAILED: ASTO₅ does not work on all G₂-transformed")
        return False


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("COMPREHENSIVE VERIFICATION OF DV-MATHEMATICS IMPLEMENTATIONS")
    print("=" * 60)
    print("Date: December 22, 2025")
    print("Author: Ivano Franco Malaspina")
    print()
    
    results = []
    
    results.append(("Octonion Multiplication", test_octonion_multiplication()))
    results.append(("Cayley-Dickson Formula", test_cayley_dickson_formula()))
    results.append(("84 Zero Divisors", test_zero_divisors()))
    results.append(("ASTO₅ on Zero Divisors", test_asto5_on_zero_divisors()))
    results.append(("G₂ Automorphism", test_g2_automorphism()))
    results.append(("G₂ Preserves Zero Divisors", test_g2_preserves_zero_divisors()))
    results.append(("ASTO₅ on G₂-Transformed", test_asto5_on_g2_transformed()))
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"  {name}: {status}")
        if not passed:
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 ALL TESTS PASSED - Ready for GitHub upload!")
        sys.exit(0)
    else:
        print("⚠️  SOME TESTS FAILED - Review before upload!")
        sys.exit(1)
