# Author: Ivano Franco Malaspina
# Date: November 30, 2025
# Description: Extensions for DV-Mathematics, including calculus, regularized functions, and holomorphy tests.

import math
import cmath
import numpy as np
from scipy.integrate import quad  # For numerical integration
from dv_core import DV2, DV4  # Import core classes if needed for type hints
import matplotlib.pyplot as plt  # For visualizations (optional)

class DVFunction2:
    def __init__(self, v_func, d_func):
        self.v_func = v_func
        self.d_func = d_func

    def __call__(self, t):
        return DV2(self.v_func(t), self.d_func(t))

    def derivative(self, t, h=1e-4):  # Increased h for stability
        f_plus = self(t + h)
        f_minus = self(t - h)
        return (f_plus - f_minus) / (2 * h)

    def integral(self, a, b, steps=1000):
        # Numerical integration using SciPy quad for each component
        v_int, _ = quad(self.v_func, a, b)
        d_int, _ = quad(self.d_func, a, b)
        return DV2(v_int, d_int)

def dv2_exp(z):
    c = z.to_complex()
    return DV2.from_complex(cmath.exp(c))

def dv2_sin(z):
    c = z.to_complex()
    return DV2.from_complex(cmath.sin(c))

def dv2_cos(z):
    c = z.to_complex()
    return DV2.from_complex(cmath.cos(c))

def dv2_log(z):
    c = z.to_complex()
    return DV2.from_complex(cmath.log(c))

def dv2_power(z, n):
    c = z.to_complex()
    return DV2.from_complex(cmath.pow(c, n))

def regularized_inverse(x, epsilon=1e-6):
    if isinstance(x, (int, float)):
        x = DV2(x)
    sign = np.sign(x.v)
    if sign == 0:
        sign = 1.0  # Default for zero, matching positive approach
    c = x.to_complex()
    reg = c + 1j * epsilon * sign
    inv = 1.0 / reg
    return DV2.from_complex(inv)

def regularized_tan(x, epsilon=1e-6):
    if isinstance(x, (int, float)):
        x = DV2(x)
    c = x.to_complex()
    tan_c = cmath.tan(c)
    if abs(tan_c.imag) > 1/epsilon:  # Detect near pole by large imag part
        return x.TR()  # Rotate
    return DV2.from_complex(tan_c)

class StableDivision:
    @staticmethod
    def divide(a, b, epsilon=1e-10):
        if isinstance(b, (int, float)) and abs(b) < epsilon:
            return DV2(a).TR()  # Handle near-zero scalar
        if isinstance(b, DV2) and b.is_zero():
            return a.TR() if isinstance(a, DV2) else DV2(a).TR()
        return a / b

def is_dv_holomorphic(f, z, h=1e-6):
    # Check Cauchy-Riemann equations numerically for DV2 function f: DV2 -> DV2
    f_z = f(z)
    f_v_plus = f(DV2(z.v + h, z.d))
    f_v_minus = f(DV2(z.v - h, z.d))
    f_d_plus = f(DV2(z.v, z.d + h))
    f_d_minus = f(DV2(z.v, z.d - h))

    du_dv = (f_v_plus.v - f_v_minus.v) / (2 * h)
    du_dd = (f_d_plus.v - f_d_minus.v) / (2 * h)
    dv_dv = (f_v_plus.d - f_v_minus.d) / (2 * h)
    dv_dd = (f_d_plus.d - f_d_minus.d) / (2 * h)

    cr1 = abs(du_dv - dv_dd) < 1e-5
    cr2 = abs(du_dd + dv_dv) < 1e-5  # Note the sign for imaginary part
    error = max(abs(du_dv - dv_dd), abs(du_dd + dv_dv))
    return cr1 and cr2, error

def plot_regularized_inverse(start=-0.2, end=0.2, num_points=100, epsilon=1e-6, save_path='regularized_inverse_plot.png'):
    x = np.linspace(start, end, num_points)
    results = [regularized_inverse(xi, epsilon=epsilon) for xi in x]
    v = [r.v for r in results]
    d = [r.d for r in results]

    # Plot 1: v-d plane trajectory
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(v, d, label='Trajectory')
    plt.scatter(v[0], d[0], color='green', label='Start')
    plt.scatter(v[-1], d[-1], color='red', label='End')
    plt.xlabel('Value (v)')
    plt.ylabel('Depth (d)')
    plt.title('DV2 in v-d Plane')
    plt.legend()
    plt.grid(True)

    # Plot 2: Components vs x
    plt.subplot(1, 2, 2)
    plt.plot(x, v, label='Value (v)')
    plt.plot(x, d, label='Depth (d)')
    plt.xlabel('x')
    plt.ylabel('Component Value')
    plt.title('DV2 Components vs x')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    print(f"Plot saved to {save_path}")

if __name__ == "__main__":
    # Updated example with smaller epsilon and broader values to show proper inversion vs. rotation
    print("Regularized 1/x example:")
    for val in [-1.0, -0.1, -0.001, 0, 0.001, 0.1, 1.0]:
        result = regularized_inverse(val, epsilon=1e-3)
        print(f"1/{val} = {result}")

    # Generate and save the plot (matches your documentation's figure)
    plot_regularized_inverse(start=-2, end=2, epsilon=1e-3, save_path='dv2_regularized_inverse.png')