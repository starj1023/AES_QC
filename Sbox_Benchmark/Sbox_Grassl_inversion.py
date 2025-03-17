from projectq.ops import H, CNOT, Measure, Toffoli, X, All, Swap, Z, T, Tdagger, S, Tdag
from projectq import MainEngine
from projectq.backends import ResourceCounter, ClassicalSimulator, IBMBackend
from projectq.meta import Loop, Compute, Uncompute, Control

def Sbox(eng):

    n = 8
    a = eng.allocate_qureg(n)

    if(resource_check != 1):
        Round_constant_XOR(eng, a, 0xff, n)

    a1 = eng.allocate_qureg(n)
    a2 = eng.allocate_qureg(n)
    a3 = eng.allocate_qureg(n)
    a4 = eng.allocate_qureg(n)

    with Compute(eng):
        copy(eng, a, a1, n) # a1 = a
        a1 = Squaring(eng, a1, n) # a1 = a^2

    Schoolbook_mul(eng, a, a1, a2) # a2 = a * a^2
    Uncompute(eng)

    # (a * a^2) ^64
    a = Squaring(eng, a, n)
    a = Squaring(eng, a, n)
    a = Squaring(eng, a, n)
    a = Squaring(eng, a, n)
    a = Squaring(eng, a, n)
    a = Squaring(eng, a, n) #^64

    Schoolbook_mul(eng, a2, a, a1)

    a2 = Squaring(eng, a2, n)
    a2 = Squaring(eng, a2, n)
    Schoolbook_mul(eng, a2, a1, a3)

    a2 = Squaring(eng, a2, n)
    a2 = Squaring(eng, a2, n)
    Schoolbook_mul(eng, a2, a3, a4)

    a4 = Squaring(eng, a4, n)

    #U
    CNOT | (a4[4], a4[0])
    CNOT | (a4[5], a4[0])
    CNOT | (a4[6], a4[0])
    CNOT | (a4[7], a4[0])
    CNOT | (a4[4], a4[1])
    CNOT | (a4[5], a4[2])
    CNOT | (a4[6], a4[3])
    CNOT | (a4[7], a4[4])

    #L
    CNOT | (a4[2], a4[7])
    CNOT | (a4[3], a4[7])
    CNOT | (a4[4], a4[7])
    CNOT | (a4[1], a4[6])
    CNOT | (a4[2], a4[6])
    CNOT | (a4[3], a4[6])
    CNOT | (a4[3], a4[5])
    CNOT | (a4[4], a4[5])
    CNOT | (a4[0], a4[4])
    CNOT | (a4[1], a4[4])
    CNOT | (a4[2], a4[4])
    CNOT | (a4[3], a4[4])
    CNOT | (a4[0], a4[3])
    CNOT | (a4[1], a4[3])
    CNOT | (a4[2], a4[3])
    CNOT | (a4[0], a4[2])
    CNOT | (a4[1], a4[2])
    CNOT | (a4[0], a4[1])

    if (resource_check != 1):
        Swap | (a4[5], a4[6])
        Swap | (a4[6], a4[7])

    X | (a4[0])
    X | (a4[1])
    X | (a4[5])
    X | (a4[6])

    if (resource_check != 1):

        print('Sbox: ')
        All(Measure) | a4
        for i in range(8):
            print(int(a4[n - 1 - i]), end=' ')


def copy(eng, a, b, n):
    for i in range(n):
        CNOT | (a[i], b[i])

