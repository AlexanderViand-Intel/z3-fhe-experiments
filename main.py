from z3 import *
from functools import reduce
from pprint import pprint


def matvecmul(M, v):
    return [sum(M[i][j] * v[j] for j in range(len(v))) for i in range(len(M))]


def vecadd(u, v):
    return [a + b for a, b in zip(u, v)]


def vecmul(u, v):
    return [a * b for a, b in zip(u, v)]


def vecrot(u, k):
    return [u[(i + k) % len(u)] for i in range(len(u))]


def to_diag(M):
    return [[M[i][(j + i) % len(M)] for i in range(len(M))] for j in range(len(M))]


def diagimpl(M, v):
    return reduce(vecadd, (vecmul(d, vecrot(v, i)) for i, d in enumerate(to_diag(M))))


def main():
    a, b = Ints("a b")
    in_size = 2**14
    v = [Int("v_%s" % i) for i in range(in_size)]
    out_size = 2**14
    M = [[Int("M_%s_%s" % (i, j)) for j in range(in_size)] for i in range(out_size)]
    # pprint(M)
    # pprint(to_diag(M))
    # pprint(matvecmul(M, v))
    # pprint(diagimpl(M, v))
    prove(And(*[a == b for a, b in zip(matvecmul(M, v), diagimpl(M, v))]))


main()
