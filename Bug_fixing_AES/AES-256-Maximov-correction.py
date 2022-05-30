from projectq import MainEngine
from projectq.ops import H, CNOT, Measure, Toffoli, X, All, T, Tdagger, S, Tdag, Swap
from projectq.backends import CircuitDrawer, ResourceCounter, ClassicalSimulator
from projectq.meta import Loop, Compute, Uncompute, Control


def AES(eng, resource_check):

    x0 = eng.allocate_qureg(32)
    x1 = eng.allocate_qureg(32)
    x2 = eng.allocate_qureg(32)
    x3 = eng.allocate_qureg(32)

    k = eng.allocate_qureg(256)

    if(resource_check != 1):
        Round_constant_XOR(eng, x3, 0x12345678, 32)
        Round_constant_XOR(eng, x2, 0x12345678, 32)
        Round_constant_XOR(eng, x1, 0x12345678, 32)
        Round_constant_XOR(eng, x0, 0x12345678, 32)

        Round_constant_XOR(eng, k, 0x1234567812345678123456781234567812345678123456781234567812345678, 256)

        print('Plaintext  \n')
        print_state(eng, x3, 8)
        print_state(eng, x2, 8)
        print_state(eng, x1, 8)
        print_state(eng, x0, 8)

        print('Key  \n')
        print_state(eng, k[224:256], 8)
        print_state(eng, k[192:224], 8)
        print_state(eng, k[160:192], 8)
        print_state(eng, k[128:160], 8)

        print_state(eng, k[96:128], 8)
        print_state(eng, k[64:96], 8)
        print_state(eng, k[32:64], 8)
        print_state(eng, k[0:32], 8)

    y = eng.allocate_qureg(27)  # 27 * 20
    t = eng.allocate_qureg(63)  # 63 * 20
    z = eng.allocate_qureg(30)  # 30 * 20

    k_i = 0
    for i in range(14):

        if(i%2 == 0):
            AddRoundkey(eng, x0, x1, x2, x3, k)
        else:
            AddRoundkey_2(eng, x0, x1, x2, x3, k)

        print('Round', i)

        if(i!=0):
            Keyshedule(eng, k, i, y, t, z, i, k_i, resource_check)
            k_i = k_i + 1

        s = eng.allocate_qureg(128)
        SBox_bp12_all(eng, x0, x1, x2, x3, y, t, z, s, i, resource_check)
        x0, x1, x2, x3 = Shiftrow(eng, x0, x1, x2, x3)

        if(i!=13):
            x0 = Maxi_mc(eng, x0, t)
            x1 = Maxi_mc(eng, x1, t)
            x2 = Maxi_mc(eng, x2, t)
            x3 = Maxi_mc(eng, x3, t)

    AddRoundkey(eng, x0, x1, x2, x3, k)

    if(resource_check != 1):
        print('\nCiphertext ')
        print_state(eng, x3, 8)
        print_state(eng, x2, 8)
        print_state(eng, x1, 8)
        print_state(eng, x0, 8)

def Keyshedule(eng, k, i, y, t, z, round, k_i, resource_check):
    Rcon = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]

    new_k0 = []
    if (k_i % 2 == 0):
        for j in range(32):
            new_k0.append(k[(24+j) % 32])
    else:
        for j in range(32):
            new_k0.append(k[(128+j)])

    if (k_i % 2 == 0):
        for j in range(4): #22 68 18
             k[224 + 8 * j: 224 + 8 * (j + 1)] = Sbox(eng, new_k0[8 * j:8 * (j + 1)], y, t,
                                                    z, k[224 + 8 * j: 224 + 8 * (j + 1)], 1, round, resource_check)
    else:
        for j in range(4): #22 68 18
             k[96 + 8 * j: 96 + 8 * (j + 1)] = Sbox(eng, new_k0[8 * j:8 * (j + 1)], y, t,
                                                    z, k[96 + 8 * j: 96 + 8 * (j + 1)], 1, round, resource_check)
    if (k_i % 2 == 0):
        for j in range(8):
            if ((Rcon[int(k_i/2)] >> j) & 1):
                X | k[248+j]

    if(k_i % 2 == 0):
        CNOT32(eng, k[224:256], k[192:224])
        CNOT32(eng, k[192:224], k[160:192])
        CNOT32(eng, k[160:192], k[128:160])

    else:
        CNOT32(eng, k[96:128], k[64:96])
        CNOT32(eng, k[64:96], k[32:64])
        CNOT32(eng, k[32:64], k[0:32])

