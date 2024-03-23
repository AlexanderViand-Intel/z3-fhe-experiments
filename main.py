from z3 import *
from functools import reduce
from pprint import pprint


def matvecmul(M, v):
    return [sum(M[i][j] * v[j] for j in range(len(v))) for i in range(len(M))]


def svecreduceadd(u, n, assumptions):
    ps = FreshConst(ArraySort(IntSort(), IntSort()), "partialsum")
    i = Int("i")
    # Based on https://stackoverflow.com/q/66696664
    symSum = RecFunction("symSum" + str(ps), IntSort(), IntSort())
    RecAddDefinition(symSum, [i], If(i < 0, 0, u[i] + symSum(i - 1)))
    return symSum(n - 1)
    # assumptions.append(ps[0] == u[0])
    # assumptions.append(
    #     ForAll([i], Implies(And(i >= 1, i < n), ps[i] == ps[i - 1] + u[i]))
    # )
    # return ps[n - 1]


def smatvecmul(M, v, n, assumptions):
    out = FreshConst(ArraySort(IntSort(), ArraySort(IntSort(), IntSort())), "out")
    i = Int("i")
    j = Int("j")

    assumptions.append(
        ForAll(
            [i],
            Implies(
                And(i >= 0, i < n),
                out[i] == Sum([M[i][j] * v[j] for j in range(len(v))]),
            ),
        )
    )
    return out


def vecadd(u, v):
    return [a + b for a, b in zip(u, v)]


def vecmul(u, v):
    return [a * b for a, b in zip(u, v)]


def svecrot(u, k):
    return [u[(i + k) % len(u)] for i in range(len(u))]


def to_diag(M):
    return [[M[i][(j + i) % len(M)] for i in range(len(M))] for j in range(len(M))]


def diagimpl(M, v):
    return reduce(vecadd, (vecmul(d, svecrot(v, i)) for i, d in enumerate(to_diag(M))))


def svecrot(u, r, n, assumptions):
    out = FreshConst(ArraySort(IntSort(), IntSort()), "rot")
    i = Int("i")
    assumptions.append(
        ForAll([i], Implies(And(i >= 0, i < n), out[i] == u[(i + r) % n]))
    )
    return out


def svecmap2(f, fname, u, v, n, assumptions):
    out = FreshConst(ArraySort(IntSort(), IntSort()), fname)
    i = Int("i")
    assumptions.append(
        ForAll([i], Implies(And(i >= 0, i < n), out[i] == f(u[i], v[i])))
    )
    return out


def svecadd(u, v, n, assumptions):
    return svecmap2(lambda a, b: a + b, "add", u, v, n, assumptions)


def svecmul(u, v, n, assumptions):
    return svecmap2(lambda a, b: a * b, "mul", u, v, n, assumptions)


def sveceq(u, v, n):
    i = Int("i")
    return ForAll([i], Implies(And(i >= 0, i < n), u[i] == v[i]))


def symbolic():
    n = 10
    input = FreshConst(ArraySort(IntSort(), IntSort()), "in1")
    input2 = FreshConst(ArraySort(IntSort(), IntSort()), "in2")
    r = Int("r")
    assumptions = [r < n, r >= 0, n > 0]
    rot = svecrot(input, r, n, assumptions)
    # rot2 = svecrot(rot, -r, n, assumptions)
    # ab = svecmul(input, input2, n, assumptions)
    # ba = svecmul(input2, input, n, assumptions)
    # correctness = sveceq(input, rot2, n)
    correctness = svecreduceadd(input, n, assumptions) == svecreduceadd(
        rot, n, assumptions
    )
    to_prove = Implies(And(*assumptions), correctness)
    s = Solver()
    s.add(Not(to_prove))
    print(s.to_smt2())
    prove(to_prove)


def concrete():
    a, b = Ints("a b")
    assumptions = []
    in_size = 2**14
    v = [Int("v_%s" % i) for i in range(in_size)]
    out_size = 2**14
    M = [[Int("M_%s_%s" % (i, j)) for j in range(in_size)] for i in range(out_size)]
    # pprint(M)
    # pprint(to_diag(M))
    # pprint(matvecmul(M, v))
    # pprint(diagimpl(M, v))
    prove(And(*[a == b for a, b in zip(matvecmul(M, v), diagimpl(M, v))]))


symbolic()
