#!/usr/bin/env python3
"""
DV16 STRUCTURE PROBE
====================
Untersuchung der Sedenionen-Struktur durch gezielte Störung (ASTO).
Analyse von Chiralität und Wilmot-Typen.

Author: 'AM' & Ivano Franco Malaspina
"""

import math
from decimal import Decimal, getcontext

# --- Setup (High Precision) ---
getcontext().prec = 50
EPSILON = Decimal("1e-35")


# --- Klassen (Importiert aus Titan, hier kompakt) ---
class TitanQuaternion:
    def __init__(self, w, x, y, z): self.c = [Decimal(i) for i in (w, x, y, z)]

    def __add__(self, o): return TitanQuaternion(*[x + y for x, y in zip(self.c, o.c)])

    def __sub__(self, o): return TitanQuaternion(*[x - y for x, y in zip(self.c, o.c)])

    def __mul__(self, o):
        w, x, y, z = self.c;
        ow, ox, oy, oz = o.c
        return TitanQuaternion(
            w * ow - x * ox - y * oy - z * oz, w * ox + x * ow + y * oz - z * oy,
            w * oy - x * oz + y * ow + z * ox, w * oz + x * oy - y * ox + z * ow)

    def conjugate(self): return TitanQuaternion(self.c[0], -self.c[1], -self.c[2], -self.c[3])

    def to_list(self): return self.c


class TitanOctonion:
    def __init__(self, *c):
        self.c = list(map(Decimal, c)) + [Decimal(0)] * (8 - len(c))
        self.a = TitanQuaternion(*self.c[:4]);
        self.b = TitanQuaternion(*self.c[4:8])

    def __add__(self, o): return TitanOctonion(*[x + y for x, y in zip(self.c, o.c)])

    def __sub__(self, o): return TitanOctonion(*[x - y for x, y in zip(self.c, o.c)])

    def conjugate(self):
        return TitanOctonion(*(self.a.conjugate().to_list() +
                               TitanQuaternion(-self.b.c[0], -self.b.c[1], -self.b.c[2], -self.b.c[3]).to_list()))

    def __mul__(self, o):
        ac = self.a * o.a;
        db = o.b.conjugate() * self.b
        da = o.b * self.a;
        bc = self.b * o.a.conjugate()
        return TitanOctonion(*((ac - db).to_list() + (da + bc).to_list()))

    def to_list(self): return self.c


class TitanSedenion:
    def __init__(self, *c):
        self.c = list(map(Decimal, c)) + [Decimal(0)] * (16 - len(c))
        self.a = TitanOctonion(*self.c[:8]);
        self.b = TitanOctonion(*self.c[8:16])

    def __add__(self, o): return TitanSedenion(*[x + y for x, y in zip(self.c, o.c)])

    def __sub__(self, o): return TitanSedenion(*[x - y for x, y in zip(self.c, o.c)])

    def __mul__(self, o):
        ac = self.a * o.a;
        d_conj = o.b.conjugate();
        db = d_conj * self.b
        da = o.b * self.a;
        bc = self.b * o.a.conjugate()
        return TitanSedenion(*((ac - db).to_list() + (da + bc).to_list()))

    def norm(self): return sum(x * x for x in self.c).sqrt()

    def associator(self, y, z):
        return (self * y) * z - self * (y * z)

    # --- SONDEN ---

    def probe_asto_left(self):
        # ASTO V5: Rotiere a (linke Hälfte)
        e1 = TitanOctonion(0, 1, 0, 0, 0, 0, 0, 0)
        return TitanSedenion(*((self.a * e1).to_list() + self.b.to_list()))

    def probe_asto_right(self):
        # Alternative: Rotiere b (rechte Hälfte)
        # Wir testen Chiralität!
        e1 = TitanOctonion(0, 1, 0, 0, 0, 0, 0, 0)
        return TitanSedenion(*(self.a.to_list() + (self.b * e1).to_list()))


