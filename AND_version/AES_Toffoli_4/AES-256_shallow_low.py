from projectq import MainEngine
from projectq.ops import H, CNOT, Measure, Toffoli, X, All, T, Tdagger, S, Tdag, Sdag
from projectq.backends import CircuitDrawer, ResourceCounter, ClassicalSimulator
from projectq.meta import Loop, Compute, Uncompute, Control, Dagger


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

    y = eng.allocate_qureg(540)  # 22 * 20
    t = eng.allocate_qureg(1260)  # 68 * 20
    z = eng.allocate_qureg(600)  # 18 * 20

    y_two = eng.allocate_qureg(540)  # 22 * 20
    t_two = eng.allocate_qureg(1260)  # 68 * 20
    z_two = eng.allocate_qureg(600)  # 18 * 20

    ancilla = eng.allocate_qureg(4)

    k_i = 0
    for i in range(14):

        if(i%2 == 0):
            AddRoundkey(eng, x0, x1, x2, x3, k)
        else:
            AddRoundkey_2(eng, x0, x1, x2, x3, k)

        print('Round', i)
        if (i == 1):
            Clean_ancilla(eng, t0, t1, t2, t3, k, y, t, z, 1, k_i, resource_check)

        if(i!= 0 and i!= 1 and i!= 13 and i % 2 == 0):
            Clean_ancilla(eng, t0, t1, t2, t3, k[0:32], y_two, t_two, z_two, 0, k_i, resource_check)

        if (i != 0 and i != 1 and i!= 13 and i % 2 == 1):
            Clean_ancilla(eng, t0, t1, t2, t3, k[128:160], y, t, z, 0, k_i, resource_check)

        if(i!=0):
            if(i%2 == 0):
                Keyshedule(eng, k, i, y, t, z, i, k_i, ancilla, resource_check) #i=2, k_i=1, _one
                CNOT32(eng, k[96:128], k[64:96])
                CNOT32(eng, k[64:96], k[32:64])
                CNOT32(eng, k[32:64], k[0:32])
            else:
                Keyshedule(eng, k, i, y_two, t_two, z_two, i, k_i, ancilla, resource_check) #i=1, k_i=0, _two, i=3, k_i=2, _two
                CNOT32(eng, k[224:256], k[192:224])
                CNOT32(eng, k[192:224], k[160:192])
                CNOT32(eng, k[160:192], k[128:160])
            k_i = k_i + 1

        s = eng.allocate_qureg(128)

        t0 = []
        for temp in range(32):
            t0.append(x0[temp])
        t1 = []
        for temp in range(32):
            t1.append(x1[temp])
        t2 = []
        for temp in range(32):
            t2.append(x2[temp])
        t3 = []
        for temp in range(32):
            t3.append(x3[temp])

        if (i % 2 == 0):
            SBox_bp12_all(eng, x0, x1, x2, x3, y, t, z, s, i, resource_check)
            x0, x1, x2, x3 = Shiftrow(eng, x0, x1, x2, x3)
            if (i != 13):
                x0 = XOR105(eng, x0, t_two[0:105])
                x1 = XOR105(eng, x1, t_two[105:210])
                x2 = XOR105(eng, x2, t_two[210:315])
                x3 = XOR105(eng, x3, t_two[315:420])
        else:
            SBox_bp12_all(eng, x0, x1, x2, x3, y_two, t_two, z_two, s, i, resource_check)
            x0, x1, x2, x3 = Shiftrow(eng, x0, x1, x2, x3)
            if (i != 13):
                x0 = XOR105(eng, x0, t[0:105])
                x1 = XOR105(eng, x1, t[105:210])
                x2 = XOR105(eng, x2, t[210:315])
                x3 = XOR105(eng, x3, t[315:420])

    AddRoundkey(eng, x0, x1, x2, x3, k)

    if(resource_check != 1):
        print('\nCiphertext ')
        print_state(eng, x3, 8)
        print_state(eng, x2, 8)
        print_state(eng, x1, 8)
        print_state(eng, x0, 8)

def Clean_ancilla(eng, x0, x1, x2, x3, temp_k, y, t, z, flag, k_i, resource_check):

    for i in range(4):
        Uncompute_sbox(eng, x0[8 * i:8 * (i + 1)], y[27 * i:27 * (i + 1)], t[63 * i:63 * (i + 1)],
                       z[30 * i:30 * (i + 1)], resource_check)
        Uncompute_sbox(eng, x1[8 * i:8 * (i + 1)], y[27 * (i + 4):27 * (i + 5)], t[63 * (i + 4):63 * (i + 5)],
                       z[30 * (i + 4):30 * (i + 5)], resource_check)
        Uncompute_sbox(eng, x2[8 * i:8 * (i + 1)], y[27 * (i + 8):27 * (i + 9)], t[63 * (i + 8):63 * (i + 9)],
                       z[30 * (i + 8):30 * (i + 9)], resource_check)
        Uncompute_sbox(eng, x3[8 * i:8 * (i + 1)], y[27 * (i + 12):27 * (i + 13)], t[63 * (i + 12):63 * (i + 13)],
                       z[30 * (i + 12):30 * (i + 13)], resource_check)

    if(flag != 1):
        new_k0 = []
        if (k_i % 2 == 0):
            for j in range(32):
                new_k0.append(temp_k[j])
        else:
            for j in range(32):
                new_k0.append(temp_k[(24 + j) % 32])

        for i in range(4):
            Uncompute_sbox(eng, new_k0[8 * i:8 * (i + 1)], y[432 + 27 * i: 432 + 27 * (i + 1)],
                           t[1008 + 63 * i: 1008 + 63 * (i + 1)],
                           z[480 + 30 * i: 480 + 30 * (i + 1)], resource_check)

