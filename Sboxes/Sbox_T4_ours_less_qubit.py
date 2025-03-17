from projectq.ops import H, CNOT, Measure, Toffoli, X, All, Swap, Z, T, Tdagger, S, Tdag
from projectq import MainEngine
from projectq.backends import ResourceCounter, ClassicalSimulator, IBMBackend
from projectq.meta import Loop, Compute, Uncompute, Control

def Sbox_test(eng):

    n = 8
    u_in = eng.allocate_qureg(8) # input
    s = eng.allocate_qureg(8) # output

    # Ancilla qubits
    q = eng.allocate_qureg(100)

    if(resource_check != 1):
        Round_constant_XOR(eng, u_in, 0x00, 8)
        print('Input')
        print_state(eng, u_in, 2)

    Sbox(eng, u_in, q, s)

    if (resource_check != 1):
        print('Output')
        print_state(eng, s, 2)

def CNOT2(eng, a, b, c):
    CNOT | (a, c)
    CNOT | (b, c)

def Sbox(eng, u, q, s):
    with Compute(eng):
        CNOT | (u[4], q[34])
        CNOT | (u[7], q[34])
        CNOT | (u[2], q[35])
        CNOT | (u[7], q[35])
        CNOT | (u[1], u[3])
        CNOT | (u[1], u[7])
        CNOT | (u[2], q[36])
        CNOT | (u[4], q[36])
        CNOT | (u[3], q[37])
        CNOT | (q[34], q[37])
        CNOT | (u[6], q[38])
        CNOT | (u[5], q[38])
        CNOT | (u[0], q[39])
        CNOT | (u[0], q[40])
        CNOT | (q[38], q[40])
        CNOT | (q[38], q[41])
        CNOT | (u[2], u[6])
        CNOT | (u[2], u[5])
        CNOT | (u[7], q[42])
        CNOT | (q[36], q[42])
        CNOT | (q[37], q[39])
        CNOT | (u[6], q[59])
        CNOT | (q[37], q[59])
        CNOT | (u[3], u[6])
        CNOT | (u[5], u[3])
        CNOT | (q[37], q[41])
        CNOT | (q[40], q[43])
        CNOT | (u[0], u[4])
        CNOT | (q[38], u[4])
        CNOT | (q[34], q[44])
        CNOT | (u[4], q[44])
        CNOT | (u[0], u[1])
        CNOT | (u[1], q[38])
        CNOT | (q[35], q[45])
        CNOT | (q[38], q[45])
        CNOT | (q[34], u[5])
        CNOT | (u[3], q[43])

        Toffoli_gate(eng, q[42], q[37], q[0])
        Toffoli_gate(eng, q[45], q[39], q[1])
        Toffoli_gate(eng, u[4], u[0], q[2])
        Toffoli_gate(eng, u[7], u[3], q[3])
        Toffoli_gate(eng, q[38], q[40], q[4])
        Toffoli_gate(eng, q[44], q[43], q[5])
        Toffoli_gate(eng, q[34], u[6], q[6])
        Toffoli_gate(eng, q[36], u[5], q[7])
        Toffoli_gate(eng, q[35], q[41], q[8])

        CNOT | (q[0], q[1])
        CNOT | (q[34], u[5])
        CNOT | (q[35], q[51])
        CNOT | (q[41], q[51])
        CNOT | (q[3], q[53])
        CNOT | (u[3], q[53])
        CNOT | (q[44], q[52])
        CNOT | (q[43], q[52])
        CNOT | (u[7], q[53])
        CNOT | (q[59], q[1])
        CNOT | (u[5], u[3])
        CNOT | (u[3], u[6])
        CNOT | (u[6], q[59])
        CNOT | (q[37], q[59])
        CNOT | (u[3], u[6])
        CNOT | (q[6], q[7])
        CNOT | (u[5], u[3])
        CNOT | (q[34], u[5])
        CNOT | (q[6], q[8])
        CNOT | (q[51], q[0])
        CNOT | (q[35], q[51])
        CNOT | (q[2], q[0])
        CNOT | (q[52], q[5])
        CNOT | (q[3], q[5])
        CNOT | (q[4], q[53])
        CNOT | (q[7], q[53])
        CNOT | (q[44], q[52])
        CNOT | (q[43], q[52])
        CNOT | (q[53], q[51])
        CNOT | (q[41], q[51])
        CNOT | (q[8], q[5])
        CNOT | (q[7], q[1])
        CNOT | (q[8], q[0])
        CNOT | (q[1], q[52])

        Toffoli_gate(eng, q[53], q[1], q[9])
        Toffoli_gate(eng, q[52], q[5], q[10])
        Toffoli_gate(eng, q[0], q[51], q[11])

        CNOT | (q[53], q[54])
        CNOT | (q[53], q[51])
        CNOT | (q[7], q[53])
        CNOT | (q[4], q[53])
        CNOT | (q[3], q[53])
        CNOT | (u[7], q[53])
        CNOT | (u[3], q[53])
        CNOT | (q[1], q[52])
        CNOT | (q[0], q[55])
        CNOT | (q[9], q[55])
        CNOT | (q[1], q[56])
        CNOT | (q[0], q[56])
        CNOT | (q[5], q[57])
        CNOT | (q[9], q[57])
        CNOT | (q[5], q[54])
        CNOT | (q[56], q[51])
        CNOT | (q[54], q[52])

        Toffoli_gate(eng, q[57], q[56], q[12])
        Toffoli_gate(eng, q[55], q[54], q[13])
        Toffoli_gate(eng, q[51], q[10], q[14])
        Toffoli_gate(eng, q[52], q[11], q[15])

        CNOT | (q[54], q[52])
        CNOT | (q[9], q[14])
        CNOT | (q[9], q[57])
        CNOT | (q[9], q[55])
        CNOT | (q[54], q[9])
        CNOT | (u[7], q[53])
        CNOT | (q[5], q[54])
        CNOT | (q[53], q[54])
        CNOT | (u[7], q[53])
        CNOT | (q[7], q[54])
        CNOT | (q[4], q[54])
        CNOT | (q[3], q[54])
        CNOT | (u[3], q[54])
        CNOT | (q[5], q[57])
        CNOT | (q[0], q[55])
        CNOT | (q[56], q[14])
        CNOT | (q[58], q[14])
        CNOT | (q[56], q[51])
        CNOT | (q[1], q[56])
        CNOT | (q[0], q[56])
        CNOT | (q[12], q[0])
        CNOT | (q[13], q[5])
        CNOT | (q[9], q[15])
        CNOT2(eng, q[14], q[15], q[46])
        CNOT2(eng, q[0], q[5], q[47])
        CNOT2(eng, q[0], q[14], q[48])
        CNOT | (q[15], q[52])
        CNOT | (q[15], q[49])
        CNOT | (q[5], q[49])
        CNOT | (q[49], q[51])
        CNOT2(eng, q[47], q[46], q[50])
        CNOT | (q[5], q[53])
        CNOT | (q[48], q[54])
        CNOT | (q[14], q[55])
        CNOT | (q[0], q[56])
        CNOT | (q[47], q[57])
        CNOT | (q[50], q[58])
        CNOT | (q[46], q[59])

        Toffoli_gate(eng, q[49], q[37], q[16])
        Toffoli_gate(eng, q[15], q[39], q[17])
        Toffoli_gate(eng, q[5], u[0], q[18])
        Toffoli_gate(eng, q[48], u[3], q[19])
        Toffoli_gate(eng, q[14], q[40], q[20])
        Toffoli_gate(eng, q[0], q[43], q[21])
        Toffoli_gate(eng, q[47], u[6], q[22])
        Toffoli_gate(eng, q[50], u[5], q[23])
        Toffoli_gate(eng, q[46], q[41], q[24])
        Toffoli_gate(eng, q[51], q[42], q[25])
        Toffoli_gate(eng, q[52], q[45], q[26])
        Toffoli_gate(eng, q[53], u[4], q[27])
        Toffoli_gate(eng, q[54], u[7], q[28])
        Toffoli_gate(eng, q[55], q[38], q[29])
        Toffoli_gate(eng, q[56], q[44], q[30])
        Toffoli_gate(eng, q[57], q[34], q[31])
        Toffoli_gate(eng, q[58], q[36], q[32])
        Toffoli_gate(eng, q[59], q[35], q[33])

    with Compute(eng):
        CNOT | (q[49], q[51])
        CNOT | (q[15], q[52])
        CNOT | (q[5], q[53])
        CNOT | (q[48], q[54])
        CNOT | (q[14], q[55])
        CNOT | (q[0], q[56])
        CNOT | (q[47], q[57])
        CNOT | (q[50], q[58])
        CNOT | (q[46], q[59])
        CNOT | (q[31], q[51])
        CNOT | (q[32], q[51])
        CNOT | (q[20], q[52])
        CNOT | (q[26], q[52])
        CNOT2(eng, q[16], q[18], q[53])
        CNOT | (q[25], q[17])
        CNOT | (q[28], q[24])
        CNOT | (q[31], q[19])
        CNOT | (q[32], q[19])
        CNOT | (q[17], q[16])
        CNOT | (q[21], q[29])
        CNOT | (q[22], q[54])
        CNOT | (q[23], q[54])
        CNOT | (q[24], q[23])
        CNOT | (q[53], q[30])
        CNOT | (q[18], q[21])
        CNOT | (q[19], q[55])
        CNOT | (q[23], q[55])
        CNOT | (q[51], q[20])
        CNOT | (q[31], q[22])
        CNOT | (q[52], q[25])
        CNOT | (q[51], q[26])
        CNOT | (q[52], q[27])
        CNOT | (q[29], q[28])
        CNOT | (q[24], q[33])
        CNOT | (q[52], q[51])
        CNOT | (q[17], q[21])
        CNOT | (q[28], q[53])
        CNOT | (q[54], q[25])
        CNOT | (q[16], q[54])
        CNOT | (q[16], q[52])
        CNOT | (q[29], q[23])
        CNOT | (q[30], q[22])
        CNOT | (q[30], q[27])

    X | s[6]
    X | s[5]
    X | s[1]
    X | s[0]

    CNOT | (q[19], s[4])
    CNOT | (q[53], s[0])
    CNOT | (q[25], s[7])
    CNOT | (q[19], s[7])
    CNOT | (q[26], s[6])
    CNOT | (q[54], s[6])
    CNOT | (q[33], s[5])
    CNOT | (q[22], s[5])
    CNOT | (q[19], s[0])
    CNOT | (q[52], s[4])
    CNOT | (q[51], s[3])
    CNOT | (q[21], s[3])
    CNOT | (q[55], s[2])
    CNOT | (q[27], s[2])
    CNOT | (q[20], s[1])
    CNOT | (q[23], s[1])

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