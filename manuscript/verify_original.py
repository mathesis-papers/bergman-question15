#!/usr/bin/env python3
"""Check the finite semigroup and sixth-power identities in the note.

Run with Python 3.9 or later: python3 verify.py
All coefficients are exact integer pairs representing a + b*t,
where t*t + t + 1 = 0.
"""

from collections import defaultdict
from itertools import product
from math import factorial


ZERO = "0"
TERMINAL = ("A", "B", "C")
CLASSES = {
    "A": ((6, 0, 0), (3, 3, 0), (5, 1, 0),
          (5, 0, 1), (2, 4, 0), (4, 2, 0)),
    "B": ((0, 6, 0), (0, 3, 3), (0, 5, 1),
          (1, 5, 0), (0, 2, 4), (0, 4, 2)),
    "C": ((0, 0, 6), (3, 0, 3), (1, 0, 5),
          (0, 1, 5), (4, 0, 2), (2, 0, 4)),
}


def triples(degree):
    return [(a, b, degree - a - b)
            for a in range(degree + 1)
            for b in range(degree - a + 1)]


LOWER = [abc for degree in range(1, 6) for abc in triples(degree)]
ELEMENTS = [ZERO] + LOWER + list(TERMINAL)
CLASS_OF = {abc: label for label, row in CLASSES.items() for abc in row}


def multiply(a, b):
    if a == ZERO or b == ZERO or a in TERMINAL or b in TERMINAL:
        return ZERO
    abc = tuple(x + y for x, y in zip(a, b))
    return abc if sum(abc) <= 5 else CLASS_OF.get(abc, ZERO)


def add_coeff(a, b):
    return (a[0] + b[0], a[1] + b[1])


def multiply_coeff(a, b):
    # (r+s*t)(u+v*t), reduced using t*t = -1-t.
    r, s = a
    u, v = b
    return (r*u - s*v, r*v + s*u - s*v)


def multiply_vectors(u, v):
    answer = defaultdict(lambda: (0, 0))
    for a, ac in u.items():
        for b, bc in v.items():
            c = multiply(a, b)
            if c != ZERO:
                answer[c] = add_coeff(answer[c], multiply_coeff(ac, bc))
    return {c: coeff for c, coeff in answer.items() if coeff != (0, 0)}


def power(a, exponent):
    answer = a
    for _ in range(1, exponent):
        answer = multiply(answer, a)
    return answer


def main():
    assert len(LOWER) == 55 and len(set(ELEMENTS)) == 59
    assert len(CLASS_OF) == 18
    assert all(sum(abc) == 6 for abc in CLASS_OF)
    assert all(multiply(ZERO, a) == multiply(a, ZERO) == ZERO
               for a in ELEMENTS)
    assert all(multiply(a, b) in ELEMENTS and
               multiply(a, b) == multiply(b, a)
               for a, b in product(ELEMENTS, repeat=2))
    assert all(multiply(multiply(a, b), c) ==
               multiply(a, multiply(b, c))
               for a, b, c in product(ELEMENTS, repeat=3))

    x, y, z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
    assert [power(a, 6) for a in (x, y, z)] == list(TERMINAL)
    assert multiply((2, 1, 0), (3, 0, 0)) == "A"
    assert multiply((0, 2, 1), (0, 3, 0)) == "B"
    assert multiply((1, 1, 1), (1, 1, 1)) == ZERO
    assert multiply("A", x) == ZERO

    # First computation: multiply the vector six times in the actual algebra.
    w = {x: (1, 0), y: (0, 1), z: (-1, -1)}
    current = w
    supports = [len(current)]
    for _ in range(5):
        current = multiply_vectors(current, w)
        supports.append(len(current))
    assert supports == [3, 6, 10, 15, 21, 0]
    assert current == {}
    assert w[x] == (1, 0)

    # Second computation: sum multinomial coefficients in each residue class.
    totals = {label: [0, 0, 0] for label in TERMINAL}
    for a, b, c in triples(6):
        label = CLASS_OF.get((a, b, c))
        if label is not None:
            weight = factorial(6) // (factorial(a)*factorial(b)*factorial(c))
            totals[label][(b + 2*c) % 3] += weight
    assert totals == {label: [21, 21, 21] for label in TERMINAL}

    print("Semigroup elements: 59; contracted algebra dimension: 58.")
    print("Closure and commutativity: all 3481 ordered pairs.")
    print("Associativity: all 205379 ordered triples.")
    print("Absorbing zero: all 59 elements on both sides.")
    print("Generator sixth powers: x -> A, y -> B, z -> C.")
    print("Nonzero terms in w^1 through w^6: 3, 6, 10, 15, 21, 0.")
    print("A, B and C coefficient sums: 21*(1+t+t^2) = 0.")
    print("The displayed multiplication examples hold.")
    print("All finite checks passed with exact integer arithmetic.")


if __name__ == "__main__":
    main()
