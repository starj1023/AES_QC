from projectq.ops import H, CNOT, Measure, Toffoli, X, All, Swap, Z, T, Tdagger, S, Tdag
from projectq import MainEngine
from projectq.backends import ResourceCounter, ClassicalSimulator, IBMBackend
from projectq.meta import Loop, Compute, Uncompute, Control

def Sbox_test(eng):

    n = 8
    u_in = eng.allocate_qureg(8) # input
    s = eng.allocate_qureg(8) # output

    # Ancilla qubits
    t = eng.allocate_qureg(100)
    m = eng.allocate_qureg(100)
    n = eng.allocate_qureg(100)
    w = eng.allocate_qureg(100)
    l = eng.allocate_qureg(100)

    if(resource_check != 1):
        Round_constant_XOR(eng, u_in, 0xfe, 8)
        print('Input')
        print_state(eng, u_in, 2)

    Sbox(eng, u_in, t, m, n, w, l, s)

    if (resource_check != 1):
        print('Output')
        print_state(eng, s, 2)

def CNOT2(eng, a, b, c):
    CNOT | (a, c)
    CNOT | (b, c)

def Sbox(eng, u_in, t, m, n, w, l, s):
    u = []
    for i in range(8):
        u.append(u_in[7 - i])
    with Compute(eng):
        CNOT | (u[1], t[6])
        CNOT | (u[7], t[7])
        CNOT | (u[3], t[0])
        CNOT | (u[0], t[1])
        CNOT | (u[5], t[1])
        CNOT | (u[3], t[3])
        CNOT | (u[5], t[3])
        CNOT | (u[4], t[4])
        CNOT | (u[6], t[4])
        CNOT | (u[0], t[2])
        CNOT | (u[6], t[2])
        CNOT | (u[0], t[0])
        CNOT | (t[4], t[5])
        CNOT | (t[0], t[5])
        CNOT | (u[2], t[6])
        CNOT | (t[5], t[7])
        CNOT | (u[7], t[8])
        CNOT | (t[6], t[8])

        CNOT | (u[1], t[13])
        CNOT | (u[5], t[13])
        CNOT | (u[2], t[15])
        CNOT | (u[5], t[15])
        CNOT | (u[2], t[26])
        CNOT | (u[5], t[26])

        CNOT | (t[2], t[12])
        CNOT | (t[3], t[12])
        CNOT | (t[4], t[14])
        CNOT | (t[4], t[15])
        CNOT | (t[8], t[16])
        CNOT | (t[15], t[16])
        CNOT | (u[3], t[18])
        CNOT | (u[7], t[18])

        CNOT | (t[6], t[18])
        CNOT | (u[1], t[14])
        CNOT | (u[5], t[14])
        CNOT | (t[0], t[19])
        CNOT | (t[18], t[19])
        CNOT | (t[5], t[13])
        CNOT | (u[6], t[21])
        CNOT | (u[7], t[21])
        CNOT | (t[6], t[21])
        CNOT | (t[5], t[9])
        CNOT | (t[6], t[9])
        CNOT | (t[1], t[22])
        CNOT | (t[21], t[22])
        CNOT | (t[0], t[26])

        Toffoli_gate(eng, t[12], t[5], m[0])
        Toffoli_gate(eng, t[22], t[7], m[19])
        Toffoli_gate(eng, t[18], u[7], m[20])
        CNOT | (m[0], m[20])
        Toffoli_gate(eng, t[2], t[15], m[5])
        Toffoli_gate(eng, t[21], t[8], m[21])
        Toffoli_gate(eng, t[19], t[16], m[22])
        CNOT | (m[5], m[22])
        CNOT | (m[5], m[21])
        Toffoli_gate(eng, t[0], t[14], m[10])
        Toffoli_gate(eng, t[3], t[26], m[12])
        CNOT | (m[10], m[12])
        Toffoli_gate(eng, t[1], t[9], m[13])
        CNOT | (t[1], m[20])
        CNOT | (t[19], m[22])
        CNOT | (t[2], m[21])
        CNOT | (t[15], m[21])
        CNOT2(eng, t[13], m[0], m[19])
        CNOT2(eng, m[13], m[10], m[22])
        CNOT | (t[9], m[20])
        CNOT | (t[16], m[22])
        CNOT2(eng, m[13], m[10], m[20])
        CNOT | (m[12], m[19])
        CNOT | (m[12], m[21])
        CNOT2(eng, m[21], m[22], m[23])
        CNOT | (u[7], m[32])
        CNOT | (t[0], m[33])
        CNOT | (t[0], m[34])
        CNOT | (t[1], m[35])
        CNOT | (t[3], m[36])
        CNOT | (t[9], m[37])
        CNOT | (t[14], m[38])
        CNOT | (t[14], m[39])
        CNOT2(eng, m[19], m[20], m[26])
        CNOT | (t[16], m[40])
        CNOT | (t[18], m[41])
        CNOT | (t[19], m[42])
        CNOT | (t[26], m[43])
        CNOT | (m[19], m[44])
        CNOT | (m[20], m[45])
        CNOT | (m[20], m[46])
        CNOT | (m[21], m[47])
        CNOT | (m[22], m[48])
        CNOT | (m[22], m[49])
        CNOT | (m[23], l[0])
        CNOT | (m[23], l[1])
        CNOT2(eng, m[20], m[22], n[14])
        CNOT | (m[23], l[2])
        CNOT | (l[0], l[3])
        CNOT | (l[1], l[4])
        CNOT | (m[23], l[5])
        CNOT | (l[0], l[6])
        CNOT | (l[1], l[7])
        CNOT | (l[2], l[8])
        CNOT | (l[3], l[9])
        CNOT | (l[4], l[10])
        CNOT | (m[26], l[11])
        CNOT | (m[26], l[12])
        CNOT | (m[26], l[13])
        CNOT | (l[11], l[14])
        CNOT | (l[12], l[15])
        CNOT | (m[26], l[16])
        CNOT | (l[11], l[17])
        CNOT | (l[12], l[18])
        CNOT | (l[13], l[19])
        CNOT | (l[14], l[20])
        CNOT | (l[15], l[21])
        CNOT | (n[14], l[22])

        Toffoli_gate(eng, m[21], m[19], m[24])
        CNOT2(eng, m[22], m[24], m[27])
        CNOT2(eng, m[20], m[24], m[25])
        Toffoli_gate(eng, m[44], m[22], m[28])
        CNOT2(eng, m[26], m[24], m[29])
        Toffoli_gate(eng, m[20], m[47], m[30])
        CNOT2(eng, m[23], m[24], m[31])
        Toffoli_gate(eng, m[23], t[5], n[0])  # 2
        CNOT2(eng, m[22], m[31], n[1])
        CNOT2(eng, m[25], m[30], n[2])
        Toffoli_gate(eng, l[0], t[7], n[3])  # 2
        Toffoli_gate(eng, l[1], u[7], n[5])  # 2
        Toffoli_gate(eng, m[48], m[32], n[6])  # 2
        CNOT2(eng, m[20], m[29], n[7])
        CNOT2(eng, m[27], m[28], n[8])
        Toffoli_gate(eng, m[26], t[15], n[9])  # 2
        Toffoli_gate(eng, l[11], t[8], n[10])  # 2
        Toffoli_gate(eng, m[45], t[16], n[12])  # 2
        Toffoli_gate(eng, l[12], m[40], n[13])  # 2
        Toffoli_gate(eng, l[13], t[14], n[15])  # 2
        Toffoli_gate(eng, l[2], m[38], n[16])  # 2
        Toffoli_gate(eng, n[14], m[39], w[8])  # 2

        CNOT2(eng, m[29], m[31], n[17])
        CNOT2(eng, n[14], n[17], n[18])
        CNOT2(eng, m[27], m[28], n[19])
        CNOT2(eng, m[25], m[30], n[20])
        Toffoli_gate(eng, l[14], t[26], n[21])  # 2
        Toffoli_gate(eng, l[3], m[43], n[22])  # 2
        Toffoli_gate(eng, l[15], t[9], n[23])  # 2
        Toffoli_gate(eng, l[4], m[37], n[24])  # 2
        Toffoli_gate(eng, l[5], t[12], n[25])  # 2
        Toffoli_gate(eng, l[6], t[22], n[26])  # 2
        Toffoli_gate(eng, l[7], t[18], n[28])  # 2
        Toffoli_gate(eng, m[49], m[41], n[29])  # 2
        Toffoli_gate(eng, l[16], t[2], n[30])  # 2
        Toffoli_gate(eng, l[17], t[21], n[31])  # 2
        Toffoli_gate(eng, m[46], t[19], n[33])  # 2
        Toffoli_gate(eng, l[18], m[42], n[34])  # 2
        Toffoli_gate(eng, l[19], t[0], n[35])  # 2
        Toffoli_gate(eng, l[8], m[33], n[36])  # 2
        Toffoli_gate(eng, l[22], m[34], w[25])  # 2
        Toffoli_gate(eng, l[20], t[3], n[37])  # 2
        Toffoli_gate(eng, l[9], m[36], n[38])  # 2
        Toffoli_gate(eng, l[21], t[1], n[39])  # 2
        Toffoli_gate(eng, l[10], m[35], n[40])  # 2

        CNOT | (n[14], l[22])
        CNOT | (l[15], l[21])
        CNOT | (l[14], l[20])
        CNOT | (l[13], l[19])
        CNOT | (l[12], l[18])
        CNOT | (l[11], l[17])
        CNOT | (m[26], l[16])
        CNOT | (l[12], l[15])
        CNOT | (l[11], l[14])
        CNOT | (m[26], l[13])
        CNOT | (m[26], l[12])
        CNOT | (m[26], l[11])
        CNOT | (l[4], l[10])
        CNOT | (l[3], l[9])
        CNOT | (l[2], l[8])
        CNOT | (l[1], l[7])
        CNOT | (l[0], l[6])
        CNOT | (m[23], l[5])
        CNOT | (l[1], l[4])
        CNOT | (l[0], l[3])
        CNOT | (m[23], l[0])
        CNOT | (m[22], m[49])
        CNOT | (m[22], m[48])
        CNOT | (m[21], m[47])
        CNOT | (m[20], m[46])
        CNOT | (m[20], m[45])
        CNOT | (m[23], l[1])
        CNOT | (m[19], m[44])
        CNOT | (t[26], m[43])
        CNOT | (t[19], m[42])
        CNOT | (m[23], l[2])
        CNOT | (t[18], m[41])
        CNOT | (t[16], m[40])
        CNOT | (t[14], m[39])
        CNOT | (t[14], m[38])
        CNOT | (t[9], m[37])
        CNOT | (t[3], m[36])
        CNOT | (t[1], m[35])
        CNOT | (t[0], m[34])
        CNOT | (t[0], m[33])
        CNOT | (u[7], m[32])


        CNOT | (m[25], l[0])
        CNOT | (m[25], l[1])
        CNOT | (m[25], l[2])
        CNOT | (m[27], l[3])
        CNOT | (m[27], l[4])
        CNOT | (m[27], l[5])
        CNOT | (m[28], l[6])
        CNOT | (m[28], l[7])
        CNOT | (m[28], l[8])
        CNOT | (m[29], l[9])
        CNOT | (m[30], l[10])
        CNOT | (m[30], l[11])
        CNOT | (m[30], l[12])
        CNOT | (m[31], l[13])
        CNOT | (n[1], l[14])
        CNOT | (n[2], l[15])
        CNOT | (n[7], l[16])
        CNOT | (n[8], l[17])
        CNOT | (n[17], l[18])
        CNOT | (n[18], l[19])
        CNOT | (n[19], l[20])
        CNOT | (n[20], l[21])

        Toffoli_gate(eng, n[2], n[0], m[32])  # 3
        Toffoli_gate(eng, n[1], t[5], w[1])  # 3
        CNOT | (w[1], m[32])
        Toffoli_gate(eng, m[31], t[7], m[33])  # 3
        Toffoli_gate(eng, n[3], m[30], w[2])  # 3
        CNOT | (w[2], m[33])
        Toffoli_gate(eng, n[5], m[25], m[34])  # 3
        CNOT | (n[6], m[34])
        Toffoli_gate(eng, n[7], t[15], m[35])  # 3
        Toffoli_gate(eng, n[8], n[9], w[5])  # 3
        CNOT | (w[5], m[35])
        Toffoli_gate(eng, m[29], t[8], m[36])  # 3
        Toffoli_gate(eng, m[28], n[10], w[6])  # 3
        CNOT | (w[6], m[36])
        Toffoli_gate(eng, m[27], n[13], m[37])  # 3
        CNOT | (n[12], m[37])
        Toffoli_gate(eng, n[15], l[3], m[38])  # 3
        Toffoli_gate(eng, n[16], l[0], w[10])  # 3
        CNOT | (w[8], m[38])
        CNOT | (w[10], m[38])
        Toffoli_gate(eng, n[18], t[26], m[39])  # 3
        Toffoli_gate(eng, n[19], n[21], w[12])  # 3
        Toffoli_gate(eng, n[20], n[22], w[13])  # 3
        CNOT | (w[12], m[39])
        CNOT | (w[13], m[39])
        Toffoli_gate(eng, l[6], n[23], m[40])  # 3
        Toffoli_gate(eng, n[17], t[9], w[15])  # 3
        Toffoli_gate(eng, l[10], n[24], w[16])  # 3
        CNOT | (w[15], m[40])
        CNOT | (w[16], m[40])
        Toffoli_gate(eng, l[15], n[25], m[41])  # 3
        Toffoli_gate(eng, l[14], t[12], w[18])  # 3
        CNOT | (w[18], m[41])
        Toffoli_gate(eng, l[13], t[22], m[42])  # 3
        Toffoli_gate(eng, n[26], l[11], w[19])  # 3
        CNOT | (w[19], m[42])
        Toffoli_gate(eng, n[28], l[1], m[43])  # 3
        CNOT | (n[29], m[43])
        Toffoli_gate(eng, l[16], t[2], m[44])  # 3
        Toffoli_gate(eng, l[17], n[30], w[22])  # 3
        CNOT | (w[22], m[44])
        Toffoli_gate(eng, l[9], t[21], m[45])  # 3
        Toffoli_gate(eng, l[7], n[31], w[23])  # 3
        CNOT | (w[23], m[45])
        Toffoli_gate(eng, l[4], n[34], m[46])  # 3
        CNOT | (n[33], m[46])
        Toffoli_gate(eng, n[35], l[5], m[47])  # 3
        Toffoli_gate(eng, n[36], l[2], w[27])  # 3
        CNOT | (w[25], m[47])
        CNOT | (w[27], m[47])
        Toffoli_gate(eng, l[19], t[3], m[48])  # 3
        Toffoli_gate(eng, l[20], n[37], w[29])  # 3
        Toffoli_gate(eng, l[21], n[38], w[30])  # 3
        CNOT | (w[29], m[48])
        CNOT | (w[30], m[48])
        Toffoli_gate(eng, l[8], n[39], m[49])  # 3
        Toffoli_gate(eng, l[18], t[1], w[32])  # 3
        Toffoli_gate(eng, l[12], n[40], w[33])  # 3

        CNOT | (w[32], m[49])
        CNOT | (w[33], m[49])
        CNOT | (m[25], l[0])
        CNOT | (m[25], l[1])
        CNOT | (m[25], l[2])
        CNOT | (m[27], l[3])
        CNOT | (m[27], l[4])
        CNOT | (m[27], l[5])
        CNOT | (m[28], l[6])
        CNOT | (m[28], l[7])
        CNOT | (m[28], l[8])
        CNOT | (m[29], l[9])
        CNOT | (m[30], l[10])
        CNOT | (m[30], l[11])
        CNOT | (m[30], l[12])
        CNOT | (m[31], l[13])
        CNOT | (n[1], l[14])
        CNOT | (n[2], l[15])
        CNOT | (n[7], l[16])
        CNOT | (n[8], l[17])
        CNOT | (n[17], l[18])
        CNOT | (n[18], l[19])
        CNOT | (n[19], l[20])
        CNOT | (n[20], l[21])

        CNOT2(eng, m[47], m[48], l[0])
        CNOT2(eng, m[36], m[42], l[1])
        CNOT2(eng, m[32], m[34], l[2])
        CNOT2(eng, m[33], m[41], l[3])
        CNOT2(eng, m[40], m[44], l[4])
        CNOT2(eng, m[35], m[47], l[5])
        CNOT2(eng, m[48], l[5], l[6])
        CNOT2(eng, m[32], l[3], l[7])
        CNOT2(eng, l[1], l[7], l[21])
        CNOT2(eng, m[37], m[45], l[8])
        CNOT2(eng, m[38], m[39], l[9])
        CNOT2(eng, m[39], l[4], l[10])
        CNOT2(eng, m[46], l[2], l[11])
        CNOT2(eng, m[34], m[37], l[12])
        CNOT2(eng, m[36], l[0], l[13])
        CNOT2(eng, m[38], m[47], l[14])
        CNOT2(eng, m[41], l[1], l[15])
        CNOT2(eng, m[42], l[0], l[16])
        CNOT2(eng, m[43], l[1], l[17])
        CNOT2(eng, m[44], l[8], l[18])
        CNOT2(eng, m[49], l[4], l[19])
        CNOT2(eng, l[0], l[1], l[20])
        CNOT2(eng, l[3], l[12], l[22])

    X | s[0]
    X | s[1]
    X | s[5]
    X | s[6]

    CNOT2(eng, l[15], l[9], s[7])
    CNOT2(eng, l[11], l[14], s[5])
    CNOT2(eng, l[7], l[9], s[6])
    CNOT2(eng, l[6], l[10], s[2])
    CNOT2(eng, l[11], l[17], s[2])
    CNOT2(eng, l[18], l[2], s[0])
    CNOT2(eng, l[8], l[10], s[1])
    CNOT2(eng, l[6], l[21], s[4])
    CNOT | (l[6], s[7])
    CNOT | (l[16], s[6])
    CNOT | (l[19], s[5])
    CNOT | (l[13], s[1])
    CNOT | (l[6], s[0])
    CNOT2(eng, l[20], l[22], s[3])

    return s

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

def print_state(eng, b, n):
    All(Measure) | b
    print('0x', end='')
    print_hex(eng, b, n)
    print('\n')

def print_input(eng, b, k):
    All(Measure) | b
    All(Measure) | k
    print('Plaintext : 0x', end='')
    print_hex(eng, b)
    print('\nKey : 0x', end='')
    print_hex(eng, k)
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

resource_check = 0
Resource = ClassicalSimulator()
eng = MainEngine(Resource)
Sbox_test(eng)
eng.flush()
print()

resource_check = 1
Resource = ResourceCounter()
eng = MainEngine(Resource)
Sbox_test(eng)
print(Resource)
eng.flush()