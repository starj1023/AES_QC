from projectq.ops import H, CNOT, Measure, Toffoli, X, All, Swap, Z, T, Tdagger, S, Tdag, Sdag
from projectq import MainEngine
from projectq.backends import ResourceCounter, ClassicalSimulator, IBMBackend
from projectq.meta import Loop, Compute, Uncompute, Control, Dagger

def Sbox(eng):

    n = 8
    a = eng.allocate_qureg(n) # input
    s = eng.allocate_qureg(n) # output

    # Ancilla qubits
    y = eng.allocate_qureg(27)  # 27 * 20
    t = eng.allocate_qureg(63)  # 63 * 20
    z = eng.allocate_qureg(30)  # 30 * 20


    if(resource_check != 1):
        Round_constant_XOR(eng, a, 0xfe, n)
        print('Input')
        print_state(eng, a, 2)

    s = Sbox_T4(eng, a, y, t, z, s)

    if (resource_check != 1):
        print('Output')
        print_state(eng, s, 2)


def Sbox_T4(eng, u_in, t, m, l, s):
    u = []
    for i in range(8):
        u.append(u_in[7 - i])

    with Compute(eng):
        CNOT | (u[5], t[12 - 1])
        CNOT | (u[1], t[7 - 1])
        CNOT | (u[7], t[8 - 1])
        CNOT | (u[3], t[1 - 1])
        CNOT | (u[0], t[2 - 1])
        CNOT | (u[5], t[2 - 1])
        CNOT | (u[3], t[4 - 1])
        CNOT | (u[5], t[4 - 1])
        CNOT | (u[4], t[5 - 1])
        CNOT | (u[6], t[5 - 1])
        CNOT | (u[0], t[3 - 1])
        CNOT | (u[6], t[3 - 1])
        CNOT | (u[0], t[1 - 1])
        CNOT | (u[5], t[11 - 1])
        CNOT | (u[2], t[12 - 1])
        CNOT | (t[5 - 1], t[6 - 1])
        CNOT | (t[1 - 1], t[6 - 1])
        CNOT | (u[2], t[7 - 1])
        CNOT | (t[6 - 1], t[8 - 1])
        CNOT | (u[7], t[9 - 1])
        CNOT | (t[7 - 1], t[9 - 1])
        CNOT | (u[1], t[11 - 1])

        CNOT | (t[12 - 1], t[16 - 1])
        CNOT | (t[3 - 1], t[13 - 1])
        CNOT | (t[4 - 1], t[13 - 1])
        CNOT | (t[5 - 1], t[15 - 1])
        CNOT | (t[11 - 1], t[15 - 1])
        CNOT | (t[5 - 1], t[16 - 1])

        CNOT | (u[3], t[18 - 1])
        CNOT | (u[7], t[18 - 1])
        CNOT | (t[7 - 1], t[19 - 1])
        CNOT | (t[18 - 1], t[19 - 1])
        CNOT | (t[1 - 1], t[20 - 1])
        CNOT | (t[9 - 1], t[17 - 1])
        CNOT | (t[6 - 1], t[14 - 1])

        CNOT | (t[11 - 1], t[14 - 1])
        CNOT | (u[6], t[21 - 1])
        CNOT | (u[7], t[21 - 1])
        CNOT | (t[7 - 1], t[22 - 1])
        CNOT | (t[21 - 1], t[22 - 1])
        CNOT | (t[6 - 1], t[10 - 1])
        CNOT | (t[19 - 1], t[20 - 1])
        CNOT | (t[7 - 1], t[10 - 1])
        CNOT | (t[22 - 1], t[23 - 1])
        CNOT | (t[2 - 1], t[23 - 1])
        CNOT | (t[2 - 1], t[24 - 1])
        CNOT | (t[16 - 1], t[17 - 1])
        CNOT | (t[20 - 1], t[25 - 1])

        CNOT | (t[3 - 1], t[26 - 1])
        CNOT | (t[10 - 1], t[24 - 1])
        CNOT | (t[16 - 1], t[26 - 1])
        CNOT | (t[1 - 1], t[27 - 1])
        CNOT | (t[12 - 1], t[27 - 1])
        CNOT | (t[17 - 1], t[25 - 1])
        CNOT | (t[24 - 1], m[17 - 1])

        Toffoli_gate(eng, t[13 - 1], t[6 - 1], m[1 - 1])
        Toffoli_gate(eng, t[23 - 1], t[8 - 1], m[2 - 1])
        Toffoli_gate(eng, t[19 - 1], u[7], m[4 - 1])
        Toffoli_gate(eng, t[3 - 1], t[16 - 1], m[6 - 1])
        Toffoli_gate(eng, t[22 - 1], t[9 - 1], m[7 - 1])
        Toffoli_gate(eng, t[20 - 1], t[17 - 1], m[9 - 1])
        Toffoli_gate(eng, t[1 - 1], t[15 - 1], m[11 - 1])
        Toffoli_gate(eng, t[4 - 1], t[27 - 1], m[12 - 1])
        Toffoli_gate(eng, t[2 - 1], t[10 - 1], m[14 - 1])

        CNOT | (m[4 - 1], m[5 - 1])
        CNOT | (m[1 - 1], m[3 - 1])
        CNOT | (m[1 - 1], m[5 - 1])
        CNOT | (t[26 - 1], m[8 - 1])
        CNOT | (m[6 - 1], m[8 - 1])
        CNOT | (m[8 - 1], m[18 - 1])
        CNOT | (m[12 - 1], m[13 - 1])
        CNOT | (m[11 - 1], m[13 - 1])
        CNOT | (m[13 - 1], m[20 - 1])
        CNOT | (t[14 - 1], m[3 - 1])
        CNOT | (m[11 - 1], m[15 - 1])

        CNOT | (m[3 - 1], m[16 - 1])
        CNOT | (m[5 - 1], m[17 - 1])

        CNOT | (m[7 - 1], m[18 - 1])  # 18 # 22 # 24
        CNOT | (m[9 - 1], m[10 - 1])
        CNOT | (m[6 - 1], m[10 - 1])

        CNOT | (m[10 - 1], m[19 - 1])
        CNOT | (m[14 - 1], m[15 - 1])

        CNOT | (m[2 - 1], m[16 - 1])

        CNOT | (m[17 - 1], m[21 - 1])

        CNOT | (m[15 - 1], m[21 - 1])
        CNOT | (m[15 - 1], m[19 - 1])

        CNOT | (t[25 - 1], m[23 - 1])
        CNOT | (m[19 - 1], m[23 - 1])
        CNOT | (m[16 - 1], m[20 - 1])
        CNOT | (m[18 - 1], m[22 - 1])
        CNOT | (m[13 - 1], m[22 - 1])

        CNOT | (m[22 - 1], l[0]);
        CNOT | (m[20 - 1], l[1])

        Toffoli_gate(eng, m[22 - 1], m[20 - 1], m[25 - 1])
        Toffoli_gate(eng, l[1], m[23 - 1], m[31 - 1])
        Toffoli_gate(eng, m[21 - 1], l[0], m[34 - 1])

        CNOT | (m[22 - 1], m[24 - 1])
        CNOT | (m[23 - 1], m[24 - 1])

        CNOT | (m[25 - 1], m[28 - 1])
        CNOT | (m[24 - 1], l[3])
        CNOT | (m[21 - 1], m[26 - 1])
        CNOT | (m[25 - 1], m[26 - 1])
        CNOT | (m[20 - 1], m[27 - 1])
        CNOT | (m[21 - 1], m[27 - 1])
        CNOT | (m[27 - 1], m[33 - 1])
        CNOT | (m[23 - 1], m[28 - 1])

        CNOT | (m[25 - 1], m[33 - 1])
        CNOT | (m[27 - 1], l[2])
        CNOT | (m[24 - 1], m[36 - 1])
        CNOT | (m[25 - 1], m[36 - 1])
        CNOT | (m[21 - 1], m[37 - 1])

        Toffoli_gate(eng, m[28 - 1], m[27 - 1], m[29 - 1])
        Toffoli_gate(eng, m[26 - 1], m[24 - 1], m[30 - 1])
        Toffoli_gate(eng, l[2], m[31 - 1], m[32 - 1])
        Toffoli_gate(eng, l[3], m[34 - 1], m[35 - 1])

        CNOT | (m[32 - 1], m[38 - 1])

        CNOT | (m[33 - 1], m[38 - 1])

        CNOT | (m[23 - 1], m[39 - 1])

        CNOT | (m[30 - 1], m[39 - 1])

        CNOT | (m[35 - 1], m[40 - 1])

        CNOT | (m[36 - 1], m[40 - 1])

        CNOT | (m[40 - 1], m[41 - 1])

        CNOT | (m[38 - 1], m[41 - 1])

        CNOT | (m[29 - 1], m[37 - 1])
        CNOT | (m[37 - 1], m[42 - 1])

        CNOT | (m[37 - 1], m[43 - 1])

        CNOT | (m[38 - 1], m[43 - 1])

        CNOT | (m[39 - 1], m[44 - 1])
        CNOT | (m[39 - 1], m[42 - 1])
        CNOT | (m[40 - 1], m[44 - 1])
        CNOT | (m[42 - 1], m[45 - 1])
        CNOT | (m[41 - 1], m[45 - 1])

        CNOT | (m[44 - 1], l[4]);
        CNOT | (m[40 - 1], l[5])
        CNOT | (m[39 - 1], l[6]);
        CNOT | (m[43 - 1], l[7])
        CNOT | (m[38 - 1], l[8]);
        CNOT | (m[37 - 1], l[9])
        CNOT | (m[42 - 1], l[10]);
        CNOT | (m[45 - 1], l[11])
        CNOT | (m[41 - 1], l[12])

        Toffoli_gate(eng, m[44 - 1], t[6 - 1], m[46 - 1])
        Toffoli_gate(eng, m[40 - 1], t[8 - 1], m[47 - 1])
        Toffoli_gate(eng, m[39 - 1], u[7], m[48 - 1])
        Toffoli_gate(eng, m[43 - 1], t[16 - 1], m[49 - 1])
        Toffoli_gate(eng, m[38 - 1], t[9 - 1], m[50 - 1])
        Toffoli_gate(eng, m[37 - 1], t[17 - 1], m[51 - 1])
        Toffoli_gate(eng, m[42 - 1], t[15 - 1], m[52 - 1])
        Toffoli_gate(eng, m[45 - 1], t[27 - 1], m[53 - 1])
        Toffoli_gate(eng, m[41 - 1], t[10 - 1], m[54 - 1])

        Toffoli_gate(eng, l[4], t[13 - 1], m[55 - 1])
        Toffoli_gate(eng, l[5], t[23 - 1], m[56 - 1])
        Toffoli_gate(eng, l[6], t[19 - 1], m[57 - 1])
        Toffoli_gate(eng, l[7], t[3 - 1], m[58 - 1])
        Toffoli_gate(eng, l[8], t[22 - 1], m[59 - 1])
        Toffoli_gate(eng, l[9], t[20 - 1], m[60 - 1])
        Toffoli_gate(eng, l[10], t[1 - 1], m[61 - 1])
        Toffoli_gate(eng, l[11], t[4 - 1], m[62 - 1])
        Toffoli_gate(eng, l[12], t[2 - 1], m[63 - 1])

        CNOT | (m[22 - 1], l[0]);
        CNOT | (m[20 - 1], l[1])
        CNOT | (m[27 - 1], l[2]);
        CNOT | (m[24 - 1], l[3])
        CNOT | (m[44 - 1], l[4]);
        CNOT | (m[40 - 1], l[5])
        CNOT | (m[39 - 1], l[6]);
        CNOT | (m[43 - 1], l[7])
        CNOT | (m[38 - 1], l[8]);
        CNOT | (m[37 - 1], l[9])
        CNOT | (m[42 - 1], l[10]);
        CNOT | (m[45 - 1], l[11])
        CNOT | (m[41 - 1], l[12])

        CNOT | (m[61 - 1], l[0])
        CNOT | (m[62 - 1], l[0])
        CNOT | (m[50 - 1], l[1])
        CNOT | (m[56 - 1], l[1])
        CNOT | (m[46 - 1], l[2])
        CNOT | (m[48 - 1], l[2])
        CNOT | (m[47 - 1], l[3])
        CNOT | (m[55 - 1], l[3])
        CNOT | (m[49 - 1], l[5])
        CNOT | (m[61 - 1], l[5])
        CNOT | (m[62 - 1], l[6])
        CNOT | (l[5], l[6])
        CNOT | (m[46 - 1], l[7])
        CNOT | (l[3], l[7])
        CNOT | (m[54 - 1], l[4])
        CNOT | (m[58 - 1], l[4])
        CNOT | (l[1], l[21])
        CNOT | (l[7], l[21])
        CNOT | (m[51 - 1], l[8])
        CNOT | (m[59 - 1], l[8])
        CNOT | (m[52 - 1], l[9])
        CNOT | (m[53 - 1], l[9])
        CNOT | (m[53 - 1], l[10])
        CNOT | (l[4], l[10])
        CNOT | (m[60 - 1], l[11])
        CNOT | (l[2], l[11])
        CNOT | (m[48 - 1], l[12])
        CNOT | (m[51 - 1], l[12])
        CNOT | (m[50 - 1], l[13])
        CNOT | (l[0], l[13])
        CNOT | (m[52 - 1], l[14])
        CNOT | (m[61 - 1], l[14])
        CNOT | (m[55 - 1], l[15])
        CNOT | (l[1], l[15])
        CNOT | (m[56 - 1], l[16])
        CNOT | (l[0], l[16])

        CNOT | (m[57 - 1], l[17])
        CNOT | (l[1], l[17])
        CNOT | (l[11], l[29])
        CNOT | (l[17], l[29])
        CNOT | (m[58 - 1], l[18])
        CNOT | (l[8], l[18])
        CNOT | (m[63 - 1], l[19])
        CNOT | (l[4], l[19])
        CNOT | (l[0], l[20])
        CNOT | (l[1], l[20])
        CNOT | (l[3], l[22])
        CNOT | (l[12], l[22])
        CNOT | (l[18], l[23])
        CNOT | (l[2], l[23])
        CNOT | (l[15], l[24])
        CNOT | (l[9], l[24])
        CNOT | (l[6], l[25])
        CNOT | (l[10], l[25])
        CNOT | (l[7], l[26])
        CNOT | (l[9], l[26])
        CNOT | (l[8], l[27])
        CNOT | (l[10], l[27])
        CNOT | (l[11], l[28])
        CNOT | (l[14], l[28])

    X | s[0]
    X | s[1]
    X | s[5]
    X | s[6]

    CNOT | (l[6], s[7])
    CNOT | (l[24], s[7])
    CNOT | (l[16], s[6])
    CNOT | (l[26], s[6])
    CNOT | (l[19], s[5])
    CNOT | (l[28], s[5])
    CNOT | (l[6], s[4])
    CNOT | (l[21], s[4])
    CNOT | (l[20], s[3])
    CNOT | (l[22], s[3])
    CNOT | (l[25], s[2])
    CNOT | (l[29], s[2])
    CNOT | (l[13], s[1])
    CNOT | (l[27], s[1])
    CNOT | (l[6], s[0])
    CNOT | (l[23], s[0])

    return s

