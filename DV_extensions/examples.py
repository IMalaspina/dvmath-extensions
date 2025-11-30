# Author: Ivano Franco Malaspina
# Date: November 30, 2025
# Description: Practical examples for DV-Mathematics, including README usage demos.

import math
from dv_core import DV2, DV4, DV8, dv2_zero, dv4_i, dv4_j, dv4_k, dv8_e1, dv8_e2
from dv_extensions import DVFunction2, dv2_exp, regularized_inverse, StableDivision, is_dv_holomorphic

# 1. Basic operations
a = DV2(3, 4)
b = DV2(1, 2)
print("1. Basic: a + b =", a + b)
print("a * b =", a * b)

# 2. Division by zero
zero = dv2_zero()
result = a / zero
print("2. Div by zero:", result)

# 3. Isomorphism to C
c = a.to_complex()
print("3. To complex:", c)

# 4. Quaternions
q = DV4(1, 2, 3, 4)
print("4. Quaternion inverse:", q.inverse())

# 5. Lie algebra su(2)
i, j, k = dv4_i(), dv4_j(), dv4_k()
print("5. [i, j] =", i.commutator(j))

# 6. DV calculus
f = DVFunction2(math.cos, math.sin)
print("6. Derivative at pi/4:", f.derivative(math.pi / 4))

# 7. Transcendental functions
z = DV2(0, math.pi)
print("7. exp(i pi) =", dv2_exp(z))

# 8. Regularized functions
print("8. Regularized 1/0.01:", regularized_inverse(0.01))

# 9. Numerical stability
print("9. Stable div 10 / 1e-12:", StableDivision.divide(10, 1e-12))

# 10. Holomorphy tests
def square(z): return z * z
is_holo, error = is_dv_holomorphic(square, DV2(1, 1))
print("10. Is holomorphic:", is_holo, "Error:", error)

# 11. DV2 usage demo (from README)
a = DV2(3, 4)
zero = dv2_zero()
print("11. DV2 demo: a / zero =", a / zero)  # Rotates to DV2(v=-4.0000, d=3.0000)

# 12. DV4 usage demo (from README)
i = dv4_i()
j = dv4_j()  # Corrected from README typo
print("12. DV4 demo: i.commutator(j) =", i.commutator(j))  # [i, j] = 2k

# 13. DV8 usage demo (from README)
e1 = dv8_e1()
e2 = dv8_e2()
print("13. DV8 demo: e1 * e2 =", e1 * e2)  # e3

# 14. Extensions usage demo (from README)
print("14. Extensions demo: regularized_inverse(0.001, epsilon=1e-3) =", regularized_inverse(0.001, epsilon=1e-3))  # Finite approximation