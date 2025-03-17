from projectq import MainEngine
from projectq.ops import H, CNOT, Measure, Toffoli, X, All, T, Tdagger, S, Tdag
from projectq.backends import CircuitDrawer, ResourceCounter, ClassicalSimulator
from projectq.meta import Loop, Compute, Uncompute, Control, Dagger


def AES(eng, resource_check):
    x0 = eng.allocate_qureg(32)
    x1 = eng.allocate_qureg(32)
    x2 = eng.allocate_qureg(32)
    x3 = eng.allocate_qureg(32)

    k = eng.allocate_qureg(128)

    if (resource_check != 1):
        Round_constant_XOR(eng, x3, 0, 32)
        Round_constant_XOR(eng, x2, 0, 32)
        Round_constant_XOR(eng, x1, 0, 32)
        Round_constant_XOR(eng, x0, 0, 32)

        Round_constant_XOR(eng, k, 0, 128)

    if (resource_check != 1):
        Round_constant_XOR(eng, x3, 0x12345678, 32)
        Round_constant_XOR(eng, x2, 0x12345678, 32)
        Round_constant_XOR(eng, x1, 0x12345678, 32)
        Round_constant_XOR(eng, x0, 0x12345678, 32)

        Round_constant_XOR(eng, k, 0x12345678123456781234567812345678, 128)

        print('Plaintext  \n')
        print_state(eng, x3, 8)
        print_state(eng, x2, 8)
        print_state(eng, x1, 8)
        print_state(eng, x0, 8)

        print('Key  \n')
        print_state(eng, k[96:128], 8)
        print_state(eng, k[64:96], 8)
        print_state(eng, k[32:64], 8)
        print_state(eng, k[0:32], 8)

    q = eng.allocate_qureg(1460)  # 60 * 20 (only 1200 qubits are practically used)

    AddRoundkey(eng, x0, x1, x2, x3, k)

    for i in range(10):

        print('Round', i+1)
        Keyshedule(eng, k, i, q, i, resource_check)

        s = eng.allocate_qureg(128)
        SBox_bp12_all(eng, x0, x1, x2, x3, q, s, i, resource_check)

        x0, x1, x2, x3 = Shiftrow(eng, x0, x1, x2, x3)

        if (i != 9):
            x0 = Mixcolumns(eng, x0)
            x1 = Mixcolumns(eng, x1)
            x2 = Mixcolumns(eng, x2)
            x3 = Mixcolumns(eng, x3)

        AddRoundkey(eng, x0, x1, x2, x3, k)

        if (resource_check != 1):
            print_state(eng, x3, 8)
            print_state(eng, x2, 8)
            print_state(eng, x1, 8)
            print_state(eng, x0, 8)

    if (resource_check != 1):
        print('\nCiphertext ')
        print_state(eng, x3, 8)
        print_state(eng, x2, 8)
        print_state(eng, x1, 8)
        print_state(eng, x0, 8)

def Keyshedule(eng, k, i, q, round, resource_check):
    Rcon = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]

    new_k0 = []
    for j in range(32):
        new_k0.append(k[(24 + j) % 32])

    for j in range(4):  # 22 68 18
        k[96 + 8 * j: 96 + 8 * (j + 1)] = Sbox(eng, new_k0[8 * j:8 * (j + 1)], q[1168 + 73 * j: 1168 + 73 * (j + 1)],
                                               k[96 + 8 * j: 96 + 8 * (j + 1)],
                                               1, round, resource_check)

    for j in range(8):
        if ((Rcon[i] >> j) & 1):
            X | k[120 + j]

    CNOT32(eng, k[96:128], k[64:96])
    CNOT32(eng, k[64:96], k[32:64])
    CNOT32(eng, k[32:64], k[0:32])

