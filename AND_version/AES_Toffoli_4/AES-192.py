from projectq import MainEngine
from projectq.ops import H, CNOT, Measure, Toffoli, X, All, T, Tdagger, S, Tdag, Sdag
from projectq.backends import CircuitDrawer, ResourceCounter, ClassicalSimulator
from projectq.meta import Loop, Compute, Uncompute, Control, Dagger


def AES(eng, resource_check):

    x0 = eng.allocate_qureg(32)
    x1 = eng.allocate_qureg(32)
    x2 = eng.allocate_qureg(32)
    x3 = eng.allocate_qureg(32)

    k = eng.allocate_qureg(192)

    if(resource_check != 1):
        Round_constant_XOR(eng, x3, 0x12345678, 32)
        Round_constant_XOR(eng, x2, 0x12345678, 32)
        Round_constant_XOR(eng, x1, 0x12345678, 32)
        Round_constant_XOR(eng, x0, 0x12345678, 32)

        Round_constant_XOR(eng, k, 0x123456781234567812345678123456781234567812345678, 192)

        print('Plaintext  \n')
        print_state(eng, x3, 8)
        print_state(eng, x2, 8)
        print_state(eng, x1, 8)
        print_state(eng, x0, 8)

        print('Key  \n')
        print_state(eng, k[160:192], 8)
        print_state(eng, k[128:160], 8)
        print_state(eng, k[96:128], 8)
        print_state(eng, k[64:96], 8)
        print_state(eng, k[32:64], 8)
        print_state(eng, k[0:32], 8)

    y = eng.allocate_qureg(540)  # 22 * 20
    t = eng.allocate_qureg(1260)  # 68 * 20
    z = eng.allocate_qureg(600)  # 18 * 20

    ancilla = eng.allocate_qureg(4)

    k_i = 0
    i = -1

    # 16 * 12 + 4 * 8 , 16 * 10 + 4* 10
    for p in range(4):

        AddRoundkey(eng, x0, x1, x2, x3, k)

        i = i + 1
        print('Round', i)
        s = eng.allocate_qureg(128)
        SBox_bp12_all(eng, x0, x1, x2, x3, y, t, z, s, i, resource_check)
        x0, x1, x2, x3 = Shiftrow(eng, x0, x1, x2, x3)

        if(i!=11):
            x0 = Mixcolumns(eng, x0)
            x1 = Mixcolumns(eng, x1)
            x2 = Mixcolumns(eng, x2)
            x3 = Mixcolumns(eng, x3)

        Keyshedule(eng, k, i, y, t, z, i, k_i, ancilla, resource_check)
        AddRoundkey_1(eng, x0, x1, x2, x3, k)
        KeyUpdate(eng, k)
        k_i = k_i + 1
        AddRoundkey_2(eng, x0, x1, x2, x3, k)

        i = i+1
        ################# next round ###########################
        print('Round', i)
        s = eng.allocate_qureg(128)
        SBox_bp12_all(eng, x0, x1, x2, x3, y, t, z, s, i, resource_check)
        x0, x1, x2, x3 = Shiftrow(eng, x0, x1, x2, x3)

        if (i != 11):
            x0 = Mixcolumns(eng, x0)
            x1 = Mixcolumns(eng, x1)
            x2 = Mixcolumns(eng, x2)
            x3 = Mixcolumns(eng, x3)

        Keyshedule(eng, k, i, y, t, z, i, k_i, ancilla, resource_check)
        AddRoundkey_3(eng, x0, x1, x2, x3, k)
        KeyUpdate(eng, k)
        k_i = k_i + 1

        i =i+1
        ################# next round ###########################
        print('Round', i)
        s = eng.allocate_qureg(128)
        SBox_bp12_all(eng, x0, x1, x2, x3, y, t, z, s, i, resource_check)

        x0, x1, x2, x3 = Shiftrow(eng, x0, x1, x2, x3)

        if (i != 11):
            x0 = Mixcolumns(eng, x0)
            x1 = Mixcolumns(eng, x1)
            x2 = Mixcolumns(eng, x2)
            x3 = Mixcolumns(eng, x3)

    AddRoundkey(eng, x0, x1, x2, x3, k)

    if(resource_check != 1):
        print('\nCiphertext ')
        print_state(eng, x3, 8)
        print_state(eng, x2, 8)
        print_state(eng, x1, 8)
        print_state(eng, x0, 8)

