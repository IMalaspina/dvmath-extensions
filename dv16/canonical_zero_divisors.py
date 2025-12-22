"""
84 Canonical Zero Divisors of DV¹⁶ (Sedenions)
===============================================

This module contains the complete list of 84 canonical zero divisor pairs
from the mathematical literature.

Source: Wikipedia Sedenion article, Reggiani (2024) arXiv:2411.18881v1

All pairs have the form: (eᵢ + eⱼ) × (eₖ ± eₗ) = 0
where i, j, k, l are distinct basis indices.

Status: VALIDATED (December 2025)
- All 84 pairs confirmed as zero divisors using correct Cayley-Dickson multiplication
- ASTO₅ achieves 100% success rate on all pairs

Author: Ivano Franco Malaspina
Date: December 2025

IMPORTANT: This file was corrected on 22.12.2025 after external review
identified sign errors in the original transcription.
"""

import json
import os
from typing import List, Tuple

# Get the directory where this file is located
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# Load the validated pairs from JSON
def _load_pairs():
    """Load the 84 canonical pairs from the validated JSON file."""
    json_path = os.path.join(_THIS_DIR, 'literature_84_pairs.json')
    with open(json_path, 'r') as f:
        return json.load(f)

# The 84 canonical zero divisor pairs loaded from validated JSON
# Format in JSON: [i, j, k, l] where negative l means (eₖ - e|l|)
_RAW_PAIRS = _load_pairs()


def get_pair_indices(index: int) -> Tuple[int, int, int, int, int]:
    """
    Get the indices for a zero divisor pair.
    
    Args:
        index: Index from 0 to 83
    
    Returns:
        Tuple of (i, j, k, l, sign) where:
        - (eᵢ + eⱼ) × (eₖ + sign*eₗ) = 0
        - sign is +1 or -1
    """
    if index < 0 or index >= len(_RAW_PAIRS):
        raise IndexError(f"Index must be 0-{len(_RAW_PAIRS)-1}")
    
    i, j, k, l = _RAW_PAIRS[index]
    
    # Handle sign encoding: negative l means subtract
    if l < 0:
        sign = -1
        l = abs(l)
    else:
        sign = +1
    
    return i, j, k, l, sign


def format_pair(index: int) -> str:
    """
    Format a zero divisor pair as a human-readable string.
    
    Args:
        index: Index from 0 to 83
    
    Returns:
        String like "(e₁ + e₁₀) × (e₅ + e₁₄)"
    """
    i, j, k, l, sign = get_pair_indices(index)
    sign_str = "+" if sign > 0 else "-"
    return f"(e{i} + e{j}) × (e{k} {sign_str} e{l})"


def get_total_pairs() -> int:
    """Return the total number of canonical zero divisor pairs."""
    return len(_RAW_PAIRS)


# ============================================================
# SEDENION IMPLEMENTATION FOR STANDALONE TESTING
# ============================================================

class _Quaternion:
    """Internal quaternion implementation for Cayley-Dickson construction."""
    
    def __init__(self, *components):
        if len(components) == 1 and hasattr(components[0], '__iter__'):
            components = tuple(components[0])
        self.components = tuple(float(c) for c in components) if len(components) == 4 else (0.0,) * 4
        if len(self.components) != 4:
            self.components = tuple(list(self.components) + [0.0] * (4 - len(self.components)))[:4]
    
    def __add__(self, other):
        return _Quaternion(*[a + b for a, b in zip(self.components, other.components)])
    
    def __sub__(self, other):
        return _Quaternion(*[a - b for a, b in zip(self.components, other.components)])
    
    def __neg__(self):
        return _Quaternion(*[-c for c in self.components])
    
    def conjugate(self):
        return _Quaternion(self.components[0], *[-c for c in self.components[1:]])
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return _Quaternion(*[c * other for c in self.components])
        a1, b1, c1, d1 = self.components
        a2, b2, c2, d2 = other.components
        return _Quaternion(
            a1*a2 - b1*b2 - c1*c2 - d1*d2,
            a1*b2 + b1*a2 + c1*d2 - d1*c2,
            a1*c2 - b1*d2 + c1*a2 + d1*b2,
            a1*d2 + b1*c2 - c1*b2 + d1*a2
        )


class _Octonion:
    """Internal octonion implementation for Cayley-Dickson construction."""
    
    def __init__(self, *components):
        if len(components) == 1 and hasattr(components[0], '__iter__'):
            components = tuple(components[0])
        self.components = tuple(float(c) for c in components) if len(components) == 8 else (0.0,) * 8
        if len(self.components) != 8:
            self.components = tuple(list(self.components) + [0.0] * (8 - len(self.components)))[:8]
    
    def __add__(self, other):
        return _Octonion(*[a + b for a, b in zip(self.components, other.components)])
    
    def __sub__(self, other):
        return _Octonion(*[a - b for a, b in zip(self.components, other.components)])
    
    def __neg__(self):
        return _Octonion(*[-c for c in self.components])
    
    def conjugate(self):
        return _Octonion(self.components[0], *[-c for c in self.components[1:]])
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return _Octonion(*[c * other for c in self.components])
        a = _Quaternion(*self.components[0:4])
        b = _Quaternion(*self.components[4:8])
        c = _Quaternion(*other.components[0:4])
        d = _Quaternion(*other.components[4:8])
        first = a * c - d.conjugate() * b
        second = d * a + b * c.conjugate()
        return _Octonion(*first.components, *second.components)