def SBox_bp12_all(eng, x0, x1, x2, x3, y, t, z, s, round, resource_check):

    for i in range(4):
        x0[8 * i:8 * (i + 1)] = Sbox(eng, x0[8 * i:8 * (i + 1)], y, t, z, s[8 * i:8 * (i + 1)], 0, round, resource_check)
        x1[8 * i:8 * (i + 1)] = Sbox(eng, x1[8 * i:8 * (i + 1)], y, t, z, s[8 * (i + 4):8 * (i + 5)], 0, round, resource_check)
        x2[8 * i:8 * (i + 1)] = Sbox(eng, x2[8 * i:8 * (i + 1)], y, t, z, s[8 * (i + 8):8 * (i + 9)], 0, round, resource_check)

        if(round == 13 and i == 3):
            x3[8 * i:8 * (i + 1)] = Sbox_omit_reverse(eng, x3[8 * i:8 * (i + 1)], y, t, z, s[8 * (i + 12):8 * (i + 13)], 0, round,
                                         resource_check)
        else:
            x3[8 * i:8 * (i + 1)] = Sbox(eng, x3[8 * i:8 * (i + 1)], y, t, z, s[8 * (i + 12):8 * (i + 13)], 0, round, resource_check)

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
        new_x0.append(x2[i+8])
    for i in range(8):
        new_x0.append(x3[i+16])
    for i in range(8):
        new_x0.append(x0[i+24])

    for i in range(8):
        new_x1.append(x2[i])
    for i in range(8):
        new_x1.append(x3[i+8])
    for i in range(8):
        new_x1.append(x0[i+16])
    for i in range(8):
        new_x1.append(x1[i+24])

    for i in range(8):
        new_x2.append(x3[i])
    for i in range(8):
        new_x2.append(x0[i+8])
    for i in range(8):
        new_x2.append(x1[i+16])
    for i in range(8):
        new_x2.append(x2[i+24])

    for i in range(8):
        new_x3.append(x0[i])
    for i in range(8):
        new_x3.append(x1[i+8])
    for i in range(8):
        new_x3.append(x2[i+16])
    for i in range(8):
        new_x3.append(x3[i+24])

    return new_x0, new_x1, new_x2, new_x3

def AddRoundkey(eng, x0, x1, x2, x3, k):

    CNOT32(eng, k[224:256], x3)
    CNOT32(eng, k[192:224], x2)
    CNOT32(eng, k[160:192], x1)
    CNOT32(eng, k[128:160], x0)

def AddRoundkey_2(eng, x0, x1, x2, x3, k):

    CNOT32(eng, k[0:32], x0)
    CNOT32(eng, k[32:64], x1)
    CNOT32(eng, k[64:96], x2)
    CNOT32(eng, k[96:128], x3)


def CNOT2_euro(eng, a, b, c):
    CNOT | (a, c)
    CNOT | (b, c)

