# Author: Ivano Franco Malaspina
# Date: November 30, 2025
# Description: Core implementation of DV-Mathematics, extending DV2 to DV4 to DV8.
# DV2: isomorphic to C (complex), commutative, associative.
# DV4: isomorphic to H (quaternions), non-commutative, associative.
# DV8: isomorphic to O (octonions), non-commutative, non-associative.

import numpy as np
import math

class DV2:
    def __init__(self, v, d=0):
        self.components = np.array([v, d], dtype=float)

    @property
    def v(self):
        return self.components[0]

    @property
    def d(self):
        return self.components[1]

    def __add__(self, other):
        if not isinstance(other, DV2):
            other = DV2(other)
        return DV2(*(self.components + other.components))

    def __sub__(self, other):
        if not isinstance(other, DV2):
            other = DV2(other)
        return DV2(*(self.components - other.components))

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return DV2(*(self.components * other))
        return DV2(
            self.v * other.v - self.d * other.d,
            self.v * other.d + self.d * other.v
        )

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return self.__mul__(other)
        return NotImplemented

    def __truediv__(self, other):
        if not isinstance(other, DV2):
            other = DV2(other)
        if np.isclose(other.norm(), 0, atol=1e-15):
            return self.TR()  # Geometric handling: depth rotation
        return self * other.inverse()

    def __neg__(self):
        return DV2(*(-self.components))

    def norm(self):
        return np.linalg.norm(self.components)

    def is_zero(self):
        return np.isclose(self.norm(), 0, atol=1e-15)

    def normalize(self):
        n = self.norm()
        if self.is_zero():
            raise ValueError("Cannot normalize zero vector")
        return DV2(*(self.components / n))

    def angle(self):
        return math.atan2(self.d, self.v)

    def conjugate(self):
        return DV2(self.v, -self.d)

    def inverse(self):
        n2 = self.norm() ** 2
        if np.isclose(n2, 0, atol=1e-30):
            raise ValueError("Cannot invert zero vector")
        return self.conjugate() * (1 / n2)

    def TR(self):
        # Depth rotation (90 degrees in v-d plane)
        return DV2(-self.d, self.v)

    def to_complex(self):
        return complex(self.v, self.d)

    @classmethod
    def from_complex(cls, z):
        return cls(z.real, z.imag)

    def __str__(self):
        return f"DV2(v={self.v:.4f}, d={self.d:.4f})"

    def __repr__(self):
        return self.__str__()

def dv2_zero():
    return DV2(0, 0)

class DV4:
    def __init__(self, v, d1=0, d2=0, d3=0):
        self.components = np.array([v, d1, d2, d3], dtype=float)

    @property
    def v(self):
        return self.components[0]

    @property
    def d1(self):
        return self.components[1]

    @property
    def d2(self):
        return self.components[2]

    @property
    def d3(self):
        return self.components[3]

    def __add__(self, other):
        if not isinstance(other, DV4):
            other = DV4(other)
        return DV4(*(self.components + other.components))

    def __sub__(self, other):
        if not isinstance(other, DV4):
            other = DV4(other)
        return DV4(*(self.components - other.components))

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return DV4(*(self.components * other))
        a = self.components
        b = other.components
        v = a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3]
        d1 = a[0] * b[1] + a[1] * b[0] + a[2] * b[3] - a[3] * b[2]
        d2 = a[0] * b[2] - a[1] * b[3] + a[2] * b[0] + a[3] * b[1]
        d3 = a[0] * b[3] + a[1] * b[2] - a[2] * b[1] + a[3] * b[0]
        return DV4(v, d1, d2, d3)

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return self.__mul__(other)
        return NotImplemented

    def __truediv__(self, other):
        if not isinstance(other, DV4):
            other = DV4(other)
        if np.isclose(other.norm(), 0, atol=1e-15):
            return self.GTR1()  # Geometric handling: use GTR1 as default rotation
        return self * other.inverse()

    def __neg__(self):
        return DV4(*(-self.components))

    def norm(self):
        return np.linalg.norm(self.components)

    def is_zero(self):
        return np.isclose(self.norm(), 0, atol=1e-15)

    def conjugate(self):
        return DV4(self.v, -self.d1, -self.d2, -self.d3)

    def inverse(self):
        n2 = self.norm() ** 2
        if np.isclose(n2, 0, atol=1e-30):
            raise ValueError("Cannot invert zero vector")
        return self.conjugate() * (1 / n2)

    def GTR1(self):
        i = dv4_i()
        return self * i

    def GTR2(self):
        j = dv4_j()
        return self * j

    def GTR3(self):
        k = dv4_k()
        return self * k

    def commutator(self, other):
        return self * other - other * self

    def __str__(self):
        return f"DV4(v={self.v:.4f}, d1={self.d1:.4f}, d2={self.d2:.4f}, d3={self.d3:.4f})"

    def __repr__(self):
        return self.__str__()

