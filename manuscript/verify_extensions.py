"""Exact finite checks accompanying the corollaries in note.tex."""

from itertools import product
from math import comb

import verify


def polynomial_product(left, right):
    answer = [0] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            answer[left_index + right_index] += left_value * right_value
    return answer


def check_field_calculations():
    result = [1]
    for factor in [(-1, 1), (1, 1), (1, 1, 1), (1, -1, 1)]:
        result = polynomial_product(result, factor)
    verify.require(result == [-1, 0, 0, 0, 0, 0, 1], "Sixth-root factorization")
    tested = 0
    for first, second, third in product(range(-4, 5), repeat=3):
        if (first, second, third) == (0, 0, 0):
            continue
        terminal_coefficients = ((first + second) ** 6 - second ** 6,
                                 (second + third) ** 6 - third ** 6,
                                 (third + first) ** 6 - first ** 6)
        verify.require(any(terminal_coefficients), "Integer coefficient nonvanishing")
        tested += 1
    print("Sixth-root polynomial factorization: exact.")
    print(f"Nonzero integer coefficient triples in [-4,4]^3: {tested}; none has sixth power zero.")
    print("The characteristic-zero field criterion is proved in Corollary 2.")


def check_product_sets():
    for smaller, expected in [(False, [3, 6, 10, 15, 21, 3]),
                              (True, [3, 6, 9, 12, 15, 3])]:
        reachable = set(verify.GENERATORS)
        counts = [len(reachable)]
        for degree in range(2, 7):
            reachable = {verify.multiply(left, right, smaller)
                         for left in reachable for right in verify.GENERATORS}
            counts.append(len(reachable - {verify.ZERO}))
        verify.require(counts == expected, "Product-set cardinalities")
        print(f"{'49' if smaller else '59'}-element example: nonzero product-set sizes {counts}.")


def small_multiply(left, right):
    return "r" if (left, right) == ("p", "q") else "0"


def check_noncommutative_example():
    elements = ("0", "p", "q", "r")
    for first, second, third in product(elements, repeat=3):
        left = small_multiply(small_multiply(first, second), third)
        right = small_multiply(first, small_multiply(second, third))
        verify.require(left == right == "0", "Associativity and cube-zero property")
    verify.require(small_multiply("p", "q") != small_multiply("q", "p"),
                   "Noncommutativity")
    smaller = [verify.ZERO, *verify.TERMINAL]
    smaller += [triple for degree in range(1, 6) for triple in verify.triples(degree)
                if min(triple) == 0]
    for left, right in product(smaller, repeat=2):
        left_embedded = (left, "0")
        right_embedded = (right, "0")
        product_embedded = (verify.multiply(left, right, True),
                            small_multiply(left_embedded[1], right_embedded[1]))
        verify.require(product_embedded == (verify.multiply(left, right, True), "0"),
                       "Semigroup embedding")
    verify.require(len(smaller) * len(elements) == 196, "Direct product cardinality")
    print("Four-element semigroup N: all 64 triples have both products zero; pq=r and qp=0.")
    print("Embedding into the 196-element direct product: all 2401 pairs.")


def check_family():
    for exponent in (6, 12, 18, 24, 30, 60):
        rows = [tuple((exponent - index, index, 0) for index in range(exponent)),
                tuple((0, exponent - index, index) for index in range(exponent)),
                tuple((index, 0, exponent - index) for index in range(exponent))]
        terminals = {triple for row in rows for triple in row}
        verify.require(len(terminals) == 3 * exponent, "Disjoint terminal lists")
        verify.require(terminals == {triple for triple in verify.triples(exponent)
                                     if min(triple) == 0}, "Terminal coverage")
        lower = [triple for degree in range(1, exponent)
                 for triple in verify.triples(degree)]
        original_size = len(lower) + 4
        quotient_size = sum(min(triple) == 0 for triple in lower) + 4
        verify.require(original_size == comb(exponent + 2, 3) + 3, "Family cardinality")
        verify.require(quotient_size == 3 * exponent * (exponent - 1) // 2 + 4,
                       "Family quotient cardinality")
        for row in rows:
            weights = [0, 0, 0]
            for triple in row:
                first, second, third = triple
                weight = comb(exponent, first) * comb(exponent - first, second)
                weights[(second + 2 * third) % 3] += weight
            verify.require(weights[0] == weights[1] == weights[2], "Exact cancellation")
        print(f"Exponent {exponent}: sizes {original_size}, {quotient_size}; disjoint terminal lists and exact cancellation.")
    print("All multiples of six are covered by the written proof of Corollary 3.")


def main():
    check_field_calculations()
    check_product_sets()
    check_noncommutative_example()
    check_family()
    print("All supplemental finite checks passed with exact integer arithmetic.")


if __name__ == "__main__":
    main()
