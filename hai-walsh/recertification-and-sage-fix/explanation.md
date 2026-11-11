Sage first proves that an integral point must have coefficients smaller than
an enormous number in a Mordell–Weil basis. It then uses a lattice to shrink
that search to a practical size. A short elliptic logarithm would produce a
short vector in this lattice. Therefore a proved lower bound on lattice
vector lengths can rule out large coefficients.

The lower bound has to beat a threshold that accounts for the allowed
coefficients and rounding errors. The old code sometimes fails that test,
assigns a much larger number to the lower bound, and continues. Assigning
the number does not make the lattice vectors longer. The resulting smaller
search can omit integral points; 2082a1 and 1701d1 demonstrate this in the
installed Sage 10.9.

The patch constructs a new lattice at a larger scale when the test fails.
It also increases numerical precision, encloses rounding errors, and uses
exact rational arithmetic for the lattice lower bound. It proceeds only
after the inequality is established. If sixteen attempts fail, it reports
an error instead of returning a purported complete list.

That repair is local. The legacy method has other reported problems in its
initial bound and floating-point final search. For the Hai–Walsh classification,
the accompanying certificate avoids both: it derives height estimates from
exact duplication formulas, uses David's original theorem and Arb enclosures,
then checks every remaining coefficient combination with exact rational
arithmetic. The report states which curves and point lists this certifies.

The fallback was already reported by Cremona in 2013, and an open 2026 PR
contains broader work on the same problem. This work confirms and tests the
defect; it does not claim priority. Nothing has been posted upstream.