def Schoolbook_mul(eng, a, b, c):

    #8
    Toffoli_gate(eng, a[1], b[7], c[0])
    Toffoli_gate(eng, a[2], b[6], c[0])
    Toffoli_gate(eng, a[3], b[5], c[0])
    Toffoli_gate(eng, a[4], b[4], c[0])
    Toffoli_gate(eng, a[5], b[3], c[0])
    Toffoli_gate(eng, a[6], b[2], c[0])
    Toffoli_gate(eng, a[7], b[1], c[0])

    #9
    Toffoli_gate(eng, a[2], b[7], c[1])
    Toffoli_gate(eng, a[3], b[6], c[1])
    Toffoli_gate(eng, a[4], b[5], c[1])
    Toffoli_gate(eng, a[5], b[4], c[1])
    Toffoli_gate(eng, a[6], b[3], c[1])
    Toffoli_gate(eng, a[7], b[2], c[1])


    #10
    Toffoli_gate(eng, a[3], b[7], c[2])
    Toffoli_gate(eng, a[4], b[6], c[2])
    Toffoli_gate(eng, a[5], b[5], c[2])
    Toffoli_gate(eng, a[6], b[4], c[2])
    Toffoli_gate(eng, a[7], b[3], c[2])


    #11
    Toffoli_gate(eng, a[4], b[7], c[3])
    Toffoli_gate(eng, a[5], b[6], c[3])
    Toffoli_gate(eng, a[6], b[5], c[3])
    Toffoli_gate(eng, a[7], b[4], c[3])


    #12
    Toffoli_gate(eng, a[5], b[7], c[4])
    Toffoli_gate(eng, a[6], b[6], c[4])
    Toffoli_gate(eng, a[7], b[5], c[4])

    #13
    Toffoli_gate(eng, a[6], b[7], c[5])
    Toffoli_gate(eng, a[7], b[6], c[5])

    #14
    Toffoli_gate(eng, a[7], b[7], c[6])


    # color
    CNOT | (c[4], c[0]) #8, 12, 13
    CNOT | (c[5], c[0])

    CNOT | (c[5], c[1]) # 9, 13, 14
    CNOT | (c[6], c[1])

    CNOT | (c[6], c[2]) # 10, 14

    # gray
    CNOT | (c[6], c[7])

    CNOT | (c[5], c[6])

    CNOT | (c[4], c[5])
    CNOT | (c[4], c[7])

    CNOT | (c[3], c[4])
    CNOT | (c[3], c[6])
    CNOT | (c[3], c[7])

    # copy
    CNOT | (c[2], c[3])
    CNOT | (c[2], c[5])
    CNOT | (c[2], c[6])

    CNOT | (c[1], c[2])
    CNOT | (c[1], c[4])
    CNOT | (c[1], c[5])

    CNOT | (c[0], c[1])
    CNOT | (c[0], c[3])
    CNOT | (c[0], c[4])

    #
    Toffoli_gate(eng, a[0], b[0], c[0])

    Toffoli_gate(eng, a[0], b[1], c[1])
    Toffoli_gate(eng, a[1], b[0], c[1])

    Toffoli_gate(eng, a[0], b[2], c[2])
    Toffoli_gate(eng, a[1], b[1], c[2])
    Toffoli_gate(eng, a[2], b[0], c[2])

    Toffoli_gate(eng, a[0], b[3], c[3])
    Toffoli_gate(eng, a[1], b[2], c[3])
    Toffoli_gate(eng, a[2], b[1], c[3])
    Toffoli_gate(eng, a[3], b[0], c[3])

    Toffoli_gate(eng, a[0], b[4], c[4])
    Toffoli_gate(eng, a[1], b[3], c[4])
    Toffoli_gate(eng, a[2], b[2], c[4])
    Toffoli_gate(eng, a[3], b[1], c[4])
    Toffoli_gate(eng, a[4], b[0], c[4])

    Toffoli_gate(eng, a[0], b[5], c[5])
    Toffoli_gate(eng, a[1], b[4], c[5])
    Toffoli_gate(eng, a[2], b[3], c[5])
    Toffoli_gate(eng, a[3], b[2], c[5])
    Toffoli_gate(eng, a[4], b[1], c[5])
    Toffoli_gate(eng, a[5], b[0], c[5])

    Toffoli_gate(eng, a[0], b[6], c[6])
    Toffoli_gate(eng, a[1], b[5], c[6])
    Toffoli_gate(eng, a[2], b[4], c[6])
    Toffoli_gate(eng, a[3], b[3], c[6])
    Toffoli_gate(eng, a[4], b[2], c[6])
    Toffoli_gate(eng, a[5], b[1], c[6])
    Toffoli_gate(eng, a[6], b[0], c[6])

    Toffoli_gate(eng, a[0], b[7], c[7])
    Toffoli_gate(eng, a[1], b[6], c[7])
    Toffoli_gate(eng, a[2], b[5], c[7])
    Toffoli_gate(eng, a[3], b[4], c[7])
    Toffoli_gate(eng, a[4], b[3], c[7])
    Toffoli_gate(eng, a[5], b[2], c[7])
    Toffoli_gate(eng, a[6], b[1], c[7])
    Toffoli_gate(eng, a[7], b[0], c[7])


