# Author: Ivano Franco Malaspina
# Date: November 30, 2025
# Description: Test suite for DV core.

import numpy as np
import math
from dv_core import DV2, DV4, DV8, dv2_zero, dv4_i, dv4_j, dv4_k, dv8_e1, dv8_e2, dv8_e4, dv8_zero

def run_tests():
    # DV2 Tests (unchanged)
    a = DV2(3, 4)
    b = DV2(1, 2)
    zero = dv2_zero()

    print("DV2 Tests:")
    c = a + b
    assert np.allclose(c.components, [4, 6])
    print(f"a + b = {c}")

    c = a * b
    assert np.allclose(c.components, [-5, 10])
    print(f"a * b = {c}")

    assert np.isclose(a.norm() * b.norm(), c.norm())

    result = a / zero
    assert np.allclose(result.components, [-4, 3])
    assert np.isclose(a.norm(), result.norm())
    print(f"a / zero = {result}")

    unit_a = a.normalize()
    assert np.isclose(unit_a.norm(), 1.0)
    print(f"Normalized a = {unit_a}")

    assert np.isclose(a.angle(), math.atan2(4, 3))
    print(f"Angle of a = {a.angle()}")

    # DV4 Tests (unchanged)
    q1 = DV4(1, 2, 3, 4)
    q2 = DV4(5, 6, 7, 8)
    i = dv4_i()
    j = dv4_j()
    k = dv4_k()

    print("\nDV4 Tests:")
    q12 = q1 * q2
    q21 = q2 * q1
    assert not np.allclose(q12.components, q21.components)
    print(f"q1 * q2 = {q12}")
    print(f"q2 * q1 = {q21}")

    assert np.allclose((i * j).components, k.components)
    assert np.allclose((j * i).components, (-k).components)
    print(f"i * j = {i * j}")

    comm = i.commutator(j)
    assert np.allclose(comm.components, (2 * k).components)
    print(f"[i, j] = {comm}")

    q_inv = q1.inverse()
    identity = q1 * q_inv
    assert np.allclose(identity.components, [1, 0, 0, 0])
    print(f"q1 * q1.inverse() = {identity}")

    # DV8 Tests
    o1 = DV8(1, 2, 3, 4, 5, 6, 7, 8)
    o2 = DV8(8, 7, 6, 5, 4, 3, 2, 1)
    e1 = dv8_e1()
    e2 = dv8_e2()
    e4 = dv8_e4()
    zero8 = dv8_zero()

    print("\nDV8 Tests:")
    # Multiplication (e1 * e2 = e3)
    e3 = DV8(0, 0, 0, 1, 0, 0, 0, 0)
    assert np.allclose((e1 * e2).components, e3.components)
    print(f"e1 * e2 = {e1 * e2}")

    # Non-commutativity
    o12 = o1 * o2
    o21 = o2 * o1
    assert not np.allclose(o12.components, o21.components)
    print(f"o1 * o2 = {o12}")

    # Non-associativity
    left = (e1 * e2) * e4
    right = e1 * (e2 * e4)
    assert not np.allclose(left.components, right.components)
    print(f"(e1 * e2) * e4 = {left}")
    print(f"e1 * (e2 * e4) = {right}")

    # Inverse and identity
    o_inv = o1.inverse()
    identity8 = o1 * o_inv
    assert np.allclose(identity8.components, [1, 0, 0, 0, 0, 0, 0, 0])
    print(f"o1 * o1.inverse() = {identity8}")

    # Division by zero
    result8 = o1 / zero8
    assert np.allclose(result8.components, o1.GTR1().components)
    assert np.isclose(o1.norm(), result8.norm())
    print(f"o1 / zero = {result8}")

    print("All tests passed!")

if __name__ == "__main__":
    run_tests()# Author: Ivano Franco Malaspina
# Date: November 30, 2025
# Description: Test suite for DV core.

import numpy as np
import math
from dv_core import DV2, DV4, DV8, dv2_zero, dv4_i, dv4_j, dv4_k, dv8_e1, dv8_e2, dv8_e4, dv8_zero

def run_tests():
    # DV2 Tests (unchanged)
    a = DV2(3, 4)
    b = DV2(1, 2)
    zero = dv2_zero()

    print("DV2 Tests:")
    c = a + b
    assert np.allclose(c.components, [4, 6])
    print(f"a + b = {c}")

    c = a * b
    assert np.allclose(c.components, [-5, 10])
    print(f"a * b = {c}")

    assert np.isclose(a.norm() * b.norm(), c.norm())

    result = a / zero
    assert np.allclose(result.components, [-4, 3])
    assert np.isclose(a.norm(), result.norm())
    print(f"a / zero = {result}")

    unit_a = a.normalize()
    assert np.isclose(unit_a.norm(), 1.0)
    print(f"Normalized a = {unit_a}")

    assert np.isclose(a.angle(), math.atan2(4, 3))
    print(f"Angle of a = {a.angle()}")

    # DV4 Tests (unchanged)
    q1 = DV4(1, 2, 3, 4)
    q2 = DV4(5, 6, 7, 8)
    i = dv4_i()
    j = dv4_j()
    k = dv4_k()

    print("\nDV4 Tests:")
    q12 = q1 * q2
    q21 = q2 * q1
    assert not np.allclose(q12.components, q21.components)
    print(f"q1 * q2 = {q12}")
    print(f"q2 * q1 = {q21}")

    assert np.allclose((i * j).components, k.components)
    assert np.allclose((j * i).components, (-k).components)
    print(f"i * j = {i * j}")

    comm = i.commutator(j)
    assert np.allclose(comm.components, (2 * k).components)
    print(f"[i, j] = {comm}")

    q_inv = q1.inverse()
    identity = q1 * q_inv
    assert np.allclose(identity.components, [1, 0, 0, 0])
    print(f"q1 * q1.inverse() = {identity}")

    # DV8 Tests
    o1 = DV8(1, 2, 3, 4, 5, 6, 7, 8)
    o2 = DV8(8, 7, 6, 5, 4, 3, 2, 1)
    e1 = dv8_e1()
    e2 = dv8_e2()
    e4 = dv8_e4()
    zero8 = dv8_zero()

    print("\nDV8 Tests:")
    # Multiplication (e1 * e2 = e3)
    e3 = DV8(0, 0, 0, 1, 0, 0, 0, 0)
    assert np.allclose((e1 * e2).components, e3.components)
    print(f"e1 * e2 = {e1 * e2}")

    # Non-commutativity
    o12 = o1 * o2
    o21 = o2 * o1
    assert not np.allclose(o12.components, o21.components)
    print(f"o1 * o2 = {o12}")

    # Non-associativity
    left = (e1 * e2) * e4
    right = e1 * (e2 * e4)
    assert not np.allclose(left.components, right.components)
    print(f"(e1 * e2) * e4 = {left}")
    print(f"e1 * (e2 * e4) = {right}")

    # Inverse and identity
    o_inv = o1.inverse()
    identity8 = o1 * o_inv
    assert np.allclose(identity8.components, [1, 0, 0, 0, 0, 0, 0, 0])
    print(f"o1 * o1.inverse() = {identity8}")

    # Division by zero
    result8 = o1 / zero8
    assert np.allclose(result8.components, o1.GTR1().components)
    assert np.isclose(o1.norm(), result8.norm())
    print(f"o1 / zero = {result8}")

    print("All tests passed!")

if __name__ == "__main__":
    run_tests()