def Keyshedule(eng, k, i, y, t, z, round, k_i, ancilla, resource_check):

    Rcon = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]

    new_k0 = []
    for j in range(32):
        new_k0.append(k[(24+j) % 32])

    for j in range(4): #22 68 18
         k[160 + 8 * j: 160 + 8 * (j + 1)] = AND_KS_Sbox_T4(eng, new_k0[8 * j:8 * (j + 1)], y[432 + 27 * j:432 + 27 * (j + 1)],t[1008 + 63 * j:1008 + 63 * (j + 1)],
                                                    z[480 + 30 * j:480 + 30 * (j + 1)], k[160 + 8 * j: 160 + 8 * (j + 1)], 1, round, ancilla[j], resource_check)

    for j in range(8):
        if ((Rcon[k_i] >> j) & 1):
            X | k[184+j]

def KeyUpdate(eng, k):
    CNOT32(eng, k[160:192], k[128:160])
    CNOT32(eng, k[128:160], k[96:128])
    CNOT32(eng, k[96:128], k[64:96])
    CNOT32(eng, k[64:96], k[32:64])
    CNOT32(eng, k[32:64], k[0:32])

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

    CNOT32(eng, k[64:96], x0)
    CNOT32(eng, k[96:128], x1)
    CNOT32(eng, k[128:160], x2)
    CNOT32(eng, k[160:192], x3)

def AddRoundkey_1(eng, x0, x1, x2, x3, k):

    CNOT32(eng, k[0:32], x2)
    CNOT32(eng, k[32:64], x3)

def AddRoundkey_2(eng, x0, x1, x2, x3, k):

    CNOT32(eng, k[128:160], x0) #128 : 160
    CNOT32(eng, k[160:192], x1) # 160 : 192

def AddRoundkey_3(eng, x0, x1, x2, x3, k):

    CNOT32(eng, k[96:128], x3)
    CNOT32(eng, k[64:96], x2)
    CNOT32(eng, k[32:64], x1) #32:64
    CNOT32(eng, k[0:32], x0) #0:32