def Squaring(eng, vector, n):

    P = [1, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 1, 0, 0, 0,
         0, 1, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 1, 0,
         0, 0, 1, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 1, 0, 0,
         0, 0, 0, 1, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 1]

    L = [1, 0, 0, 0, 0, 0, 0, 0,
         0, 1, 0, 0, 0, 0, 0, 0,
         0, 0, 1, 0, 0, 0, 0, 0,
         0, 0, 0, 1, 0, 0, 0, 0,
         0, 0, 0, 0, 1, 0, 0, 0,
         0, 0, 0, 0, 0, 1, 0, 0,
         0, 0, 0, 0, 1, 1, 1, 0,
         0, 0, 0, 0, 0, 0, 1, 1]

    U = [1, 0, 0, 0, 1, 0, 1, 0,
         0, 1, 0, 0, 0, 1, 0, 0,
         0, 0, 1, 0, 1, 0, 0, 1,
         0, 0, 0, 1, 0, 1, 0, 0,
         0, 0, 0, 0, 1, 0, 1, 1,
         0, 0, 0, 0, 0, 1, 1, 0,
         0, 0, 0, 0, 0, 0, 1, 0,
         0, 0, 0, 0, 0, 0, 0, 1]

    Apply_U(eng, vector, n, U)
    Apply_L(eng, vector, n, L)

    out = []
    out.append(vector[0])
    out.append(vector[4])
    out.append(vector[1])
    out.append(vector[6])

    out.append(vector[2])
    out.append(vector[5])
    out.append(vector[3])
    out.append(vector[7])

    return out

def Apply_U(eng, key, n, U):
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if (U[(i * n) + 1 + i + j] == 1):
                CNOT | (key[1 + i + j], key[i])


def Apply_L(eng, key, n, L):
    for i in range(n - 1):
        for j in range(n - 1, 0 + i, -1):
            if (L[n * (n - 1 - i) + (n - 1 - j)] == 1):
                CNOT | (key[n - 1 - j], key[n - 1 - i])


def Round_constant_XOR(eng, k, rc, bit):
    for i in range(bit):
        if (rc >> i & 1):
            X | k[i]

def Toffoli_gate(eng, a, b, c):
    if(resource_check ==1):
        Tdag | a
        Tdag | b
        H | c
        CNOT | (c, a)
        T | a
        CNOT | (b, c)
        CNOT | (b, a)
        T  | c
        Tdag | a
        CNOT | (b, c)
        CNOT | (c, a)
        T | a
        Tdag | c
        CNOT | (b, a)
        H | c
    else:
        Toffoli | (a, b, c)

global resource_check

resource_check = 0
Resource = ClassicalSimulator()
eng = MainEngine(Resource)
Sbox(eng)  # (회로, a, b, n-bit, carryqubit)
eng.flush()
print()

resource_check = 1
Resource = ResourceCounter()
eng = MainEngine(Resource)
Sbox(eng)  # (회로, a, b, n-bit, carryqubit)
print(Resource)
eng.flush()