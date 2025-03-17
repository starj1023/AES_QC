from projectq.ops import H, CNOT, Measure, Toffoli, X, All, Swap, Z, T, Tdagger, S, Tdag
from projectq import MainEngine
from projectq.backends import ResourceCounter, ClassicalSimulator, IBMBackend
from projectq.meta import Loop, Compute, Uncompute, Control

def Sbox(eng):

    n = 8
    a = eng.allocate_qureg(n) # input
    s = eng.allocate_qureg(n) # output

    # Ancilla qubits
    y = eng.allocate_qureg(100)  #
    t = eng.allocate_qureg(100)  #
    z = eng.allocate_qureg(100)  #

    if(resource_check != 1):
        Round_constant_XOR(eng, a, 0xff, n)

    s = Langenberg(eng, a, y, t, s)

    if (resource_check != 1):
        print('Sbox: ')
        All(Measure) | s
        for i in range(8):
            print(int(s[n - 1 - i]), end=' ')

def Langenberg(eng, u, T, Z, S):
    U = []

    # print('sbox input')
    U.append(u[7])
    U.append(u[6])
    U.append(u[5])
    U.append(u[4])

    U.append(u[3])
    U.append(u[2])
    U.append(u[1])
    U.append(u[0])
    # Toffoli_gate(eng, t[33], x[7], z[2])
    with Compute(eng):
        CNOT | (U[0], U[5])
        CNOT | (U[3], U[5])
        CNOT | (U[6], U[5])
        CNOT | (U[0], U[4])
        CNOT | (U[3], U[4])
        CNOT | (U[6], U[4])
        Toffoli_gate(eng, U[5], U[4], T[0])  # t2
        CNOT | (T[0], T[5])
        CNOT | (U[1], U[3])
        CNOT | (U[2], U[3])
        CNOT | (U[7], U[3])
        Toffoli_gate(eng, U[3], U[7], T[0])  # t6
        CNOT | (U[0], U[6])
        CNOT | (U[0], U[2])
        CNOT | (U[4], U[2])
        CNOT | (U[5], U[2])
        CNOT | (U[6], U[2])
        Toffoli_gate(eng, U[6], U[2], T[1])  # t7
        CNOT | (T[1], T[2])
        CNOT | (U[2], U[1])
        CNOT | (U[4], U[1])
        CNOT | (U[5], U[1])
        CNOT | (U[7], U[1])
        CNOT | (U[1], U[0])
        CNOT | (U[6], U[0])
        Toffoli_gate(eng, U[1], U[0], T[1])  # t9
        CNOT | (U[1], U[6])
        CNOT | (U[0], U[2])
        Toffoli_gate(eng, U[6], U[2], T[2])  # t11
        CNOT | (U[6], U[3])
        CNOT | (U[7], U[2])
        Toffoli_gate(eng, U[3], U[2], T[3])  # t12
        CNOT | (T[3], T[4])
        CNOT | (U[1], U[6])
        CNOT | (U[5], U[6])
        CNOT | (U[2], U[0])
        CNOT | (U[4], U[0])
        CNOT | (U[7], U[0])
        Toffoli_gate(eng, U[6], U[0], T[3])  # t14
        CNOT | (U[6], U[3])
        CNOT | (U[2], U[0])
        Toffoli_gate(eng, U[3], U[0], T[4])  # t16
        CNOT | (T[3], T[1])  # t19
        CNOT | (U[1], U[3])

        CNOT | (U[7], U[4])
        Toffoli_gate(eng, U[3], U[4], T[5])  # t4
        CNOT | (T[5], T[3])  # t17
        CNOT | (T[4], T[0])  # t18
        CNOT | (T[2], T[4])  # t20
        CNOT | (U[1], U[6])
        CNOT | (U[2], U[6])
        CNOT | (U[3], U[6])
        CNOT | (U[6], T[3])  # t21
        CNOT | (U[0], U[1])
        CNOT | (U[3], U[1])
        CNOT | (U[1], T[0])  # t22
        CNOT | (U[1], U[5])
        CNOT | (U[4], U[5])
        CNOT | (U[6], U[5])
        CNOT | (U[7], U[5])
        CNOT | (U[5], T[1])  # t23
        CNOT | (U[1], U[4])
        CNOT | (U[3], U[4])
        CNOT | (U[5], U[4])
        CNOT | (U[4], T[4])  # t24
        Toffoli_gate(eng, T[3], T[1], T[6])  # t26
        CNOT | (T[0], T[3])  # t25
        CNOT | (T[4], T[7])
        CNOT | (T[6], T[7])  # t27
        CNOT | (T[0], T[6])  # t31
        Toffoli_gate(eng, T[3], T[7], T[0])  # t29
        CNOT | (T[1], T[8])
        CNOT | (T[4], T[8])  # t30
        Toffoli_gate(eng, T[6], T[8], T[9])  # t32
        # clean up T[8]:
        CNOT | (T[4], T[8])
        CNOT | (T[1], T[8])
        # t[8] is free to reuse
        CNOT | (T[4], T[9])  # t33
        CNOT | (T[9], T[1])  # t34
        CNOT | (T[7], T[8])
        CNOT | (T[9], T[8])  # t35
        Toffoli_gate(eng, T[4], T[8], T[10])  # t36
        # clean up T[8] again:
        CNOT | (T[9], T[8])
        CNOT | (T[7], T[8])
        # t[8] is free to reuse
        CNOT | (T[10], T[1])  # t37
        CNOT | (T[10], T[7])  # t38
        Toffoli_gate(eng, T[0], T[7], T[3])  # t40
        CNOT | (T[3], T[8])
        CNOT | (T[1], T[8])  # t41
        CNOT | (T[0], T[11])
        CNOT | (T[9], T[11])  # t42
        CNOT | (T[0], T[12])
        CNOT | (T[3], T[12])  # t43
        CNOT | (T[9], T[13])
        CNOT | (T[1], T[13])  # t44
        CNOT | (T[11], T[14])
        CNOT | (T[8], T[14])  # t45
        CNOT | (U[0], U[2])
        CNOT | (U[1], U[2])
        CNOT | (U[6], U[2])  # for z16
        CNOT | (U[1], U[4])
        CNOT | (U[3], U[4])
        CNOT | (U[5], U[4])  # for z1
        CNOT | (U[1], U[6])
        CNOT | (U[3], U[6])
        CNOT | (U[4], U[6])
        CNOT | (U[5], U[6])
        CNOT | (U[7], U[6])  # for z11
        CNOT | (U[1], U[0])
        CNOT | (U[3], U[0])  # for z13
        CNOT | (U[0], U[3])
        CNOT | (U[2], U[3])
        CNOT | (U[6], U[3])  # for z14

    Toffoli_gate(eng, T[0], U[3], S[2])  # z14
    CNOT | (S[2], S[5])
    CNOT | (U[0], U[3])
    Toffoli_gate(eng, T[12], U[3], S[6])  # z12

    CNOT | (S[6], S[2])
    CNOT | (S[6], S[5])
    CNOT | (U[0], U[3])
    Toffoli_gate(eng, T[1], U[4], S[1])  # z1
    CNOT | (S[1], S[3])
    CNOT | (S[1], S[4])
    CNOT | (U[7], U[4])
    Toffoli_gate(eng, T[13], U[4], S[7])  # z0
    CNOT | (S[7], S[1])
    CNOT | (S[7], S[2])
    CNOT | (S[7], S[3])
    CNOT | (S[7], S[5])
    CNOT | (U[7], U[4])
    Toffoli_gate(eng, T[3], U[0], S[6])  # z13
    CNOT | (S[6], S[7])
    CNOT | (U[3], U[6])
    Toffoli_gate(eng, T[11], U[6], S[0])  # z15
    CNOT | (S[0], S[2])
    CNOT | (U[3], U[6])
    Toffoli_gate(eng, T[14], U[2], S[0])  # z16
    CNOT | (S[0], S[1])
    CNOT | (S[0], S[3])
    CNOT | (S[0], S[4])
    CNOT | (S[0], S[5])
    CNOT | (S[0], S[6])
    CNOT | (S[0], S[7])
    Toffoli_gate(eng, T[9], U[7], Z[0])  # z2
    CNOT | (Z[0], S[2])
    CNOT | (Z[0], S[4])
    CNOT | (Z[0], S[5])
    CNOT | (Z[0], S[7])
    Toffoli_gate(eng, T[9], U[7], Z[0])

    with Compute(eng):
        CNOT | (U[0], U[5])
        CNOT | (U[3], U[5])
        Toffoli_gate(eng, T[12], U[5], Z[0])  # z3
    CNOT | (Z[0], S[0])
    CNOT | (Z[0], S[3])
    CNOT | (Z[0], S[5])
    CNOT | (Z[0], S[7])
    Uncompute(eng)

    with Compute(eng):
        CNOT | (U[1], U[6])
        CNOT | (U[2], U[6])
        CNOT | (U[3], U[6])
        CNOT | (U[4], U[6])
        Toffoli_gate(eng, T[3], U[6], Z[0])  # z4
    CNOT | (Z[0], S[0])
    CNOT | (Z[0], S[3])
    CNOT | (Z[0], S[4])
    CNOT | (Z[0], S[5])
    CNOT | (Z[0], S[6])
    Uncompute(eng)

    with Compute(eng):
        CNOT | (U[0], U[6])
        CNOT | (U[1], U[6])
        CNOT | (U[2], U[6])
        CNOT | (U[4], U[6])
        CNOT | (U[5], U[6])
        Toffoli_gate(eng, T[0], U[6], Z[0])  # z5
    CNOT | (Z[0], S[4])
    CNOT | (Z[0], S[6])
    CNOT | (Z[0], S[7])
    Uncompute(eng)

    with Compute(eng):
        CNOT | (U[0], U[7])
        CNOT | (U[1], U[7])
        CNOT | (U[2], U[7])
        CNOT | (U[4], U[7])
        CNOT | (U[5], U[7])
        CNOT | (U[6], U[7])
        Toffoli_gate(eng, T[11], U[7], Z[0])  # z6
    CNOT | (Z[0], S[0])
    CNOT | (Z[0], S[1])
    CNOT | (Z[0], S[2])
    Uncompute(eng)

    with Compute(eng):
        CNOT | (U[0], U[7])
        CNOT | (U[3], U[7])
        CNOT | (U[4], U[7])
        CNOT | (U[5], U[7])
        Toffoli_gate(eng, T[14], U[7], Z[0])  # z7
    CNOT | (Z[0], S[0])
    CNOT | (Z[0], S[1])
    CNOT | (Z[0], S[5])
    CNOT | (Z[0], S[6])
    Uncompute(eng)

    with Compute(eng):
        CNOT | (U[1], U[6])
        CNOT | (U[2], U[6])
        CNOT | (U[3], U[6])
        Toffoli_gate(eng, T[8], U[6], Z[0])  # z8
    CNOT | (Z[0], S[2])
    CNOT | (Z[0], S[5])
    CNOT | (Z[0], S[6])
    Uncompute(eng)
    with Compute(eng):
        CNOT | (U[0], U[3])
        CNOT | (U[2], U[3])
        Toffoli_gate(eng, T[13], U[3], Z[0])  # z9
    CNOT | (Z[0], S[0])
    CNOT | (Z[0], S[1])
    CNOT | (Z[0], S[3])
    CNOT | (Z[0], S[4])
    Uncompute(eng)
    with Compute(eng):
        CNOT | (U[0], U[6])
        CNOT | (U[2], U[6])
        CNOT | (U[3], U[6])
        Toffoli_gate(eng, T[1], U[6], Z[0])  # z10
    CNOT | (Z[0], S[0])
    CNOT | (Z[0], S[1])
    CNOT | (Z[0], S[3])
    CNOT | (Z[0], S[4])
    CNOT | (Z[0], S[5])
    Uncompute(eng)
    CNOT | (U[2], U[6])
    CNOT | (U[3], U[6])
    Toffoli_gate(eng, T[8], U[6], S[2])  # z17
    CNOT | (U[3], U[6])
    CNOT | (U[2], U[6])
    Toffoli_gate(eng, T[9], U[6], S[5])  # z11

    X | S[1]
    X | S[2]
    X | S[6]
    X | S[7]

    out = []
    out.append(S[7])
    out.append(S[6])
    out.append(S[5])
    out.append(S[4])

    out.append(S[3])
    out.append(S[2])
    out.append(S[1])
    out.append(S[0])

    Uncompute(eng)

    return out

def CNOT2(eng, a, b, c):
    CNOT | (a, c)
    CNOT | (b, c)

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
Sbox(eng)
eng.flush()
print()

resource_check = 1
Resource = ResourceCounter()
eng = MainEngine(Resource)
Sbox(eng)
print(Resource)
eng.flush()