def SBox_bp12_all(eng, x0, x1, x2, x3, q, s, round, resource_check):
    for i in range(4):
        x0[8 * i:8 * (i + 1)] = Sbox(eng, x0[8 * i:8 * (i + 1)], q[73 * i:73 * (i + 1)], s[8 * i:8 * (i + 1)], 0, round,
                                     resource_check)
        x1[8 * i:8 * (i + 1)] = Sbox(eng, x1[8 * i:8 * (i + 1)], q[73 * (i + 4):73 * (i + 5)],
                                     s[8 * (i + 4):8 * (i + 5)], 0, round, resource_check)
        x2[8 * i:8 * (i + 1)] = Sbox(eng, x2[8 * i:8 * (i + 1)], q[73 * (i + 8):73 * (i + 9)],
                                     s[8 * (i + 8):8 * (i + 9)], 0, round, resource_check)
        x3[8 * i:8 * (i + 1)] = Sbox(eng, x3[8 * i:8 * (i + 1)], q[73 * (i + 12):73 * (i + 13)],
                                     s[8 * (i + 12):8 * (i + 13)], 0, round, resource_check)

def CNOT32(eng, a, b):
    for i in range(32):
        CNOT | (a[i], b[i])

def Shiftrow(eng, x0, x1, x2, x3):
    new_x0 = []
    new_x1 = []
    new_x2 = []
    new_x3 = []

    for i in range(8):
        new_x0.append(x1[i])
    for i in range(8):
        new_x0.append(x2[i + 8])
    for i in range(8):
        new_x0.append(x3[i + 16])
    for i in range(8):
        new_x0.append(x0[i + 24])

    for i in range(8):
        new_x1.append(x2[i])
    for i in range(8):
        new_x1.append(x3[i + 8])
    for i in range(8):
        new_x1.append(x0[i + 16])
    for i in range(8):
        new_x1.append(x1[i + 24])

    for i in range(8):
        new_x2.append(x3[i])
    for i in range(8):
        new_x2.append(x0[i + 8])
    for i in range(8):
        new_x2.append(x1[i + 16])
    for i in range(8):
        new_x2.append(x2[i + 24])

    for i in range(8):
        new_x3.append(x0[i])
    for i in range(8):
        new_x3.append(x1[i + 8])
    for i in range(8):
        new_x3.append(x2[i + 16])
    for i in range(8):
        new_x3.append(x3[i + 24])

    return new_x0, new_x1, new_x2, new_x3

def AddRoundkey(eng, x0, x1, x2, x3, k):
    CNOT32(eng, k[0:32], x0)
    CNOT32(eng, k[32:64], x1)
    CNOT32(eng, k[64:96], x2)
    CNOT32(eng, k[96:128], x3)

def reverse_CNOT(eng, a, b):
    CNOT | (b, a)