def Mixcolumns(eng, xi):

    x = []
    for i in range(8):
        x.append(xi[24+i])
    for i in range(8):
        x.append(xi[16+i])
    for i in range(8):
        x.append(xi[8+i])
    for i in range(8):
        x.append(xi[i])

    CNOT | (x[31], x[23])
    CNOT | (x[15], x[31])
    CNOT | (x[4], x[12])
    CNOT | (x[21], x[13])
    CNOT | (x[9], x[17])
    CNOT | (x[27], x[11])
    CNOT | (x[28], x[4])
    CNOT | (x[5], x[21])
    CNOT | (x[24], x[0])
    CNOT | (x[7], x[15])
    CNOT | (x[1], x[9])

    CNOT | (x[6], x[14])
    CNOT | (x[16], x[24])
    CNOT | (x[22], x[6])
    CNOT | (x[31], x[16])
    CNOT | (x[8], x[24])
    CNOT | (x[26], x[18])
    CNOT | (x[30], x[22])
    CNOT | (x[10], x[26])
    CNOT | (x[23], x[8])
    CNOT | (x[13], x[30])

    CNOT | (x[29], x[13])
    CNOT | (x[13], x[5])
    CNOT | (x[4], x[29])
    CNOT | (x[11], x[4])
    CNOT | (x[19], x[11])
    CNOT | (x[12], x[13])
    CNOT | (x[23], x[19])
    CNOT | (x[31], x[4])
    CNOT | (x[20], x[12])
    CNOT | (x[12], x[28])
    #####################
    CNOT | (x[27], x[20])
    CNOT | (x[19], x[20])
    CNOT | (x[31], x[27])
    CNOT | (x[15], x[12])
    CNOT | (x[3], x[27])
    CNOT | (x[11], x[3])
    CNOT | (x[2], x[11])
    CNOT | (x[18], x[19])
    CNOT | (x[10], x[11])
    CNOT | (x[18], x[10])

    CNOT | (x[2], x[18])
    CNOT | (x[9], x[10])
    CNOT | (x[9], x[2])
    CNOT | (x[17], x[18])
    CNOT | (x[25], x[17])
    CNOT | (x[17], x[1])
    CNOT | (x[24], x[25])
    CNOT | (x[8], x[9])
    CNOT | (x[15], x[24])
    CNOT | (x[15], x[11])

    CNOT | (x[0], x[8])
    CNOT | (x[23], x[15])
    CNOT | (x[16], x[17])
    CNOT | (x[0], x[16])
    CNOT | (x[31], x[0])
    CNOT | (x[23], x[16])
    CNOT | (x[6], x[23])
    CNOT | (x[7], x[31])
    CNOT | (x[22], x[31])
    CNOT | (x[6], x[30])
    CNOT | (x[14], x[7])
    #####################
    CNOT | (x[21], x[14])
    CNOT | (x[5], x[6])
    CNOT | (x[21], x[22])
    CNOT | (x[29], x[5])
    CNOT | (x[28], x[21])
    CNOT | (x[21], x[29])
    CNOT | (x[13], x[21])
    CNOT | (x[27], x[12])
    CNOT | (x[26], x[27])
    CNOT | (x[20], x[28])

    CNOT | (x[4], x[20])
    CNOT | (x[1], x[26])
    CNOT | (x[30], x[14])
    CNOT | (x[12], x[4])
    CNOT | (x[19], x[3])
    CNOT | (x[27], x[19])
    CNOT | (x[25], x[1])
    CNOT | (x[24], x[0])
    CNOT | (x[0], x[1])
    CNOT | (x[26], x[2])

    CNOT | (x[9], x[25])
    CNOT | (x[7], x[15])
    CNOT | (x[23], x[7])
    CNOT | (x[14], x[6])
    CNOT | (x[17], x[9])
    CNOT | (x[31], x[23])
    CNOT | (x[18], x[26])
    CNOT | (x[6], x[22])
    CNOT | (x[0], x[17])
    CNOT | (x[11], x[27])

    y = [] #24~31 ->0~7
           #16~23 ->8~15
           #8~15 ->16~23
           #0~7 -> 24~31

    y.append(x[0])
    y.append(x[1])
    y.append(x[26])
    y.append(x[27])
    y.append(x[12])
    y.append(x[5])
    y.append(x[22])
    y.append(x[23])

    y.append(x[8])
    y.append(x[25])
    y.append(x[2])
    y.append(x[3])
    y.append(x[28])
    y.append(x[21])
    y.append(x[6])
    y.append(x[31])

    y.append(x[16])
    y.append(x[9])
    y.append(x[18])
    y.append(x[19])
    y.append(x[20])
    y.append(x[29])
    y.append(x[30])
    y.append(x[7])

    y.append(x[24])
    y.append(x[17])
    y.append(x[10])
    y.append(x[11])
    y.append(x[4])
    y.append(x[13])
    y.append(x[14])
    y.append(x[15])

    return y

def CNOT2(eng, a, b, c):

    CNOT | (a, c)
    CNOT | (b, c)

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

    # check_ancilla(eng, l[13:30], 17) l[13~29] are idle state

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

    if (round != 11):
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
            AND_gate_dag(eng, l[12], t[2 - 1], m[63 - 1], ancilla)

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

    if (round != 11):
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
            AND_gate_dag(eng, l[12], t[2 - 1], m[63 - 1], s[0])

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
