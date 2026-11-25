"""Exact checks for the binomial-partition and truncated right-zero examples."""

from collections import defaultdict
from itertools import product
from math import comb


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def algebra_product(left, right, multiply):
    result = defaultdict(int)
    for left_element, left_coefficient in left.items():
        for right_element, right_coefficient in right.items():
            element = multiply(left_element, right_element)
            if element != "0":
                result[element] += left_coefficient * right_coefficient
    return {element: coefficient for element, coefficient in result.items() if coefficient}


def algebra_power(vector, exponent, multiply):
    result = vector
    for step in range(1, exponent):
        result = algebra_product(result, vector, multiply)
    return result


def check_partition():
    exponent = 35
    selected = set(range(14)) | {20, 21}
    unfolded = [int(index in selected) for index in range(exponent + 1)]
    folded = [unfolded[index] - unfolded[exponent - index] for index in range(18)]
    require(folded == [1] * 14 + [-1, -1, 0, 0], "Published folded vector")
    require(unfolded[0] == 1 and unfolded[-1] == 0, "Separated endpoints")
    signed_selected = sum((-1) ** index * comb(exponent, index) for index in selected)
    signed_other = sum((-1) ** index * comb(exponent, index)
                       for index in range(exponent + 1) if index not in selected)
    signed_folded = sum((-1) ** index * comb(exponent, index) * value
                        for index, value in enumerate(folded))
    require(signed_selected == signed_other == signed_folded == 0, "Exact signed sums")
    require(comb(34, 15) == 2 * comb(34, 13), "Binomial coefficient ratio")

    def reduce_monomial(first_power, second_power):
        degree = first_power + second_power
        if degree > exponent:
            return "0"
        if degree == exponent:
            return "A" if second_power in selected else "B"
        return first_power, second_power

    def lift(element):
        if element == "A":
            return exponent, 0
        if element == "B":
            return 0, exponent
        return element

    def multiply(left, right):
        if left == "0" or right == "0":
            return "0"
        left_first, left_second = lift(left)
        right_first, right_second = lift(right)
        return reduce_monomial(left_first + right_first, left_second + right_second)

    lower = [(degree - index, index) for degree in range(1, exponent)
             for index in range(degree + 1)]
    elements = ["0", "A", "B", *lower]
    element_set = set(elements)
    require(len(element_set) == 632, "Semigroup cardinality")
    pairs = 0
    for left, right in product(elements, repeat=2):
        answer = multiply(left, right)
        require(answer in element_set, "Closure")
        require(answer == multiply(right, left), "Commutativity")
        if left in ("A", "B") or right in ("A", "B"):
            require(answer == "0", "Terminal annihilation")
        pairs += 1
    for index in range(exponent + 1):
        monomial = (exponent - index, index)
        terminal = reduce_monomial(*monomial)
        for generator in [(1, 0), (0, 1)]:
            require(reduce_monomial(monomial[0] + generator[0],
                                    monomial[1] + generator[1]) == "0",
                    "Defining congruence compatibility")
            require(multiply(terminal, generator) == "0", "Terminal representative compatibility")
    first, second = (1, 0), (0, 1)
    require(algebra_power({first: 1}, exponent, multiply) == {"A": 1}, "First generator power")
    require(algebra_power({second: 1}, exponent, multiply) == {"B": 1}, "Second generator power")
    require(algebra_power({first: 1}, exponent + 1, multiply) == {}, "Nilpotency index")
    require(algebra_power({first: 1, second: -1}, exponent, multiply) == {},
            "Independent repeated-product cancellation")
    print("Published n=35 folded vector and unfolding: exact; endpoints separated.")
    print("Folded, selected and complementary signed binomial sums: all zero.")
    print("Identity C(34,15)=2*C(34,13): exact.")
    print(f"Commutative example: 632 elements; all {pairs} ordered products checked.")
    print("All 72 terminal-monomial/generator congruence checks pass.")
    print("Distinct generator powers A,B; (x-y)^35=0 by repeated multiplication; nilpotency index 36.")


def check_right_zero_examples():
    for exponent in (2, 3, 6):
        elements = ["0", *((degree, label) for degree in range(1, exponent + 1)
                           for label in ("e", "f"))]

        def multiply(left, right):
            if left == "0" or right == "0":
                return "0"
            degree = left[0] + right[0]
            return (degree, right[1]) if degree <= exponent else "0"

        for left, middle, right in product(elements, repeat=3):
            require(multiply(multiply(left, middle), right) ==
                    multiply(left, multiply(middle, right)), "Associativity")
        first, second = (1, "e"), (1, "f")
        require(multiply(first, second) != multiply(second, first), "Strict noncommutativity")
        require(algebra_power({first: 1}, exponent, multiply) == {(exponent, "e"): 1},
                "First generator power")
        require(algebra_power({second: 1}, exponent, multiply) == {(exponent, "f"): 1},
                "Second generator power")
        difference = {first: 1, second: -1}
        require(algebra_power(difference, 2, multiply) == {}, "Square-zero difference")
        require(algebra_power(difference, exponent, multiply) == {}, "Exponent cancellation")
        require(algebra_power({first: 1}, exponent + 1, multiply) == {}, "Nilpotency index")
        print(f"Right-zero truncation n={exponent}: {len(elements)} elements; all {len(elements) ** 3} associativity triples; square-zero difference.")
    print("The general constructions and associativity are proved in note.tex.")


if __name__ == "__main__":
    check_partition()
    check_right_zero_examples()
    print("All prior-identity consequence checks passed with exact integer arithmetic.")
