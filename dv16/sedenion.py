"""
DV16 (Sedenions) - EXPERIMENTAL PROTOTYPE
==========================================

⚠️ WARNING: This implementation is NOT VALIDATED and is purely experimental.

Key Challenges:
- Loss of norm preservation (zero divisors exist)
- Loss of alternativity
- Potential inconsistencies in STO application

Status: Research Prototype
Last Updated: December 2025
"""

import math
from typing import List, Tuple


class DV16:
    """
    16-dimensional Sedenion implementation using Cayley-Dickson construction.
    
    ⚠️ EXPERIMENTAL: Contains zero divisors and does not preserve norm in all cases.
    """
    
    def __init__(self, components: List[float]):
        """
        Initialize a DV16 (Sedenion) vector.
        
        Args:
            components: List of 16 float values
        """
        if len(components) != 16:
            raise ValueError("DV16 requires exactly 16 components")
        self.components = tuple(components)
    
    def __repr__(self) -> str:
        return f"DV16({list(self.components)})"
    
    def __str__(self) -> str:
        return f"[{', '.join(f'{c:.4f}' for c in self.components)}]"
    
    # ============================================================================
    # Cayley-Dickson Multiplication
    # ============================================================================
    
    def __mul__(self, other: 'DV16') -> 'DV16':
        """
        Sedenion multiplication via Cayley-Dickson construction.
        
        ⚠️ WARNING: This operation may produce zero divisors.
        Example: There exist non-zero a, b such that a * b = 0
        """
        # Split into two octonions
        a_left = list(self.components[:8])
        a_right = list(self.components[8:])
        b_left = list(other.components[:8])
        b_right = list(other.components[8:])
        
        # Import DV8 for octonion operations
        # This creates a dependency on the validated dvmath repository
        try:
            import sys
            sys.path.insert(0, '/home/ubuntu/dvmath/research/dv8')
            from dv8 import DV8
            
            a_l = DV8(a_left)
            a_r = DV8(a_right)
            b_l = DV8(b_left)
            b_r = DV8(b_right)
            
            # Cayley-Dickson formula: (a, b) * (c, d) = (ac - d*b, da + bc*)
            left_part = a_l * b_l - b_r.conjugate() * a_r
            right_part = b_r * a_l + a_r * b_l.conjugate()
            
            result_components = list(left_part.components) + list(right_part.components)
            return DV16(result_components)
        
        except ImportError:
            raise RuntimeError("DV16 requires DV8 from dvmath repository. Please ensure dvmath is installed.")
    
    # ============================================================================
    # Basic Operations
    # ============================================================================
    
    def __add__(self, other: 'DV16') -> 'DV16':
        """Component-wise addition."""
        return DV16([a + b for a, b in zip(self.components, other.components)])
    
    def __sub__(self, other: 'DV16') -> 'DV16':
        """Component-wise subtraction."""
        return DV16([a - b for a, b in zip(self.components, other.components)])
    
    def __neg__(self) -> 'DV16':
        """Negation."""
        return DV16([-c for c in self.components])
    
    def __truediv__(self, other: 'DV16') -> 'DV16':
        """
        Division via multiplication by inverse.
        
        ⚠️ WARNING: May fail for zero divisors.
        """
        if other.is_zero():
            return self.STO()
        return self * other.inverse()
    
    # ============================================================================
    # Algebraic Properties
    # ============================================================================
    
    def norm(self) -> float:
        """
        Euclidean norm.
        
        ⚠️ NOTE: Norm is NOT preserved under multiplication for sedenions.
        """
        return math.sqrt(sum(c**2 for c in self.components))
    
    def conjugate(self) -> 'DV16':
        """
        Sedenion conjugate: negate all components except the first.
        """
        return DV16([self.components[0]] + [-c for c in self.components[1:]])
    
    def inverse(self) -> 'DV16':
        """
        Multiplicative inverse.
        
        ⚠️ WARNING: May not exist for zero divisors.
        """
        norm_sq = sum(c**2 for c in self.components)
        if norm_sq < 1e-10:
            raise ZeroDivisionError("Cannot invert zero-norm sedenion (potential zero divisor)")
        
        conj = self.conjugate()
        return DV16([c / norm_sq for c in conj.components])
    
    def is_zero(self) -> bool:
        """Check if the sedenion is approximately zero."""
        return self.norm() < 1e-10
    
    # ============================================================================
    # STO (Singularity Treatment Operation)
    # ============================================================================
    
    def STO(self) -> 'DV16':
        """
        Singularity Treatment Operation for DV16.
        
        ⚠️ EXPERIMENTAL: The consistency of STO in the presence of zero divisors
        is an open research question.
        
        Current implementation: Rotate into the first orthogonal dimension (e1).
        """
        # Rotate: [v, d1, d2, ..., d15] -> [0, v, -d2, d1, -d4, d3, ...]
        # This is a generalization of GTR1, but its mathematical validity is unproven.
        result = [0.0] * 16
        result[1] = self.components[0]  # v -> d1
        
        # Apply alternating pattern for higher dimensions
        for i in range(1, 15, 2):
            result[i+1] = -self.components[i+1]
            if i+2 < 16:
                result[i+2] = self.components[i]
        
        return DV16(result)
    
    # ============================================================================
    # Utility Methods
    # ============================================================================
    
    def __eq__(self, other: 'DV16') -> bool:
        """Equality check with tolerance."""
        if not isinstance(other, DV16):
            return False
        return all(abs(a - b) < 1e-10 for a, b in zip(self.components, other.components))
    
    @classmethod
    def zero(cls) -> 'DV16':
        """Return the zero sedenion."""
        return cls([0.0] * 16)
    
    @classmethod
    def one(cls) -> 'DV16':
        """Return the multiplicative identity."""
        return cls([1.0] + [0.0] * 15)
    
    @classmethod
    def basis(cls, index: int) -> 'DV16':
        """
        Return the i-th basis sedenion.
        
        Args:
            index: 0-15 (e0, e1, ..., e15)
        """
        if not 0 <= index < 16:
            raise ValueError("Basis index must be 0-15")
        components = [0.0] * 16
        components[index] = 1.0
        return cls(components)


# ============================================================================
# Module-level Constants
# ============================================================================

ZERO = DV16.zero()
ONE = DV16.one()

# Basis elements
e0 = DV16.basis(0)
e1 = DV16.basis(1)
e2 = DV16.basis(2)
e3 = DV16.basis(3)
e4 = DV16.basis(4)
e5 = DV16.basis(5)
e6 = DV16.basis(6)
e7 = DV16.basis(7)
e8 = DV16.basis(8)
e9 = DV16.basis(9)
e10 = DV16.basis(10)
e11 = DV16.basis(11)
e12 = DV16.basis(12)
e13 = DV16.basis(13)
e14 = DV16.basis(14)
e15 = DV16.basis(15)
