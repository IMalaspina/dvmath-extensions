#!/usr/bin/env python3
"""
DV16 TITAN - High Precision Sedenion Analysis Engine
====================================================
Eine hochpräzise Implementierung der Sedenionen-Algebra (S16) mit
integrierter S-Algebra-Logik und Klassifizierungswerkzeugen nach Wilmot.

Features:
- Decimal Arbitrary Precision (Standard: 50 Stellen)
- Wilmot-Klassifizierung (Types A, B, C, X)
- Automatische ASTO V5 Anwendung bei Singularitäten
- Detaillierte Laborberichte für Vektorpaare

Author: 'AM' & Ivano Franco Malaspina
"""

import math
from decimal import Decimal, getcontext, InvalidOperation

# --- KONFIGURATION: PRÄZISION ---
getcontext().prec = 50  # 50 Stellen Genauigkeit für Titan-Level Analysen
EPSILON = Decimal("1e-40")  # Schwellenwert für "Null"


class TitanQuaternion:
    """Basis-Baustein mit Decimal-Präzision."""

    def __init__(self, w, x, y, z):
        self.w, self.x, self.y, self.z = map(Decimal, (w, x, y, z))

    def __add__(self, o): return TitanQuaternion(self.w + o.w, self.x + o.x, self.y + o.y, self.z + o.z)

    def __sub__(self, o): return TitanQuaternion(self.w - o.w, self.x - o.x, self.y - o.y, self.z - o.z)

    def __mul__(self, o):
        return TitanQuaternion(
            self.w * o.w - self.x * o.x - self.y * o.y - self.z * o.z,
            self.w * o.x + self.x * o.w + self.y * o.z - self.z * o.y,
            self.w * o.y - self.x * o.z + self.y * o.w + self.z * o.x,
            self.w * o.z + self.x * o.y - self.y * o.x + self.z * o.w
        )

    def conjugate(self): return TitanQuaternion(self.w, -self.x, -self.y, -self.z)

    def to_list(self): return [self.w, self.x, self.y, self.z]


class TitanOctonion:
    """Oktonion mit Decimal-Präzision."""

    def __init__(self, *components):
        c = [Decimal(x) for x in components]
        if len(c) < 8: c += [Decimal(0)] * (8 - len(c))
        self.c = c
        self.a = TitanQuaternion(*c[:4])
        self.b = TitanQuaternion(*c[4:8])

    def __add__(self, o): return TitanOctonion(*[x + y for x, y in zip(self.c, o.c)])

    def __sub__(self, o): return TitanOctonion(*[x - y for x, y in zip(self.c, o.c)])

    def conjugate(self):
        ac = self.a.conjugate()
        # b wird negiert für Oktonion-Konjugat (a*, -b)
        bn = TitanQuaternion(-self.b.w, -self.b.x, -self.b.y, -self.b.z)
        return TitanOctonion(*(ac.to_list() + bn.to_list()))

    def __mul__(self, o):
        # Cayley-Dickson
        ac = self.a * o.a
        d_conj = o.b.conjugate()
        db = d_conj * self.b
        part1 = ac - db

        da = o.b * self.a
        bc = self.b * o.a.conjugate()
        part2 = da + bc
        return TitanOctonion(*(part1.to_list() + part2.to_list()))

    def to_list(self): return self.c