def Maxi_mc(eng, x_in, t):

    x = []
    for i in range(8):
        x.append(x_in[24 + i])
    for i in range(8):
        x.append(x_in[16 + i])
    for i in range(8):
        x.append(x_in[8 + i])
    for i in range(8):
        x.append(x_in[i])

    y = eng.allocate_qureg(32)

    CNOT2_euro(eng, x[15], x[23], t[0])
    CNOT2_euro(eng, x[7], x[31], t[1])
    CNOT2_euro(eng, x[23], x[31], t[2])
    CNOT2_euro(eng, x[7], x[15], t[3])
    CNOT2_euro(eng, x[6], x[14], t[4])
    CNOT2_euro(eng, x[4], x[12], t[5])
    CNOT2_euro(eng, x[3], x[11], t[6])
    CNOT2_euro(eng, x[0], x[8], t[7])
    CNOT2_euro(eng, x[13], x[21], t[8])
    CNOT2_euro(eng, x[5], x[29], t[9])
    CNOT2_euro(eng, x[20], x[28], t[10])
    CNOT2_euro(eng, x[16], x[24], t[11])
    CNOT2_euro(eng, x[19], x[27], t[12])
    CNOT2_euro(eng, x[22], x[30], t[13])
    CNOT2_euro(eng, x[17], x[25], t[14])
    CNOT2_euro(eng, x[1], x[9], t[15])
    CNOT2_euro(eng, x[10], x[18], t[16])
    CNOT2_euro(eng, x[2], x[26], t[17])
    CNOT2_euro(eng, x[24], t[7], t[18])
    CNOT2_euro(eng, t[2], t[18], y[16])
    CNOT2_euro(eng, t[1], t[18], t[19])
    CNOT2_euro(eng, t[11], t[19], y[24])
    CNOT2_euro(eng, x[0], t[11], t[20])
    CNOT2_euro(eng, t[0], t[20], y[8])
    CNOT2_euro(eng, t[3], t[7], t[21])
    CNOT2_euro(eng, t[20], t[21], y[0])
    CNOT2_euro(eng, x[22], t[4], t[22])
    CNOT2_euro(eng, t[9], t[22], y[30])
    CNOT2_euro(eng, x[6], x[7], t[23])
    CNOT2_euro(eng, x[5], t[13], t[24])
    CNOT2_euro(eng, x[13], t[10], t[25])
    CNOT2_euro(eng, t[9], t[25], y[21])
    CNOT2_euro(eng, x[26], t[16], t[26])
    CNOT2_euro(eng, t[15], t[26], y[2])
    CNOT2_euro(eng, x[9], t[17], t[27])
    CNOT2_euro(eng, x[28], t[8], t[28])
    CNOT2_euro(eng, x[25], y[2], t[29])
    CNOT2_euro(eng, t[27], t[29], y[26])
    CNOT2_euro(eng, t[2], t[26], t[30])
    CNOT2_euro(eng, x[3], t[0], t[31])
    CNOT2_euro(eng, x[19], t[6], t[32])
    CNOT2_euro(eng, t[1], t[32], t[33])
    CNOT2_euro(eng, t[17], t[33], y[27])
    CNOT2_euro(eng, t[5], t[12], t[34])
    CNOT2_euro(eng, x[27], t[30], t[35])
    CNOT2_euro(eng, x[10], t[35], t[36])
    CNOT2_euro(eng, t[6], t[36], y[19])
    CNOT2_euro(eng, t[16], t[31], t[37])
    CNOT2_euro(eng, t[12], t[37], y[11])
    CNOT2_euro(eng, t[14], y[8], t[38])
    CNOT2_euro(eng, t[18], t[38], t[39])
    CNOT2_euro(eng, x[1], t[39], y[9])
    CNOT2_euro(eng, t[29], t[30], t[40])
    CNOT2_euro(eng, t[11], t[40], y[17])
    CNOT2_euro(eng, x[14], t[24], t[41])
    CNOT2_euro(eng, x[13], t[41], y[6])
    CNOT2_euro(eng, x[29], t[8], t[42])
    CNOT2_euro(eng, t[5], t[42], y[5])
    CNOT2_euro(eng, x[30], t[23], t[43])
    CNOT2_euro(eng, t[0], t[43], y[31])
    CNOT2_euro(eng, t[2], t[4], t[44])
    CNOT2_euro(eng, x[15], t[44], y[7])
    CNOT2_euro(eng, x[28], t[34], t[45])
    CNOT2_euro(eng, t[2], t[45], y[20])
    CNOT2_euro(eng, t[1], t[13], t[46])
    CNOT2_euro(eng, x[15], t[46], y[23])
    CNOT2_euro(eng, y[27], t[37], t[47])
    CNOT2_euro(eng, t[36], t[47], y[3])
    CNOT2_euro(eng, t[14], t[17], t[48])
    CNOT2_euro(eng, x[10], t[48], y[18])
    CNOT2_euro(eng, x[6], t[8], t[49])
    CNOT2_euro(eng, t[13], t[49], y[14])
    CNOT2_euro(eng, x[21], y[30], t[50])
    CNOT2_euro(eng, t[24], t[50], y[22])
    CNOT2_euro(eng, x[4], x[5], t[51])
    CNOT2_euro(eng, t[28], t[51], y[29])
    CNOT2_euro(eng, x[22], t[23], t[52])
    CNOT2_euro(eng, t[44], t[52], y[15])
    CNOT2_euro(eng, t[39], y[17], t[53])
    CNOT2_euro(eng, t[21], t[53], y[25])
    CNOT2_euro(eng, x[17], t[27], t[54])
    CNOT2_euro(eng, x[18], t[54], y[10])
    CNOT2_euro(eng, x[9], t[21], t[55])
    CNOT2_euro(eng, t[14], t[55], y[1])
    CNOT2_euro(eng, x[12], y[21], t[56])
    CNOT2_euro(eng, t[28], t[56], y[13])
    CNOT2_euro(eng, t[3], t[10], t[57])
    CNOT2_euro(eng, t[6], t[57], t[58])
    CNOT2_euro(eng, x[12], t[58], y[4])
    CNOT2_euro(eng, t[31], t[32], t[59])
    CNOT2_euro(eng, x[4], t[10], t[60])
    CNOT2_euro(eng, t[59], t[60], y[12])
    CNOT2_euro(eng, y[20], t[58], t[61])
    CNOT2_euro(eng, t[59], t[61], y[28])

    # now need to cleanup the t array
    # everything is an XOR, fine not using Adjoint decorator

    CNOT2_euro(eng, y[20], t[58], t[61])
    CNOT2_euro(eng, x[4], t[10], t[60])
    CNOT2_euro(eng, t[31], t[32], t[59])
    CNOT2_euro(eng, t[6], t[57], t[58])
    CNOT2_euro(eng, t[3], t[10], t[57])
    CNOT2_euro(eng, x[12], y[21], t[56])
    CNOT2_euro(eng, x[9], t[21], t[55])
    CNOT2_euro(eng, x[17], t[27], t[54])
    CNOT2_euro(eng, t[39], y[17], t[53])
    CNOT2_euro(eng, x[22], t[23], t[52])
    CNOT2_euro(eng, x[4], x[5], t[51])
    CNOT2_euro(eng, x[21], y[30], t[50])
    CNOT2_euro(eng, x[6], t[8], t[49])
    CNOT2_euro(eng, t[14], t[17], t[48])
    CNOT2_euro(eng, y[27], t[37], t[47])
    CNOT2_euro(eng, t[1], t[13], t[46])
    CNOT2_euro(eng, x[28], t[34], t[45])
    CNOT2_euro(eng, t[2], t[4], t[44])
    CNOT2_euro(eng, x[30], t[23], t[43])
    CNOT2_euro(eng, x[29], t[8], t[42])
    CNOT2_euro(eng, x[14], t[24], t[41])
    CNOT2_euro(eng, t[29], t[30], t[40])
    CNOT2_euro(eng, t[18], t[38], t[39])
    CNOT2_euro(eng, t[14], y[8], t[38])
    CNOT2_euro(eng, t[16], t[31], t[37])
    CNOT2_euro(eng, x[10], t[35], t[36])
    CNOT2_euro(eng, x[27], t[30], t[35])
    CNOT2_euro(eng, t[5], t[12], t[34])
    CNOT2_euro(eng, t[1], t[32], t[33])
    CNOT2_euro(eng, x[19], t[6], t[32])
    CNOT2_euro(eng, x[3], t[0], t[31])
    CNOT2_euro(eng, t[2], t[26], t[30])
    CNOT2_euro(eng, x[25], y[2], t[29])
    CNOT2_euro(eng, x[28], t[8], t[28])
    CNOT2_euro(eng, x[9], t[17], t[27])
    CNOT2_euro(eng, x[26], t[16], t[26])
    CNOT2_euro(eng, x[13], t[10], t[25])
    CNOT2_euro(eng, x[5], t[13], t[24])
    CNOT2_euro(eng, x[6], x[7], t[23])
    CNOT2_euro(eng, x[22], t[4], t[22])
    CNOT2_euro(eng, t[3], t[7], t[21])
    CNOT2_euro(eng, x[0], t[11], t[20])
    CNOT2_euro(eng, t[1], t[18], t[19])
    CNOT2_euro(eng, x[24], t[7], t[18])
    CNOT2_euro(eng, x[2], x[26], t[17])
    CNOT2_euro(eng, x[10], x[18], t[16])
    CNOT2_euro(eng, x[1], x[9], t[15])
    CNOT2_euro(eng, x[17], x[25], t[14])
    CNOT2_euro(eng, x[22], x[30], t[13])
    CNOT2_euro(eng, x[19], x[27], t[12])
    CNOT2_euro(eng, x[16], x[24], t[11])
    CNOT2_euro(eng, x[20], x[28], t[10])
    CNOT2_euro(eng, x[5], x[29], t[9])
    CNOT2_euro(eng, x[13], x[21], t[8])
    CNOT2_euro(eng, x[0], x[8], t[7])
    CNOT2_euro(eng, x[3], x[11], t[6])
    CNOT2_euro(eng, x[4], x[12], t[5])
    CNOT2_euro(eng, x[6], x[14], t[4])
    CNOT2_euro(eng, x[7], x[15], t[3])
    CNOT2_euro(eng, x[23], x[31], t[2])
    CNOT2_euro(eng, x[7], x[31], t[1])
    CNOT2_euro(eng, x[15], x[23], t[0])

    out = []
    for i in range(8):
        out.append(y[24 + i])
    for i in range(8):
        out.append(y[16 + i])
    for i in range(8):
        out.append(y[8 + i])
    for i in range(8):
        out.append(y[i])

    return out

