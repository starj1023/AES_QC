from projectq import MainEngine
from projectq.ops import H, CNOT, Measure, Toffoli, X, All, T, Tdagger, S, Tdag
from projectq.backends import CircuitDrawer, ResourceCounter, ClassicalSimulator
from projectq.meta import Loop, Compute, Uncompute, Control, Dagger


def AES(eng, resource_check):

    x0 = eng.allocate_qureg(32)
    x1 = eng.allocate_qureg(32)
    x2 = eng.allocate_qureg(32)
    x3 = eng.allocate_qureg(32)

    k = eng.allocate_qureg(192)
    mq1 = eng.allocate_qureg(420)  # We do not count these qubits

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

    q = eng.allocate_qureg(1460)
    q_two = eng.allocate_qureg(1200)

    k_i = 0
    i = -1
    for p in range(4):

        AddRoundkey(eng, x0, x1, x2, x3, k)

        if(i != -1):
            if (i % 2 == 0):
                Clean_ancilla(eng, t0, t1, t2, t3, k[32:64], q, 1, resource_check)
            else:
                Clean_ancilla_two(eng, t0, t1, t2, t3, k[32:64], q_two, q, 1, resource_check)

        i = i + 1


        print('Round', i)
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

        if(i%2 == 0):
            SBox_bp12_all(eng, x0, x1, x2, x3, q, s, i, resource_check)
        else:
            SBox_bp12_all_two(eng, x0, x1, x2, x3, q_two, q, s, i, resource_check)

        x0, x1, x2, x3 = Shiftrow(eng, x0, x1, x2, x3)

        x0 = XOR105(eng, x0, mq1[0:105], i)
        x1 = XOR105(eng, x1, mq1[105:210], i)
        x2 = XOR105(eng, x2, mq1[210:315], i)
        x3 = XOR105(eng, x3, mq1[315:420], i)

        if (i % 2 == 0):
            Keyshedule(eng, k, i, q, i, k_i, resource_check)
        else:
            Keyshedule_two(eng, k, i, q_two, q, i, k_i, resource_check)

        AddRoundkey_1(eng, x0, x1, x2, x3, k)

        KeyUpdate(eng, k)
        k_i = k_i + 1
        AddRoundkey_2(eng, x0, x1, x2, x3, k)

        CNOT32(eng, k[0:32], k[32:64])
        if (i % 2 == 0):
            Clean_ancilla(eng, t0, t1, t2, t3, k[32:64], q, 0, resource_check)
        else:
            Clean_ancilla_two(eng, t0, t1, t2, t3, k[32:64], q_two, q, 0, resource_check)

        i = i+1
        ################# next round ###########################
        print('Round', i)
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
            SBox_bp12_all(eng, x0, x1, x2, x3, q, s, i, resource_check)
        else:
            SBox_bp12_all_two(eng, x0, x1, x2, x3, q_two, q, s, i, resource_check)

        x0, x1, x2, x3 = Shiftrow(eng, x0, x1, x2, x3)

        x0 = XOR105(eng, x0, mq1[0:105], i)
        x1 = XOR105(eng, x1, mq1[105:210], i)
        x2 = XOR105(eng, x2, mq1[210:315], i)
        x3 = XOR105(eng, x3, mq1[315:420], i)

        if (i % 2 == 0):
            Keyshedule(eng, k, i, q, i, k_i, resource_check)
        else:
            Keyshedule_two(eng, k, i, q_two, q, i, k_i, resource_check)

        CNOT32(eng, k[0:32], k[32:64])

        AddRoundkey_3(eng, x0, x1, x2, x3, k)
        KeyUpdate(eng, k)

        CNOT32(eng, k[0:32], k[32:64])
        if (i != 10):
            if (i % 2 == 0 ):
                Clean_ancilla(eng, t0, t1, t2, t3, k[32:64], q, 0, resource_check)
            else:
                Clean_ancilla_two(eng, t0, t1, t2, t3, k[32:64], q_two, q, 0, resource_check)
        else:
            Clean_ancilla_special(eng, t0, t1, t2, t3, k[32:64], q, resource_check)

        i = i + 1
        ################# next round ###########################
        print('Round', i)
        if (i != 11):
            s = eng.allocate_qureg(128)
        else:
            s = recycle(eng, q) # key: 0~8, 34~45, Sbox: 6~8

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
            SBox_bp12_all(eng, x0, x1, x2, x3, q, s, i, resource_check)
        else:
            SBox_bp12_all_two(eng, x0, x1, x2, x3, q_two, q, s, i, resource_check)

        if(i!= 11):
            CNOT32(eng, k[0:32], k[32:64])

        x0, x1, x2, x3 = Shiftrow(eng, x0, x1, x2, x3)

        if (i != 11):
            x0 = XOR105(eng, x0, mq1[0:105], i)
            x1 = XOR105(eng, x1, mq1[105:210], i)
            x2 = XOR105(eng, x2, mq1[210:315], i)
            x3 = XOR105(eng, x3, mq1[315:420], i)

        k_i = k_i + 1

    AddRoundkey(eng, x0, x1, x2, x3, k)

    if(resource_check != 1):
        print('\nCiphertext ')
        print_state(eng, x3, 8)
        print_state(eng, x2, 8)
        print_state(eng, x1, 8)
        print_state(eng, x0, 8)

def recycle(eng, q):
    s1 = []
    for i in range(16):
        s1.append(q[6 + 73 * i])
        s1.append(q[7 + 73 * i])
        s1.append(q[8 + 73 * i])

    for i in range(4):
        s1.append(q[1168 + 73 * i])
        s1.append(q[1168 + 1 + 73 * i])
        s1.append(q[1168 + 2 + 73 * i])
        s1.append(q[1168 + 3 + 73 * i])
        s1.append(q[1168 + 4 + 73 * i])
        s1.append(q[1168 + 5 + 73 * i])
        s1.append(q[1168 + 6 + 73 * i])
        s1.append(q[1168 + 7 + 73 * i])
        s1.append(q[1168 + 8 + 73 * i])
        s1.append(q[1168 + 34 + 73 * i])
        s1.append(q[1168 + 35 + 73 * i])
        s1.append(q[1168 + 36 + 73 * i])
        s1.append(q[1168 + 37 + 73 * i])
        s1.append(q[1168 + 38 + 73 * i])
        s1.append(q[1168 + 39 + 73 * i])
        s1.append(q[1168 + 40 + 73 * i])
        s1.append(q[1168 + 41 + 73 * i])
        s1.append(q[1168 + 42 + 73 * i])
        s1.append(q[1168 + 43 + 73 * i])
        s1.append(q[1168 + 44 + 73 * i])
        s1.append(q[1168 + 45 + 73 * i])

    return s1