class TitanSedenion:
    """
    DV16 TITAN KLASSE
    Implementiert S-Algebra Logik und wissenschaftliche Analyse-Tools.
    """

    def __init__(self, *components):
        c = [Decimal(x) for x in components]
        if len(c) < 16: c += [Decimal(0)] * (16 - len(c))
        self.c = c
        self.a = TitanOctonion(*c[:8])
        self.b = TitanOctonion(*c[8:16])

    # --- Algebraische Operationen ---

    def __add__(self, o):
        return TitanSedenion(*[x + y for x, y in zip(self.c, o.c)])

    def __sub__(self, o):
        return TitanSedenion(*[x - y for x, y in zip(self.c, o.c)])

    def conjugate(self):
        ac = self.a.conjugate()
        # b wird negiert
        bn_list = [-x for x in self.b.to_list()]
        return TitanSedenion(*(ac.to_list() + bn_list))

    def __mul__(self, o):
        ac = self.a * o.a
        d_conj = o.b.conjugate()
        db = d_conj * self.b
        part1 = ac - db

        da = o.b * self.a
        bc = self.b * o.a.conjugate()
        part2 = da + bc
        return TitanSedenion(*(part1.to_list() + part2.to_list()))

    def norm_sq(self):
        return sum(x * x for x in self.c)

    def norm(self):
        return self.norm_sq().sqrt()

    def is_zero(self):
        return self.norm_sq() < EPSILON

    def inverse(self):
        n2 = self.norm_sq()
        if n2 < EPSILON:
            raise ZeroDivisionError("TitanSedenion Norm is zero.")
        conj = self.conjugate()
        return TitanSedenion(*[x / n2 for x in conj.c])

    # --- S-ALGEBRA LOGIK (ASTO V5) ---

    def asto5(self):
        """Wendet ASTO V5 an: Rotation des ersten Oktonions um e1."""
        e1_oct = TitanOctonion(0, 1, 0, 0, 0, 0, 0, 0)
        a_prime = self.a * e1_oct
        return TitanSedenion(*(a_prime.to_list() + self.b.to_list()))

    def __truediv__(self, other):
        """
        S-Algebra Division:
        1. Normaler Versuch A * B^-1
        2. Wenn Ergebnis 0 (Nullteiler-Auslöschung) -> ASTO(A) * B^-1
        """
        if other.is_zero():
            return self.asto5()  # Singularity 1st order

        inv_b = other.inverse()
        res = self * inv_b

        # Nullteiler-Check (Singularität 2. Art)
        # Wenn Ergebnis 0 ist, aber A nicht 0 war
        if res.is_zero() and not self.is_zero():
            # Aktiviere S-Algebra Protokoll
            a_prime = self.asto5()
            return a_prime * inv_b

        return res

    # --- WISSENSCHAFTLICHE ANALYSE-TOOLS ---

    def associator(self, y, z):
        """Berechnet [x,y,z] = (xy)z - x(yz)"""
        x = self
        term1 = (x * y) * z
        term2 = x * (y * z)
        return term1 - term2

    def analyze_wilmot_type(self, y, z):
        """
        Bestimmt den Wilmot-Typ (A, B, C, X) für das Tripel (self, y, z).
        Basierend auf Wilmot, Table 1[cite: 2702].
        Prüft [b,a,c], [a,b,c], [a,c,b] (hier mapped auf x,y,z).
        """
        # Wir testen die drei Assoziatoren für das Tripel
        # T1: [y, x, z] (entspricht [b, a, c] im Paper)
        # T2: [x, y, z] (entspricht [a, b, c] im Paper)
        # T3: [x, z, y] (entspricht [a, c, b] im Paper)

        # Hinweis: Wilmot definiert Typen basierend darauf, WELCHE Assoziatoren != 0 sind.

        a1 = y.associator(self, z).norm()  # [y,x,z]
        a2 = self.associator(y, z).norm()  # [x,y,z]
        a3 = self.associator(z, y).norm()  # [x,z,y]

        is_nz = lambda n: n > Decimal("0.1")

        t1, t2, t3 = is_nz(a1), is_nz(a2), is_nz(a3)

        if t1 and not t2 and not t3: return "Type A (Asymmetric Left)"  #
        if not t1 and t2 and not t3: return "Type B (Asymmetric Center)"  #
        if not t1 and not t2 and t3: return "Type C (Asymmetric Right)"  #
        if t1 and t2 and t3: return "Type X (Fully Non-Associative)"  #
        if not t1 and not t2 and not t3: return "Associative (H/O Subalgebra)"
        return "Mixed/Undefined"

    def lab_report(self, other, name_a="A", name_b="B"):
        """Erstellt einen detaillierten Bericht über das Paar."""
        prod = self * other
        is_zd = prod.is_zero()

        report = []
        report.append(f"--- LABORBERICHT: {name_a} und {name_b} ---")
        report.append(f"Norm {name_a}: {self.norm():.10f}")
        report.append(f"Norm {name_b}: {other.norm():.10f}")
        report.append(f"Produkt Norm: {prod.norm():.20f}")

        if is_zd:
            report.append(f">> STATUS: NULLTEILER DETEKTIERT [cite: 1774]")

            # Wilmot Analyse: Wir brauchen ein Tripel.
            # Nullteiler (a+b)(c+d) kommen aus nicht-assoziativen Tripeln.
            # Wir nehmen a (self) und zerlegen es theoretisch, oder wir testen
            # Assoziativität mit einem Test-Vektor.
            # Besser: Wir testen die S-Algebra Heilung.

            asto_res = self.asto5() * other
            report.append(f">> ASTO V5 Anwendung (Rotation {name_a}):")
            report.append(f"   Neue Norm: {asto_res.norm():.10f}")

            if asto_res.norm() > 0.1:
                report.append(f"   [ERFOLG] Singularität aufgelöst.")
            else:
                report.append(f"   [FEHLER] ASTO wirkungslos.")

            # Divisionstest
            try:
                inv_b = other.inverse()
                div_res = self / inv_b  # Sollte ASTO triggern
                report.append(f">> S-Algebra Division ({name_a} / {name_b}^-1):")
                report.append(f"   Ergebnis Norm: {div_res.norm():.10f}")
            except Exception as e:
                report.append(f"   Divisions-Fehler: {e}")

        else:
            report.append(">> STATUS: Reguläres Paar (Keine Singularität).")

        return "\n".join(report)


