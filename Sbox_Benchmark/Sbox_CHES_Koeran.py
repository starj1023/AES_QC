from projectq.ops import H, CNOT, Measure, Toffoli, X, All, Swap, Z, T, Tdagger, S, Tdag
from projectq import MainEngine
from projectq.backends import ResourceCounter, ClassicalSimulator, IBMBackend
from projectq.meta import Loop, Compute, Uncompute, Control

def Sbox_test(eng):

    n = 8
    u_in = eng.allocate_qureg(8) # input

    if(resource_check != 1):
        Round_constant_XOR(eng, u_in, 0x00, 8)
        print('Input')
        print_state(eng, u_in, 2)

    out = Sbox(eng, u_in)

    if (resource_check != 1):
        print('Output')
        print_state(eng, out, 2)

def CNOT2(eng, a, b, c):
    CNOT | (b, a)
    CNOT | (c, a)

def CNOT2_X(eng, a, b, c):
    CNOT | (b, a)
    CNOT | (c, a)
    X | a

def Sbox(eng, x):

    r = eng.allocate_qureg(100)
    t = eng.allocate_qureg(100)
    g = eng.allocate_qureg(100)

    # Depth 0
    Copy(eng, r[5], x[0])
    Copy(eng, r[37], x[0])

    # Depth 1
    CNOT2(eng, t[0], x[1], x[7])
    CNOT2(eng, t[1], x[4], x[7])
    CNOT2(eng, t[2], x[2], x[4])
    CNOT2(eng, t[4], x[2], x[7])
    CNOT2(eng, t[5], x[5], x[6])
    CNOT2(eng, t[10], x[1], x[3])
    CNOT2(eng, t[14], x[2], x[5])
    CNOT2(eng, t[18], x[2], x[6])
    Copy(eng, r[6], t[0])
    Copy(eng, r[12], t[1])
    Copy(eng, r[14], t[2])
    Copy(eng, r[16], t[4])
    Copy(eng, r[57], t[0])
    Copy(eng, r[63], t[1])
    Copy(eng, r[65], t[2])
    Copy(eng, r[67], t[4])

    # Depth 2
    CNOT2(eng, t[3], t[0], t[2])
    CNOT2(eng, t[6], x[0], t[5])
    CNOT2(eng, t[11], t[1], t[10])
    CNOT2(eng, t[15], t[10], t[14])
    CNOT2(eng, t[17], t[1], t[14])
    CNOT2(eng, t[19], t[10], t[18])
    CNOT2(eng, t[25], x[1], t[4])
    Copy(eng, r[0], t[3])
    Copy(eng, r[1], t[11])
    Copy(eng, r[7], t[15])
    Copy(eng, r[9], t[6])
    Copy(eng, r[13], t[19])
    Copy(eng, r[15], t[17])
    Copy(eng, r[33], t[11])
    Copy(eng, r[39], t[15])
    Copy(eng, r[41], t[6])
    Copy(eng, r[45], t[19])
    Copy(eng, r[47], t[17])
    Copy(eng, r[51], t[3])

    # Depth 3 (correct)
    Toffoli_gate(eng, r[0], r[1], g[0])
    Toffoli_gate(eng, r[6], r[7], g[3])
    Toffoli_gate(eng, r[12], r[13], g[6])
    Toffoli_gate(eng, r[14], r[15], g[7])
    CNOT2(eng, t[7], x[4], t[6])
    CNOT2(eng, t[8], x[1], t[6])
    CNOT2(eng, t[9], x[7], t[6])
    CNOT2(eng, t[12], x[0], t[11])
    CNOT2(eng, t[13], t[5], t[11])
    CNOT2(eng, t[16], t[6], t[15])
    CNOT2(eng, t[26], t[6], t[25])
    Copy(eng, r[2], t[26])
    Copy(eng, r[3], t[12])
    Copy(eng, r[4], t[7])
    Copy(eng, r[8], t[8])
    Copy(eng, r[10], t[9])
    Copy(eng, r[11], t[16])
    Copy(eng, r[17], t[13])
    Copy(eng, r[35], t[12])
    Copy(eng, r[43], t[16])
    Copy(eng, r[49], t[13])
    Copy(eng, r[53], t[26])
    Copy(eng, r[55], t[7])
    Copy(eng, r[59], t[8])
    Copy(eng, r[61], t[9])

    # Depth 4 (Done)
    Toffoli_gate(eng, r[2], r[3], g[1])
    Toffoli_gate(eng, r[4], r[5], g[2])
    Toffoli_gate(eng, r[8], r[9], g[4])
    Toffoli_gate(eng, r[10], r[11], g[5])
    Toffoli_gate(eng, r[16], r[17], g[8])
    CNOT2(eng, t[22], t[15], g[6])
    CNOT2(eng, t[27], t[14], g[7])
    CNOT2(eng, t[29], t[13], g[6])
    CNOT2(eng, t[36], t[0], g[3])
    CNOT2(eng, t[48], x[7], g[3])

    # Depth 5 (D)
    CNOT2(eng, t[20], g[4], g[7])
    CNOT2(eng, t[21], g[8], g[5])
    CNOT2(eng, t[28], g[1], t[27])
    CNOT2(eng, t[30], g[0], t[29])
    CNOT2(eng, t[32], t[4], g[8])
    CNOT2(eng, t[37], t[22], t[36])
    CNOT2(eng, t[49], t[22], t[48])

    # Depth 6 (D)
    CNOT2(eng, t[23], x[1], t[21])
    CNOT2(eng, t[31], t[28], t[30])
    CNOT2(eng, t[33], g[2], t[32])
    CNOT2(eng, t[38], t[20], t[37])
    CNOT2(eng, t[50], t[21], t[49])
    Copy(eng, r[18], t[38])
    Copy(eng, r[19], t[31])
    Copy(eng, r[24], t[31])
    Copy(eng, r[25], t[50])
    Copy(eng, r[29], t[38])

    # Depth 7 (D)
    Toffoli_gate(eng, r[18], r[19], g[9])
    Toffoli_gate(eng, r[24], r[25], g[12])
    CNOT2(eng, t[24], t[20], t[23])
    CNOT2(eng, t[34], t[28], t[33])
    CNOT2(eng, t[35], t[30], t[33])
    CNOT2(eng, t[50], t[23], t[37])
    CNOT2(eng, t[60], t[31], t[38])
    Copy(eng, r[21], t[34])
    Copy(eng, r[23], t[24])
    Copy(eng, r[26], t[34])
    Copy(eng, r[27], g[12])
    Copy(eng, r[28], t[35])
    Copy(eng, r[30], t[24])

    # Depth 8 (D)
    Toffoli_gate(eng, r[26], r[27], g[13])
    Toffoli_gate(eng, r[28], r[29], g[14])
    CNOT2(eng, t[39], t[35], g[9])
    CNOT2(eng, t[41], g[9], t[50])
    CNOT2(eng, t[45], t[24], g[9])
    CNOT2(eng, t[53], t[24], t[34])
    CNOT2(eng, t[56], t[31], g[9])
    Copy(eng, r[20], t[41])
    Copy(eng, r[22], t[39])
    Copy(eng, r[31], g[14])

    # Depth 9 (D)
    Toffoli_gate(eng, r[20], r[21], g[10])
    Toffoli_gate(eng, r[22], r[23], g[11])
    Toffoli_gate(eng, r[30], r[31], g[15])
    CNOT2(eng, t[51], t[39], g[13])
    CNOT2(eng, t[54], g[13], t[53])
    CNOT2(eng, t[57], g[13], t[56])
    CNOT2(eng, t[61], g[13], t[60])

    # Depth 10 (D)
    CNOT2(eng, t[42], g[11], t[50])
    CNOT2(eng, t[43], t[35], g[10])
    CNOT2(eng, t[46], g[15], t[45])
    CNOT2(eng, t[52], t[31], t[51])
    CNOT2(eng, t[55], g[15], t[54])
    CNOT2(eng, t[58], g[10], t[57])
    CNOT2(eng, t[59], g[15], g[11])
    CNOT2(eng, t[62], g[10], t[61])
    Copy(eng, r[34], t[46])
    Copy(eng, r[36], t[42])
    Copy(eng, r[38], t[58])
    Copy(eng, r[40], t[52])
    Copy(eng, r[42], t[43])
    Copy(eng, r[48], t[55])
    Copy(eng, r[52], t[46])
    Copy(eng, r[54], t[42])
    Copy(eng, r[56], t[58])
    Copy(eng, r[58], t[52])
    Copy(eng, r[60], t[43])
    Copy(eng, r[66], t[55])

    # Depth 11 (D)
    Toffoli_gate(eng, r[34], r[35], g[17])
    Toffoli_gate(eng, r[36], r[37], g[18])
    Toffoli_gate(eng, r[38], r[39], g[19])
    Toffoli_gate(eng, r[40], r[41], g[20])
    Toffoli_gate(eng, r[42], r[43], g[21])
    Toffoli_gate(eng, r[48], r[49], g[24])
    Toffoli_gate(eng, r[52], r[53], g[26])
    Toffoli_gate(eng, r[54], r[55], g[27])
    Toffoli_gate(eng, r[56], r[57], g[28])
    Toffoli_gate(eng, r[58], r[59], g[29])
    Toffoli_gate(eng, r[60], r[61], g[30])
    Toffoli_gate(eng, r[66], r[67], g[33])
    CNOT2(eng, t[44], t[42], t[43])
    CNOT2(eng, t[47], t[42], t[46])
    CNOT2(eng, t[63], t[59], t[62])
    Copy(eng, r[32], t[47])
    Copy(eng, r[44], t[44])
    Copy(eng, r[46], t[63])
    Copy(eng, r[50], t[47])
    Copy(eng, r[62], t[44])
    Copy(eng, r[64], t[63])

    # Depth 12 (D)
    Toffoli_gate(eng, r[32], r[33], g[16])
    Toffoli_gate(eng, r[44], r[45], g[22])
    Toffoli_gate(eng, r[46], r[47], g[23])
    Toffoli_gate(eng, r[50], r[51], g[25])
    Toffoli_gate(eng, r[62], r[63], g[31])
    Toffoli_gate(eng, r[64], r[65], g[32])
    CNOT2(eng, t[69], g[20], g[19])
    CNOT2(eng, t[70], g[21], g[20])
    CNOT2(eng, t[72], g[29], g[28])
    CNOT2(eng, t[89], g[24], g[28])
    CNOT2(eng, t[90], g[18], g[30])
    CNOT2(eng, t[96], g[27], g[26])

    # Depth 13 ()
    CNOT2(eng, t[64], g[31], g[32])
    CNOT2(eng, t[65], g[26], g[25])
    CNOT2(eng, t[67], g[17], g[16])
    CNOT2(eng, t[68], g[22], g[23])
    CNOT2(eng, t[71], g[18], t[70])
    CNOT2(eng, t[82], g[24], g[23])
    CNOT2(eng, t[85], g[16], t[69])
    CNOT2(eng, t[88], g[22], g[31])
    CNOT2(eng, t[91], t[89], t[90])
    CNOT2(eng, t[97], g[23], t[96])

    # Depth 14 ()
    CNOT2(eng, t[66], t[64], t[65])
    CNOT2(eng, t[73], t[64], t[72])
    CNOT2(eng, t[74], t[68], t[69])
    CNOT2(eng, t[76], g[17], t[71])
    CNOT2(eng, t[78], t[67], t[69])
    CNOT2(eng, t[80], t[67], t[68])
    CNOT2(eng, t[83], t[70], t[82])
    CNOT2(eng, t[86], t[71], t[85])
    CNOT2(eng, t[92], g[16], t[91])
    CNOT2(eng, t[93], g[33], t[88])
    CNOT2(eng, t[95], t[85], t[91])
    CNOT2(eng, t[98], t[64], t[97])

    CNOT2(eng, t[75], t[66], t[74])
    CNOT2(eng, t[77], t[66], t[76])
    CNOT2(eng, t[79], t[66], t[78])
    CNOT2_X(eng, t[81], t[66], t[80])
    CNOT2_X(eng, t[84], t[73], t[83])
    CNOT2_X(eng, t[87], t[73], t[86])
    CNOT2_X(eng, t[94], t[92], t[93])
    CNOT2(eng, t[99], t[95], t[98])

    y = []
    y.append(t[87])
    y.append(t[84])
    y.append(t[99])
    y.append(t[77])
    y.append(t[79])
    y.append(t[94])
    y.append(t[81])
    y.append(t[75])

    return y

def Copy(eng, a, b):
    CNOT | (b, a)

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

# 44 -> 69

# 41 + 24

# 40 + 32

# 39 + 40 # AD = 5

