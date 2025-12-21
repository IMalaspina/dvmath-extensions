#!/usr/bin/env python3
"""
G₂-Invarianz Test für ASTO₅ - Version 2

Verwendet die validierten 84 Nullteiler-Paare aus unserer früheren Arbeit.

Autor: Ivano Franco Malaspina
Datum: 22. Dezember 2025
"""

import numpy as np
from scipy.linalg import expm
import json
from typing import Tuple, List

# =============================================================================
# OCTONION MULTIPLICATION (Standard Fano Plane Convention)
# =============================================================================

# Cayley multiplication table for octonions
# e_i * e_j where i,j in {1,...,7}
# Returns (sign, index) where index 0 means real unit

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
    """
    Multiply two octonions using standard Cayley multiplication.
    Octonions are 8-vectors: [real, e1, e2, e3, e4, e5, e6, e7]
    """
    result = np.zeros(8)
    
    # Real * Real
    result[0] = a[0] * b[0]
    
    # Real * Imaginary
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
# SEDENION (DV16) USING CAYLEY-DICKSON
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
# G₂ AUTOMORPHISMS
# =============================================================================

def g2_basis_matrices() -> List[np.ndarray]:
    """
    Construct the 14 basis matrices of the G₂ Lie algebra.
    Based on Reggiani (2024).
    """
    sqrt3_6 = np.sqrt(3) / 6
    
    def E(i, j):
        """E_ij in so(8): antisymmetric matrix"""
        M = np.zeros((8, 8))
        M[i, j] = 1
        M[j, i] = -1
        return M
    
    # Basis from Reggiani's paper
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
    """Apply G₂ transformation to octonion (acts on imaginary part)."""
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
# LOAD VALIDATED 84 PAIRS
# =============================================================================

def load_84_pairs() -> List[Tuple[np.ndarray, np.ndarray]]:
    """Load the validated 84 zero divisor pairs."""
    with open('/home/ubuntu/literature_84_pairs.json', 'r') as f:
        raw_pairs = json.load(f)
    
    pairs = []
    for entry in raw_pairs:
        i, j, k, l = entry
        
        # A = e_i + e_j
        A = sedenion_basis(i) + sedenion_basis(j)
        
        # B = e_k + e_l or e_k - e_l (negative l means minus)
        if l > 0:
            B = sedenion_basis(k) + sedenion_basis(l)
        else:
            B = sedenion_basis(k) - sedenion_basis(abs(l))
        
        pairs.append((A, B))
    
    return pairs


# =============================================================================
# MAIN TEST
# =============================================================================

def test_g2_invariance(num_samples: int = 100):
    """
    Test ASTO₅ on G₂-transformed zero divisors.
    """
    print("=" * 70)
    print("G₂-INVARIANZ TEST FÜR ASTO₅")
    print("=" * 70)
    print()
    
    # Load validated pairs
    pairs = load_84_pairs()
    print(f"Geladene Nullteiler-Paare: {len(pairs)}")
    
    # First verify all pairs are zero divisors
    print("\nVerifiziere Original-Nullteiler...")
    valid_pairs = []
    for idx, (A, B) in enumerate(pairs):
        product = sedenion_mult(A, B)
        norm = np.linalg.norm(product)
        if norm < 1e-10:
            valid_pairs.append((A, B))
        else:
            print(f"  Paar {idx}: Norm = {norm:.2e} (kein Nullteiler)")
    
    print(f"Validierte Nullteiler: {len(valid_pairs)}/{len(pairs)}")
    print()
    
    # Test G₂ invariance
    print(f"Teste G₂-Invarianz mit {num_samples} Samples pro Paar...")
    print()
    
    results = {
        'total_tests': 0,
        'g2_preserves': 0,
        'asto5_left_success': 0,
        'asto5_right_success': 0,
        'both_success': 0
    }
    
    for pair_idx, (A, B) in enumerate(valid_pairs[:20]):  # Test first 20
        if pair_idx % 5 == 0:
            print(f"  Teste Paar {pair_idx + 1}...")
        
        for _ in range(num_samples):
            results['total_tests'] += 1
            
            # Random G₂ transformation
            g = random_g2_element(scale=0.5)
            
            # Transform
            A_g = apply_g2_to_sedenion(g, A)
            B_g = apply_g2_to_sedenion(g, B)
            
            # Check if still zero divisor
            product_g = sedenion_mult(A_g, B_g)
            norm_g = np.linalg.norm(product_g)
            
            if norm_g < 1e-8:
                results['g2_preserves'] += 1
                
                # Test ASTO₅
                A_asto_left = asto5_left(A_g)
                A_asto_right = asto5_right(A_g)
                
                prod_left = sedenion_mult(A_asto_left, B_g)
                prod_right = sedenion_mult(A_asto_right, B_g)
                
                left_ok = np.linalg.norm(prod_left) > 1e-8
                right_ok = np.linalg.norm(prod_right) > 1e-8
                
                if left_ok:
                    results['asto5_left_success'] += 1
                if right_ok:
                    results['asto5_right_success'] += 1
                if left_ok and right_ok:
                    results['both_success'] += 1
    
    # Report
    print()
    print("=" * 70)
    print("ERGEBNISSE")
    print("=" * 70)
    print()
    print(f"Gesamtanzahl Tests: {results['total_tests']}")
    
    preserved = results['g2_preserves']
    print(f"G₂ erhält Nullteiler: {preserved} ({100*preserved/results['total_tests']:.1f}%)")
    
    if preserved > 0:
        print()
        print("Auf G₂-transformierten Nullteilern:")
        print(f"  ASTO₅ (links) erfolgreich:  {results['asto5_left_success']} ({100*results['asto5_left_success']/preserved:.1f}%)")
        print(f"  ASTO₅ (rechts) erfolgreich: {results['asto5_right_success']} ({100*results['asto5_right_success']/preserved:.1f}%)")
        print(f"  Beide erfolgreich:          {results['both_success']} ({100*results['both_success']/preserved:.1f}%)")
    
    # Save results
    with open('/home/ubuntu/g2_asto5_results_v2.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print()
    print("Ergebnisse gespeichert in: /home/ubuntu/g2_asto5_results_v2.json")
    
    return results


def verify_g2_automorphism():
    """Verify G₂ preserves octonion multiplication."""
    print("Verifiziere G₂-Automorphismus-Eigenschaft...")
    
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
    
    print(f"  Max. Fehler: {max_error:.2e}")
    if max_error < 1e-10:
        print("  ✓ G₂ erhält Oktonionen-Multiplikation!")
    else:
        print("  ✗ WARNUNG: Fehler zu groß!")
    print()


if __name__ == "__main__":
    verify_g2_automorphism()
    test_g2_invariance(num_samples=100)