def XOR105(eng, x_in, t):
    y = eng.allocate_qureg(32)
    x = []
    for i in range(8):
        x.append(x_in[24 + i])
    for i in range(8):
        x.append(x_in[16 + i])
    for i in range(8):
        x.append(x_in[8 + i])
    for i in range(8):
        x.append(x_in[i])

    with Compute(eng):
        CNOT2_mc(eng, t[1], x[7], x[15])
        CNOT2_mc(eng, t[2], x[23], x[31])
        CNOT2_mc(eng, t[3], x[7], x[31])
        CNOT2_mc(eng, t[4], x[15], x[23])
        CNOT2_mc(eng, t[5], x[0], x[8])
        CNOT2_mc(eng, t[6], x[6], x[14])
        CNOT2_mc(eng, t[7], x[5], x[29])
        CNOT2_mc(eng, t[8], x[16], x[24])
        CNOT2_mc(eng, t[9], x[22], x[30])
        CNOT2_mc(eng, t[10], x[13], x[21])
        CNOT2_mc(eng, t[11], x[1], x[9])
        CNOT2_mc(eng, t[12], x[10], x[18])
        CNOT2_mc(eng, t[13], x[2], x[26])
        CNOT2_mc(eng, t[14], x[17], x[25])
        CNOT2_mc(eng, t[15], x[4], x[12])
        CNOT2_mc(eng, t[16], x[3], x[27])
        CNOT2_mc(eng, t[17], x[20], x[28])
        CNOT2_mc(eng, t[18], x[11], x[19])
        CNOT2_mc(eng, t[19], x[0], t[4])
    CNOT2_mc(eng, y[8], t[8], t[19])  # y8  (3)
    with Compute(eng):
        CNOT2_mc(eng, t[21], x[6], t[9])
    CNOT2_mc(eng, y[14], t[10], t[21])  # y14  (3)
    with Compute(eng):
        CNOT2_mc(eng, t[23], x[7], x[22])
        CNOT2_mc(eng, t[24], x[8], t[1])
    CNOT2_mc(eng, y[0], t[8], t[24])  # y0  (3)
    with Compute(eng):
        CNOT2_mc(eng, t[26], x[10], t[13])
    CNOT2_mc(eng, y[18], t[14], t[26])  # y18  (3)
    with Compute(eng):
        CNOT2_mc(eng, t[28], x[13], t[7])
    CNOT2_mc(eng, y[21], t[17], t[28])  # y21  (3)
    with Compute(eng):
        CNOT2_mc(eng, t[30], x[14], t[2])
    CNOT2_mc(eng, y[15], t[23], t[30])  # y15  (3)
    with Compute(eng):
        CNOT2_mc(eng, t[32], x[6], x[15])
    CNOT2_mc(eng, y[7], t[30], t[32])  # y7  (3)
    with Compute(eng):
        CNOT2_mc(eng, t[34], x[15], t[3])
    CNOT2_mc(eng, y[23], t[9], t[34]) #y23
    with Compute(eng):
        CNOT2_mc(eng, t[36], x[16], t[3])
    CNOT2_mc(eng, y[24], t[5], t[36])  # y24
    with Compute(eng):
        CNOT2_mc(eng, t[38], x[22], t[6])
    CNOT2_mc(eng, y[30], t[7], t[38]) #y30
    with Compute(eng):
        CNOT2_mc(eng, t[40], x[24], t[2])
    CNOT2_mc(eng, y[16], t[5], t[40])  # y16  (3)
    with Compute(eng):
        CNOT2_mc(eng, t[42], x[26], t[11])
    CNOT2_mc(eng, y[2], t[12], t[42])  # y2  (3)
    with Compute(eng):
        CNOT2_mc(eng, t[44], x[29], t[10])
    CNOT2_mc(eng, y[5], t[15], t[44])  # y5  (3)
    with Compute(eng):
        CNOT2_mc(eng, t[46], t[4], t[23])
    CNOT2_mc(eng, y[31], t[21], t[46])  # y31  (3)
    with Compute(eng):
        CNOT2_mc(eng, t[48], x[0], x[9])
        CNOT2_mc(eng, t[49], t[14], t[48])
    CNOT2_mc(eng, y[1], t[24], t[49])  # y1  (3)
    with Compute(eng):
        CNOT2_mc(eng, t[51], x[1], x[2])
        CNOT2_mc(eng, t[52], x[25], t[12])
    CNOT2_mc(eng, y[26], t[51], t[52])  # y26  (3)
    with Compute(eng):
        CNOT2_mc(eng, t[54], x[3], t[3])
        CNOT2_mc(eng, t[55], t[13], t[18])
    CNOT2_mc(eng, y[27], t[54], t[55])  # y27  (3)
    with Compute(eng):
        CNOT2_mc(eng, t[57], x[4], x[5])
        CNOT2_mc(eng, t[58], x[28], t[10])
    CNOT2_mc(eng, y[29], t[57], t[58])  # y29  (3)
    with Compute(eng):
        CNOT2_mc(eng, t[60], x[4], t[4])
        CNOT2_mc(eng, t[61], t[17], t[18])
    CNOT2_mc(eng, y[12], t[60], t[61])  # y12  (3)
    with Compute(eng):
        CNOT2_mc(eng, t[63], x[5], x[13])
        CNOT2_mc(eng, t[64], x[14], t[9])
    CNOT2_mc(eng, y[6], t[63], t[64])  # y6  (3)
    with Compute(eng):
        CNOT2_mc(eng, t[66], x[9], x[17])
        CNOT2_mc(eng, t[67], x[18], t[13])
    CNOT2_mc(eng, y[10], t[66], t[67])  # y10  (3)
    with Compute(eng):
        CNOT2_mc(eng, t[69], x[12], x[20])
        CNOT2_mc(eng, t[70], x[21], t[7])
    CNOT2_mc(eng, y[13], t[69], t[70])  # y13  (3)
    with Compute(eng):
        CNOT2_mc(eng, t[72], x[4], x[27])
        CNOT2_mc(eng, t[73], t[69], t[72])
    CNOT2_mc(eng, y[28], t[54], t[73])  # y28  (3)
    with Compute(eng):
        CNOT2_mc(eng, t[75], x[5], x[30])
        CNOT2_mc(eng, t[76], t[6], t[75])
    CNOT2_mc(eng, y[22], t[70], t[76])  # y22  (3)
    with Compute(eng):
        CNOT2_mc(eng, t[78], x[16], x[25])
        CNOT2_mc(eng, t[79], x[1], x[17])
        CNOT2_mc(eng, t[80], t[11], t[78])
    CNOT2_mc(eng, y[17], t[40], t[80])  # y17  (3)
    with Compute(eng):
        CNOT2_mc(eng, t[82], x[8], t[4])
        CNOT2_mc(eng, t[83], t[78], t[79])
    CNOT2_mc(eng, y[9], t[82], t[83])  # y9  (3)
    with Compute(eng):
        CNOT2_mc(eng, t[85], x[19], t[4])
        CNOT2_mc(eng, t[86], t[12], t[16])
    CNOT2_mc(eng, y[11], t[85], t[86])  # y11  (3)
    with Compute(eng):
        CNOT2_mc(eng, t[88], x[24], t[3])
        CNOT2_mc(eng, t[89], t[48], t[79])
    CNOT2_mc(eng, y[25], t[88], t[89])  # y25  (3)
    with Compute(eng):
        CNOT2_mc(eng, t[91], x[2], x[10])
        CNOT2_mc(eng, t[92], x[27], t[1])
        CNOT2_mc(eng, t[93], t[18], t[91])
    CNOT2_mc(eng, y[3], t[92], t[93])  # y3  (3)
    with Compute(eng):
        CNOT2_mc(eng, t[95], x[3], x[11])
        CNOT2_mc(eng, t[96], x[27], t[2])
        CNOT2_mc(eng, t[97], x[12], t[1])
        CNOT2_mc(eng, t[98], t[17], t[95])
    CNOT2_mc(eng, y[4], t[97], t[98])  # y4  (3)
    with Compute(eng):
        CNOT2_mc(eng, t[100], x[18], x[26])
        CNOT2_mc(eng, t[101], t[95], t[100])
    CNOT2_mc(eng, y[19], t[96], t[101])  # y19  (3)
    with Compute(eng):
        CNOT2_mc(eng, t[103], x[19], x[28])
        CNOT2_mc(eng, t[104], t[15], t[103])
    CNOT2_mc(eng, y[20], t[96], t[104])  # y20  (3)

    Uncompute(eng)
    Uncompute(eng)
    Uncompute(eng)
    Uncompute(eng)
    Uncompute(eng)

    Uncompute(eng)
    Uncompute(eng)
    Uncompute(eng)
    Uncompute(eng)
    Uncompute(eng)

    Uncompute(eng)
    Uncompute(eng)
    Uncompute(eng)
    Uncompute(eng)
    Uncompute(eng)

    Uncompute(eng)
    Uncompute(eng)
    Uncompute(eng)
    Uncompute(eng)
    Uncompute(eng)

    Uncompute(eng)
    Uncompute(eng)
    Uncompute(eng)
    Uncompute(eng)
    Uncompute(eng)

    Uncompute(eng)
    Uncompute(eng)
    Uncompute(eng)
    Uncompute(eng)
    Uncompute(eng)

    Uncompute(eng)
    Uncompute(eng)

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

