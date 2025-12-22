"""
Detailed analysis of the 12 pairs where ASTO₅ fails.
"""

import json
import os

# ============================================================
# CORRECT CAYLEY-DICKSON IMPLEMENTATION
# ============================================================

class Quaternion:
    def __init__(self, *components):
        if len(components) == 1 and hasattr(components[0], '__iter__'):
            components = tuple(components[0])
        self.components = tuple(float(c) for c in components) if len(components) == 4 else (0.0,) * 4
        if len(self.components) != 4:
            self.components = tuple(list(self.components) + [0.0] * (4 - len(self.components)))[:4]
    
    def __add__(self, other):
        return Quaternion(*[a + b for a, b in zip(self.components, other.components)])
    
    def __sub__(self, other):
        return Quaternion(*[a - b for a, b in zip(self.components, other.components)])
    
    def __neg__(self):
        return Quaternion(*[-c for c in self.components])
    
    def conjugate(self):
        return Quaternion(self.components[0], *[-c for c in self.components[1:]])
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Quaternion(*[c * other for c in self.components])
        a1, b1, c1, d1 = self.components
        a2, b2, c2, d2 = other.components
        return Quaternion(
            a1*a2 - b1*b2 - c1*c2 - d1*d2,
            a1*b2 + b1*a2 + c1*d2 - d1*c2,
            a1*c2 - b1*d2 + c1*a2 + d1*b2,
            a1*d2 + b1*c2 - c1*b2 + d1*a2
        )


class Octonion:
    def __init__(self, *components):
        if len(components) == 1 and hasattr(components[0], '__iter__'):
            components = tuple(components[0])
        self.components = tuple(float(c) for c in components) if len(components) == 8 else (0.0,) * 8
        if len(self.components) != 8:
            self.components = tuple(list(self.components) + [0.0] * (8 - len(self.components)))[:8]
    
    def __add__(self, other):
        return Octonion(*[a + b for a, b in zip(self.components, other.components)])
    
    def __sub__(self, other):
        return Octonion(*[a - b for a, b in zip(self.components, other.components)])
    
    def __neg__(self):
        return Octonion(*[-c for c in self.components])
    
    def conjugate(self):
        return Octonion(self.components[0], *[-c for c in self.components[1:]])
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Octonion(*[c * other for c in self.components])
        a = Quaternion(*self.components[0:4])
        b = Quaternion(*self.components[4:8])
        c = Quaternion(*other.components[0:4])
        d = Quaternion(*other.components[4:8])
        first = a * c - d.conjugate() * b
        second = d * a + b * c.conjugate()
        return Octonion(*first.components, *second.components)


class Sedenion:
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
            return Sedenion(*result)
        return Sedenion(*[a + b for a, b in zip(self.components, other.components)])
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        return Sedenion(*[a - b for a, b in zip(self.components, other.components)])
    
    def __neg__(self):
        return Sedenion(*[-c for c in self.components])
    
    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return Sedenion(*[c * other for c in self.components])
        return NotImplemented
    
    def conjugate(self):
        return Sedenion(self.components[0], *[-c for c in self.components[1:]])
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Sedenion(*[c * other for c in self.components])
        a = Octonion(*self.components[0:8])
        b = Octonion(*self.components[8:16])
        c = Octonion(*other.components[0:8])
        d = Octonion(*other.components[8:16])
        first = a * c - d.conjugate() * b
        second = d * a + b * c.conjugate()
        return Sedenion(*first.components, *second.components)
    
    def norm(self):
        return sum(c**2 for c in self.components) ** 0.5
    
    def is_zero(self, tol=1e-10):
        return self.norm() < tol
    
    def __repr__(self):
        non_zero = [(i, c) for i, c in enumerate(self.components) if abs(c) > 1e-10]
        if not non_zero:
            return "0"
        terms = []
        for i, c in non_zero:
            if i == 0:
                terms.append(f"{c:.2f}")
            else:
                sign = "+" if c > 0 else ""
                terms.append(f"{sign}{c:.2f}e{i}")
        return " ".join(terms)


def e(i):
    components = [0.0] * 16
    components[i] = 1.0
    return Sedenion(*components)


# ============================================================
# ASTO VARIANTS
# ============================================================

def asto5_left(s):
    """ASTO₅: Left multiplication by e₁"""
    return e(1) * s

def asto5_right(s):
    """ASTO₅: Right multiplication by e₁"""
    return s * e(1)

def asto_e2_left(s):
    """Alternative: Left multiplication by e₂"""
    return e(2) * s

def asto_e8_left(s):
    """Alternative: Left multiplication by e₈ (first element of second octonion)"""
    return e(8) * s

def asto_e9_left(s):
    """Alternative: Left multiplication by e₉"""
    return e(9) * s

def asto_partial_second(s):
    """ASTO on second octonion only: (a, e₁b)"""
    a = Octonion(*s.components[0:8])
    b = Octonion(*s.components[8:16])
    e1_oct = Octonion(0, 1, 0, 0, 0, 0, 0, 0)
    b_transformed = e1_oct * b
    return Sedenion(*a.components, *b_transformed.components)


# ============================================================
# ANALYSIS
# ============================================================

# The 12 problematic pairs (indices in the JSON file, 0-based)
PROBLEMATIC_INDICES = [34, 37, 38, 41, 53, 54, 56, 57, 63, 64, 72, 74]