def CNOT2(eng, a, b, c):

    CNOT | (a, c)
    CNOT | (b, c)

def Sbox(eng, u, t, m, l, s, flag, round, resource_check):

    with Compute(eng):
        CNOT2(eng, u[7], u[4], t[1 - 1]); CNOT2(eng, u[7], u[2], t[2 - 1])
        CNOT2(eng, u[7], u[1], t[3 - 1]); CNOT2(eng, u[4], u[2], t[4 - 1])
        CNOT2(eng, u[3], u[1], t[5 - 1]); CNOT2(eng, t[1 - 1], t[5 - 1], t[6 - 1])
        CNOT2(eng, u[6], u[5], t[7 - 1]); CNOT2(eng, u[0], t[6 - 1], t[8 - 1])
        CNOT2(eng, u[0], t[7 - 1], t[9 - 1]); CNOT2(eng, t[6 - 1], t[7 - 1], t[10 - 1])
        CNOT2(eng, u[6], u[2], t[11 - 1]); CNOT2(eng, u[5], u[2], t[12 - 1])
        CNOT2(eng, t[3 - 1], t[4 - 1], t[13 - 1]); CNOT2(eng, t[6 - 1], t[11 - 1], t[14 - 1])
        CNOT2(eng, t[5 - 1], t[11 - 1], t[15 - 1]); CNOT2(eng, t[5 - 1], t[12 - 1], t[16 - 1])
        CNOT2(eng, t[9 - 1], t[16 - 1], t[17 - 1]); CNOT2(eng, u[4], u[0], t[18 - 1])
        CNOT2(eng, t[7 - 1], t[18 - 1], t[19 - 1]); CNOT2(eng, t[1 - 1], t[19 - 1], t[20 - 1])
        CNOT2(eng, u[1], u[0], t[21 - 1]); CNOT2(eng, t[7 - 1], t[21 - 1], t[22 - 1])
        CNOT2(eng, t[2 - 1], t[22 - 1], t[23 - 1]); CNOT2(eng, t[2 - 1], t[10 - 1], t[24 - 1])
        CNOT2(eng, t[20 - 1], t[17 - 1], t[25 - 1]); CNOT2(eng, t[3 - 1], t[16 - 1], t[26 - 1])
        CNOT2(eng, t[1 - 1], t[12 - 1], t[27 - 1])

        Toffoli_gate(eng, t[13 - 1], t[6 - 1], m[1 - 1], resource_check)
        Toffoli_gate(eng, t[23 - 1], t[8 - 1], m[2 - 1], resource_check)
        CNOT2(eng, t[14 - 1], m[1 - 1], m[3 - 1])
        Toffoli_gate(eng, t[19 - 1], u[0], m[4 - 1], resource_check)
        CNOT2(eng, m[4 - 1], m[1 - 1], m[5 - 1])
        Toffoli_gate(eng, t[3 - 1], t[16 - 1], m[6 - 1], resource_check)
        Toffoli_gate(eng, t[22 - 1], t[9 - 1], m[7 - 1], resource_check)
        CNOT2(eng, t[26 - 1], m[6 - 1], m[8 - 1])
        Toffoli_gate(eng, t[20 - 1], t[17 - 1], m[9 - 1], resource_check)
        CNOT2(eng, m[9 - 1], m[6 - 1], m[10 - 1])
        Toffoli_gate(eng, t[1 - 1], t[15 - 1], m[11 - 1], resource_check)
        Toffoli_gate(eng, t[4 - 1], t[27 - 1], m[12 - 1], resource_check)
        CNOT2(eng, m[12 - 1], m[11 - 1], m[13 - 1])
        Toffoli_gate(eng, t[2 - 1], t[10 - 1], m[14 - 1], resource_check)
        CNOT2(eng, m[14 - 1], m[11 - 1], m[15 - 1]); CNOT2(eng, m[3 - 1], m[2 - 1], m[16 - 1])
        CNOT2(eng, m[5 - 1], t[24 - 1], m[17 - 1]); CNOT2(eng, m[8 - 1], m[7 - 1], m[18 - 1])
        CNOT2(eng, m[10 - 1], m[15 - 1], m[19 - 1]); CNOT2(eng, m[16 - 1], m[13 - 1], m[20 - 1])
        CNOT2(eng, m[17 - 1], m[15 - 1], m[21 - 1]); CNOT2(eng, m[18 - 1], m[13 - 1], m[22 - 1])
        CNOT2(eng, m[19 - 1], t[25 - 1], m[23 - 1]); CNOT2(eng, m[22 - 1], m[23 - 1], m[24 - 1])
        Toffoli_gate(eng, m[22 - 1], m[20 - 1], m[25 - 1], resource_check)
        CNOT2(eng, m[21 - 1], m[25 - 1], m[26 - 1]); CNOT2(eng, m[20 - 1], m[21 - 1], m[27 - 1])
        CNOT2(eng, m[23 - 1], m[25 - 1], m[28 - 1])
        Toffoli_gate(eng, m[28 - 1], m[27 - 1], m[29 - 1], resource_check)
        Toffoli_gate(eng, m[26 - 1], m[24 - 1], m[30 - 1], resource_check)
        Toffoli_gate(eng, m[20 - 1], m[23 - 1], m[31 - 1], resource_check)
        Toffoli_gate(eng, m[27 - 1], m[31 - 1], m[32 - 1], resource_check)
        CNOT2(eng, m[27 - 1], m[25 - 1], m[33 - 1])
        Toffoli_gate(eng, m[21 - 1], m[22 - 1], m[34 - 1], resource_check)
        Toffoli_gate(eng, m[24 - 1], m[34 - 1], m[35 - 1], resource_check)
        CNOT2(eng, m[24 - 1], m[25 - 1], m[36 - 1]); CNOT2(eng, m[21 - 1], m[29 - 1], m[37 - 1])
        CNOT2(eng, m[32 - 1], m[33 - 1], m[38 - 1]); CNOT2(eng, m[23 - 1], m[30 - 1], m[39 - 1])
        CNOT2(eng, m[35 - 1], m[36 - 1], m[40 - 1]); CNOT2(eng, m[38 - 1], m[40 - 1], m[41 - 1])
        CNOT2(eng, m[37 - 1], m[39 - 1], m[42 - 1]); CNOT2(eng, m[37 - 1], m[38 - 1], m[43 - 1])
        CNOT2(eng, m[39 - 1], m[40 - 1], m[44 - 1]); CNOT2(eng, m[42 - 1], m[41 - 1], m[45 - 1])
        Toffoli_gate(eng, m[44 - 1], t[6 - 1], m[46 - 1], resource_check)
        Toffoli_gate(eng, m[40 - 1], t[8 - 1], m[47 - 1], resource_check)
        Toffoli_gate(eng, m[39 - 1], u[0], m[48 - 1], resource_check)
        Toffoli_gate(eng, m[43 - 1], t[16 - 1], m[49 - 1], resource_check)
        Toffoli_gate(eng, m[38 - 1], t[9 - 1], m[50 - 1], resource_check)
        Toffoli_gate(eng, m[37 - 1], t[17 - 1], m[51 - 1], resource_check)
        Toffoli_gate(eng, m[42 - 1], t[15 - 1], m[52 - 1], resource_check)
        Toffoli_gate(eng, m[45 - 1], t[27 - 1], m[53 - 1], resource_check)
        Toffoli_gate(eng, m[41 - 1], t[10 - 1], m[54 - 1], resource_check)
        Toffoli_gate(eng, m[44 - 1], t[13 - 1], m[55 - 1], resource_check)
        Toffoli_gate(eng, m[40 - 1], t[23 - 1], m[56 - 1], resource_check)
        Toffoli_gate(eng, m[39 - 1], t[19 - 1], m[57 - 1], resource_check)
        Toffoli_gate(eng, m[43 - 1], t[3 - 1], m[58 - 1], resource_check)
        Toffoli_gate(eng, m[38 - 1], t[22 - 1], m[59 - 1], resource_check)
        Toffoli_gate(eng, m[37 - 1], t[20 - 1], m[60 - 1], resource_check)
        Toffoli_gate(eng, m[42 - 1], t[1 - 1], m[61 - 1], resource_check)
        Toffoli_gate(eng, m[45 - 1], t[4 - 1], m[62 - 1], resource_check)
        Toffoli_gate(eng, m[41 - 1], t[2 - 1], m[63 - 1], resource_check)

        CNOT2(eng, m[61 - 1], m[62 - 1], l[0]); CNOT2(eng, m[50 - 1], m[56 - 1], l[1])
        CNOT2(eng, m[46 - 1], m[48 - 1], l[2]); CNOT2(eng, m[47 - 1], m[55 - 1], l[3])
        CNOT2(eng, m[54 - 1], m[58 - 1], l[4]); CNOT2(eng, m[49 - 1], m[61 - 1], l[5])
        CNOT2(eng, m[62 - 1], l[5], l[6]); CNOT2(eng, m[46 - 1], l[3], l[7])
        CNOT2(eng, m[51 - 1], m[59 - 1], l[8]); CNOT2(eng, m[52 - 1], m[53 - 1], l[9])
        CNOT2(eng, m[53 - 1], l[4], l[10]); CNOT2(eng, m[60 - 1], l[2], l[11])
        CNOT2(eng, m[48 - 1], m[51 - 1], l[12]); CNOT2(eng, m[50 - 1], l[0], l[13])
        CNOT2(eng, m[52 - 1], m[61 - 1], l[14]); CNOT2(eng, m[55 - 1], l[1], l[15])
        CNOT2(eng, m[56 - 1], l[0], l[16]); CNOT2(eng, m[57 - 1], l[1], l[17])
        CNOT2(eng, m[58 - 1], l[8], l[18]); CNOT2(eng, m[63 - 1], l[4], l[19])
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
    Uncompute(eng)

    return s