def CNOT2_mc(eng, a, b, c):
    CNOT | (b, a)
    CNOT | (c, a)

def Keyshedule(eng, k, i, y, t, z, round, k_i, ancilla, resource_check):

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
             k[224 + 8 * j: 224 + 8 * (j + 1)] = AND_KS_Sbox_T4(eng, new_k0[8 * j:8 * (j + 1)], y[432+27*j:432+27*(j+1)],
                                         t[1008+63*j:1008+63*(j+1)], z[480+30*j:480+30*(j+1)], k[224 + 8 * j: 224 + 8 * (j + 1)], 1, round, ancilla[j], resource_check)
    else:
        for j in range(4): #22 68 18
             k[96 + 8 * j: 96 + 8 * (j + 1)] = AND_KS_Sbox_T4(eng, new_k0[8 * j:8 * (j + 1)], y[432+27*j:432+27*(j+1)],
                                         t[1008+63*j:1008+63*(j+1)], z[480+30*j:480+30*(j+1)], k[96 + 8 * j: 96 + 8 * (j + 1)], 1, round, ancilla[j], resource_check)
    if (k_i % 2 == 0):
        for j in range(8):
            if ((Rcon[int(k_i/2)] >> j) & 1):
                X | k[248+j]

def SBox_bp12_all(eng, x0, x1, x2, x3, y, t, z, s, round, resource_check):
    for i in range(4):
        x0[8 * i:8 * (i + 1)] = AND_Sbox_T4(eng, x0[8 * i:8 * (i + 1)], y[27 * i:27 * (i + 1)], t[63 * i:63 * (i + 1)],
                                     z[30 * i:30 * (i + 1)], s[8 * i:8 * (i + 1)], 0, round, resource_check)
        x1[8 * i:8 * (i + 1)] = AND_Sbox_T4(eng, x1[8 * i:8 * (i + 1)], y[27 * (i + 4):27 * (i + 5)],
                                     t[63 * (i + 4):63 * (i + 5)], z[30 * (i + 4):30 * (i + 5)],
                                     s[8 * (i + 4):8 * (i + 5)], 0, round, resource_check)
        x2[8 * i:8 * (i + 1)] = AND_Sbox_T4(eng, x2[8 * i:8 * (i + 1)], y[27 * (i + 8):27 * (i + 9)],
                                     t[63 * (i + 8):63 * (i + 9)], z[30 * (i + 8):30 * (i + 9)],
                                     s[8 * (i + 8):8 * (i + 9)], 0, round, resource_check)
        x3[8 * i:8 * (i + 1)] = AND_Sbox_T4(eng, x3[8 * i:8 * (i + 1)], y[27 * (i + 12):27 * (i + 13)],
                                     t[63 * (i + 12):63 * (i + 13)], z[30 * (i + 12):30 * (i + 13)],
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

def CNOT2(eng, a, b, c):

    CNOT | (a, c)
    CNOT | (b, c)

def Uncompute_sbox(eng, u_in, t, m, l, resource_check):

    u = []
    for i in range(8):
        u.append(u_in[7 - i])

    with Dagger(eng):
            CNOT2(eng, u[0], u[3], t[1 - 1]);
            CNOT2(eng, u[0], u[5], t[2 - 1])
            CNOT2(eng, u[0], u[6], t[3 - 1]);
            CNOT2(eng, u[3], u[5], t[4 - 1])
            CNOT2(eng, u[4], u[6], t[5 - 1]);
            CNOT2(eng, t[1 - 1], t[5 - 1], t[6 - 1])
            CNOT2(eng, u[1], u[2], t[7 - 1]);
            CNOT2(eng, u[7], t[6 - 1], t[8 - 1])
            CNOT2(eng, u[7], t[7 - 1], t[9 - 1]);
            CNOT2(eng, t[6 - 1], t[7 - 1], t[10 - 1])
            CNOT2(eng, u[1], u[5], t[11 - 1]);
            CNOT2(eng, u[2], u[5], t[12 - 1])
            CNOT2(eng, t[3 - 1], t[4 - 1], t[13 - 1]);
            CNOT2(eng, t[6 - 1], t[11 - 1], t[14 - 1])
            CNOT2(eng, t[5 - 1], t[11 - 1], t[15 - 1]);
            CNOT2(eng, t[5 - 1], t[12 - 1], t[16 - 1])
            CNOT2(eng, t[9 - 1], t[16 - 1], t[17 - 1]);
            CNOT2(eng, u[3], u[7], t[18 - 1])
            CNOT2(eng, t[7 - 1], t[18 - 1], t[19 - 1]);
            CNOT2(eng, t[1 - 1], t[19 - 1], t[20 - 1])
            CNOT2(eng, u[6], u[7], t[21 - 1]);
            CNOT2(eng, t[7 - 1], t[21 - 1], t[22 - 1])
            CNOT2(eng, t[2 - 1], t[22 - 1], t[23 - 1]);
            CNOT2(eng, t[2 - 1], t[10 - 1], t[24 - 1])
            CNOT2(eng, t[20 - 1], t[17 - 1], t[25 - 1]);
            CNOT2(eng, t[3 - 1], t[16 - 1], t[26 - 1])
            CNOT2(eng, t[1 - 1], t[12 - 1], t[27 - 1])

            AND_gate_dag(eng, t[13 - 1], t[6 - 1], m[1 - 1], l[13])
            AND_gate_dag(eng, t[23 - 1], t[8 - 1], m[2 - 1], l[14])
            CNOT2(eng, t[14 - 1], m[1 - 1], m[3 - 1])
            AND_gate_dag(eng, t[19 - 1], u[7], m[4 - 1], l[15])
            CNOT2(eng, m[4 - 1], m[1 - 1], m[5 - 1])
            AND_gate_dag(eng, t[3 - 1], t[16 - 1], m[6 - 1], l[16])
            AND_gate_dag(eng, t[22 - 1], t[9 - 1], m[7 - 1], l[17])
            CNOT2(eng, t[26 - 1], m[6 - 1], m[8 - 1])
            AND_gate_dag(eng, t[20 - 1], t[17 - 1], m[9 - 1], l[18])
            CNOT2(eng, m[9 - 1], m[6 - 1], m[10 - 1])
            AND_gate_dag(eng, t[1 - 1], t[15 - 1], m[11 - 1], l[19])
            AND_gate_dag(eng, t[4 - 1], t[27 - 1], m[12 - 1], l[20])
            CNOT2(eng, m[12 - 1], m[11 - 1], m[13 - 1])
            AND_gate_dag(eng, t[2 - 1], t[10 - 1], m[14 - 1], l[21])
            CNOT2(eng, m[14 - 1], m[11 - 1], m[15 - 1]);
            CNOT2(eng, m[3 - 1], m[2 - 1], m[16 - 1])
            CNOT2(eng, m[5 - 1], t[24 - 1], m[17 - 1]);
            CNOT2(eng, m[8 - 1], m[7 - 1], m[18 - 1])
            CNOT2(eng, m[10 - 1], m[15 - 1], m[19 - 1]);
            CNOT2(eng, m[16 - 1], m[13 - 1], m[20 - 1])
            CNOT2(eng, m[17 - 1], m[15 - 1], m[21 - 1]);
            CNOT2(eng, m[18 - 1], m[13 - 1], m[22 - 1])
            CNOT2(eng, m[19 - 1], t[25 - 1], m[23 - 1]);
            CNOT2(eng, m[22 - 1], m[23 - 1], m[24 - 1])

            CNOT | (m[22 - 1], l[0]);
            CNOT | (m[20 - 1], l[1])

            AND_gate_dag(eng, m[22 - 1], m[20 - 1], m[25 - 1], l[22])
            AND_gate_dag(eng, l[1], m[23 - 1], m[31 - 1], l[23])
            AND_gate_dag(eng, m[21 - 1], l[0], m[34 - 1], l[24])

            CNOT | (m[24 - 1], l[3])
            CNOT2(eng, m[21 - 1], m[25 - 1], m[26 - 1]);
            CNOT2(eng, m[20 - 1], m[21 - 1], m[27 - 1])
            CNOT | (m[27 - 1], l[2])

            CNOT2(eng, m[23 - 1], m[25 - 1], m[28 - 1]);
            CNOT2(eng, m[27 - 1], m[25 - 1], m[33 - 1])

            AND_gate_dag(eng, m[28 - 1], m[27 - 1], m[29 - 1], l[25])
            AND_gate_dag(eng, m[26 - 1], m[24 - 1], m[30 - 1], l[26])
            AND_gate_dag(eng, l[2], m[31 - 1], m[32 - 1], l[27])
            AND_gate_dag(eng, l[3], m[34 - 1], m[35 - 1], l[28])

            CNOT2(eng, m[24 - 1], m[25 - 1], m[36 - 1]);
            CNOT2(eng, m[21 - 1], m[29 - 1], m[37 - 1])
            CNOT2(eng, m[32 - 1], m[33 - 1], m[38 - 1]);
            CNOT2(eng, m[23 - 1], m[30 - 1], m[39 - 1])
            CNOT2(eng, m[35 - 1], m[36 - 1], m[40 - 1]);
            CNOT2(eng, m[38 - 1], m[40 - 1], m[41 - 1])
            CNOT2(eng, m[37 - 1], m[39 - 1], m[42 - 1]);
            CNOT2(eng, m[37 - 1], m[38 - 1], m[43 - 1])
            CNOT2(eng, m[39 - 1], m[40 - 1], m[44 - 1]);
            CNOT2(eng, m[42 - 1], m[41 - 1], m[45 - 1])

            CNOT | (m[44 - 1], l[4]);
            CNOT | (m[40 - 1], l[5])
            CNOT | (m[39 - 1], l[6]);
            CNOT | (m[43 - 1], l[7])
            CNOT | (m[38 - 1], l[8]);
            CNOT | (m[37 - 1], l[9])
            CNOT | (m[42 - 1], l[10]);
            CNOT | (m[45 - 1], l[11])
            CNOT | (m[41 - 1], l[12])

            # check_ancilla(eng, l[13:30], 17) l[13~29] are idle state

            AND_gate_dag(eng, m[44 - 1], t[6 - 1], m[46 - 1], l[13])
            AND_gate_dag(eng, m[40 - 1], t[8 - 1], m[47 - 1], l[14])
            AND_gate_dag(eng, m[39 - 1], u[7], m[48 - 1], l[15])
            AND_gate_dag(eng, m[43 - 1], t[16 - 1], m[49 - 1], l[16])
            AND_gate_dag(eng, m[38 - 1], t[9 - 1], m[50 - 1], l[17])
            AND_gate_dag(eng, m[37 - 1], t[17 - 1], m[51 - 1], l[18])
            AND_gate_dag(eng, m[42 - 1], t[15 - 1], m[52 - 1], l[19])
            AND_gate_dag(eng, m[45 - 1], t[27 - 1], m[53 - 1], l[20])
            AND_gate_dag(eng, m[41 - 1], t[10 - 1], m[54 - 1], l[21])

            AND_gate_dag(eng, l[4], t[13 - 1], m[55 - 1], l[22])
            AND_gate_dag(eng, l[5], t[23 - 1], m[56 - 1], l[23])
            AND_gate_dag(eng, l[6], t[19 - 1], m[57 - 1], l[24])
            AND_gate_dag(eng, l[7], t[3 - 1], m[58 - 1], l[25])
            AND_gate_dag(eng, l[8], t[22 - 1], m[59 - 1], l[26])
            AND_gate_dag(eng, l[9], t[20 - 1], m[60 - 1], l[27])
            AND_gate_dag(eng, l[10], t[1 - 1], m[61 - 1], l[28])
            AND_gate_dag(eng, l[11], t[4 - 1], m[62 - 1], l[29])
            AND_gate_dag(eng, l[12], t[2 - 1], m[63 - 1], l[29]) #l[29] is not used.

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

            CNOT2(eng, m[61 - 1], m[62 - 1], l[0]);
            CNOT2(eng, m[50 - 1], m[56 - 1], l[1])
            CNOT2(eng, m[46 - 1], m[48 - 1], l[2]);
            CNOT2(eng, m[47 - 1], m[55 - 1], l[3])
            CNOT2(eng, m[54 - 1], m[58 - 1], l[4]);
            CNOT2(eng, m[49 - 1], m[61 - 1], l[5])
            CNOT2(eng, m[62 - 1], l[5], l[6]);
            CNOT2(eng, m[46 - 1], l[3], l[7])
            CNOT2(eng, m[51 - 1], m[59 - 1], l[8]);
            CNOT2(eng, m[52 - 1], m[53 - 1], l[9])
            CNOT2(eng, m[53 - 1], l[4], l[10]);
            CNOT2(eng, m[60 - 1], l[2], l[11])
            CNOT2(eng, m[48 - 1], m[51 - 1], l[12]);
            CNOT2(eng, m[50 - 1], l[0], l[13])
            CNOT2(eng, m[52 - 1], m[61 - 1], l[14]);
            CNOT2(eng, m[55 - 1], l[1], l[15])
            CNOT2(eng, m[56 - 1], l[0], l[16]);
            CNOT2(eng, m[57 - 1], l[1], l[17])
            CNOT2(eng, m[58 - 1], l[8], l[18]);
            CNOT2(eng, m[63 - 1], l[4], l[19])
            CNOT2(eng, l[0], l[1], l[20]);
            CNOT2(eng, l[1], l[7], l[21])
            CNOT2(eng, l[3], l[12], l[22]);
            CNOT2(eng, l[18], l[2], l[23])
            CNOT2(eng, l[15], l[9], l[24]);
            CNOT2(eng, l[6], l[10], l[25])
            CNOT2(eng, l[7], l[9], l[26]);
            CNOT2(eng, l[8], l[10], l[27])
            CNOT2(eng, l[11], l[14], l[28]);
            CNOT2(eng, l[11], l[17], l[29])

def AND_KS_Sbox_T4(eng, u_in, t, m, l, s, flag, round, ancilla, resource_check):
    u = []
    for i in range(8):
        u.append(u_in[7 - i])

    CNOT2(eng, u[0], u[3], t[1 - 1]);
    CNOT2(eng, u[0], u[5], t[2 - 1])
    CNOT2(eng, u[0], u[6], t[3 - 1]);
    CNOT2(eng, u[3], u[5], t[4 - 1])
    CNOT2(eng, u[4], u[6], t[5 - 1]);
    CNOT2(eng, t[1 - 1], t[5 - 1], t[6 - 1])
    CNOT2(eng, u[1], u[2], t[7 - 1]);
    CNOT2(eng, u[7], t[6 - 1], t[8 - 1])
    CNOT2(eng, u[7], t[7 - 1], t[9 - 1]);
    CNOT2(eng, t[6 - 1], t[7 - 1], t[10 - 1])
    CNOT2(eng, u[1], u[5], t[11 - 1]);
    CNOT2(eng, u[2], u[5], t[12 - 1])
    CNOT2(eng, t[3 - 1], t[4 - 1], t[13 - 1]);
    CNOT2(eng, t[6 - 1], t[11 - 1], t[14 - 1])
    CNOT2(eng, t[5 - 1], t[11 - 1], t[15 - 1]);
    CNOT2(eng, t[5 - 1], t[12 - 1], t[16 - 1])
    CNOT2(eng, t[9 - 1], t[16 - 1], t[17 - 1]);
    CNOT2(eng, u[3], u[7], t[18 - 1])
    CNOT2(eng, t[7 - 1], t[18 - 1], t[19 - 1]);
    CNOT2(eng, t[1 - 1], t[19 - 1], t[20 - 1])
    CNOT2(eng, u[6], u[7], t[21 - 1]);
    CNOT2(eng, t[7 - 1], t[21 - 1], t[22 - 1])
    CNOT2(eng, t[2 - 1], t[22 - 1], t[23 - 1]);
    CNOT2(eng, t[2 - 1], t[10 - 1], t[24 - 1])
    CNOT2(eng, t[20 - 1], t[17 - 1], t[25 - 1]);
    CNOT2(eng, t[3 - 1], t[16 - 1], t[26 - 1])
    CNOT2(eng, t[1 - 1], t[12 - 1], t[27 - 1])

    AND_gate(eng, t[13 - 1], t[6 - 1], m[1 - 1], l[13])
    AND_gate(eng, t[23 - 1], t[8 - 1], m[2 - 1], l[14])
    CNOT2(eng, t[14 - 1], m[1 - 1], m[3 - 1])
    AND_gate(eng, t[19 - 1], u[7], m[4 - 1], l[15])
    CNOT2(eng, m[4 - 1], m[1 - 1], m[5 - 1])
    AND_gate(eng, t[3 - 1], t[16 - 1], m[6 - 1], l[16])
    AND_gate(eng, t[22 - 1], t[9 - 1], m[7 - 1], l[17])
    CNOT2(eng, t[26 - 1], m[6 - 1], m[8 - 1])
    AND_gate(eng, t[20 - 1], t[17 - 1], m[9 - 1], l[18])
    CNOT2(eng, m[9 - 1], m[6 - 1], m[10 - 1])
    AND_gate(eng, t[1 - 1], t[15 - 1], m[11 - 1], l[19])
    AND_gate(eng, t[4 - 1], t[27 - 1], m[12 - 1], l[20])
    CNOT2(eng, m[12 - 1], m[11 - 1], m[13 - 1])
    AND_gate(eng, t[2 - 1], t[10 - 1], m[14 - 1], l[21])
    CNOT2(eng, m[14 - 1], m[11 - 1], m[15 - 1]);
    CNOT2(eng, m[3 - 1], m[2 - 1], m[16 - 1])
    CNOT2(eng, m[5 - 1], t[24 - 1], m[17 - 1]);
    CNOT2(eng, m[8 - 1], m[7 - 1], m[18 - 1])
    CNOT2(eng, m[10 - 1], m[15 - 1], m[19 - 1]);
    CNOT2(eng, m[16 - 1], m[13 - 1], m[20 - 1])
    CNOT2(eng, m[17 - 1], m[15 - 1], m[21 - 1]);
    CNOT2(eng, m[18 - 1], m[13 - 1], m[22 - 1])
    CNOT2(eng, m[19 - 1], t[25 - 1], m[23 - 1]);
    CNOT2(eng, m[22 - 1], m[23 - 1], m[24 - 1])

    CNOT | (m[22 - 1], l[0]);
    CNOT | (m[20 - 1], l[1])

    AND_gate(eng, m[22 - 1], m[20 - 1], m[25 - 1], l[22])
    AND_gate(eng, l[1], m[23 - 1], m[31 - 1], l[23])
    AND_gate(eng, m[21 - 1], l[0], m[34 - 1], l[24])

    CNOT | (m[24 - 1], l[3])
    CNOT2(eng, m[21 - 1], m[25 - 1], m[26 - 1]);
    CNOT2(eng, m[20 - 1], m[21 - 1], m[27 - 1])
    CNOT | (m[27 - 1], l[2])

    CNOT2(eng, m[23 - 1], m[25 - 1], m[28 - 1]);
    CNOT2(eng, m[27 - 1], m[25 - 1], m[33 - 1])

    AND_gate(eng, m[28 - 1], m[27 - 1], m[29 - 1], l[25])
    AND_gate(eng, m[26 - 1], m[24 - 1], m[30 - 1], l[26])
    AND_gate(eng, l[2], m[31 - 1], m[32 - 1], l[27])
    AND_gate(eng, l[3], m[34 - 1], m[35 - 1], l[28])

    CNOT2(eng, m[24 - 1], m[25 - 1], m[36 - 1]);
    CNOT2(eng, m[21 - 1], m[29 - 1], m[37 - 1])
    CNOT2(eng, m[32 - 1], m[33 - 1], m[38 - 1]);
    CNOT2(eng, m[23 - 1], m[30 - 1], m[39 - 1])
    CNOT2(eng, m[35 - 1], m[36 - 1], m[40 - 1]);
    CNOT2(eng, m[38 - 1], m[40 - 1], m[41 - 1])
    CNOT2(eng, m[37 - 1], m[39 - 1], m[42 - 1]);
    CNOT2(eng, m[37 - 1], m[38 - 1], m[43 - 1])
    CNOT2(eng, m[39 - 1], m[40 - 1], m[44 - 1]);
    CNOT2(eng, m[42 - 1], m[41 - 1], m[45 - 1])

    CNOT | (m[44 - 1], l[4]);
    CNOT | (m[40 - 1], l[5])
    CNOT | (m[39 - 1], l[6]);
    CNOT | (m[43 - 1], l[7])
    CNOT | (m[38 - 1], l[8]);
    CNOT | (m[37 - 1], l[9])
    CNOT | (m[42 - 1], l[10]);
    CNOT | (m[45 - 1], l[11])
    CNOT | (m[41 - 1], l[12])

    #check_ancilla(eng, l[13:30], 17) l[13~29] are idle state

    AND_gate(eng, m[44 - 1], t[6 - 1], m[46 - 1], l[13])
    AND_gate(eng, m[40 - 1], t[8 - 1], m[47 - 1], l[14])
    AND_gate(eng, m[39 - 1], u[7], m[48 - 1], l[15])
    AND_gate(eng, m[43 - 1], t[16 - 1], m[49 - 1], l[16])
    AND_gate(eng, m[38 - 1], t[9 - 1], m[50 - 1], l[17])
    AND_gate(eng, m[37 - 1], t[17 - 1], m[51 - 1], l[18])
    AND_gate(eng, m[42 - 1], t[15 - 1], m[52 - 1], l[19])
    AND_gate(eng, m[45 - 1], t[27 - 1], m[53 - 1], l[20])
    AND_gate(eng, m[41 - 1], t[10 - 1], m[54 - 1], l[21])

    AND_gate(eng, l[4], t[13 - 1], m[55 - 1], l[22])
    AND_gate(eng, l[5], t[23 - 1], m[56 - 1], l[23])
    AND_gate(eng, l[6], t[19 - 1], m[57 - 1], l[24])
    AND_gate(eng, l[7], t[3 - 1], m[58 - 1], l[25])
    AND_gate(eng, l[8], t[22 - 1], m[59 - 1], l[26])
    AND_gate(eng, l[9], t[20 - 1], m[60 - 1], l[27])
    AND_gate(eng, l[10], t[1 - 1], m[61 - 1], l[28])
    AND_gate(eng, l[11], t[4 - 1], m[62 - 1], l[29])
    AND_gate(eng, l[12], t[2 - 1], m[63 - 1], ancilla)

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

    CNOT2(eng, m[61 - 1], m[62 - 1], l[0]);
    CNOT2(eng, m[50 - 1], m[56 - 1], l[1])
    CNOT2(eng, m[46 - 1], m[48 - 1], l[2]);
    CNOT2(eng, m[47 - 1], m[55 - 1], l[3])
    CNOT2(eng, m[54 - 1], m[58 - 1], l[4]);
    CNOT2(eng, m[49 - 1], m[61 - 1], l[5])
    CNOT2(eng, m[62 - 1], l[5], l[6]);
    CNOT2(eng, m[46 - 1], l[3], l[7])
    CNOT2(eng, m[51 - 1], m[59 - 1], l[8]);
    CNOT2(eng, m[52 - 1], m[53 - 1], l[9])
    CNOT2(eng, m[53 - 1], l[4], l[10]);
    CNOT2(eng, m[60 - 1], l[2], l[11])
    CNOT2(eng, m[48 - 1], m[51 - 1], l[12]);
    CNOT2(eng, m[50 - 1], l[0], l[13])
    CNOT2(eng, m[52 - 1], m[61 - 1], l[14]);
    CNOT2(eng, m[55 - 1], l[1], l[15])
    CNOT2(eng, m[56 - 1], l[0], l[16]);
    CNOT2(eng, m[57 - 1], l[1], l[17])
    CNOT2(eng, m[58 - 1], l[8], l[18]);
    CNOT2(eng, m[63 - 1], l[4], l[19])
    CNOT2(eng, l[0], l[1], l[20]);
    CNOT2(eng, l[1], l[7], l[21])
    CNOT2(eng, l[3], l[12], l[22]);
    CNOT2(eng, l[18], l[2], l[23])
    CNOT2(eng, l[15], l[9], l[24]);
    CNOT2(eng, l[6], l[10], l[25])
    CNOT2(eng, l[7], l[9], l[26]);
    CNOT2(eng, l[8], l[10], l[27])
    CNOT2(eng, l[11], l[14], l[28]);
    CNOT2(eng, l[11], l[17], l[29])

    CNOT2(eng, l[6], l[24], s[7]);
    CNOT2(eng, l[16], l[26], s[6])
    X | s[6]
    CNOT2(eng, l[19], l[28], s[5])
    X | s[5]

    CNOT2(eng, l[6], l[21], s[4]);
    CNOT2(eng, l[20], l[22], s[3])
    CNOT2(eng, l[25], l[29], s[2]);
    CNOT2(eng, l[13], l[27], s[1])
    X | s[1]
    CNOT2(eng, l[6], l[23], s[0])
    X | s[0]

    return s

def AND_Sbox_T4(eng, u_in, t, m, l, s, flag, round, resource_check):
    u = []
    for i in range(8):
        u.append(u_in[7 - i])

    CNOT2(eng, u[0], u[3], t[1 - 1]);
    CNOT2(eng, u[0], u[5], t[2 - 1])
    CNOT2(eng, u[0], u[6], t[3 - 1]);
    CNOT2(eng, u[3], u[5], t[4 - 1])
    CNOT2(eng, u[4], u[6], t[5 - 1]);
    CNOT2(eng, t[1 - 1], t[5 - 1], t[6 - 1])
    CNOT2(eng, u[1], u[2], t[7 - 1]);
    CNOT2(eng, u[7], t[6 - 1], t[8 - 1])
    CNOT2(eng, u[7], t[7 - 1], t[9 - 1]);
    CNOT2(eng, t[6 - 1], t[7 - 1], t[10 - 1])
    CNOT2(eng, u[1], u[5], t[11 - 1]);
    CNOT2(eng, u[2], u[5], t[12 - 1])
    CNOT2(eng, t[3 - 1], t[4 - 1], t[13 - 1]);
    CNOT2(eng, t[6 - 1], t[11 - 1], t[14 - 1])
    CNOT2(eng, t[5 - 1], t[11 - 1], t[15 - 1]);
    CNOT2(eng, t[5 - 1], t[12 - 1], t[16 - 1])
    CNOT2(eng, t[9 - 1], t[16 - 1], t[17 - 1]);
    CNOT2(eng, u[3], u[7], t[18 - 1])
    CNOT2(eng, t[7 - 1], t[18 - 1], t[19 - 1]);
    CNOT2(eng, t[1 - 1], t[19 - 1], t[20 - 1])
    CNOT2(eng, u[6], u[7], t[21 - 1]);
    CNOT2(eng, t[7 - 1], t[21 - 1], t[22 - 1])
    CNOT2(eng, t[2 - 1], t[22 - 1], t[23 - 1]);
    CNOT2(eng, t[2 - 1], t[10 - 1], t[24 - 1])
    CNOT2(eng, t[20 - 1], t[17 - 1], t[25 - 1]);
    CNOT2(eng, t[3 - 1], t[16 - 1], t[26 - 1])
    CNOT2(eng, t[1 - 1], t[12 - 1], t[27 - 1])

    AND_gate(eng, t[13 - 1], t[6 - 1], m[1 - 1], l[13])
    AND_gate(eng, t[23 - 1], t[8 - 1], m[2 - 1], l[14])
    CNOT2(eng, t[14 - 1], m[1 - 1], m[3 - 1])
    AND_gate(eng, t[19 - 1], u[7], m[4 - 1], l[15])
    CNOT2(eng, m[4 - 1], m[1 - 1], m[5 - 1])
    AND_gate(eng, t[3 - 1], t[16 - 1], m[6 - 1], l[16])
    AND_gate(eng, t[22 - 1], t[9 - 1], m[7 - 1], l[17])
    CNOT2(eng, t[26 - 1], m[6 - 1], m[8 - 1])
    AND_gate(eng, t[20 - 1], t[17 - 1], m[9 - 1], l[18])
    CNOT2(eng, m[9 - 1], m[6 - 1], m[10 - 1])
    AND_gate(eng, t[1 - 1], t[15 - 1], m[11 - 1], l[19])
    AND_gate(eng, t[4 - 1], t[27 - 1], m[12 - 1], l[20])
    CNOT2(eng, m[12 - 1], m[11 - 1], m[13 - 1])
    AND_gate(eng, t[2 - 1], t[10 - 1], m[14 - 1], l[21])
    CNOT2(eng, m[14 - 1], m[11 - 1], m[15 - 1]);
    CNOT2(eng, m[3 - 1], m[2 - 1], m[16 - 1])
    CNOT2(eng, m[5 - 1], t[24 - 1], m[17 - 1]);
    CNOT2(eng, m[8 - 1], m[7 - 1], m[18 - 1])
    CNOT2(eng, m[10 - 1], m[15 - 1], m[19 - 1]);
    CNOT2(eng, m[16 - 1], m[13 - 1], m[20 - 1])
    CNOT2(eng, m[17 - 1], m[15 - 1], m[21 - 1]);
    CNOT2(eng, m[18 - 1], m[13 - 1], m[22 - 1])
    CNOT2(eng, m[19 - 1], t[25 - 1], m[23 - 1]);
    CNOT2(eng, m[22 - 1], m[23 - 1], m[24 - 1])

    CNOT | (m[22 - 1], l[0]);
    CNOT | (m[20 - 1], l[1])

    AND_gate(eng, m[22 - 1], m[20 - 1], m[25 - 1], l[22])
    AND_gate(eng, l[1], m[23 - 1], m[31 - 1], l[23])
    AND_gate(eng, m[21 - 1], l[0], m[34 - 1], l[24])

    CNOT | (m[24 - 1], l[3])
    CNOT2(eng, m[21 - 1], m[25 - 1], m[26 - 1]);
    CNOT2(eng, m[20 - 1], m[21 - 1], m[27 - 1])
    CNOT | (m[27 - 1], l[2])

    CNOT2(eng, m[23 - 1], m[25 - 1], m[28 - 1]);
    CNOT2(eng, m[27 - 1], m[25 - 1], m[33 - 1])

    AND_gate(eng, m[28 - 1], m[27 - 1], m[29 - 1], l[25])
    AND_gate(eng, m[26 - 1], m[24 - 1], m[30 - 1], l[26])
    AND_gate(eng, l[2], m[31 - 1], m[32 - 1], l[27])
    AND_gate(eng, l[3], m[34 - 1], m[35 - 1], l[28])

    CNOT2(eng, m[24 - 1], m[25 - 1], m[36 - 1]);
    CNOT2(eng, m[21 - 1], m[29 - 1], m[37 - 1])
    CNOT2(eng, m[32 - 1], m[33 - 1], m[38 - 1]);
    CNOT2(eng, m[23 - 1], m[30 - 1], m[39 - 1])
    CNOT2(eng, m[35 - 1], m[36 - 1], m[40 - 1]);
    CNOT2(eng, m[38 - 1], m[40 - 1], m[41 - 1])
    CNOT2(eng, m[37 - 1], m[39 - 1], m[42 - 1]);
    CNOT2(eng, m[37 - 1], m[38 - 1], m[43 - 1])
    CNOT2(eng, m[39 - 1], m[40 - 1], m[44 - 1]);
    CNOT2(eng, m[42 - 1], m[41 - 1], m[45 - 1])

    CNOT | (m[44 - 1], l[4]);
    CNOT | (m[40 - 1], l[5])
    CNOT | (m[39 - 1], l[6]);
    CNOT | (m[43 - 1], l[7])
    CNOT | (m[38 - 1], l[8]);
    CNOT | (m[37 - 1], l[9])
    CNOT | (m[42 - 1], l[10]);
    CNOT | (m[45 - 1], l[11])
    CNOT | (m[41 - 1], l[12])

    #check_ancilla(eng, l[13:30], 17) l[13~29] are idle state

    AND_gate(eng, m[44 - 1], t[6 - 1], m[46 - 1], l[13])
    AND_gate(eng, m[40 - 1], t[8 - 1], m[47 - 1], l[14])
    AND_gate(eng, m[39 - 1], u[7], m[48 - 1], l[15])
    AND_gate(eng, m[43 - 1], t[16 - 1], m[49 - 1], l[16])
    AND_gate(eng, m[38 - 1], t[9 - 1], m[50 - 1], l[17])
    AND_gate(eng, m[37 - 1], t[17 - 1], m[51 - 1], l[18])
    AND_gate(eng, m[42 - 1], t[15 - 1], m[52 - 1], l[19])
    AND_gate(eng, m[45 - 1], t[27 - 1], m[53 - 1], l[20])
    AND_gate(eng, m[41 - 1], t[10 - 1], m[54 - 1], l[21])

    AND_gate(eng, l[4], t[13 - 1], m[55 - 1], l[22])
    AND_gate(eng, l[5], t[23 - 1], m[56 - 1], l[23])
    AND_gate(eng, l[6], t[19 - 1], m[57 - 1], l[24])
    AND_gate(eng, l[7], t[3 - 1], m[58 - 1], l[25])
    AND_gate(eng, l[8], t[22 - 1], m[59 - 1], l[26])
    AND_gate(eng, l[9], t[20 - 1], m[60 - 1], l[27])
    AND_gate(eng, l[10], t[1 - 1], m[61 - 1], l[28])
    AND_gate(eng, l[11], t[4 - 1], m[62 - 1], l[29])
    AND_gate(eng, l[12], t[2 - 1], m[63 - 1], s[0])

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

    CNOT2(eng, m[61 - 1], m[62 - 1], l[0]);
    CNOT2(eng, m[50 - 1], m[56 - 1], l[1])
    CNOT2(eng, m[46 - 1], m[48 - 1], l[2]);
    CNOT2(eng, m[47 - 1], m[55 - 1], l[3])
    CNOT2(eng, m[54 - 1], m[58 - 1], l[4]);
    CNOT2(eng, m[49 - 1], m[61 - 1], l[5])
    CNOT2(eng, m[62 - 1], l[5], l[6]);
    CNOT2(eng, m[46 - 1], l[3], l[7])
    CNOT2(eng, m[51 - 1], m[59 - 1], l[8]);
    CNOT2(eng, m[52 - 1], m[53 - 1], l[9])
    CNOT2(eng, m[53 - 1], l[4], l[10]);
    CNOT2(eng, m[60 - 1], l[2], l[11])
    CNOT2(eng, m[48 - 1], m[51 - 1], l[12]);
    CNOT2(eng, m[50 - 1], l[0], l[13])
    CNOT2(eng, m[52 - 1], m[61 - 1], l[14]);
    CNOT2(eng, m[55 - 1], l[1], l[15])
    CNOT2(eng, m[56 - 1], l[0], l[16]);
    CNOT2(eng, m[57 - 1], l[1], l[17])
    CNOT2(eng, m[58 - 1], l[8], l[18]);
    CNOT2(eng, m[63 - 1], l[4], l[19])
    CNOT2(eng, l[0], l[1], l[20]);
    CNOT2(eng, l[1], l[7], l[21])
    CNOT2(eng, l[3], l[12], l[22]);
    CNOT2(eng, l[18], l[2], l[23])
    CNOT2(eng, l[15], l[9], l[24]);
    CNOT2(eng, l[6], l[10], l[25])
    CNOT2(eng, l[7], l[9], l[26]);
    CNOT2(eng, l[8], l[10], l[27])
    CNOT2(eng, l[11], l[14], l[28]);
    CNOT2(eng, l[11], l[17], l[29])

    CNOT2(eng, l[6], l[24], s[7]);
    CNOT2(eng, l[16], l[26], s[6])
    X | s[6]
    CNOT2(eng, l[19], l[28], s[5])
    X | s[5]

    CNOT2(eng, l[6], l[21], s[4]);
    CNOT2(eng, l[20], l[22], s[3])
    CNOT2(eng, l[25], l[29], s[2]);
    CNOT2(eng, l[13], l[27], s[1])
    X | s[1]
    CNOT2(eng, l[6], l[23], s[0])
    X | s[0]

    return s

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
    with Dagger(eng):
        Measure | c

    #if(eng, c): # consider upper bound
    X | c
    Sdag | a # consider dag + dag -> S
    Sdag | b # consider dag + dag -> S
    CNOT | (a, b)
    S | b #consider dag -> Sdag
    CNOT | (a, b)

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

#
# Simulate = ClassicalSimulator()
# eng = MainEngine(Simulate)
# AES(eng, 0)

print('Estimate cost...')
Resource = ResourceCounter()
eng = MainEngine(Resource)
AES(eng, 1)
print(Resource)
print('\n')
eng.flush()