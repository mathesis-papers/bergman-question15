# Examples answering Bergman's Question 15 by extending a partition of von zur Gathen and Roche

*Thoughts on Eggert's Conjecture*, arXiv:1206.0326v2, Section 4, printed page 6.
The corresponding locator in the 17-page published layout is Section 4, page 9.

Haobo Ma (ChronoAI Pte Ltd, Singapore), then Wenlin Zhang (National University
of Singapore; ChronoAI Pte Ltd, Singapore). 19 November 2026. Revision 5.
License: Creative Commons Attribution 4.0 International (CC BY 4.0; cc-by-4.0).

## Result

The 59-element commutative semigroup S and its 49-element quotient have
three generators with distinct nonzero sixth powers. Nevertheless,
(x + omega*y + omega^2*z)^6 = 0 in the contracted semigroup algebra whenever
omega is a primitive cube root of unity. For these presentations over a
characteristic-zero field, such a nonzero cancellation exists exactly when
the field contains a primitive cube root of unity. No two-generator span
has a nonzero sixth-power zero.

The note proves the analogous construction for every positive exponent
divisible by six. The 49-element example also embeds into a strictly
noncommutative, nilpotent 196-element example. Thus the Question-15 branch
of Question 19 is answered negatively. Other branches of Question 19 are
separate questions. The exact product-set counts show compatibility with
Question 11 for the displayed generating sets, not a universal answer.

A binomial partition of Joachim von zur Gathen and James R. Roche,
*Polynomials with two values*, Combinatorica 17 (1997), Table 2, p. 359,
gives a 632-element commutative example at exponent 35 over every
characteristic-zero field, including Q. The note proves the semigroup
deduction from that partition explicitly. The cited paper does not formulate
it as an answer to Bergman's later question.

The square-zero identity in Almeida, Margolis, Steinberg and Volkov,
arXiv:math/0702400v1 (2007), proof of Proposition 3.4, p. 11, gives a
strictly noncommutative nilpotent example of 2n+1 elements for every n>=2
by degree truncation. At exponent 6 this has 13 elements. The note also
credits Benjamin and Scott (2011) for the underlying residue-class binomial sums.

Appendix A gives a second 59-element degree-six partition, its full
multinomial cancellation and worked products, including the expansion of
the square of the cancelling vector. This is the partition used by the
linked Lean statement; the cyclic presentation is a different semigroup.

## Build

Use Tectonic 0.17.0:

```sh
tectonic note.tex
```

Alternatively use a standard LaTeX installation:

```sh
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error note.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error note.tex
```

The bibliography is contained in note.tex; no BibTeX step is needed.

## Exact checks

Use Python 3.9 or later, with no additional packages:

```sh
python3 verify.py > actual.txt
diff -u verification.txt actual.txt
python3 verify_extensions.py > extensions-actual.txt
diff -u extension-verification.txt extensions-actual.txt
python3 verify_priorwork.py > priorwork-actual.txt
diff -u priorwork-verification.txt priorwork-actual.txt
python3 verify_original.py > original-actual.txt
diff -u original-verification.txt original-actual.txt
```

The first checker exhaustively checks the two multiplication tables
(59^2 and 49^2 ordered pairs; 59^3 and 49^3 ordered triples), their
nilpotency and quotient map, and the sixth-power cancellation in
Z[t]/(t^2+t+1) by two exact methods. Each terminal coefficient has
residue weights [21,21,21].

The supplemental checker verifies the product-set counts, the four-element
semigroup used for the noncommutative example, the embedding on all 2401
pairs, the sixth-root polynomial factorization, and selected family
instances n = 6, 12, 18, 24, 30, 60. Its integer-coefficient search is
restricted to [-4,4]^3. The unrestricted field criterion and the full
family are written proofs in Corollaries 2 and 3, not conclusions drawn
from a finite search.

## Formal statement and mathematical scope

The declaration
`D5.S0.Certificates.Algebra.BergmanQuestion15Refutation.result` in
[BergmanQuestion15Refutation.lean](https://github.com/the-omega-institute/trureturing/blob/72243b116c47bc4fee2838e6b95fbab9802ed050/D5/S0/Certificates/Algebra/BergmanQuestion15Refutation.lean)
proves the negative answer to Question 15 using a different 59-element
partition, displayed and proved in Appendix A. With A=x^6, B=y^6, C=z^6,
it assigns x^5*z to A rather than C,
x*y^5 to B rather than A, and y*z^5 to C rather than B.
The simplified presentation, its 49-element quotient and all six
corollaries have the written proofs in note.tex and supporting finite
checks with the scopes stated above.

George M. Bergman suggested the cyclic simplification and the quotient
obtained by adding xyz=0.

The third checker verifies the published folded vector and its unfolding,
both vanishing signed sums, all 399424 products of the 632-element example,
terminal-congruence compatibility and an independent repeated-product
calculation of (x-y)^35. It exhaustively checks the truncated right-zero
examples at n=2,3,6, including all associativity triples. The general
construction and all-parameter statements have written proofs in note.tex.

The fourth checker, verify_original.py, checks all 3481 ordered products
and 205379 associativity triples for the 59-element partition in Appendix A,
the absorbing zero, generator powers and worked products. It verifies the
sixth-power identity by repeated multiplication and independently by
multinomial weights in Z[t]/(t^2+t+1). The supports in powers one through
six have sizes 3, 6, 10, 15, 21, 0.

## Scientific reference

George M. Bergman, *Thoughts on Eggert's Conjecture*, in *Ring Theory and
Its Applications*, Contemporary Mathematics 609 (2014), 1-17.
DOI: https://doi.org/10.1090/conm/609/12101.
Posing version: https://arxiv.org/abs/1206.0326v2.

Copyright 2026 Haobo Ma and Wenlin Zhang.
License: https://creativecommons.org/licenses/by/4.0/.