def Clean_ancilla(eng, x0, x1, x2, x3, temp_k, q, flag, resource_check):


    for i in range(4):
        Uncompute_sbox(eng, x0[8 * i:8 * (i + 1)], q[73 * i:73 * (i + 1)], resource_check)
        Uncompute_sbox(eng, x1[8 * i:8 * (i + 1)], q[73 * (i + 4):73 * (i + 5)], resource_check)
        Uncompute_sbox(eng, x2[8 * i:8 * (i + 1)], q[73 * (i + 8):73 * (i + 9)], resource_check)
        Uncompute_sbox(eng, x3[8 * i:8 * (i + 1)], q[73 * (i + 12):73 * (i + 13)], resource_check)

    if(flag != 1):
        new_k0 = []
        for j in range(32):
            new_k0.append(temp_k[(24 + j) % 32])

        for i in range(4):
            Uncompute_sbox_key(eng, new_k0[8 * i:8 * (i + 1)], q[1168 + 73 * i: 1168 + 73 * (i + 1)], resource_check)

def Clean_ancilla_two(eng, x0, x1, x2, x3, temp_k, q2, q1, flag, resource_check):

    for i in range(4):
        Uncompute_sbox_two(eng, x0[8 * i:8 * (i + 1)], q2[60 * i:60 * (i + 1)], q1[73 * i:73 * (i + 1)], resource_check)
        Uncompute_sbox_two(eng, x1[8 * i:8 * (i + 1)], q2[60 * (i + 4):60 * (i + 5)], q1[73 * (i+4):73 * (i + 5)], resource_check)
        Uncompute_sbox_two(eng, x2[8 * i:8 * (i + 1)], q2[60 * (i + 8):60 * (i + 9)], q1[73 * (i+8):73 * (i + 9)], resource_check)
        Uncompute_sbox_two(eng, x3[8 * i:8 * (i + 1)], q2[60 * (i + 12):60 * (i + 13)], q1[73 * (i+12):73 * (i + 13)], resource_check)

    if (flag != 1):
        new_k0 = []
        for j in range(32):
            new_k0.append(temp_k[(24 + j) % 32])

        for i in range(4):
            Uncompute_sbox_key_two(eng, new_k0[8 * i:8 * (i + 1)], q2[960 + 60 * i:960 + 60 * (i + 1)], q1[1168 + 73 * i: 1168 + 73 * (i + 1)], resource_check)

def Clean_ancilla_special(eng, x0, x1, x2, x3, temp_k, q, resource_check):

    for i in range(4):
        Uncompute_sbox_special(eng, x0[8 * i:8 * (i + 1)], q[73 * i:73 * (i + 1)], resource_check)
        Uncompute_sbox_special(eng, x1[8 * i:8 * (i + 1)], q[73 * (i + 4):73 * (i + 5)], resource_check)
        Uncompute_sbox_special(eng, x2[8 * i:8 * (i + 1)], q[73 * (i + 8):73 * (i + 9)], resource_check)
        Uncompute_sbox_special(eng, x3[8 * i:8 * (i + 1)], q[73 * (i + 12):73 * (i + 13)], resource_check)

    new_k0 = []
    for j in range(32):
        new_k0.append(temp_k[(24 + j) % 32])

    for i in range(4):
        Uncompute_sbox_key_special(eng, new_k0[8 * i:8 * (i + 1)], q[1168 + 73 * i: 1168 + 73 * (i + 1)], resource_check)

def Clean_ancilla_omit_key_two(eng, x0, x1, x2, x3, temp_k, q2, q1, flag, resource_check):

    for i in range(4):
        Uncompute_sbox_two(eng, x0[8 * i:8 * (i + 1)], q2[60 * i:60 * (i + 1)], q1[73 * i:73 * (i + 1)], resource_check)
        Uncompute_sbox_two(eng, x1[8 * i:8 * (i + 1)], q2[60 * (i + 4):60 * (i + 5)], q1[73 * (i + 4):73 * (i + 5)],
                           resource_check)
        Uncompute_sbox_two(eng, x2[8 * i:8 * (i + 1)], q2[60 * (i + 8):60 * (i + 9)], q1[73 * (i + 8):73 * (i + 9)],
                           resource_check)
        Uncompute_sbox_two(eng, x3[8 * i:8 * (i + 1)], q2[60 * (i + 12):60 * (i + 13)], q1[73 * (i + 12):73 * (i + 13)],
                           resource_check)

        new_k0 = []
        for j in range(32):
            new_k0.append(temp_k[(24 + j) % 32])

        for i in range(4):
            Uncompute_sbox_key_two(eng, new_k0[8 * i:8 * (i + 1)], q2[960 + 60 * i:960 + 60 * (i + 1)],
                                   q1[1168 + 73 * i: 1168 + 73 * (i + 1)], resource_check)

def Keyshedule(eng, k, i, q, round, k_i, resource_check):

    Rcon = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]

    new_k0 = []
    for j in range(32):
        new_k0.append(k[(24+j) % 32])

    for j in range(4): #22 68 18
         k[160 + 8 * j: 160 + 8 * (j + 1)] = Sbox(eng, new_k0[8 * j:8 * (j + 1)], q[1168 + 73 * j:1168 + 73 * (j + 1)],
                                                  k[160 + 8 * j: 160 + 8 * (j + 1)], 1, round, resource_check)


    for j in range(8):
        if ((Rcon[k_i] >> j) & 1):
            X | k[184+j]