def load_pairs():
    with open('/home/ubuntu/dvmath-extensions/dv16/literature_84_pairs.json', 'r') as f:
        return json.load(f)

def get_pair(pairs, idx):
    i, j, k, l = pairs[idx]
    if l < 0:
        sign = -1
        l = abs(l)
    else:
        sign = +1
    return i, j, k, l, sign

def format_pair(i, j, k, l, sign):
    sign_str = "+" if sign > 0 else "-"
    return f"(e{i} + e{j}) × (e{k} {sign_str} e{l})"


def main():
    pairs = load_pairs()
    
    print("=" * 90)
    print("DETAILED ANALYSIS OF ASTO₅ FAILURES")
    print("=" * 90)
    print()
    
    # First, identify all failures
    print("STEP 1: Identify all failures")
    print("-" * 90)
    
    failures = []
    for idx in range(len(pairs)):
        i, j, k, l, sign = get_pair(pairs, idx)
        A = e(i) + e(j)
        B = e(k) + sign * e(l)
        
        # Check if it's a zero divisor
        product = A * B
        if not product.is_zero():
            continue  # Not a zero divisor
        
        # Check ASTO₅
        asto_result = asto5_left(A) * B
        if asto_result.is_zero():
            failures.append((idx, i, j, k, l, sign))
    
    print(f"Total failures: {len(failures)}")
    print()
    
    # Analyze the pattern
    print("STEP 2: Analyze the pattern")
    print("-" * 90)
    
    # Count occurrences of each index
    index_counts = {}
    for idx, i, j, k, l, sign in failures:
        for x in [i, j, k, l]:
            index_counts[x] = index_counts.get(x, 0) + 1
    
    print("Index frequency in failures:")
    for x in sorted(index_counts.keys()):
        print(f"  e{x}: {index_counts[x]} occurrences")
    print()
    
    # Show the failures
    print("STEP 3: List all failures")
    print("-" * 90)
    for idx, i, j, k, l, sign in failures:
        pair_str = format_pair(i, j, k, l, sign)
        print(f"  {idx+1:3d}. {pair_str}")
        
        # Show the structure
        A = e(i) + e(j)
        B = e(k) + sign * e(l)
        
        # Which octonion does each index belong to?
        oct_A1 = "first" if i < 8 else "second"
        oct_A2 = "first" if j < 8 else "second"
        oct_B1 = "first" if k < 8 else "second"
        oct_B2 = "first" if l < 8 else "second"
        
        print(f"       A: e{i}({oct_A1}) + e{j}({oct_A2})")
        print(f"       B: e{k}({oct_B1}) + e{l}({oct_B2})")
    print()
    
    # Test alternative ASTO variants
    print("STEP 4: Test alternative ASTO variants")
    print("-" * 90)
    
    variants = [
        ("ASTO₅ (e₁ left)", asto5_left),
        ("ASTO₅ (e₁ right)", asto5_right),
        ("ASTO e₂ left", asto_e2_left),
        ("ASTO e₈ left", asto_e8_left),
        ("ASTO e₉ left", asto_e9_left),
        ("ASTO partial second", asto_partial_second),
    ]
    
    print(f"{'Pair':<35} | ", end="")
    for name, _ in variants:
        print(f"{name[:10]:^12} | ", end="")
    print()
    print("-" * 90)
    
    for idx, i, j, k, l, sign in failures:
        pair_str = format_pair(i, j, k, l, sign)
        A = e(i) + e(j)
        B = e(k) + sign * e(l)
        
        print(f"{pair_str:<35} | ", end="")
        for name, func in variants:
            result = func(A) * B
            status = "✓" if not result.is_zero() else "✗"
            print(f"{status:^12} | ", end="")
        print()
    
    print()
    
    # Count successes per variant
    print("STEP 5: Success rate per variant on failures")
    print("-" * 90)
    
    for name, func in variants:
        successes = 0
        for idx, i, j, k, l, sign in failures:
            A = e(i) + e(j)
            B = e(k) + sign * e(l)
            result = func(A) * B
            if not result.is_zero():
                successes += 1
        print(f"  {name}: {successes}/{len(failures)} ({100*successes/len(failures):.1f}%)")
    
    print()
    
    # Test if applying ASTO to B instead of A works
    print("STEP 6: Test ASTO on B instead of A")
    print("-" * 90)
    
    for idx, i, j, k, l, sign in failures:
        pair_str = format_pair(i, j, k, l, sign)
        A = e(i) + e(j)
        B = e(k) + sign * e(l)
        
        # ASTO on A
        result_A = asto5_left(A) * B
        status_A = "✓" if not result_A.is_zero() else "✗"
        
        # ASTO on B
        result_B = A * asto5_left(B)
        status_B = "✓" if not result_B.is_zero() else "✗"
        
        # ASTO on both
        result_both = asto5_left(A) * asto5_left(B)
        status_both = "✓" if not result_both.is_zero() else "✗"
        
        print(f"{pair_str:<35} | ASTO(A): {status_A} | ASTO(B): {status_B} | ASTO(both): {status_both}")
    
    print()
    
    # Final analysis
    print("=" * 90)
    print("CONCLUSIONS")
    print("=" * 90)


if __name__ == "__main__":
    main()
