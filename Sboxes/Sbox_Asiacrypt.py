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

    new_a = []
    for i in range(8):
        new_a.append(a[7 - i])

    s = AES_Sbox(eng, new_a, y, s)

    if (resource_check != 1):
        print('Sbox: ')
        All(Measure) | s
        for i in range(8):
            print(int(s[n - 1 - i]), end=' ')

def CNOT2(eng, a, b, c):
    CNOT | (a, c)
    CNOT | (b, c)

def CNOT3(eng, a, b, c, d): #output:d
    CNOT |(a,d)
    CNOT | (b,d)
    CNOT | (c,d)

def CNOT4(eng, a, b, c, d, e): #output:e
    CNOT3(eng, a, b, c, e)
    CNOT | (d,e)

def CNOT5(eng, a, b, c, d, e, f): #output:f
    CNOT4(eng, a, b, c, d, f)
    CNOT | (e, f)

def CNOT6(eng, a, b, c, d, e, f, g): #output:g
    CNOT5(eng, a, b, c, d, e, g)
    CNOT | (f, g)


def AES_Sbox(eng, u, t, s): #Output t29 , t33 , t37 , t40 of S-box with 6 ancilla qubits
    CNOT | (u[6], u[0])
    CNOT3(eng, u[2], u[4], u[5], u[6])
    Toffoli_gate(eng, u[0], u[6], t[0])
    CNOT | (t[0], t[1])
    CNOT2(eng, u[2], u[7], u[1])
    CNOT4(eng, u[1], u[4], u[5], u[6], u[2])
    Toffoli_gate(eng, u[1], u[2], t[1])
    CNOT3(eng, u[1], u[2], u[3], u[0])

    CNOT2(eng, u[1], u[7], u[6])
    Toffoli_gate(eng, u[0], u[6], t[2])
    CNOT | (t[2], t[3])
    CNOT | (u[3], u[5])
    CNOT4(eng, u[2], u[4], u[6], u[7], u[0])
    Toffoli_gate(eng, u[5], u[0], t[3])
    CNOT | (t[3], t[1])
    CNOT2(eng, u[3], u[4], u[0])
    CNOT | (u[0], t[1])
    CNOT4(eng, u[1], u[2], u[6], u[7], u[0])

    CNOT | (u[7], u[6])
    Toffoli_gate(eng, u[0], u[6], t[0])
    CNOT2(eng, u[2], u[5], u[0])
    CNOT3(eng, u[0], u[3], u[4], u[5])
    Toffoli_gate(eng, u[0], u[5], t[4])
    CNOT | (t[4], t[3])
    CNOT2(eng, u[1], u[3], u[0])
    CNOT | (u[7], u[5])
    Toffoli_gate(eng, u[0], u[5], t[3])
    CNOT4(eng, u[2], u[4], u[5], u[6], u[1])
    CNOT | (u[1], t[3])
    CNOT3(eng, u[2], u[4], u[6], u[1])
    CNOT | (u[2], u[0])
    Toffoli_gate(eng, u[1], u[0], t[2])
    CNOT | (t[2], t[0])
    CNOT | (t[4], t[2])
    CNOT4(eng, u[1], u[2], u[3], u[5], u[0])
    CNOT | (u[7], u[5])
    Toffoli_gate(eng, u[0], u[5], t[4])
    CNOT4(eng, u[3], u[4], u[5], u[6], u[2])
    CNOT | (u[2], t[0])
    CNOT3(eng, u[3], u[5], u[7], u[1])
    Toffoli_gate(eng, u[1], u[7], t[2])
    CNOT4(eng, u[2], u[4], u[6], u[7], u[0])
    CNOT | (u[0], t[2])

    Toffoli_gate(eng, t[1], t[3], t[4])
    CNOT | (t[0], t[1])
    CNOT | (t[2], t[4])
    Toffoli_gate(eng, t[1], t[4], t[5])
    CNOT | (t[0], t[5])
    CNOT2(eng, t[0], t[5], t[1])
    CNOT2(eng, t[2], t[0], t[4])
    CNOT | (t[4], t[5])
    Toffoli_gate(eng, t[0], t[5], t[1])
    CNOT | (t[2], t[3])
    Toffoli_gate(eng, t[3], t[4], t[2])
    Toffoli_gate(eng, t[0], t[5], t[4])
    Toffoli_gate(eng, t[2], t[4], t[3])
    Toffoli_gate(eng, t[0], t[5], t[4])
    CNOT | (t[4], t[5])
    CNOT4(eng, u[2], u[4], u[5], u[6], u[3])
    CNOT3(eng, u[0], u[3], u[7], u[4])
    CNOT | (u[6], u[2])
    CNOT | (u[7], u[5])
    CNOT5(eng, u[0], u[1], u[3], u[4], u[5], u[6])

    s = AES_Sbox2(eng, t, u, s)

    return s