def dv4_i():
    return DV4(0, 1, 0, 0)

def dv4_j():
    return DV4(0, 0, 1, 0)

def dv4_k():
    return DV4(0, 0, 0, 1)

def dv4_zero():
    return DV4(0, 0, 0, 0)

# DV8 (Octonions) implementation
class DV8:
    def __init__(self, v, d1=0, d2=0, d3=0, d4=0, d5=0, d6=0, d7=0):
        self.components = np.array([v, d1, d2, d3, d4, d5, d6, d7], dtype=float)

    @property
    def v(self):
        return self.components[0]

    def __add__(self, other):
        if not isinstance(other, DV8):
            other = DV8(other)
        return DV8(*(self.components + other.components))

    def __sub__(self, other):
        if not isinstance(other, DV8):
            other = DV8(other)
        return DV8(*(self.components - other.components))

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return DV8(*(self.components * other))
        a = self.components
        b = other.components
        result = np.zeros(8)
        # Real part: v1*v2 - vec1 · vec2
        result[0] = a[0] * b[0] - np.dot(a[1:], b[1:])
        # Scalar * vector terms
        result[1:] += a[0] * b[1:] + b[0] * a[1:]
        # Vector cross terms using structure constants
        for i in range(1, 8):
            for j in range(1, 8):
                if i != j:
                    k = OCT_ABS_TABLE[i, j]
                    s = OCT_SIGNS[i, j]
                    result[k] += s * a[i] * b[j]
        return DV8(*result)

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return self.__mul__(other)
        return NotImplemented

    def __truediv__(self, other):
        if not isinstance(other, DV8):
            other = DV8(other)
        if np.isclose(other.norm(), 0, atol=1e-15):
            return self.GTR1()  # Default to GTR1 for zero-division
        return self * other.inverse()

    def __neg__(self):
        return DV8(*(-self.components))

    def norm(self):
        return np.linalg.norm(self.components)

    def is_zero(self):
        return np.isclose(self.norm(), 0, atol=1e-15)

    def conjugate(self):
        return DV8(self.v, *(-self.components[1:]))

    def inverse(self):
        n2 = self.norm() ** 2
        if np.isclose(n2, 0, atol=1e-30):
            raise ValueError("Cannot invert zero vector")
        return self.conjugate() * (1 / n2)

    def GTR1(self):
        return self * dv8_e1()

    def GTR2(self):
        return self * dv8_e2()

    def GTR3(self):
        return self * dv8_e3()

    def GTR4(self):
        return self * dv8_e4()

    def GTR5(self):
        return self * dv8_e5()

    def GTR6(self):
        return self * dv8_e6()

    def GTR7(self):
        return self * dv8_e7()

    def commutator(self, other):
        return self * other - other * self

    def __str__(self):
        return f"DV8(v={self.v:.4f}, d1={self.components[1]:.4f}, d2={self.components[2]:.4f}, d3={self.components[3]:.4f}, d4={self.components[4]:.4f}, d5={self.components[5]:.4f}, d6={self.components[6]:.4f}, d7={self.components[7]:.4f})"

    def __repr__(self):
        return self.__str__()

# Octonion multiplication tables (for cross terms only)
OCT_TABLE = np.array([
    [0, 1, 2, 3, 4, 5, 6, 7],
    [1, 0, 3, -2, 5, -4, -7, 6],
    [2, -3, 0, 1, 6, 7, -4, -5],
    [3, 2, -1, 0, 7, -6, 5, -4],
    [4, -5, -6, -7, 0, 1, 2, 3],
    [5, 4, -7, 6, -1, 0, -3, 2],
    [6, 7, 4, -5, -2, 3, 0, -1],
    [7, -6, 5, 4, -3, -2, 1, 0]
])
OCT_SIGNS = np.sign(OCT_TABLE)
OCT_ABS_TABLE = np.abs(OCT_TABLE)

def dv8_e1():
    return DV8(0, 1, 0, 0, 0, 0, 0, 0)

def dv8_e2():
    return DV8(0, 0, 1, 0, 0, 0, 0, 0)

def dv8_e3():
    return DV8(0, 0, 0, 1, 0, 0, 0, 0)

def dv8_e4():
    return DV8(0, 0, 0, 0, 1, 0, 0, 0)

def dv8_e5():
    return DV8(0, 0, 0, 0, 0, 1, 0, 0)

def dv8_e6():
    return DV8(0, 0, 0, 0, 0, 0, 1, 0)

def dv8_e7():
    return DV8(0, 0, 0, 0, 0, 0, 0, 1)

def dv8_zero():
    return DV8(0, 0, 0, 0, 0, 0, 0, 0)