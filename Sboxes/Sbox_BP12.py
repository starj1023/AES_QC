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

    s = Sbox_bp12(eng, a, y, t, z, s)

    if (resource_check != 1):
        print('Sbox: ')
        All(Measure) | s
        for i in range(8):
            print(int(s[n - 1 - i]), end=' ')


def Sbox_bp12(eng, u, t, m, l, s):

    with Compute(eng):
        CNOT2(eng, u[7], u[4], t[0]); CNOT2(eng, u[7], u[2], t[1])
        CNOT2(eng, u[7], u[1], t[2]); CNOT2(eng, u[4], u[2], t[3])
        CNOT2(eng, u[3], u[1], t[4]); CNOT2(eng, t[0], t[4], t[5])
        CNOT2(eng, u[6], u[5], t[6]); CNOT2(eng, u[0], t[5], t[7])
        CNOT2(eng, u[0], t[6], t[8]); CNOT2(eng, t[5], t[6], t[9])
        CNOT2(eng, u[6], u[2], t[10]); CNOT2(eng, u[5], u[2], t[11])
        CNOT2(eng, t[2], t[3], t[12]); CNOT2(eng, t[5], t[10], t[13])
        CNOT2(eng, t[4], t[10], t[14]); CNOT2(eng, t[4], t[11], t[15])
        CNOT2(eng, t[8], t[15], t[16]); CNOT2(eng, u[4], u[0], t[17])
        CNOT2(eng, t[6], t[17], t[18]); CNOT2(eng, t[0], t[18], t[19])
        CNOT2(eng, u[1], u[0], t[20]); CNOT2(eng, t[6], t[20], t[21])
        CNOT2(eng, t[1], t[21], t[22]); CNOT2(eng, t[1], t[9], t[23])
        CNOT2(eng, t[19], t[16], t[24]); CNOT2(eng, t[2], t[15], t[25])
        CNOT2(eng, t[0], t[11], t[26])

        Toffoli_gate(eng, t[12], t[5], m[0] )
        Toffoli_gate(eng, t[22], t[7], m[1] )
        CNOT2(eng, t[13], m[0], m[2])
        Toffoli_gate(eng, t[18], u[0], m[3] )
        CNOT2(eng, m[3], m[0], m[4])
        Toffoli_gate(eng, t[2], t[15], m[5] )
        Toffoli_gate(eng, t[21], t[8], m[6] )
        CNOT2(eng, t[25], m[5], m[7])
        Toffoli_gate(eng, t[19], t[16], m[8] )
        CNOT2(eng, m[8], m[5], m[9])
        Toffoli_gate(eng, t[0], t[14], m[10] )
        Toffoli_gate(eng, t[3], t[26], m[11] )
        CNOT2(eng, m[11], m[10], m[12])
        Toffoli_gate(eng, t[1], t[9], m[13] )
        CNOT2(eng, m[13], m[10], m[14]); CNOT2(eng, m[2], m[1], m[15])
        CNOT2(eng, m[4], t[23], m[16]); CNOT2(eng, m[7], m[6], m[17])
        CNOT2(eng, m[9], m[14], m[18]); CNOT2(eng, m[15], m[12], m[19])
        CNOT2(eng, m[16], m[14], m[20]); CNOT2(eng, m[17], m[12], m[21])
        CNOT2(eng, m[18], t[24], m[22]); CNOT2(eng, m[21], m[22], m[23])
        Toffoli_gate(eng, m[21], m[19], m[24] )
        CNOT2(eng, m[20], m[24], m[25]); CNOT2(eng, m[19], m[20], m[26])
        CNOT2(eng, m[22], m[24], m[27])
        Toffoli_gate(eng, m[27], m[26], m[28] )
        Toffoli_gate(eng, m[25], m[23], m[29] )
        Toffoli_gate(eng, m[19], m[22], m[30] )
        Toffoli_gate(eng, m[26], m[30], m[31] )
        CNOT2(eng, m[26], m[24], m[32])
        Toffoli_gate(eng, m[20], m[21], m[33] )
        Toffoli_gate(eng, m[23], m[33], m[34] )
        CNOT2(eng, m[23], m[24], m[35]); CNOT2(eng, m[20], m[28], m[36])
        CNOT2(eng, m[31], m[32], m[37]); CNOT2(eng, m[22], m[29], m[38])
        CNOT2(eng, m[34], m[35], m[39]); CNOT2(eng, m[37], m[39], m[40])
        CNOT2(eng, m[36], m[38], m[41]); CNOT2(eng, m[36], m[37], m[42])
        CNOT2(eng, m[38], m[39], m[43]); CNOT2(eng, m[41], m[40], m[44])
        Toffoli_gate(eng, m[43], t[5], m[45] )
        Toffoli_gate(eng, m[39], t[7], m[46] )
        Toffoli_gate(eng, m[38], u[0], m[47] )
        Toffoli_gate(eng, m[42], t[15], m[48] )
        Toffoli_gate(eng, m[37], t[8], m[49] )
        Toffoli_gate(eng, m[36], t[16], m[50] )
        Toffoli_gate(eng, m[41], t[14], m[51] )
        Toffoli_gate(eng, m[44], t[26], m[52] )
        Toffoli_gate(eng, m[40], t[9], m[53] )
        Toffoli_gate(eng, m[43], t[12], m[54] )
        Toffoli_gate(eng, m[39], t[22], m[55] )
        Toffoli_gate(eng, m[38], t[18], m[56] )
        Toffoli_gate(eng, m[42], t[2], m[57] )
        Toffoli_gate(eng, m[37], t[21], m[58] )
        Toffoli_gate(eng, m[36], t[19], m[59] )
        Toffoli_gate(eng, m[41], t[0], m[60] )
        Toffoli_gate(eng, m[44], t[3], m[61] )
        Toffoli_gate(eng, m[40], t[1], m[62] )

        CNOT2(eng, m[60], m[61], l[0]); CNOT2(eng, m[49], m[55], l[1])
        CNOT2(eng, m[45], m[47], l[2]); CNOT2(eng, m[46], m[54], l[3])
        CNOT2(eng, m[53], m[57], l[4]); CNOT2(eng, m[48], m[60], l[5])
        CNOT2(eng, m[61], l[5], l[6]); CNOT2(eng, m[45], l[3], l[7])
        CNOT2(eng, m[50], m[58], l[8]); CNOT2(eng, m[51], m[52], l[9])
        CNOT2(eng, m[52], l[4], l[10]); CNOT2(eng, m[59], l[2], l[11])
        CNOT2(eng, m[47], m[50], l[12]); CNOT2(eng, m[49], l[0], l[13])
        CNOT2(eng, m[51], m[60], l[14]); CNOT2(eng, m[54], l[1], l[15])
        CNOT2(eng, m[55], l[0], l[16]); CNOT2(eng, m[56], l[1], l[17])
        CNOT2(eng, m[57], l[8], l[18]); CNOT2(eng, m[62], l[4], l[19])
        CNOT2(eng, l[0], l[1], l[20]); CNOT2(eng, l[1], l[7], l[21])
        CNOT2(eng, l[3], l[12], l[22]); CNOT2(eng, l[18], l[2], l[23])
        CNOT2(eng, l[15], l[9], l[24]); CNOT2(eng, l[6], l[10], l[25])
        CNOT2(eng, l[7], l[9], l[26]); CNOT2(eng, l[8], l[10], l[27])
        CNOT2(eng, l[11], l[14], l[28]); CNOT2(eng, l[11], l[17], l[29])

    CNOT2(eng, l[6], l[24], s[7])
    CNOT2(eng, l[16], l[26], s[6])
    CNOT2(eng, l[19], l[28], s[5])
    X | s[6]
    X | s[5]

    CNOT2(eng, l[6], l[21], s[4])
    CNOT2(eng, l[20], l[22], s[3])
    CNOT2(eng, l[25], l[29], s[2])

    CNOT2(eng, l[13], l[27], s[1])
    CNOT2(eng, l[6], l[23], s[0])
    X | s[1]
    X | s[0]

    # reverse

    #Uncompute(eng)

    return s

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