def CNOT2(eng, a, b, c):
    CNOT | (a, c)
    CNOT | (b, c)

def check_ancilla(eng, ancilla, length):
    for i in range(length):
        Measure | (ancilla[i])

    for i in range(length):
        print(int(ancilla[i]), end = '')


def Round_constant_XOR(eng, k, rc, bit):
    for i in range(bit):
        if (rc >> i & 1):
            X | k[i]


def AND_gate(eng, a, b, c, ancilla):
    H | c
    CNOT | (b, ancilla)
    CNOT | (c, a)
    CNOT | (c, b)
    CNOT | (a, ancilla)

    Tdag | a
    Tdag | b
    T | c
    T | ancilla

    CNOT | (a, ancilla)
    CNOT | (c, b)
    CNOT | (c, a)
    CNOT | (b, ancilla)

    H | c
    S | c

def AND_gate_dag(eng, a, b, c, ancilla):
    H | c
    Measure | c
    #if(eng, c):
    X | c
    S | a
    S | b
    CNOT | (a, b)
    Sdag | b
    CNOT | (a, b)


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

def print_state(eng, b, n):
    All(Measure) | b
    print('0x', end='')
    print_hex(eng, b, n)
    print('\n')

def print_hex(eng, qubits, n):
    for i in reversed(range(n)):
        temp = 0
        temp = temp + int(qubits[4 * i + 3]) * 8
        temp = temp + int(qubits[4 * i + 2]) * 4
        temp = temp + int(qubits[4 * i + 1]) * 2
        temp = temp + int(qubits[4 * i])

        temp = hex(temp)
        y = temp.replace("0x", "")
        print(y, end='')

global resource_check
#
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