def Mixcolumns(eng, x_in):
    x = []
    for i in range(8):
        x.append(x_in[24 + i])
    for i in range(8):
        x.append(x_in[16 + i])
    for i in range(8):
        x.append(x_in[8 + i])
    for i in range(8):
        x.append(x_in[i])

    CNOT | (x[23], x[15])
    CNOT | (x[1], x[25])
    CNOT | (x[18], x[10])
    CNOT | (x[13], x[5])
    CNOT | (x[19], x[3])
    CNOT | (x[28], x[4])
    CNOT | (x[0], x[16])
    CNOT | (x[9], x[1])
    CNOT | (x[7], x[23])
    CNOT | (x[31], x[7])
    CNOT | (x[20], x[28])
    CNOT | (x[14], x[22])
    CNOT | (x[16], x[8])
    CNOT | (x[8], x[0])
    CNOT | (x[30], x[14])
    CNOT | (x[6], x[30])
    CNOT | (x[15], x[24])
    CNOT | (x[29], x[13])
    CNOT | (x[5], x[6])
    CNOT | (x[21], x[5])
    CNOT | (x[28], x[21])
    CNOT | (x[23], x[28])
    CNOT | (x[5], x[29])
    CNOT | (x[4], x[5])
    CNOT | (x[2], x[18])
    CNOT | (x[3], x[28])
    CNOT | (x[11], x[3])
    CNOT | (x[15], x[11])
    CNOT | (x[12], x[4])
    CNOT | (x[4], x[20])
    CNOT | (x[11], x[12])

    CNOT | (x[19], x[12])
    CNOT | (x[27], x[19])
    CNOT | (x[10], x[11])
    CNOT | (x[3], x[27])
    CNOT | (x[2], x[3])
    CNOT | (x[10], x[2])
    CNOT | (x[26], x[10])
    CNOT | (x[26], x[3])
    CNOT | (x[25], x[26])
    CNOT | (x[25], x[2])
    CNOT | (x[17], x[25])
    CNOT | (x[25], x[9])
    CNOT | (x[8], x[17])
    CNOT | (x[7], x[8])
    CNOT | (x[23], x[19])
    CNOT | (x[1], x[10])
    CNOT | (x[15], x[25])
    CNOT | (x[7], x[3])
    CNOT | (x[7], x[4])
    CNOT | (x[15], x[7])
    CNOT | (x[14], x[15])
    CNOT | (x[0], x[25])
    CNOT | (x[23], x[0])
    CNOT | (x[23], x[1])
    CNOT | (x[31], x[23])
    CNOT | (x[30], x[31])
    CNOT | (x[24], x[0])
    CNOT | (x[29], x[14])
    CNOT | (x[21], x[29])
    CNOT | (x[19], x[4])
    CNOT | (x[18], x[19])

    CNOT | (x[9], x[18])
    CNOT | (x[11], x[27])
    CNOT | (x[16], x[24])
    CNOT | (x[16], x[1])
    CNOT | (x[22], x[23])
    CNOT | (x[7], x[16])
    CNOT | (x[0], x[16])
    CNOT | (x[6], x[22])
    CNOT | (x[22], x[30])
    CNOT | (x[13], x[22])
    CNOT | (x[20], x[13])
    CNOT | (x[12], x[20])
    CNOT | (x[18], x[26])
    CNOT | (x[19], x[11])
    CNOT | (x[14], x[6])
    CNOT | (x[31], x[7])
    CNOT | (x[3], x[19])
    CNOT | (x[28], x[12])
    CNOT | (x[10], x[18])
    CNOT | (x[16], x[17])
    CNOT | (x[17], x[9])
    CNOT | (x[1], x[17])
    CNOT | (x[4], x[28])
    CNOT | (x[13], x[21])
    CNOT | (x[5], x[13])
    CNOT | (x[15], x[31])
    CNOT | (x[25], x[1])
    CNOT | (x[23], x[15])
    CNOT | (x[22], x[14])

    y = []
    y.append(x[0])
    y.append(x[1])
    y.append(x[10])
    y.append(x[11])

    y.append(x[12])
    y.append(x[21])
    y.append(x[30])
    y.append(x[31])

    y.append(x[24])
    y.append(x[25])
    y.append(x[26])
    y.append(x[27])

    y.append(x[20])
    y.append(x[13])
    y.append(x[14])
    y.append(x[23])

    y.append(x[16])
    y.append(x[9])
    y.append(x[18])
    y.append(x[19])

    y.append(x[4])
    y.append(x[29])
    y.append(x[6])
    y.append(x[15])

    y.append(x[8])
    y.append(x[17])
    y.append(x[2])
    y.append(x[3])

    y.append(x[28])
    y.append(x[5])
    y.append(x[22])
    y.append(x[7])

    out_x = []
    for i in range(8):
        out_x.append(y[24 + i])
    for i in range(8):
        out_x.append(y[16 + i])
    for i in range(8):
        out_x.append(y[8 + i])
    for i in range(8):
        out_x.append(y[0 + i])

    return out_x

def CNOT2(eng, a, b, c):
    CNOT | (a, c)
    CNOT | (b, c)

