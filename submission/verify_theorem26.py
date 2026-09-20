"""verify_theorem26.py — exact symbolic verification of Theorem 26.

Checks, using SymPy exact arithmetic, the 8x8 Bloch-block determinant formula
and its s=2 factorization used in the proof of Theorem 26 of
"Parity families and signed spectra".

Run: python3 submission/verify_theorem26.py
"""

import sympy as sp


def main() -> None:
    x, z = sp.symbols("x z")

    H = sp.Matrix([
        [0, 1, 1, 0, 0, 0, z**-1, z**-1],
        [1, 0, 1, 1, 0, 0, 0, -z**-1],
        [1, 1, 0, 1, -1, 0, 0, 0],
        [0, 1, 1, 0, 1, 1, 0, 0],
        [0, 0, -1, 1, 0, 1, -1, 0],
        [0, 0, 0, 1, 1, 0, 1, -1],
        [z, 0, 0, 0, -1, 1, 0, 1],
        [z, -z, 0, 0, 0, -1, 1, 0],
    ])

    det_exact = sp.expand(sp.together((x * sp.eye(8) - H).det()))
    s_expr = z + z**-1
    expected = (
        x**8 - 16*x**6 + 80*x**4 - 128*x**2 + 38
        + s_expr * (-2*x**4 + 16*x**2 - 13)
        + s_expr**2
    )

    ok_det = sp.simplify(det_exact - expected) == 0

    f_minus = x**4 - 2*x**3 - 6*x**2 + 12*x - 4
    f_plus = x**4 + 2*x**3 - 6*x**2 - 12*x - 4
    factorized = sp.expand(expected.subs(z, 1) - f_minus * f_plus) == 0

    print(f"[{'PASS' if ok_det else 'FAIL'}] Formula (3): det(xI-H(z))")
    print(
        f"[{'PASS' if factorized else 'FAIL'}] "
        "Factorization at s=2: P(x,2)=f_-(x)f_+(x)"
    )

    if not (ok_det and factorized):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
