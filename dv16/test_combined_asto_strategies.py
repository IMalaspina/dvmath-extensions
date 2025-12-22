"""
Test combined ASTO strategies on all 84 canonical zero divisor pairs.
Goal: Find a strategy that achieves 100% success rate.
"""

import json

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


def e(i):
    components = [0.0] * 16
    components[i] = 1.0
    return Sedenion(*components)


# ============================================================
# ASTO VARIANTS
# ============================================================

def asto5_left_A(A, B):
    """ASTO₅: Apply e₁ left multiplication to A"""
    return (e(1) * A) * B

def asto5_left_B(A, B):
    """ASTO₅: Apply e₁ left multiplication to B"""
    return A * (e(1) * B)

def asto5_left_both(A, B):
    """ASTO₅: Apply e₁ left multiplication to both A and B"""
    return (e(1) * A) * (e(1) * B)

def asto5_right_A(A, B):
    """ASTO₅: Apply e₁ right multiplication to A"""
    return (A * e(1)) * B

def asto5_right_B(A, B):
    """ASTO₅: Apply e₁ right multiplication to B"""
    return A * (B * e(1))

def asto_adaptive(A, B):
    """
    Adaptive ASTO: Try ASTO on A first, if it fails, try on B.
    """
    result_A = (e(1) * A) * B
    if not result_A.is_zero():
        return result_A, "A"
    
    result_B = A * (e(1) * B)
    if not result_B.is_zero():
        return result_B, "B"
    
    return None, "FAIL"

def asto_e2_left_A(A, B):
    """ASTO with e₂: Apply e₂ left multiplication to A"""
    return (e(2) * A) * B

def asto_e2_left_B(A, B):
    """ASTO with e₂: Apply e₂ left multiplication to B"""
    return A * (e(2) * B)


