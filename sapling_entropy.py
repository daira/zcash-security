#!/usr/bin/env python3

from math import e, log2 as lg
from fractions import Fraction
from itertools import count

# <https://zips.z.cash/protocol/protocol.pdf#jubjub>
rJ = 6554484396890773809930967563523245729705921265872317281365359162392183254199
n  = 1 << 256

COUNT = 10

def binomials(n, r):
    min_k = 3*n//(2*r)
    c = COUNT

    # We have a random function f : T -> S where |T| = n and |S| = r.
    # For a random scalar x in S, we have a p(k) probability that there are k inputs
    # in T mapping to x.
    #
    # Let p = 1/r. The binomial probability Pr(k; n, p) is
    #   nCk * p^k * (1-p)^(n-k)
    # = nCk / r^k * ((r-1)/r)^(n-k)
    # = nCk * ((r-1)/r)^n / ((r-1)/r * r)^k
    # = nCk * ((r-1)/r)^n / (r-1)^k
    #
    # We have ((r-1)/r)^n = (((r-1)/r)^r)^(n/r).
    # Since ((r-1)/r)^r tends to 1/e as r -> inf, we approximate this as (1/e)^(n/r).
    # (See <https://www.symbolab.com/solver/limit-calculator/%5Clim_%7Bx%5Cto%5Cinfty%20%7D%5Cleft(%5Cleft(%5Cleft(x-1%5Cright)%2Fx%5Cright)%5E%7Bx%7D%5Cright)?or=input>.)
    #
    # We then multiply by nCk / (r-1)^k for each k.

    Pr0 = (1/e)**(float(n)/r)

    Prm = Fraction(1)
    yield Pr0
    for k in count(start=1):
        Prm *= Fraction(n+1-k, k * (r-1))
        Pr = Pr0 * Prm
        yield Pr

        if k > min_k and Pr < 0.0000001:
            c -= 1
        else:
            c = COUNT
        if c == 0: break

def shannon_entropy(ps, n, r):
    # This is not strictly accurate, but we can estimate the Shannon entropy based on the
    # assumption that the outcomes will be distributed exactly according to the expectation
    # for a random function. So we need to calculate the expectation of -lg(P(X)).
    #
    # For random x in S, there is a probability p(k) that the inverse image f^-1(x)
    # has k elements. (Note that this is *not* the same thing as saying that for random
    # a in T, there is a probability p(k) that f^-1(f(a)) has k elements. For example,
    # there is zero probability that f(a) has no preimage, but p(0) is not necessarily
    # zero.)
    #
    # The entropy of X = f(T) is defined as the expectation of -lg(Pr[X = x]) over all x.
    #
    # Let M(k) = { x ∈ S : |f^-1(x)| = k }.
    #
    # We can estimate |M(k)| as r * p(k). Then, the entropy of f(T) is
    #
    #   ∑_{x ∈ S} Pr[f(T) = x] * -lg(Pr[f(T) = x])
    # = ∑_k ∑_{x ∈ M(k)} Pr_k[f(T) = x] * -lg(Pr_k[f(T) = x])
    #
    # where Pr_k[f(T) = x] is the probability that f(T) = x given that x ∈ M(k).
    # Since there are k preimages of x in T, Pr_k[f(T) = x] = k/n. So the entropy is
    #
    #   ∑_k |M(k)| * k/n * -lg(k/n)
    # = ∑_k r * p(k) * k/n * -lg(k/n)
    # = r/n * ∑_k p(k) * k * lg(n/k)

    lg_n = lg(n)
    return float(r)/n * sum([p * k * (lg_n - lg(k)) for (k, p) in enumerate(ps) if k > 0])

def plot(ps):
    from matplotlib import pyplot

    pyplot.rcParams['figure.figsize'] = (12, 8)
    pyplot.rcParams['axes.labelpad'] = 10
    pyplot.plot(range(len(ps)), ps)
    pyplot.axis((0.0, len(ps)-1, 0.0, 1.05*max(ps)))
    pyplot.title("Distribution of ToScalar^Sapling output frequencies", {'fontsize': 20}, pad=20)
    pyplot.xlabel("Frequency", {'fontsize': 14})
    pyplot.ylabel("Probability that a scalar has the given frequency", {'fontsize': 14})
    pyplot.show()


ps = list(binomials(n, rJ))

print(" k  p(k)")
for (k, p) in enumerate(ps):
    print("%2d  %f" % (k, p))

print("sum = %f" % (sum(ps),))
print("Shannon entropy = %f bits" % (shannon_entropy(ps, n, rJ),))
print("ideal   entropy = %f bits" % (lg(rJ),))
print("expected peak frequency = %f" % (n/rJ,))

plot(ps)
