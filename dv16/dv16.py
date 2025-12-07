"""
DV¹⁶ (Sedenions) Implementation
⚠️ WARNING: EXPERIMENTAL - NOT VALIDATED
This implementation is for research purposes to test the limits of DV-Mathematics.
Sedenions have zero divisors and do not preserve norms.
"""

import sys
sys.path.append('/home/ubuntu/dvmath/research/dv8')
from dv8 import DV8


class DV16:
    """
    16-dimensional DV vector (Sedenions) using Cayley-Dickson construction from DV8.
    
    WARNING: Sedenions have zero divisors and do not preserve norms.
    This implementation is experimental and tests the limits of the DV framework.
    """
    
    def __init__(self, components):
        """Initialize a DV16 vector with 16 components."""
        if isinstance(components, (int, float)):
            self.components = [float(components)] + [0.0] * 15
        elif len(components) == 16:
            self.components = [float(c) for c in components]
        else:
            raise ValueError("DV16 requires exactly 16 components")
    
    def __repr__(self):
        return f"DV16({self.components})"
    
    def __str__(self):
        return f"[{', '.join(f'{c:.6f}' for c in self.components)}]"
    
    def __eq__(self, other):
        if not isinstance(other, DV16):
            return False
        return all(abs(a - b) < 1e-10 for a, b in zip(self.components, other.components))
    
    def __add__(self, other):
        """Component-wise addition."""
        if not isinstance(other, DV16):
            raise TypeError("Can only add DV16 to DV16")
        return DV16([a + b for a, b in zip(self.components, other.components)])
    
    def __sub__(self, other):
        """Component-wise subtraction."""
        if not isinstance(other, DV16):
            raise TypeError("Can only subtract DV16 from DV16")
        return DV16([a - b for a, b in zip(self.components, other.components)])
    
    def __mul__(self, other):
        """
        Cayley-Dickson multiplication for Sedenions.
        (a, b) * (c, d) = (ac - d*b, da + bc*)
        where a, b, c, d are DV8 vectors.
        """
        if isinstance(other, (int, float)):
            return DV16([c * other for c in self.components])
        
        if not isinstance(other, DV16):
            raise TypeError("Can only multiply DV16 by DV16 or scalar")
        
        # Split into two DV8 vectors
        a = DV8(*self.components[:8])
        b = DV8(*self.components[8:])
        c = DV8(*other.components[:8])
        d = DV8(*other.components[8:])
        
        # Cayley-Dickson: (a, b) * (c, d) = (ac - d*b, da + bc*)
        first = a * c - d.conjugate() * b
        second = d * a + b * c.conjugate()
        
        result = first.components + second.components
        return DV16(result)
    
    def __rmul__(self, other):
        """Right multiplication by scalar."""
        if isinstance(other, (int, float)):
            return DV16([other * c for c in self.components])
        return NotImplemented
    
    def __truediv__(self, other):
        """Division with STO fallback for zero divisors."""
        if isinstance(other, (int, float)):
            if abs(other) < 1e-10:
                return self.STO()
            return DV16([c / other for c in self.components])
        
        if not isinstance(other, DV16):
            raise TypeError("Can only divide DV16 by DV16 or scalar")
        
        # Check if divisor is zero or a zero divisor
        if other.norm() < 1e-10:
            return self.STO()
        
        # Try to compute inverse
        try:
            return self * other.inverse()
        except ValueError:
            # If inverse fails (zero divisor), apply STO
            return self.STO()
    
    def norm(self):
        """Euclidean norm (magnitude) of the vector."""
        return sum(c**2 for c in self.components) ** 0.5
    
    def conjugate(self):
        """Sedenion conjugate: negate all components except the first."""
        return DV16([self.components[0]] + [-c for c in self.components[1:]])
    
    def inverse(self):
        """
        Multiplicative inverse.
        WARNING: This will fail for zero divisors!
        """
        norm_sq = sum(c**2 for c in self.components)
        if norm_sq < 1e-10:
            raise ValueError("Cannot compute inverse of zero-norm vector (zero divisor)")
        
        conj = self.conjugate()
        return DV16([c / norm_sq for c in conj.components])
    
    def STO(self):
        """
        Singularity Treatment Operation.
        Defined as multiplication by e₁ (first basis vector).
        """
        e1 = DV16([0, 1] + [0] * 14)
        return self * e1
    
    def is_zero(self):
        """Check if this is a zero vector."""
        return self.norm() < 1e-10


# Basis vectors for testing
def basis_vector(index):
    """Create a basis vector with 1 at the given index."""
    components = [0.0] * 16
    components[index] = 1.0
    return DV16(components)


# Known zero divisor example
def known_zero_divisor():
    """
    Returns a known zero divisor pair: (e₃ + e₁₀, e₆ - e₁₅).
    These should multiply to zero.
    """
    e3 = basis_vector(3)
    e10 = basis_vector(10)
    e6 = basis_vector(6)
    e15 = basis_vector(15)
    
    A = e3 + e10
    B = e6 - e15
    
    return A, B


if __name__ == "__main__":
    print("DV¹⁶ (Sedenions) Implementation")
    print("=" * 50)
    
    # Test basic operations
    a = DV16([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
    b = DV16([16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1])
    
    print(f"\nTest 1: Basic Operations")
    print(f"a = {a}")
    print(f"b = {b}")
    print(f"a + b = {a + b}")
    print(f"a * b = {a * b}")
    print(f"norm(a) = {a.norm():.6f}")
    print(f"norm(b) = {b.norm():.6f}")
    print(f"norm(a*b) = {(a*b).norm():.6f}")
    print(f"norm(a) * norm(b) = {a.norm() * b.norm():.6f}")
    print(f"Norm preserved? {abs((a*b).norm() - a.norm() * b.norm()) < 1e-6}")
    
    # Test known zero divisor
    print(f"\nTest 2: Known Zero Divisor")
    A, B = known_zero_divisor()
    product = A * B
    print(f"A = e₃ + e₁₀ = {A}")
    print(f"B = e₆ - e₁₅ = {B}")
    print(f"A * B = {product}")
    print(f"norm(A * B) = {product.norm():.10f}")
    print(f"Is zero divisor? {product.is_zero()}")
    
    # Test STO
    print(f"\nTest 3: STO on Zero Divisor")
    sto_a = A.STO()
    sto_b = B.STO()
    print(f"STO(A) = {sto_a}")
    print(f"STO(B) = {sto_b}")
    print(f"STO(A) * B = {sto_a * B}")
    print(f"A * STO(B) = {A * sto_b}")
    print(f"Is STO(A) * B zero? {(sto_a * B).is_zero()}")
    print(f"Is A * STO(B) zero? {(A * sto_b).is_zero()}")
