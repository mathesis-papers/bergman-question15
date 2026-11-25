"""Exact checks of the two semigroups and the sixth-power identities.

Run with Python 3.9 or later: python3 verify.py
Coefficient pairs represent constant + linear*t in Z[t]/(t*t+t+1).
"""

from collections import defaultdict
from itertools import product
from math import factorial


ZERO = "0"
TERMINAL = ("x^6", "y^6", "z^6")
GENERATORS = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
ROWS = {
    "x^6": tuple((6 - index, index, 0) for index in range(6)),
    "y^6": tuple((0, 6 - index, index) for index in range(6)),
    "z^6": tuple((index, 0, 6 - index) for index in range(6)),
}
CLASS_OF = {triple: terminal for terminal, row in ROWS.items() for triple in row}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def triples(degree):
    return [(first, second, degree - first - second)
            for first in range(degree + 1)
            for second in range(degree - first + 1)]


def normal_form(triple, smaller=False):
    if smaller and min(triple) > 0:
        return ZERO
    degree = sum(triple)
    if 1 <= degree <= 5:
        return triple
    return CLASS_OF.get(triple, ZERO) if degree == 6 else ZERO


def multiply(left, right, smaller=False):
    if left == ZERO or right == ZERO or left in TERMINAL or right in TERMINAL:
        return ZERO
    return normal_form(tuple(first + second for first, second in zip(left, right)),
                       smaller)


def add_coeff(left, right):
    return left[0] + right[0], left[1] + right[1]


def multiply_coeff(left, right):
    constant_left, linear_left = left
    constant_right, linear_right = right
    return (constant_left * constant_right - linear_left * linear_right,
            constant_left * linear_right + linear_left * constant_right
            - linear_left * linear_right)


def multiply_vectors(left, right, smaller=False):
    answer = defaultdict(lambda: (0, 0))
    for left_basis, left_coeff in left.items():
        for right_basis, right_coeff in right.items():
            basis = multiply(left_basis, right_basis, smaller)
            if basis != ZERO:
                answer[basis] = add_coeff(
                    answer[basis], multiply_coeff(left_coeff, right_coeff))
    return {basis: coefficient for basis, coefficient in answer.items()
            if coefficient != (0, 0)}


def rotate(element):
    if element == ZERO:
        return ZERO
    if element in TERMINAL:
        return TERMINAL[(TERMINAL.index(element) + 1) % 3]
    first, second, third = element
    return third, first, second


def quotient(element):
    return ZERO if isinstance(element, tuple) and min(element) > 0 else element


def check_semigroup(smaller=False):
    lower = [triple for degree in range(1, 6) for triple in triples(degree)
             if not smaller or min(triple) == 0]
    elements = [ZERO] + lower + list(TERMINAL)
    expected_size = 49 if smaller else 59
    require(len(elements) == len(set(elements)) == expected_size, "Cardinality")
    table = {(left, right): multiply(left, right, smaller)
             for left, right in product(elements, repeat=2)}
    for left, right in product(elements, repeat=2):
        result = table[left, right]
        require(result in elements, "Closure")
        require(result == table[right, left], "Commutativity")
        require(rotate(result) == table[rotate(left), rotate(right)], "Rotation")
    for first, second, third in product(elements, repeat=3):
        require(table[table[first, second], third]
                == table[first, table[second, third]], "Associativity")
    require(all(table[ZERO, element] == table[element, ZERO] == ZERO
                for element in elements), "Zero element")
    require(all(table[terminal, element] == ZERO
                for terminal in TERMINAL for element in elements), "Annihilation")
    for generator, terminal in zip(GENERATORS, TERMINAL):
        current = generator
        for exponent in range(2, 8):
            current = table[current, generator]
            if exponent == 6:
                require(current == terminal, "Generator sixth power")
        require(current == ZERO, "Generator seventh power")
    reachable = set(elements)
    for length in range(2, 8):
        reachable = {table[left, right] for left in reachable for right in elements}
        if length == 6:
            require(set(TERMINAL).issubset(reachable), "Nilpotency lower bound")
    require(reachable == {ZERO}, "Every seven-factor product is zero")
    require(table[(2, 1, 0), (3, 0, 0)] == "x^6", "First example")
    require(table[(0, 2, 1), (0, 3, 0)] == "y^6", "Second example")
    require(table["x^6", GENERATORS[0]] == ZERO, "Fourth example")
    if not smaller:
        require(table[(1, 1, 1), (1, 1, 1)] == ZERO, "Third example")
    witness = dict(zip(GENERATORS, ((1, 0), (0, 1), (-1, -1))))
    require(witness[GENERATORS[0]] == (1, 0), "Nonzero witness")
    current = witness
    supports = [len(current)]
    for exponent in range(2, 7):
        current = multiply_vectors(current, witness, smaller)
        supports.append(len(current))
    expected_supports = [3, 6, 9, 12, 15, 0] if smaller else [3, 6, 10, 15, 21, 0]
    require(supports == expected_supports and current == {}, "Exact sixth power")
    print(f"Semigroup elements: {expected_size}; contracted algebra dimension: {expected_size - 1}.")
    print(f"Closure, commutativity and rotation: all {expected_size ** 2} ordered pairs.")
    print(f"Associativity: all {expected_size ** 3} ordered triples.")
    print("Zero element, terminal annihilation and selected products: satisfied.")
    print("Generator sixth powers: x -> x^6, y -> y^6, z -> z^6; distinct and nonzero.")
    print("All seven-factor products: zero; nilpotency index: seven.")
    print("Nonzero terms in u^1 through u^6: " + ", ".join(map(str, supports)) + ".")
    return elements


def main():
    require(len(CLASS_OF) == 18, "Disjoint degree-six classes")
    require(all(sum(triple) == 6 and min(triple) == 0 for triple in CLASS_OF),
            "Degree-six support")
    require(set(CLASS_OF) == {triple for triple in triples(6) if min(triple) == 0},
            "All two-generator degree-six monomials")
    for terminal, row in ROWS.items():
        for triple in row:
            require(normal_form(triple) == terminal, "Defining relation")
    for triple in triples(6):
        if min(triple) > 0:
            require(normal_form(triple) == ZERO, "Mixed degree-six relation")
    require(all(normal_form(triple) == ZERO for triple in triples(7)),
            "Degree-seven relations")
    totals = {terminal: [0, 0, 0] for terminal in TERMINAL}
    for first, second, third in triples(6):
        terminal = CLASS_OF.get((first, second, third))
        if terminal is not None:
            weight = factorial(6) // (factorial(first) * factorial(second)
                                      * factorial(third))
            totals[terminal][(second + 2 * third) % 3] += weight
    require(totals == {terminal: [21, 21, 21] for terminal in TERMINAL},
            "Multinomial residue sums")
    original = check_semigroup()
    smaller = check_semigroup(smaller=True)
    removed = [element for element in original if quotient(element) == ZERO
               and element != ZERO]
    require(len(removed) == 10, "Ten additional zero monomials")
    require({quotient(element) for element in original} == set(smaller),
            "Surjective quotient")
    for left, right in product(original, repeat=2):
        require(quotient(multiply(left, right))
                == multiply(quotient(left), quotient(right), smaller=True),
                "Quotient homomorphism")
    print("Each terminal coefficient has residue weights [21, 21, 21].")
    print("Each coefficient equals 21*(1+t+t^2) = 0 in Z[t]/(t^2+t+1).")
    print("Adding xyz=0 removes exactly ten elements; quotient map: all 3481 pairs.")
    print("All finite checks passed with exact integer arithmetic.")


if __name__ == "__main__":
    main()