def AES_Sbox2(eng, t, u, s):
    CNOT3(eng, u[0], u[4], u[2], u[1])
    CNOT | (t[1], t[3])
    Toffoli_gate(eng, t[3], u[1], s[5])
    CNOT | (s[5], s[6])
    CNOT3(eng, u[0], u[4], u[2], u[1])
    CNOT | (t[1], t[3])
    Toffoli_gate(eng, t[2], u[2], s[2])
    CNOT | (s[2], s[5])
    CNOT | (s[6], s[2])
    Toffoli_gate(eng, t[1], u[5], s[4])
    CNOT | (s[4], s[1])
    CNOT | (s[4], s[3])
    CNOT | (u[7], u[5])
    CNOT | (t[5], t[1])
    Toffoli_gate(eng, t[1], u[5], s[7])
    CNOT | (s[7], s[1])
    CNOT | (s[7], s[3])
    CNOT | (s[7], s[4])
    CNOT | (u[7], u[5])
    CNOT | (t[5], t[1])
    Toffoli_gate(eng, t[5], u[7], s[7])

    CNOT | (s[7], s[2])
    CNOT | (s[7], s[5])
    CNOT | (s[7], s[6])
    CNOT5(eng, u[3], u[0], u[4], u[5], u[6], u[1])

    Toffoli_gate(eng, t[2], u[1], s[7])
    CNOT | (s[7], s[2])
    CNOT | (s[7], s[4])
    CNOT | (s[7], s[5])
    CNOT5(eng, u[3], u[0], u[4], u[5], u[6], u[1])

    CNOT | (u[3], u[2])
    CNOT | (t[2], t[3])
    Toffoli_gate(eng, t[3], u[2], s[7])
    CNOT | (s[7], s[2])
    CNOT | (s[7], s[5])
    CNOT | (u[3], u[2])
    CNOT | (t[2], t[3])
    Toffoli_gate(eng, t[3], u[3], s[7])
    CNOT | (s[7], s[6])
    CNOT2(eng, u[3], u[2], u[6])
    CNOT | (t[3], t[2])
    Toffoli_gate(eng, t[2], u[6], s[0])
    CNOT | (s[0], s[4])
    CNOT | (s[0], s[6])
    CNOT | (s[0], s[7])

    CNOT2(eng, u[3], u[2], u[6])
    CNOT | (t[3], t[2])
    CNOT4(eng, u[0], u[4], u[2], u[5], u[1])
    Toffoli_gate(eng, t[3], u[1], s[0])
    CNOT | (s[0], s[1])
    CNOT | (s[0], s[2])
    CNOT | (s[0], s[3])
    CNOT | (s[0], s[4])
    CNOT | (s[0], s[5])
    CNOT | (s[0], s[6])
    CNOT4(eng, u[0], u[4], u[2], u[5], u[1])
    CNOT6(eng, u[7], u[0], u[4], u[5], u[6], u[1], u[3])

    CNOT | (t[2], t[5])
    Toffoli_gate(eng, t[5], u[3], s[0])
    CNOT | (s[0], s[2])
    CNOT | (s[0], s[5])
    CNOT | (s[0], s[6])
    CNOT6(eng, u[7], u[0], u[4], u[5], u[6], u[1], u[3])

    CNOT | (t[2], t[5])
    CNOT4(eng, u[7], u[2], u[5], u[6], u[3])
    CNOT3(eng, t[2], t[1], t[3], t[5])
    Toffoli_gate(eng, t[5], u[3], s[0])
    CNOT | (s[0], s[3])
    CNOT | (s[0], s[4])
    CNOT | (s[0], s[5])
    CNOT | (s[0], s[6])
    CNOT4(eng, u[7], u[2], u[5], u[6], u[3])
    CNOT3(eng, t[2], t[1], t[3], t[5])
    CNOT2(eng, u[3], u[4], u[2])
    CNOT | (t[1], t[5])
    Toffoli_gate(eng, t[5], u[2], s[0])
    CNOT | (s[0], s[5])

    CNOT2(eng, u[3], u[4], u[2])
    CNOT | (t[1], t[5])
    CNOT3(eng, u[3], u[4], u[2], u[1])
    Toffoli_gate(eng, t[1], u[1], s[0])
    CNOT | (s[0], s[2])
    CNOT | (s[0], s[6])
    CNOT | (s[0], s[7])
    CNOT3(eng, u[3], u[4], u[2], u[1])
    CNOT | (u[2], u[1])
    CNOT | (t[2], t[5])
    Toffoli_gate(eng, t[5], u[1], s[0])
    CNOT | (s[0], s[2])
    CNOT | (u[2], u[1])
    CNOT | (t[2], t[5])
    CNOT3(eng, t[2], t[1], t[3], t[5])
    Toffoli_gate(eng, t[5], u[4], s[0])
    CNOT | (s[0], s[1])
    CNOT | (s[0], s[3])
    CNOT | (s[0], s[4])
    CNOT | (s[0], s[5])
    CNOT | (s[0], s[6])
    CNOT | (s[0], s[7])

    CNOT3(eng, t[2], t[1], t[3], t[5])
    CNOT2(eng, u[4], u[2], u[1])
    CNOT | (t[1], t[3])
    Toffoli_gate(eng, t[3], u[1], s[2])
    CNOT2(eng, u[4], u[2], u[1])
    CNOT | (t[1], t[3])
    Toffoli_gate(eng, t[5], u[1], s[5])

    X | s[1]
    X | s[2]
    X | s[6]
    X | s[7]

    new_s = []
    for i in range(8):
        new_s.append(s[7-i])

    return new_s


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