# --- HILFSFUNKTIONEN ---
def e(i):
    c = [0] * 16
    c[i] = 1
    return TitanSedenion(*c)


def analyze_triplet(x, y, z, names):
    print(f"\nANALYSE TRIPEL: {names}")

    # 1. Wilmot Typ Bestimmung (Präzise)
    # T1: [y, x, z], T2: [x, y, z], T3: [x, z, y]
    a1 = y.associator(x, z).norm()
    a2 = x.associator(y, z).norm()
    a3 = x.associator(z, y).norm()

    # Threshold für "Nicht-Null"
    th = Decimal("0.1")
    t1, t2, t3 = a1 > th, a2 > th, a3 > th

    print(f"  Assoziatoren Normen:")
    print(f"  [y,x,z] = {a1:.4f} ({'NZ' if t1 else '0'})")
    print(f"  [x,y,z] = {a2:.4f} ({'NZ' if t2 else '0'})")
    print(f"  [x,z,y] = {a3:.4f} ({'NZ' if t3 else '0'})")

    w_type = "Unbekannt"
    if t1 and not t2 and not t3: w_type = "Type A (Links-Asymm)"
    if not t1 and t2 and not t3: w_type = "Type B (Zentral-Asymm)"
    if not t1 and not t2 and t3: w_type = "Type C (Rechts-Asymm)"
    if t1 and t2 and t3: w_type = "Type X (Voll)"
    if not t1 and not t2 and not t3: w_type = "Assoziativ"

    print(f"  => KLASSIFIZIERUNG: {w_type}")
    return w_type


def analyze_chirality(A, B):
    print(f"\nCHIRALITÄTS-CHECK FÜR NULLTEILER (A * B = 0)")

    # 1. ASTO Links (Standard V5)
    A_L = A.probe_asto_left()
    res_L = (A_L * B).norm()

    # 2. ASTO Rechts (Experiment)
    A_R = A.probe_asto_right()
    res_R = (A_R * B).norm()

    print(f"  Norm nach ASTO Links (a' = a*e1): {res_L:.20f}")
    print(f"  Norm nach ASTO Rechts (b' = b*e1): {res_R:.20f}")

    if abs(res_L - res_R) < Decimal("1e-10"):
        print("  => SYMMETRISCH (Beide Hälften gleich wirksam)")
    else:
        print("  => ASYMMETRISCH (Chiralität entdeckt!)")


# --- HAUPTPROGRAMM ---
if __name__ == "__main__":
    print("=" * 60)
    print("DV16 STRUCTURE PROBE")
    print("=" * 60)

    # 1. Tiefenanalyse des "Type C" Fundes
    # Wir untersuchen (e2, e4, e9)
    # e9 = e(1+8) -> Index 1 im zweiten Oktonion
    print("Untersuchung des exotischen Fundes (e2, e4, e9)...")
    analyze_triplet(e(2), e(4), e(9), "(e2, e4, e9)")

    # Gegenprobe: Verschiebung der Indizes
    # Wenn e9 (Index 1 in b) entscheidend ist, was ist mit (e2, e4, e10)? (Index 2 in b)
    analyze_triplet(e(2), e(4), e(10), "(e2, e4, e10)")

    # 2. Chiralitäts-Test an einem Nullteiler
    # Wir nehmen den Klassiker: A = e1+e10, B = e5+e14
    A = e(1) + e(10)
    B = e(5) + e(14)

    # Sicherstellen, dass es ein Nullteiler ist
    if (A * B).norm() < Decimal("1e-10"):
        analyze_chirality(A, B)
    else:
        print("Fehler im Setup: Kein Nullteiler.")

    # 3. Test an einem "bösen" Nullteiler (negatives Vorzeichen)
    # A = e1+e10, B = e4-e15
    A2 = e(1) + e(10)
    B2 = e(4) - e(15)

    if (A2 * B2).norm() < Decimal("1e-10"):
        print(f"\nTest am alternierenden Paar (e1+e10) * (e4-e15):")
        analyze_chirality(A2, B2)