def Keyshedule_two(eng, k, i, q2, q1, round, k_i, resource_check): #eng, k, i, q_two, q, k_i, resource_check
    Rcon = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]

    new_k0 = []
    for j in range(32):
        new_k0.append(k[(24 + j) % 32])

    for j in range(4):  # 22 68 18
        k[160 + 8 * j: 160 + 8 * (j + 1)] = Sbox_two(eng, new_k0[8 * j:8 * (j + 1)], q2[960 + 60 * j:960 + 60 * (j + 1)], q1[1168 + 73 * j:1168 + 73 * (j + 1)],
                                               k[160 + 8 * j: 160 + 8 * (j + 1)], 1, round, resource_check)
    for j in range(8):
        if ((Rcon[k_i] >> j) & 1):
            X | k[184 + j]

def KeyUpdate(eng, k):
    CNOT32(eng, k[160:192], k[128:160])
    CNOT32(eng, k[128:160], k[96:128])
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

def SBox_bp12_all_two(eng, x0, x1, x2, x3, q2, q1, s, round, resource_check):
    for i in range(4):
        x0[8 * i:8 * (i + 1)] = Sbox_two(eng, x0[8 * i:8 * (i + 1)], q2[60 * i:60 * (i + 1)], q1[73 * i:73 * (i + 1)], s[8 * i:8 * (i + 1)], 0, round,
                                     resource_check)
        x1[8 * i:8 * (i + 1)] = Sbox_two(eng, x1[8 * i:8 * (i + 1)], q2[60 * (i + 4):60 * (i + 5)], q1[73 * (i + 4):73 * (i + 5)],
                                     s[8 * (i + 4):8 * (i + 5)], 0, round, resource_check)
        x2[8 * i:8 * (i + 1)] = Sbox_two(eng, x2[8 * i:8 * (i + 1)], q2[60 * (i + 8):60 * (i + 9)], q1[73 * (i + 8):73 * (i + 9)],
                                     s[8 * (i + 8):8 * (i + 9)], 0, round, resource_check)
        x3[8 * i:8 * (i + 1)] = Sbox_two(eng, x3[8 * i:8 * (i + 1)], q2[60 * (i + 12):60 * (i + 13)], q1[73 * (i + 12):73 * (i + 13)],
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

def reverse_CNOT(eng, a, b):
    CNOT | (b, a)

def CNOT2_mc(eng, a, b, c):
    CNOT | (b, a)
    CNOT | (c, a)

def XOR105(eng, x_in, t, i):
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
        CNOT | (x[31], t[3])
        CNOT | (x[9], t[48])
        CNOT2_mc(eng, t[2], x[23], x[31])
        CNOT2_mc(eng, t[4], x[15], x[23])
        CNOT2_mc(eng, t[1], x[7], x[15])
        CNOT | (x[7], t[3])
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

    CNOT2_mc(eng, y[16], x[0], t[4])

    CNOT | (t[8], y[16])
    with Compute(eng):
        CNOT2_mc(eng, t[21], x[6], t[9])
    CNOT2_mc(eng, y[22], t[10], t[21])  # y14  (3)
    CNOT | (t[1], y[28])
    with Compute(eng):
        CNOT2_mc(eng, t[23], x[7], x[22])
    with Compute(eng):
        CNOT2_mc(eng, t[24], x[8], t[1])

    CNOT2_mc(eng, y[24], t[8], t[24])  # y0  (3)
    CNOT2_mc(eng, y[10], x[10], t[13])
    CNOT | (t[14], y[10])
    CNOT2_mc(eng, y[13], x[13], t[7])
    CNOT | (t[17], y[13])

    with Compute(eng):
        CNOT2_mc(eng, t[30], x[14], t[2])

    CNOT2_mc(eng, y[0], x[16], t[3])
    CNOT | (t[7], y[6])
    CNOT2_mc(eng, y[23], t[23], t[30])  # y15  (3)
    CNOT2_mc(eng, y[31], x[6], x[15])
    CNOT | (t[30], y[31])
    CNOT | (t[3], y[1])

    with Compute(eng):
        CNOT2_mc(eng, t[54], x[3], t[3])

    CNOT2_mc(eng, y[15], x[15], t[3])
    CNOT | (x[27], y[27])

    CNOT | (t[9], y[15])
    CNOT | (t[5], y[0])
    CNOT2_mc(eng, y[6], x[22], t[6])

    with Compute(eng):
        CNOT2_mc(eng, t[40], x[24], t[2])

    CNOT2_mc(eng, y[8], t[5], t[40])  # y16  (3)
    CNOT2_mc(eng, y[26], x[26], t[11])
    CNOT | (t[12], y[26])

    CNOT2_mc(eng, y[29], x[29], t[10])
    CNOT | (t[15], y[29])
    CNOT | (t[21], y[7])
    with Compute(eng):
        CNOT | (x[0], t[48])

    CNOT2_mc(eng, y[25], t[14], t[48])
    CNOT | (t[24], y[25])
    CNOT2_mc(eng, y[2], x[1], x[2])
    CNOT2_mc(eng, y[2], x[25], t[12])
    CNOT2_mc(eng, y[3], t[13], t[18])
    CNOT | (t[54], y[3])

    CNOT2_mc(eng, y[5], x[28], t[10])
    CNOT2_mc(eng, y[20], x[4], t[4])
    CNOT2_mc(eng, y[20], t[17], t[18])
    CNOT2_mc(eng, y[30], x[5], x[13])
    CNOT2_mc(eng, y[30], x[14], t[9])
    CNOT2_mc(eng, y[18], x[9], x[17])
    CNOT2_mc(eng, y[18], x[18], t[13])

    with Compute(eng):
        CNOT2_mc(eng, t[69], x[12], x[20])
        CNOT2_mc(eng, t[70], x[21], t[7])
    CNOT2_mc(eng, y[21], t[69], t[70])  # y13  (3)

    with Compute(eng):
        CNOT2_mc(eng, t[73], x[4], x[27])
        CNOT | (t[69], t[73])

    CNOT2_mc(eng, y[4], t[54], t[73])  # y28  (3)
    CNOT2_mc(eng, y[14], x[5], x[30])
    CNOT2_mc(eng, y[14], t[6], t[70])
    CNOT2_mc(eng, y[5], x[4], x[5])

    with Compute(eng):
        CNOT2_mc(eng, t[78], x[16], x[25])
        CNOT2_mc(eng, t[79], x[1], x[17])

    CNOT | (t[11], y[9])

    CNOT | (t[40], y[9])

    CNOT2_mc(eng, y[17], x[8], t[4])

    CNOT2_mc(eng, y[17], t[78], t[79])

    CNOT | (t[78], y[9])

    CNOT | (t[23], y[7])

    CNOT2_mc(eng, y[19], x[19], t[4])

    CNOT | (t[4], y[7])

    CNOT2_mc(eng, y[19], t[12], t[16])

    CNOT | (x[24], y[1])

    CNOT2_mc(eng, y[1], t[48], t[79])

    CNOT | (t[1], y[27])

    CNOT2_mc(eng, y[27], x[2], x[10])

    CNOT | (t[18], y[27])
    CNOT | (x[26], y[11])
    #
    with Compute(eng):
        CNOT2_mc(eng, t[95], x[3], x[11])
        CNOT2_mc(eng, t[96], x[27], t[2])
    #

    CNOT2_mc(eng, y[28], t[17], t[95])
    CNOT | (x[12], y[28])
    CNOT | (x[18], y[11])

    CNOT | (t[96], y[11])

    CNOT | (t[95], y[11])

    #
    CNOT2_mc(eng, y[12], x[19], x[28])

    CNOT | (t[15], y[12])
    CNOT | (t[96], y[12])  ##

    out = []

    # 0x75a4f56d

    out.append(y[0])
    out.append(y[1])
    out.append(y[2])
    out.append(y[3])

    out.append(y[4])
    out.append(y[5])
    out.append(y[6])
    out.append(y[7])

    out.append(y[8])
    out.append(y[9])
    out.append(y[10])
    out.append(y[11])

    out.append(y[12])
    out.append(y[13])
    out.append(y[14])
    out.append(y[15])

    out.append(y[16])
    out.append(y[17])
    out.append(y[18])
    out.append(y[19])

    out.append(y[20])
    out.append(y[21])
    out.append(y[22])
    out.append(y[23])

    out.append(y[24])
    out.append(y[25])
    out.append(y[26])
    out.append(y[27])

    out.append(y[28])
    out.append(y[29])
    out.append(y[30])
    out.append(y[31])

    if(i!=10):
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

    return out

def CNOT2(eng, a, b, c):

    CNOT | (a, c)
    CNOT | (b, c)

def Uncompute_sbox_key(eng, u, q, resource_check):
    with Dagger(eng):
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
        CNOT | (u[5], u[3])  #
        CNOT | (u[3], u[6])  #
        CNOT | (u[6], q[59])
        CNOT | (q[37], q[59])
        CNOT | (u[3], u[6])  #
        CNOT | (q[6], q[7])
        CNOT | (u[5], u[3])  #
        CNOT | (q[34], u[5])  # done
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

def Uncompute_sbox(eng, u, q, resource_check):
    with Dagger(eng):
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
        CNOT | (u[5], u[3])  #
        CNOT | (u[3], u[6])  #
        CNOT | (u[6], q[59])
        CNOT | (q[37], q[59])
        CNOT | (u[3], u[6])  #
        CNOT | (q[6], q[7])
        CNOT | (u[5], u[3])  #
        CNOT | (q[34], u[5])  # done
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

def Uncompute_sbox_key_special(eng, u, q, resource_check):
    with Dagger(eng):
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
        CNOT | (u[5], u[3])  #
        CNOT | (u[3], u[6])  #
        CNOT | (u[6], q[59])
        CNOT | (q[37], q[59])
        CNOT | (u[3], u[6])  #
        CNOT | (q[6], q[7])
        CNOT | (u[5], u[3])  #
        CNOT | (q[34], u[5])  # done
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

def Uncompute_sbox_special(eng, u, q, resource_check):
    with Dagger(eng):
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
        CNOT | (u[5], u[3])  #
        CNOT | (u[3], u[6])  #
        CNOT | (u[6], q[59])
        CNOT | (q[37], q[59])
        CNOT | (u[3], u[6])  #
        CNOT | (q[6], q[7])
        CNOT | (u[5], u[3])  #
        CNOT | (q[34], u[5])  # done
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

def Uncompute_sbox_key_two(eng, u, q, q2, resource_check):
    with Dagger(eng):
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

        CNOT | (q[0], q[1])  ##### q [16~33], #### q[12~15], q[46~50], q2[13] #### q[9~11], q[54~57] ##### q[0~8], q[51~53]
        CNOT | (q[34], u[5])
        CNOT | (q[35], q2[33])
        CNOT | (q[41], q2[33])
        CNOT | (q[3], q2[31])
        CNOT | (u[3], q2[31])
        CNOT | (q[44], q2[32])
        CNOT | (q[43], q2[32])
        CNOT | (u[7], q2[31])
        CNOT | (q[59], q[1])
        CNOT | (u[5], u[3])  #
        CNOT | (u[3], u[6])  #
        CNOT | (u[6], q[59])
        CNOT | (q[37], q[59])
        CNOT | (u[3], u[6])  #
        CNOT | (q[6], q[7])
        CNOT | (u[5], u[3])  #
        CNOT | (q[34], u[5])  # done
        CNOT | (q[6], q[8])
        CNOT | (q2[33], q[0])
        CNOT | (q[35], q2[33])
        CNOT | (q[2], q[0])
        CNOT | (q2[32], q[5])
        CNOT | (q[3], q[5])
        CNOT | (q[4], q2[31])
        CNOT | (q[7], q2[31])
        CNOT | (q[44], q2[32])
        CNOT | (q[43], q2[32])
        CNOT | (q2[31], q2[33])
        CNOT | (q[41], q2[33])
        CNOT | (q[8], q[5])
        CNOT | (q[7], q[1])
        CNOT | (q[8], q[0])
        CNOT | (q[1], q2[32])

        Toffoli_gate(eng, q2[31], q[1], q2[30], resource_check)
        Toffoli_gate(eng, q2[32], q[5], q2[29], resource_check)
        Toffoli_gate(eng, q[0], q2[33], q2[28], resource_check)

        ##### q [22~33], #### q[12~15], q[46~50], q[58~59] #### q[9~11], q[54~57] ##### q[0~8], q[51~53]

        CNOT | (q2[31], q2[27])
        CNOT | (q2[31], q2[33])
        CNOT | (q[7], q2[31])
        CNOT | (q[4], q2[31])
        CNOT | (q[3], q2[31])
        CNOT | (u[7], q2[31])
        CNOT | (u[3], q2[31])
        CNOT | (q[1], q2[32])
        CNOT | (q[0], q2[26])
        CNOT | (q2[30], q2[26])
        CNOT | (q[1], q2[25])
        CNOT | (q[0], q2[25])
        CNOT | (q[5], q2[24])
        CNOT | (q2[30], q2[24])
        CNOT | (q[5], q2[27])
        CNOT | (q2[25], q2[33])
        CNOT | (q2[27], q2[32])

        Toffoli_gate(eng, q2[24], q2[25], q2[23], resource_check)
        Toffoli_gate(eng, q2[26], q2[27], q2[22], resource_check)
        Toffoli_gate(eng, q2[33], q2[29], q2[21], resource_check)
        Toffoli_gate(eng, q2[32], q2[28], q2[20], resource_check)

        ##### q [30~33], #### q[12~15], q[46~50],  #### q[9~11], q[54~57] ##### q[0~8], q[51~53]

        CNOT | (q2[27], q2[32])
        CNOT | (q2[30], q2[21])
        CNOT | (q2[30], q2[24])
        CNOT | (q2[30], q2[26])
        CNOT | (q2[27], q2[30])
        CNOT | (u[7], q2[31])
        CNOT | (q[5], q2[27])
        CNOT | (q2[31], q2[27])
        CNOT | (u[7], q2[31])
        CNOT | (q[7], q2[27])
        CNOT | (q[4], q2[27])
        CNOT | (q[3], q2[27])
        CNOT | (u[3], q2[27])
        CNOT | (q[5], q2[24])
        CNOT | (q[0], q2[26])
        CNOT | (q2[25], q2[21])
        CNOT | (q2[13], q2[21])
        CNOT | (q2[25], q2[33])
        CNOT | (q[1], q2[25])
        CNOT | (q[0], q2[25])
        CNOT | (q2[23], q[0])
        CNOT | (q2[22], q[5])
        CNOT | (q2[30], q2[20])
        CNOT2(eng, q2[21], q2[20], q2[19])
        CNOT2(eng, q[0], q[5], q2[18])
        CNOT2(eng, q[0], q2[21], q2[17])
        CNOT | (q2[20], q2[32])
        CNOT | (q2[20], q2[16])
        CNOT | (q[5], q2[16])
        CNOT | (q2[16], q2[33])
        CNOT2(eng, q2[18], q2[19], q2[12])
        CNOT | (q[5], q2[31])
        CNOT | (q2[17], q2[27])
        CNOT | (q2[21], q2[26])
        CNOT | (q[0], q2[25])
        CNOT | (q2[18], q2[24])
        CNOT | (q2[12], q2[13])
        CNOT | (q2[19], q[59])

        ##### q [30~33], #### q[12~15], q[46~50],  #### q[9~11], q[54~57] ##### q[0~8], q[51~53]

        Toffoli_gate(eng, q2[16], q[37], q2[14], resource_check)
        Toffoli_gate(eng, q2[20], q[39], q2[15], resource_check)
        Toffoli_gate(eng, q[5], u[0], q2[46], resource_check)
        Toffoli_gate(eng, q2[17], u[3], q2[47], resource_check)
        Toffoli_gate(eng, q2[21], q[40], q2[48], resource_check)
        Toffoli_gate(eng, q[0], q[43], q2[49], resource_check)
        Toffoli_gate(eng, q2[18], u[6], q2[50], resource_check)
        Toffoli_gate(eng, q2[12], u[5], q2[58], resource_check)
        Toffoli_gate(eng, q2[19], q[41], q2[9], resource_check)
        Toffoli_gate(eng, q2[33], q[42], q2[10], resource_check)
        Toffoli_gate(eng, q2[32], q[45], q2[11], resource_check)
        Toffoli_gate(eng, q2[31], u[4], q2[54], resource_check)
        Toffoli_gate(eng, q2[27], u[7], q2[55], resource_check)
        Toffoli_gate(eng, q2[26], q[38], q2[56], resource_check)
        Toffoli_gate(eng, q2[25], q[44], q2[57], resource_check)
        Toffoli_gate(eng, q2[24], q[34], q2[51], resource_check)
        Toffoli_gate(eng, q2[13], q[36], q2[52], resource_check)
        Toffoli_gate(eng, q[59], q[35], q2[53], resource_check)

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

        CNOT | (q2[16], q2[33])
        CNOT | (q2[20], q2[32])
        CNOT | (q[5], q2[31])
        CNOT | (q2[17], q2[27])
        CNOT | (q2[21], q2[26])
        CNOT | (q[0], q2[25])
        CNOT | (q2[18], q2[24])
        CNOT | (q2[12], q2[13])
        CNOT | (q2[19], q[59])
        CNOT | (q2[51], q2[33])
        CNOT | (q2[52], q2[33])
        CNOT | (q2[48], q2[32])
        CNOT | (q2[11], q2[32])
        CNOT2(eng, q2[14], q2[46], q2[31])
        CNOT | (q2[10], q2[15])
        CNOT | (q2[55], q2[9])
        CNOT | (q2[51], q2[47])
        CNOT | (q2[52], q2[47])
        CNOT | (q2[15], q2[14])
        CNOT | (q2[49], q2[56])
        CNOT | (q2[50], q2[27])
        CNOT | (q2[58], q2[27])
        CNOT | (q2[9], q2[58])
        CNOT | (q2[31], q2[57])
        CNOT | (q2[46], q2[49])
        CNOT | (q2[47], q2[26])
        CNOT | (q2[58], q2[26])
        CNOT | (q2[33], q2[48])
        CNOT | (q2[51], q2[50])
        CNOT | (q2[32], q2[10])
        CNOT | (q2[33], q2[11])
        CNOT | (q2[32], q2[54])
        CNOT | (q2[56], q2[55])
        CNOT | (q2[9], q2[53])
        CNOT | (q2[32], q2[33])
        CNOT | (q2[15], q2[49])
        CNOT | (q2[55], q2[31])
        CNOT | (q2[27], q2[10])
        CNOT | (q2[14], q2[27])
        CNOT | (q2[14], q2[32])
        CNOT | (q2[56], q2[58])
        CNOT | (q2[57], q2[50])
        CNOT | (q2[57], q2[54])

def Uncompute_sbox_two(eng, u, q, q2, resource_check):
    with Dagger(eng):
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

        CNOT | (q[0], q[1])  ##### q [16~33], #### q[12~15], q[46~50], q2[13] #### q[9~11], q[54~57] ##### q[0~8], q[51~53]
        CNOT | (q[34], u[5])
        CNOT | (q[35], q2[33])
        CNOT | (q[41], q2[33])
        CNOT | (q[3], q2[31])
        CNOT | (u[3], q2[31])
        CNOT | (q[44], q2[32])
        CNOT | (q[43], q2[32])
        CNOT | (u[7], q2[31])
        CNOT | (q[59], q[1])
        CNOT | (u[5], u[3])  #
        CNOT | (u[3], u[6])  #
        CNOT | (u[6], q[59])
        CNOT | (q[37], q[59])
        CNOT | (u[3], u[6])  #
        CNOT | (q[6], q[7])
        CNOT | (u[5], u[3])  #
        CNOT | (q[34], u[5])  # done
        CNOT | (q[6], q[8])
        CNOT | (q2[33], q[0])
        CNOT | (q[35], q2[33])
        CNOT | (q[2], q[0])
        CNOT | (q2[32], q[5])
        CNOT | (q[3], q[5])
        CNOT | (q[4], q2[31])
        CNOT | (q[7], q2[31])
        CNOT | (q[44], q2[32])
        CNOT | (q[43], q2[32])
        CNOT | (q2[31], q2[33])
        CNOT | (q[41], q2[33])
        CNOT | (q[8], q[5])
        CNOT | (q[7], q[1])
        CNOT | (q[8], q[0])
        CNOT | (q[1], q2[32])

        Toffoli_gate(eng, q2[31], q[1], q2[30], resource_check)
        Toffoli_gate(eng, q2[32], q[5], q2[29], resource_check)
        Toffoli_gate(eng, q[0], q2[33], q2[28], resource_check)

        ##### q [22~33], #### q[12~15], q[46~50], q[58~59] #### q[9~11], q[54~57] ##### q[0~8], q[51~53]

        CNOT | (q2[31], q2[27])
        CNOT | (q2[31], q2[33])
        CNOT | (q[7], q2[31])
        CNOT | (q[4], q2[31])
        CNOT | (q[3], q2[31])
        CNOT | (u[7], q2[31])
        CNOT | (u[3], q2[31])
        CNOT | (q[1], q2[32])
        CNOT | (q[0], q2[26])
        CNOT | (q2[30], q2[26])
        CNOT | (q[1], q2[25])
        CNOT | (q[0], q2[25])
        CNOT | (q[5], q2[24])
        CNOT | (q2[30], q2[24])
        CNOT | (q[5], q2[27])
        CNOT | (q2[25], q2[33])
        CNOT | (q2[27], q2[32])

        Toffoli_gate(eng, q2[24], q2[25], q2[23], resource_check)
        Toffoli_gate(eng, q2[26], q2[27], q2[22], resource_check)
        Toffoli_gate(eng, q2[33], q2[29], q2[21], resource_check)
        Toffoli_gate(eng, q2[32], q2[28], q2[20], resource_check)

        ##### q [30~33], #### q[12~15], q[46~50],  #### q[9~11], q[54~57] ##### q[0~8], q[51~53]

        CNOT | (q2[27], q2[32])
        CNOT | (q2[30], q2[21])
        CNOT | (q2[30], q2[24])
        CNOT | (q2[30], q2[26])
        CNOT | (q2[27], q2[30])
        CNOT | (u[7], q2[31])
        CNOT | (q[5], q2[27])
        CNOT | (q2[31], q2[27])
        CNOT | (u[7], q2[31])
        CNOT | (q[7], q2[27])
        CNOT | (q[4], q2[27])
        CNOT | (q[3], q2[27])
        CNOT | (u[3], q2[27])
        CNOT | (q[5], q2[24])
        CNOT | (q[0], q2[26])
        CNOT | (q2[25], q2[21])
        CNOT | (q2[13], q2[21])
        CNOT | (q2[25], q2[33])
        CNOT | (q[1], q2[25])
        CNOT | (q[0], q2[25])
        CNOT | (q2[23], q[0])
        CNOT | (q2[22], q[5])
        CNOT | (q2[30], q2[20])
        CNOT2(eng, q2[21], q2[20], q2[19])
        CNOT2(eng, q[0], q[5], q2[18])
        CNOT2(eng, q[0], q2[21], q2[17])
        CNOT | (q2[20], q2[32])
        CNOT | (q2[20], q2[16])
        CNOT | (q[5], q2[16])
        CNOT | (q2[16], q2[33])
        CNOT2(eng, q2[18], q2[19], q2[12])
        CNOT | (q[5], q2[31])
        CNOT | (q2[17], q2[27])
        CNOT | (q2[21], q2[26])
        CNOT | (q[0], q2[25])
        CNOT | (q2[18], q2[24])
        CNOT | (q2[12], q2[13])
        CNOT | (q2[19], q[59])

        ##### q [30~33], #### q[12~15], q[46~50],  #### q[9~11], q[54~57] ##### q[0~8], q[51~53]

        Toffoli_gate(eng, q2[16], q[37], q2[14], resource_check)
        Toffoli_gate(eng, q2[20], q[39], q2[15], resource_check)
        Toffoli_gate(eng, q[5], u[0], q2[46], resource_check)
        Toffoli_gate(eng, q2[17], u[3], q2[47], resource_check)
        Toffoli_gate(eng, q2[21], q[40], q2[48], resource_check)
        Toffoli_gate(eng, q[0], q[43], q2[49], resource_check)
        Toffoli_gate(eng, q2[18], u[6], q2[50], resource_check)
        Toffoli_gate(eng, q2[12], u[5], q2[58], resource_check)
        Toffoli_gate(eng, q2[19], q[41], q2[9], resource_check)
        Toffoli_gate(eng, q2[33], q[42], q2[10], resource_check)
        Toffoli_gate(eng, q2[32], q[45], q2[11], resource_check)
        Toffoli_gate(eng, q2[31], u[4], q2[54], resource_check)
        Toffoli_gate(eng, q2[27], u[7], q2[55], resource_check)
        Toffoli_gate(eng, q2[26], q[38], q2[56], resource_check)
        Toffoli_gate(eng, q2[25], q[44], q2[57], resource_check)
        Toffoli_gate(eng, q2[24], q[34], q2[51], resource_check)
        Toffoli_gate(eng, q2[13], q[36], q2[52], resource_check)
        Toffoli_gate(eng, q[59], q[35], q2[53], resource_check)

        CNOT | (q2[16], q2[33])
        CNOT | (q2[20], q2[32])
        CNOT | (q[5], q2[31])
        CNOT | (q2[17], q2[27])
        CNOT | (q2[21], q2[26])
        CNOT | (q[0], q2[25])
        CNOT | (q2[18], q2[24])
        CNOT | (q2[12], q2[13])
        CNOT | (q2[19], q[59])
        CNOT | (q2[51], q2[33])
        CNOT | (q2[52], q2[33])
        CNOT | (q2[48], q2[32])
        CNOT | (q2[11], q2[32])
        CNOT2(eng, q2[14], q2[46], q2[31])
        CNOT | (q2[10], q2[15])
        CNOT | (q2[55], q2[9])
        CNOT | (q2[51], q2[47])
        CNOT | (q2[52], q2[47])
        CNOT | (q2[15], q2[14])
        CNOT | (q2[49], q2[56])
        CNOT | (q2[50], q2[27])
        CNOT | (q2[58], q2[27])
        CNOT | (q2[9], q2[58])
        CNOT | (q2[31], q2[57])
        CNOT | (q2[46], q2[49])
        CNOT | (q2[47], q2[26])
        CNOT | (q2[58], q2[26])
        CNOT | (q2[33], q2[48])
        CNOT | (q2[51], q2[50])
        CNOT | (q2[32], q2[10])
        CNOT | (q2[33], q2[11])
        CNOT | (q2[32], q2[54])
        CNOT | (q2[56], q2[55])
        CNOT | (q2[9], q2[53])
        CNOT | (q2[32], q2[33])
        CNOT | (q2[15], q2[49])
        CNOT | (q2[55], q2[31])
        CNOT | (q2[27], q2[10])
        CNOT | (q2[14], q2[27])
        CNOT | (q2[14], q2[32])
        CNOT | (q2[56], q2[58])
        CNOT | (q2[57], q2[50])
        CNOT | (q2[57], q2[54])

def Sbox(eng, u, q, s, flag, round, resource_check):
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
    CNOT | (u[5], u[3])  #
    CNOT | (u[3], u[6])  #
    CNOT | (u[6], q[59])
    CNOT | (q[37], q[59])
    CNOT | (u[3], u[6])  #
    CNOT | (q[6], q[7])
    CNOT | (u[5], u[3])  #
    CNOT | (q[34], u[5])  # done
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

    if (flag == 1):
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

def Sbox_two(eng, u, q, q2, s, flag, round, resource_check):

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

    CNOT | (q[0], q[1])  ##### q [16~33], #### q[12~15], q[46~50], q2[13] #### q[9~11], q[54~57] ##### q[0~8], q[51~53]
    CNOT | (q[34], u[5])
    CNOT | (q[35], q2[33])
    CNOT | (q[41], q2[33])
    CNOT | (q[3], q2[31])
    CNOT | (u[3], q2[31])
    CNOT | (q[44], q2[32])
    CNOT | (q[43], q2[32])
    CNOT | (u[7], q2[31])
    CNOT | (q[59], q[1])
    CNOT | (u[5], u[3])  #
    CNOT | (u[3], u[6])  #
    CNOT | (u[6], q[59])
    CNOT | (q[37], q[59])
    CNOT | (u[3], u[6])  #
    CNOT | (q[6], q[7])
    CNOT | (u[5], u[3])  #
    CNOT | (q[34], u[5])  # done
    CNOT | (q[6], q[8])
    CNOT | (q2[33], q[0])
    CNOT | (q[35], q2[33])
    CNOT | (q[2], q[0])
    CNOT | (q2[32], q[5])
    CNOT | (q[3], q[5])
    CNOT | (q[4], q2[31])
    CNOT | (q[7], q2[31])
    CNOT | (q[44], q2[32])
    CNOT | (q[43], q2[32])
    CNOT | (q2[31], q2[33])
    CNOT | (q[41], q2[33])
    CNOT | (q[8], q[5])
    CNOT | (q[7], q[1])
    CNOT | (q[8], q[0])
    CNOT | (q[1], q2[32])

    Toffoli_gate(eng, q2[31], q[1], q2[30], resource_check)
    Toffoli_gate(eng, q2[32], q[5], q2[29], resource_check)
    Toffoli_gate(eng, q[0], q2[33], q2[28], resource_check)

    ##### q [22~33], #### q[12~15], q[46~50], q[58~59] #### q[9~11], q[54~57] ##### q[0~8], q[51~53]

    CNOT | (q2[31], q2[27])
    CNOT | (q2[31], q2[33])
    CNOT | (q[7], q2[31])
    CNOT | (q[4], q2[31])
    CNOT | (q[3], q2[31])
    CNOT | (u[7], q2[31])
    CNOT | (u[3], q2[31])
    CNOT | (q[1], q2[32])
    CNOT | (q[0], q2[26])
    CNOT | (q2[30], q2[26])
    CNOT | (q[1], q2[25])
    CNOT | (q[0], q2[25])
    CNOT | (q[5], q2[24])
    CNOT | (q2[30], q2[24])
    CNOT | (q[5], q2[27])
    CNOT | (q2[25], q2[33])
    CNOT | (q2[27], q2[32])

    Toffoli_gate(eng, q2[24], q2[25], q2[23], resource_check)
    Toffoli_gate(eng, q2[26], q2[27], q2[22], resource_check)
    Toffoli_gate(eng, q2[33], q2[29], q2[21], resource_check)
    Toffoli_gate(eng, q2[32], q2[28], q2[20], resource_check)

    ##### q [30~33], #### q[12~15], q[46~50],  #### q[9~11], q[54~57] ##### q[0~8], q[51~53]

    CNOT | (q2[27], q2[32])
    CNOT | (q2[30], q2[21])
    CNOT | (q2[30], q2[24])
    CNOT | (q2[30], q2[26])
    CNOT | (q2[27], q2[30])
    CNOT | (u[7], q2[31])
    CNOT | (q[5], q2[27])
    CNOT | (q2[31], q2[27])
    CNOT | (u[7], q2[31])
    CNOT | (q[7], q2[27])
    CNOT | (q[4], q2[27])
    CNOT | (q[3], q2[27])
    CNOT | (u[3], q2[27])
    CNOT | (q[5], q2[24])
    CNOT | (q[0], q2[26])
    CNOT | (q2[25], q2[21])
    CNOT | (q2[13], q2[21])
    CNOT | (q2[25], q2[33])
    CNOT | (q[1], q2[25])
    CNOT | (q[0], q2[25])
    CNOT | (q2[23], q[0])
    CNOT | (q2[22], q[5])
    CNOT | (q2[30], q2[20])
    CNOT2(eng, q2[21], q2[20], q2[19])
    CNOT2(eng, q[0], q[5], q2[18])
    CNOT2(eng, q[0], q2[21], q2[17])
    CNOT | (q2[20], q2[32])
    CNOT | (q2[20], q2[16])
    CNOT | (q[5], q2[16])
    CNOT | (q2[16], q2[33])
    CNOT2(eng, q2[18], q2[19], q2[12])
    CNOT | (q[5], q2[31])
    CNOT | (q2[17], q2[27])
    CNOT | (q2[21], q2[26])
    CNOT | (q[0], q2[25])
    CNOT | (q2[18], q2[24])
    CNOT | (q2[12], q2[13])
    CNOT | (q2[19], q[59])

    ##### q [30~33], #### q[12~15], q[46~50],  #### q[9~11], q[54~57] ##### q[0~8], q[51~53]

    Toffoli_gate(eng, q2[16], q[37], q2[14], resource_check)
    Toffoli_gate(eng, q2[20], q[39], q2[15], resource_check)
    Toffoli_gate(eng, q[5], u[0], q2[46], resource_check)
    Toffoli_gate(eng, q2[17], u[3], q2[47], resource_check)
    Toffoli_gate(eng, q2[21], q[40], q2[48], resource_check)
    Toffoli_gate(eng, q[0], q[43], q2[49], resource_check)
    Toffoli_gate(eng, q2[18], u[6], q2[50], resource_check)
    Toffoli_gate(eng, q2[12], u[5], q2[58], resource_check)
    Toffoli_gate(eng, q2[19], q[41], q2[9], resource_check)
    Toffoli_gate(eng, q2[33], q[42], q2[10], resource_check)
    Toffoli_gate(eng, q2[32], q[45], q2[11], resource_check)
    Toffoli_gate(eng, q2[31], u[4], q2[54], resource_check)
    Toffoli_gate(eng, q2[27], u[7], q2[55], resource_check)
    Toffoli_gate(eng, q2[26], q[38], q2[56], resource_check)
    Toffoli_gate(eng, q2[25], q[44], q2[57], resource_check)
    Toffoli_gate(eng, q2[24], q[34], q2[51], resource_check)
    Toffoli_gate(eng, q2[13], q[36], q2[52], resource_check)
    Toffoli_gate(eng, q[59], q[35], q2[53], resource_check)

    if (flag == 1):
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

    CNOT | (q2[16], q2[33])
    CNOT | (q2[20], q2[32])
    CNOT | (q[5], q2[31])
    CNOT | (q2[17], q2[27])
    CNOT | (q2[21], q2[26])
    CNOT | (q[0], q2[25])
    CNOT | (q2[18], q2[24])
    CNOT | (q2[12], q2[13])
    CNOT | (q2[19], q[59])
    CNOT | (q2[51], q2[33])
    CNOT | (q2[52], q2[33])
    CNOT | (q2[48], q2[32])
    CNOT | (q2[11], q2[32])
    CNOT2(eng, q2[14], q2[46], q2[31])
    CNOT | (q2[10], q2[15])
    CNOT | (q2[55], q2[9])
    CNOT | (q2[51], q2[47])
    CNOT | (q2[52], q2[47])
    CNOT | (q2[15], q2[14])
    CNOT | (q2[49], q2[56])
    CNOT | (q2[50], q2[27])
    CNOT | (q2[58], q2[27])
    CNOT | (q2[9], q2[58])
    CNOT | (q2[31], q2[57])
    CNOT | (q2[46], q2[49])
    CNOT | (q2[47], q2[26])
    CNOT | (q2[58], q2[26])
    CNOT | (q2[33], q2[48])
    CNOT | (q2[51], q2[50])
    CNOT | (q2[32], q2[10])
    CNOT | (q2[33], q2[11])
    CNOT | (q2[32], q2[54])
    CNOT | (q2[56], q2[55])
    CNOT | (q2[9], q2[53])
    CNOT | (q2[32], q2[33])
    CNOT | (q2[15], q2[49])
    CNOT | (q2[55], q2[31])
    CNOT | (q2[27], q2[10])
    CNOT | (q2[14], q2[27])
    CNOT | (q2[14], q2[32])
    CNOT | (q2[56], q2[58])
    CNOT | (q2[57], q2[50])
    CNOT | (q2[57], q2[54])

    X | s[6]
    X | s[5]
    X | s[1]
    X | s[0]

    CNOT | (q2[47], s[4])
    CNOT | (q2[31], s[0])
    CNOT | (q2[10], s[7])
    CNOT | (q2[47], s[7])
    CNOT | (q2[11], s[6])
    CNOT | (q2[27], s[6])
    CNOT | (q2[53], s[5])
    CNOT | (q2[50], s[5])
    CNOT | (q2[47], s[0])
    CNOT | (q2[32], s[4])
    CNOT | (q2[33], s[3])
    CNOT | (q2[49], s[3])
    CNOT | (q2[26], s[2])
    CNOT | (q2[54], s[2])
    CNOT | (q2[48], s[1])
    CNOT | (q2[58], s[1])

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