# ============================================================
# LOAD AND TEST
# ============================================================

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
    
    print("=" * 100)
    print("COMPREHENSIVE TEST OF ASTO STRATEGIES ON ALL 84 PAIRS")
    print("=" * 100)
    print()
    
    # Define strategies to test
    strategies = [
        ("ASTO₅(A) e₁ left", lambda A, B: (e(1) * A) * B),
        ("ASTO₅(B) e₁ left", lambda A, B: A * (e(1) * B)),
        ("ASTO₅(A) e₁ right", lambda A, B: (A * e(1)) * B),
        ("ASTO₅(B) e₁ right", lambda A, B: A * (B * e(1))),
        ("ASTO₅(A,B) e₁ left", lambda A, B: (e(1) * A) * (e(1) * B)),
        ("ASTO e₂(A) left", lambda A, B: (e(2) * A) * B),
        ("ASTO e₂(B) left", lambda A, B: A * (e(2) * B)),
    ]
    
    # Test each strategy
    results = {name: [] for name, _ in strategies}
    
    for idx in range(len(pairs)):
        i, j, k, l, sign = get_pair(pairs, idx)
        A = e(i) + e(j)
        B = e(k) + sign * e(l)
        
        # Verify it's a zero divisor
        product = A * B
        if not product.is_zero():
            print(f"WARNING: Pair {idx+1} is not a zero divisor!")
            continue
        
        for name, func in strategies:
            result = func(A, B)
            success = not result.is_zero()
            results[name].append((idx, success))
    
    # Print summary
    print("STRATEGY SUCCESS RATES:")
    print("-" * 100)
    
    for name, _ in strategies:
        successes = sum(1 for _, s in results[name] if s)
        total = len(results[name])
        rate = 100 * successes / total if total > 0 else 0
        status = "✅" if rate == 100 else "⚠️" if rate >= 85 else "❌"
        print(f"  {name:<25}: {successes:3d}/{total} ({rate:5.1f}%) {status}")
    
    print()
    
    # Test adaptive strategy
    print("=" * 100)
    print("ADAPTIVE STRATEGY: Try ASTO(A), if fails try ASTO(B)")
    print("=" * 100)
    
    adaptive_results = []
    for idx in range(len(pairs)):
        i, j, k, l, sign = get_pair(pairs, idx)
        A = e(i) + e(j)
        B = e(k) + sign * e(l)
        
        result, which = asto_adaptive(A, B)
        success = result is not None
        adaptive_results.append((idx, success, which))
    
    successes = sum(1 for _, s, _ in adaptive_results if s)
    total = len(adaptive_results)
    rate = 100 * successes / total
    
    print(f"\nAdaptive ASTO₅: {successes}/{total} ({rate:.1f}%)")
    
    # Count which was used
    used_A = sum(1 for _, s, w in adaptive_results if s and w == "A")
    used_B = sum(1 for _, s, w in adaptive_results if s and w == "B")
    failed = sum(1 for _, s, _ in adaptive_results if not s)
    
    print(f"  - Used ASTO(A): {used_A}")
    print(f"  - Used ASTO(B): {used_B}")
    print(f"  - Failed: {failed}")
    
    if failed > 0:
        print("\nFailed pairs:")
        for idx, success, which in adaptive_results:
            if not success:
                i, j, k, l, sign = get_pair(pairs, idx)
                print(f"  {idx+1}. {format_pair(i, j, k, l, sign)}")
    
    print()
    
    # Test combined e₁ OR e₂ strategy
    print("=" * 100)
    print("COMBINED STRATEGY: ASTO e₁(A) OR ASTO e₂(A)")
    print("=" * 100)
    
    combined_results = []
    for idx in range(len(pairs)):
        i, j, k, l, sign = get_pair(pairs, idx)
        A = e(i) + e(j)
        B = e(k) + sign * e(l)
        
        # Try e₁ first
        result_e1 = (e(1) * A) * B
        if not result_e1.is_zero():
            combined_results.append((idx, True, "e₁"))
            continue
        
        # Try e₂
        result_e2 = (e(2) * A) * B
        if not result_e2.is_zero():
            combined_results.append((idx, True, "e₂"))
            continue
        
        combined_results.append((idx, False, "FAIL"))
    
    successes = sum(1 for _, s, _ in combined_results if s)
    total = len(combined_results)
    rate = 100 * successes / total
    
    print(f"\nCombined e₁/e₂ ASTO(A): {successes}/{total} ({rate:.1f}%)")
    
    used_e1 = sum(1 for _, s, w in combined_results if s and w == "e₁")
    used_e2 = sum(1 for _, s, w in combined_results if s and w == "e₂")
    failed = sum(1 for _, s, _ in combined_results if not s)
    
    print(f"  - Used e₁: {used_e1}")
    print(f"  - Used e₂: {used_e2}")
    print(f"  - Failed: {failed}")
    
    print()
    
    # Final comprehensive test: Any ASTO variant works?
    print("=" * 100)
    print("ULTIMATE TEST: Does ANY single ASTO variant work for each pair?")
    print("=" * 100)
    
    all_variants = [
        ("e₁(A)L", lambda A, B: (e(1) * A) * B),
        ("e₁(B)L", lambda A, B: A * (e(1) * B)),
        ("e₁(A)R", lambda A, B: (A * e(1)) * B),
        ("e₁(B)R", lambda A, B: A * (B * e(1))),
        ("e₂(A)L", lambda A, B: (e(2) * A) * B),
        ("e₂(B)L", lambda A, B: A * (e(2) * B)),
        ("e₃(A)L", lambda A, B: (e(3) * A) * B),
        ("e₄(A)L", lambda A, B: (e(4) * A) * B),
        ("e₅(A)L", lambda A, B: (e(5) * A) * B),
        ("e₆(A)L", lambda A, B: (e(6) * A) * B),
        ("e₇(A)L", lambda A, B: (e(7) * A) * B),
    ]
    
    ultimate_results = []
    for idx in range(len(pairs)):
        i, j, k, l, sign = get_pair(pairs, idx)
        A = e(i) + e(j)
        B = e(k) + sign * e(l)
        
        working_variants = []
        for name, func in all_variants:
            result = func(A, B)
            if not result.is_zero():
                working_variants.append(name)
        
        ultimate_results.append((idx, len(working_variants) > 0, working_variants))
    
    successes = sum(1 for _, s, _ in ultimate_results if s)
    total = len(ultimate_results)
    rate = 100 * successes / total
    
    print(f"\nAt least one variant works: {successes}/{total} ({rate:.1f}%)")
    
    if rate == 100:
        print("\n✅ SUCCESS: For every zero divisor pair, at least one ASTO variant works!")
    else:
        print("\n❌ FAILURE: Some pairs have no working ASTO variant!")
        for idx, success, variants in ultimate_results:
            if not success:
                i, j, k, l, sign = get_pair(pairs, idx)
                print(f"  {idx+1}. {format_pair(i, j, k, l, sign)}")
    
    print()
    print("=" * 100)
    print("CONCLUSION")
    print("=" * 100)


if __name__ == "__main__":
    main()