def Sbox(eng, u, q, s, flag, round, resource_check):
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

        Toffoli_gate(eng, q[42], q[37], q[0], resource_check)
        Toffoli_gate(eng, q[45], q[39], q[1], resource_check)
        Toffoli_gate(eng, u[4], u[0], q[2], resource_check)
        Toffoli_gate(eng, u[7], u[3], q[3], resource_check)
        Toffoli_gate(eng, q[38], q[40], q[4], resource_check)
        Toffoli_gate(eng, q[44], q[43], q[5], resource_check)
        Toffoli_gate(eng, q[34], u[6], q[6], resource_check)
        Toffoli_gate(eng, q[36], u[5], q[7], resource_check)
        Toffoli_gate(eng, q[35], q[41], q[8], resource_check)

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
        CNOT | (u[5], u[3]) #
        CNOT | (u[3], u[6]) #
        CNOT | (u[6], q[59])
        CNOT | (q[37], q[59])
        CNOT | (u[3], u[6]) #
        CNOT | (q[6], q[7])
        CNOT | (u[5], u[3]) #
        CNOT | (q[34], u[5]) # done
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

        Toffoli_gate(eng, q[53], q[1], q[9], resource_check)
        Toffoli_gate(eng, q[52], q[5], q[10], resource_check)
        Toffoli_gate(eng, q[0], q[51], q[11], resource_check)

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

        Toffoli_gate(eng, q[57], q[56], q[12], resource_check)
        Toffoli_gate(eng, q[55], q[54], q[13], resource_check)
        Toffoli_gate(eng, q[51], q[10], q[14], resource_check)
        Toffoli_gate(eng, q[52], q[11], q[15], resource_check)

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

        Toffoli_gate(eng, q[49], q[37], q[16], resource_check)
        Toffoli_gate(eng, q[15], q[39], q[17], resource_check)
        Toffoli_gate(eng, q[5], u[0], q[18], resource_check)
        Toffoli_gate(eng, q[48], u[3], q[19], resource_check)
        Toffoli_gate(eng, q[14], q[40], q[20], resource_check)
        Toffoli_gate(eng, q[0], q[43], q[21], resource_check)
        Toffoli_gate(eng, q[47], u[6], q[22], resource_check)
        Toffoli_gate(eng, q[50], u[5], q[23], resource_check)
        Toffoli_gate(eng, q[46], q[41], q[24], resource_check)
        Toffoli_gate(eng, q[51], q[42], q[25], resource_check)
        Toffoli_gate(eng, q[52], q[45], q[26], resource_check)
        Toffoli_gate(eng, q[53], u[4], q[27], resource_check)
        Toffoli_gate(eng, q[54], u[7], q[28], resource_check)
        Toffoli_gate(eng, q[55], q[38], q[29], resource_check)
        Toffoli_gate(eng, q[56], q[44], q[30], resource_check)
        Toffoli_gate(eng, q[57], q[34], q[31], resource_check)
        Toffoli_gate(eng, q[58], q[36], q[32], resource_check)
        Toffoli_gate(eng, q[59], q[35], q[33], resource_check)

    if (round == 9):
        if(flag == 1):
            with Dagger(eng):
                CNOT | (u[1], u[3])
                CNOT | (u[1], u[7])
                CNOT | (u[2], u[6])
                CNOT | (u[2], u[5])
                CNOT | (u[3], u[6])
                CNOT | (u[5], u[3])
                CNOT | (u[0], u[4])
                CNOT | (q[38], u[4])
                CNOT | (u[0], u[1])
                CNOT | (u[1], q[38])
                CNOT | (u[5], u[3])
                CNOT | (u[3], u[6])
                CNOT | (u[3], u[6])
                CNOT | (u[5], u[3])
                CNOT | (q[34], u[5])

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

    if (round != 9):
        Uncompute(eng)
        Uncompute(eng)

    return s

def Round_constant_XOR(eng, k, rc, bit):
    for i in range(bit):
        if (rc >> i & 1):
            X | k[i]

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

def Toffoli_gate(eng, a, b, c, resource_check):
    if (resource_check):
        Tdag | a
        Tdag | b
        H | c
        CNOT | (c, a)
        T | a
        CNOT | (b, c)
        CNOT | (b, a)
        T | c
        Tdag | a
        CNOT | (b, c)
        CNOT | (c, a)
        T | a
        Tdag | c
        CNOT | (b, a)
        H | c
    else:
        Toffoli | (a, b, c)


Simulate = ClassicalSimulator()
eng = MainEngine(Simulate)
AES(eng, 0)

print('Estimate cost...')
Resource = ResourceCounter()
eng = MainEngine(Resource)
AES(eng, 1)
print(Resource)
print('\n')
eng.flush()
