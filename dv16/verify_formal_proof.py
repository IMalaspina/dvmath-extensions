#!/usr/bin/env python3
"""
Verification of Formal Proof Claims

This script verifies the key claims in the formal proof:
1. The associator [e₁, a, c] is non-zero for most octonion triples
2. ASTO₅ breaks the zero divisor condition via non-associativity
3. Both left and right variants work

Author: Ivano Franco Malaspina
Date: December 22, 2025
"""

import numpy as np
from verify_all_implementations import (
    octonion_mult, octonion_conj, sedenion_mult, sedenion_basis,
    asto5_left, asto5_right
)
import json


def compute_associator(x, y, z):
    """
    Compute the associator [x, y, z] = (xy)z - x(yz)
    """
    xy = octonion_mult(x, y)
    xyz_left = octonion_mult(xy, z)
    
    yz = octonion_mult(y, z)
    xyz_right = octonion_mult(x, yz)
    
    return xyz_left - xyz_right


def test_associator_non_zero():
    """
    Verify that the associator [e₁, eᵢ, eⱼ] is non-zero for most i, j.
    """
    print("=" * 60)
    print("PROOF VERIFICATION 1: Associator Non-Zero")
    print("=" * 60)
    
    e1 = np.zeros(8)
    e1[1] = 1.0
    
    non_zero_count = 0
    zero_count = 0
    
    print("\n  Associator [e₁, eᵢ, eⱼ] for i, j ∈ {1, ..., 7}:")
    print()
    
    for i in range(1, 8):
        for j in range(1, 8):
            ei = np.zeros(8)
            ei[i] = 1.0
            ej = np.zeros(8)
            ej[j] = 1.0
            
            assoc = compute_associator(e1, ei, ej)
            norm = np.linalg.norm(assoc)
            
            if norm > 1e-10:
                non_zero_count += 1
            else:
                zero_count += 1
    
    print(f"  Non-zero associators: {non_zero_count}/49")
    print(f"  Zero associators: {zero_count}/49")
    print()
    
    # The claim is that MOST associators are non-zero
    if non_zero_count > zero_count:
        print("  ✓ VERIFIED: Most associators [e₁, eᵢ, eⱼ] are non-zero")
        return True
    else:
        print("  ✗ NOT VERIFIED: Most associators are zero")
        return False


def test_asto5_breaks_condition():
    """
    Verify that ASTO₅ breaks the zero divisor condition by showing
    (e₁a)c ≠ ac for a specific zero divisor.
    """
    print("\n" + "=" * 60)
    print("PROOF VERIFICATION 2: ASTO₅ Breaks Zero Divisor Condition")
    print("=" * 60)
    
    # Take the first canonical zero divisor: (e₁ + e₁₀) × (e₅ + e₁₄) = 0
    # A = e₁ + e₁₀ = (e₁, e₂) in octonion pair notation
    # B = e₅ + e₁₄ = (e₅, e₆)
    
    A = sedenion_basis(1) + sedenion_basis(10)
    B = sedenion_basis(5) + sedenion_basis(14)
    
    # Extract octonion components
    a, b = A[:8], A[8:]
    c, d = B[:8], B[8:]
    
    print(f"\n  Zero divisor: A = e₁ + e₁₀, B = e₅ + e₁₄")
    print(f"  A × B norm: {np.linalg.norm(sedenion_mult(A, B)):.2e}")
    
    # Original product ac
    ac = octonion_mult(a, c)
    print(f"\n  Original: ac = {ac}")
    
    # After ASTO₅: (e₁a)c
    e1 = np.zeros(8)
    e1[1] = 1.0
    e1_a = octonion_mult(e1, a)
    e1_a_c = octonion_mult(e1_a, c)
    print(f"  After ASTO₅: (e₁a)c = {e1_a_c}")
    
    # Check if they are different
    diff = np.linalg.norm(e1_a_c - ac)
    print(f"\n  Difference ||(e₁a)c - ac||: {diff:.4f}")
    
    if diff > 1e-10:
        print("  ✓ VERIFIED: (e₁a)c ≠ ac, ASTO₅ breaks the condition")
        return True
    else:
        print("  ✗ NOT VERIFIED: (e₁a)c = ac")
        return False