# --- BASISVEKTOREN ERSTELLEN ---
def e(i):
    c = [0] * 16
    c[i] = 1
    return TitanSedenion(*c)


# --- HAUPTPROGRAMM (DEMO) ---
if __name__ == "__main__":
    print("DV16 TITAN SYSTEM ONLINE\n")

    # 1. Testfall: Kanonischer Nullteiler #1
    # (e1 + e10) * (e5 + e14)
    A = e(1) + e(10)
    B = e(5) + e(14)

    print(A.lab_report(B, "A(e1+e10)", "B(e5+e14)"))
    print("\n" + "=" * 50 + "\n")

    # 2. Testfall: Wilmot Klassifizierung eines Tripels
    # Wir nehmen ein Tripel, das bekanntlich nicht-assoziativ ist.
    # z.B. e1, e2, e4 (in Oktonionen assoziativ? Nein e1(e2e4) vs (e1e2)e4)
    # e1(e2e4) = e1(e6) = e7
    # (e1e2)e4 = e3e4 = e7
    # Ok, Octonions sind alternativ.

    # Sedenionen Tripel: e1, e2+e10, e5+e14?
    # Wir testen einfach e1, e2, e8 (e8 ist neu in Sedenionen)
    X = e(1)
    Y = e(2)
    Z = e(8)

    type_res = X.analyze_wilmot_type(Y, Z)
    print(f"Wilmot-Analyse für Tripel (e1, e2, e8):")
    print(f"Ergebnis: {type_res}")

    # Teste ein Tripel, das A-Typ sein könnte (laut Wilmot Table 3)
    # o1, o34, o2 -> e1, e3+e4, e2
    W1 = e(1)
    W2 = e(3) + e(4)
    W3 = e(2)

    print(f"\nWilmot-Analyse für Tripel (e1, e3+e4, e2):")
    print(f"Ergebnis: {W1.analyze_wilmot_type(W2, W3)}")