class _Sedenion:
    """Internal sedenion implementation for validation."""
    
    def __init__(self, *components):
        if len(components) == 1 and hasattr(components[0], '__iter__'):
            components = tuple(components[0])
        self.components = tuple(float(c) for c in components) if len(components) == 16 else (0.0,) * 16
        if len(self.components) != 16:
            self.components = tuple(list(self.components) + [0.0] * (16 - len(self.components)))[:16]
    
    def __add__(self, other):
        if isinstance(other, (int, float)):
            result = list(self.components)
            result[0] += other
            return _Sedenion(*result)
        return _Sedenion(*[a + b for a, b in zip(self.components, other.components)])
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        return _Sedenion(*[a - b for a, b in zip(self.components, other.components)])
    
    def __neg__(self):
        return _Sedenion(*[-c for c in self.components])
    
    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return _Sedenion(*[c * other for c in self.components])
        return NotImplemented
    
    def conjugate(self):
        return _Sedenion(self.components[0], *[-c for c in self.components[1:]])
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return _Sedenion(*[c * other for c in self.components])
        a = _Octonion(*self.components[0:8])
        b = _Octonion(*self.components[8:16])
        c = _Octonion(*other.components[0:8])
        d = _Octonion(*other.components[8:16])
        first = a * c - d.conjugate() * b
        second = d * a + b * c.conjugate()
        return _Sedenion(*first.components, *second.components)
    
    def norm(self):
        return sum(c**2 for c in self.components) ** 0.5
    
    def is_zero(self, tol=1e-10):
        return self.norm() < tol


def _e(i):
    """Create basis element e_i."""
    components = [0.0] * 16
    components[i] = 1.0
    return _Sedenion(*components)


def get_zero_divisor_pair(index: int) -> Tuple['_Sedenion', '_Sedenion']:
    """
    Get a zero divisor pair by index using internal implementation.
    
    Args:
        index: Index from 0 to 83
    
    Returns:
        Tuple of (A, B) where A × B = 0
    """
    i, j, k, l, sign = get_pair_indices(index)
    A = _e(i) + _e(j)
    B = _e(k) + sign * _e(l)
    return A, B


def asto5_left(s: '_Sedenion') -> '_Sedenion':
    """Apply ASTO₅ (left multiplication by e₁ on first octonion)."""
    return _e(1) * s


def asto5_right(s: '_Sedenion') -> '_Sedenion':
    """Apply ASTO₅ (right multiplication by e₁ on first octonion)."""
    return s * _e(1)


# ============================================================
# VALIDATION
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("VALIDATION: 84 Canonical Zero Divisors")
    print("Source: literature_84_pairs.json")
    print("=" * 70)
    
    zd_success = 0
    asto_left_success = 0
    asto_right_success = 0
    
    for i in range(get_total_pairs()):
        A, B = get_zero_divisor_pair(i)
        product = A * B
        
        is_zero = product.is_zero()
        if is_zero:
            zd_success += 1
        
        # Test ASTO₅ (left)
        asto_left_result = asto5_left(A) * B
        asto_left_works = not asto_left_result.is_zero()
        if asto_left_works:
            asto_left_success += 1
        
        # Test ASTO₅ (right)
        asto_right_result = asto5_right(A) * B
        asto_right_works = not asto_right_result.is_zero()
        if asto_right_works:
            asto_right_success += 1
        
        zd_status = "✓" if is_zero else "✗"
        asto_l_status = "✓" if asto_left_works else "✗"
        asto_r_status = "✓" if asto_right_works else "✗"
        
        print(f"{i+1:3d}. {format_pair(i):35s} | ZD: {zd_status} | ASTO₅L: {asto_l_status} | ASTO₅R: {asto_r_status}")
    
    print("=" * 70)
    print(f"Zero Divisors Confirmed: {zd_success}/{get_total_pairs()} ({100*zd_success/get_total_pairs():.1f}%)")
    print(f"ASTO₅ (Left) Success:    {asto_left_success}/{get_total_pairs()} ({100*asto_left_success/get_total_pairs():.1f}%)")
    print(f"ASTO₅ (Right) Success:   {asto_right_success}/{get_total_pairs()} ({100*asto_right_success/get_total_pairs():.1f}%)")
    print("=" * 70)
    
    if zd_success == get_total_pairs():
        print("\n✅ ALL 84 PAIRS ARE VALID ZERO DIVISORS!")
    else:
        print(f"\n❌ ERROR: {get_total_pairs() - zd_success} pairs are NOT zero divisors!")