def test_both_variants_work():
    """
    Verify that both left and right ASTO₅ variants work on all 84 pairs.
    """
    print("\n" + "=" * 60)
    print("PROOF VERIFICATION 3: Both ASTO₅ Variants Work")
    print("=" * 60)
    
    with open('/home/ubuntu/literature_84_pairs.json', 'r') as f:
        raw_pairs = json.load(f)
    
    left_success = 0
    right_success = 0
    both_success = 0
    
    for entry in raw_pairs:
        i, j, k, l = entry
        
        A = sedenion_basis(i) + sedenion_basis(j)
        if l > 0:
            B = sedenion_basis(k) + sedenion_basis(l)
        else:
            B = sedenion_basis(k) - sedenion_basis(abs(l))
        
        # Test left
        A_left = asto5_left(A)
        left_ok = np.linalg.norm(sedenion_mult(A_left, B)) > 1e-8
        
        # Test right
        A_right = asto5_right(A)
        right_ok = np.linalg.norm(sedenion_mult(A_right, B)) > 1e-8
        
        if left_ok:
            left_success += 1
        if right_ok:
            right_success += 1
        if left_ok and right_ok:
            both_success += 1
    
    print(f"\n  Left variant success: {left_success}/84")
    print(f"  Right variant success: {right_success}/84")
    print(f"  Both variants success: {both_success}/84")
    
    if both_success == 84:
        print("\n  ✓ VERIFIED: Both ASTO₅ variants work on all 84 pairs")
        return True
    else:
        print("\n  ✗ NOT VERIFIED: Not all pairs work with both variants")
        return False


def test_universality_claim():
    """
    Verify the main theorem: ASTO₅(S₁) × S₂ ≠ 0 for all zero divisor pairs.
    """
    print("\n" + "=" * 60)
    print("PROOF VERIFICATION 4: Main Theorem (Universality)")
    print("=" * 60)
    
    with open('/home/ubuntu/literature_84_pairs.json', 'r') as f:
        raw_pairs = json.load(f)
    
    # Test on A
    success_on_A = 0
    for entry in raw_pairs:
        i, j, k, l = entry
        A = sedenion_basis(i) + sedenion_basis(j)
        if l > 0:
            B = sedenion_basis(k) + sedenion_basis(l)
        else:
            B = sedenion_basis(k) - sedenion_basis(abs(l))
        
        A_asto = asto5_left(A)
        if np.linalg.norm(sedenion_mult(A_asto, B)) > 1e-8:
            success_on_A += 1
    
    # Test on B
    success_on_B = 0
    for entry in raw_pairs:
        i, j, k, l = entry
        A = sedenion_basis(i) + sedenion_basis(j)
        if l > 0:
            B = sedenion_basis(k) + sedenion_basis(l)
        else:
            B = sedenion_basis(k) - sedenion_basis(abs(l))
        
        B_asto = asto5_left(B)
        if np.linalg.norm(sedenion_mult(A, B_asto)) > 1e-8:
            success_on_B += 1
    
    print(f"\n  ASTO₅(S₁) × S₂ ≠ 0: {success_on_A}/84")
    print(f"  S₁ × ASTO₅(S₂) ≠ 0: {success_on_B}/84")
    
    if success_on_A == 84 and success_on_B == 84:
        print("\n  ✓ VERIFIED: Main theorem holds for all 84 pairs")
        return True
    else:
        print("\n  ✗ NOT VERIFIED: Main theorem does not hold for all pairs")
        return False


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("VERIFICATION OF FORMAL PROOF CLAIMS")
    print("=" * 60)
    print("Date: December 22, 2025")
    print()
    
    results = []
    
    results.append(("Associator Non-Zero", test_associator_non_zero()))
    results.append(("ASTO₅ Breaks Condition", test_asto5_breaks_condition()))
    results.append(("Both Variants Work", test_both_variants_work()))
    results.append(("Main Theorem", test_universality_claim()))
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "✓ VERIFIED" if passed else "✗ NOT VERIFIED"
        print(f"  {name}: {status}")
        if not passed:
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 ALL PROOF CLAIMS VERIFIED!")
    else:
        print("⚠️  SOME CLAIMS NOT VERIFIED - Review proof!")