def Sbox_omit_reverse(eng, u, t, m, l, s, flag, round, resource_check):

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

    Toffoli_gate(eng, t[12], t[5], m[0], resource_check)
    Toffoli_gate(eng, t[22], t[7], m[1], resource_check)
    CNOT2(eng, t[13], m[0], m[2])
    Toffoli_gate(eng, t[18], u[0], m[3], resource_check)
    CNOT2(eng, m[3], m[0], m[4])
    Toffoli_gate(eng, t[2], t[15], m[5], resource_check)
    Toffoli_gate(eng, t[21], t[8], m[6], resource_check)
    CNOT2(eng, t[25], m[5], m[7])
    Toffoli_gate(eng, t[19], t[16], m[8], resource_check)
    CNOT2(eng, m[8], m[5], m[9])
    Toffoli_gate(eng, t[0], t[14], m[10], resource_check)
    Toffoli_gate(eng, t[3], t[26], m[11], resource_check)
    CNOT2(eng, m[11], m[10], m[12])
    Toffoli_gate(eng, t[1], t[9], m[13], resource_check)
    CNOT2(eng, m[13], m[10], m[14]); CNOT2(eng, m[2], m[1], m[15])
    CNOT2(eng, m[4], t[23], m[16]); CNOT2(eng, m[7], m[6], m[17])
    CNOT2(eng, m[9], m[14], m[18]); CNOT2(eng, m[15], m[12], m[19])
    CNOT2(eng, m[16], m[14], m[20]); CNOT2(eng, m[17], m[12], m[21])
    CNOT2(eng, m[18], t[24], m[22]); CNOT2(eng, m[21], m[22], m[23])
    Toffoli_gate(eng, m[21], m[19], m[24], resource_check)
    CNOT2(eng, m[20], m[24], m[25]); CNOT2(eng, m[19], m[20], m[26])
    CNOT2(eng, m[22], m[24], m[27])
    Toffoli_gate(eng, m[27], m[26], m[28], resource_check)
    Toffoli_gate(eng, m[25], m[23], m[29], resource_check)
    Toffoli_gate(eng, m[19], m[22], m[30], resource_check)
    Toffoli_gate(eng, m[26], m[30], m[31], resource_check)
    CNOT2(eng, m[26], m[24], m[32])
    Toffoli_gate(eng, m[20], m[21], m[33], resource_check)
    Toffoli_gate(eng, m[23], m[33], m[34], resource_check)
    CNOT2(eng, m[23], m[24], m[35]); CNOT2(eng, m[20], m[28], m[36])
    CNOT2(eng, m[31], m[32], m[37]); CNOT2(eng, m[22], m[29], m[38])
    CNOT2(eng, m[34], m[35], m[39]); CNOT2(eng, m[37], m[39], m[40])
    CNOT2(eng, m[36], m[38], m[41]); CNOT2(eng, m[36], m[37], m[42])
    CNOT2(eng, m[38], m[39], m[43]); CNOT2(eng, m[41], m[40], m[44])
    Toffoli_gate(eng, m[43], t[5], m[45], resource_check)
    Toffoli_gate(eng, m[39], t[7], m[46], resource_check)
    Toffoli_gate(eng, m[38], u[0], m[47], resource_check)
    Toffoli_gate(eng, m[42], t[15], m[48], resource_check)
    Toffoli_gate(eng, m[37], t[8], m[49], resource_check)
    Toffoli_gate(eng, m[36], t[16], m[50], resource_check)
    Toffoli_gate(eng, m[41], t[14], m[51], resource_check)
    Toffoli_gate(eng, m[44], t[26], m[52], resource_check)
    Toffoli_gate(eng, m[40], t[9], m[53], resource_check)
    Toffoli_gate(eng, m[43], t[12], m[54], resource_check)
    Toffoli_gate(eng, m[39], t[22], m[55], resource_check)
    Toffoli_gate(eng, m[38], t[18], m[56], resource_check)
    Toffoli_gate(eng, m[42], t[2], m[57], resource_check)
    Toffoli_gate(eng, m[37], t[21], m[58], resource_check)
    Toffoli_gate(eng, m[36], t[19], m[59], resource_check)
    Toffoli_gate(eng, m[41], t[0], m[60], resource_check)
    Toffoli_gate(eng, m[44], t[3], m[61], resource_check)
    Toffoli_gate(eng, m[40], t[1], m[62], resource_check)

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

    print('omit reverse')

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
        temp = temp+int(qubits[4*i+3])*8
        temp = temp+int(qubits[4*i+2])*4
        temp = temp+int(qubits[4*i+1])*2
        temp = temp+int(qubits[4*i])

        temp = hex(temp)
        y = temp.replace("0x", "")
        print(y, end='')

def Toffoli_gate(eng, a, b, c, resource_check):

    if(resource_check):
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
