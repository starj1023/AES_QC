from projectq import MainEngine
from projectq.ops import H, CNOT, Measure, Toffoli, X, All, T, Tdagger, S, Tdag
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

    y = eng.allocate_qureg(540)  # 27 * 20
    t = eng.allocate_qureg(1000)  # 50 * 20
    z = eng.allocate_qureg(820)  # 41 * 20
    w = eng.allocate_qureg(680)  # 34 * 20
    l = eng.allocate_qureg(600)  # 30 * 20

    y_two = eng.allocate_qureg(540)  # 27 * 20
    t_two = eng.allocate_qureg(1000)  # 50 * 20
    z_two = eng.allocate_qureg(820)  # 41 * 20
    w_two = eng.allocate_qureg(680)  # 34 * 20
    l_two = eng.allocate_qureg(600)  # 30 * 20

    mq = eng.allocate_qureg(420)

    k_i = 0
    for i in range(14):

        if(i%2 == 0):
            AddRoundkey(eng, x0, x1, x2, x3, k)
        else:
            AddRoundkey_2(eng, x0, x1, x2, x3, k)

        print('Round', i)

        if (i == 1):
            Clean_ancilla(eng, t0, t1, t2, t3, k, y, t, z, w, l, 1, k_i, resource_check)

        if(i!= 0 and i!= 1 and i!= 13 and i % 2 == 0):
            Clean_ancilla_two(eng, t0, t1, t2, t3, k[0:32], y_two, t_two, z_two, z, w_two, w, l_two, 0, k_i, resource_check)

        if (i != 0 and i != 1 and i!= 13 and i % 2 == 1):
            Clean_ancilla(eng, t0, t1, t2, t3, k[128:160], y, t, z, w, l, 0, k_i, resource_check)

        if(i == 13):
            Clean_ancilla_special(eng, t0, t1, t2, t3, k[128:160], y, t, z, w, l, 0, k_i, resource_check)

        if(i!=0):
            if(i%2 == 0):
                Keyshedule(eng, k, i, y, t, z, w, l, i, k_i, resource_check) #i=2, k_i=1, _one
                CNOT32(eng, k[96:128], k[64:96])
                CNOT32(eng, k[64:96], k[32:64])
                CNOT32(eng, k[32:64], k[0:32])
            else:
                Keyshedule_two(eng, k, i, y_two, t_two, z_two, z, w_two, w, l_two, i, k_i, resource_check) #i=1, k_i=0, _two, i=3, k_i=2, _two
                CNOT32(eng, k[224:256], k[192:224])
                CNOT32(eng, k[192:224], k[160:192])
                CNOT32(eng, k[160:192], k[128:160])
            k_i = k_i + 1

        if (i != 13):
            s = eng.allocate_qureg(128)
        else:
            s = recycle(eng, l)  # key: 0~8, 34~45, Sbox: 6~8

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
            SBox_bp12_all(eng, x0, x1, x2, x3, y, t, z, w, l, s, i, resource_check)
        else:
            SBox_bp12_all_two(eng, x0, x1, x2, x3, y_two, t_two, z_two, z, w_two, w, l_two, s, i, resource_check)

        x0, x1, x2, x3 = Shiftrow(eng, x0, x1, x2, x3)

        if(i!=13):
            x0 = XOR105(eng, x0, mq[0:105], i)
            x1 = XOR105(eng, x1, mq[105:210], i)
            x2 = XOR105(eng, x2, mq[210:315], i)
            x3 = XOR105(eng, x3, mq[315:420], i)

        if (resource_check != 1):
            print('\nCiphertext ')
            print_state(eng, x3, 8)
            print_state(eng, x2, 8)
            print_state(eng, x1, 8)
            print_state(eng, x0, 8)

    AddRoundkey(eng, x0, x1, x2, x3, k)

    if(resource_check != 1):
        print('\nCiphertext ')
        print_state(eng, x3, 8)
        print_state(eng, x2, 8)
        print_state(eng, x1, 8)
        print_state(eng, x0, 8)

def recycle(eng, l): # l[15~22]

    s1 = []
    for i in range(16):
        s1.append(l[15 + 30 * i])
        s1.append(l[16 + 30 * i])
        s1.append(l[17 + 30 * i])
        s1.append(l[18 + 30 * i])

        s1.append(l[19 + 30 * i])
        s1.append(l[20 + 30 * i])
        s1.append(l[21 + 30 * i])
        s1.append(l[22 + 30 * i])

    return s1

def Clean_ancilla(eng, x0, x1, x2, x3, temp_k, y, t, z, w, l, flag, k_i, resource_check):

    for i in range(4):
        Uncompute_sbox(eng, x0[8 * i:8 * (i + 1)], y[27 * i:27 * (i + 1)], t[50 * i:50 * (i + 1)],
                       z[41 * i:41 * (i + 1)], w[34 * i:34 * (i + 1)], l[30 * i:30 * (i + 1)], resource_check)

        Uncompute_sbox(eng, x1[8 * i:8 * (i + 1)], y[27 * (i + 4):27 * (i + 5)],
                       t[50 * (i + 4):50 * (i + 5)], z[41 * (i + 4):41 * (i + 5)],
                       w[34 * (i + 4):34 * (i + 5)], l[30 * (i + 4):30 * (i + 5)], resource_check)
        Uncompute_sbox(eng, x2[8 * i:8 * (i + 1)], y[27 * (i + 8):27 * (i + 9)],
                       t[50 * (i + 8):50 * (i + 9)], z[41 * (i + 8):41 * (i + 9)], w[34 * (i + 8):34 * (i + 9)],
                       l[30 * (i + 8):30 * (i + 9)],
                       resource_check)

        Uncompute_sbox(eng, x3[8 * i:8 * (i + 1)], y[27 * (i + 12):27 * (i + 13)],
                       t[50 * (i + 12):50 * (i + 13)], z[41 * (i + 12):41 * (i + 13)],
                       w[34 * (i + 12):34 * (i + 13)], l[30 * (i + 12):30 * (i + 13)], resource_check)

    if(flag != 1):
        new_k0 = []
        if (k_i % 2 == 0):
            for j in range(32):
                new_k0.append(temp_k[j])
        else:
            for j in range(32):
                new_k0.append(temp_k[(24 + j) % 32])

        for i in range(4):
            Uncompute_sbox(eng, new_k0[8 * i:8 * (i + 1)], y[432 + 27 * i:432 + 27 * (i + 1)],
                           t[800 + 50 * i:800 + 50 * (i + 1)],
                           z[656 + 41 * i:656 + 41 * (i + 1)], w[544 + 34 * i:544 + 34 * (i + 1)],
                           l[480 + 30 * i:480 + 30 * (i + 1)], resource_check)

def Clean_ancilla_special(eng, x0, x1, x2, x3, temp_k, y, t, z, w, l, flag, k_i, resource_check):

    for i in range(4):
        Uncompute_sbox_special(eng, x0[8 * i:8 * (i + 1)], y[27 * i:27 * (i + 1)], t[50 * i:50 * (i + 1)],
                       z[41 * i:41 * (i + 1)], w[34 * i:34 * (i + 1)], l[30 * i:30 * (i + 1)], resource_check)

        Uncompute_sbox_special(eng, x1[8 * i:8 * (i + 1)], y[27 * (i + 4):27 * (i + 5)],
                       t[50 * (i + 4):50 * (i + 5)], z[41 * (i + 4):41 * (i + 5)],
                       w[34 * (i + 4):34 * (i + 5)], l[30 * (i + 4):30 * (i + 5)], resource_check)
        Uncompute_sbox_special(eng, x2[8 * i:8 * (i + 1)], y[27 * (i + 8):27 * (i + 9)],
                       t[50 * (i + 8):50 * (i + 9)], z[41 * (i + 8):41 * (i + 9)], w[34 * (i + 8):34 * (i + 9)],
                       l[30 * (i + 8):30 * (i + 9)],
                       resource_check)

        Uncompute_sbox_special(eng, x3[8 * i:8 * (i + 1)], y[27 * (i + 12):27 * (i + 13)],
                       t[50 * (i + 12):50 * (i + 13)], z[41 * (i + 12):41 * (i + 13)],
                       w[34 * (i + 12):34 * (i + 13)], l[30 * (i + 12):30 * (i + 13)], resource_check)

    if(flag != 1):
        new_k0 = []
        if (k_i % 2 == 0):
            for j in range(32):
                new_k0.append(temp_k[j])
        else:
            for j in range(32):
                new_k0.append(temp_k[(24 + j) % 32])

        for i in range(4):
            Uncompute_sbox_special(eng, new_k0[8 * i:8 * (i + 1)], y[432 + 27 * i:432 + 27 * (i + 1)],
                           t[800 + 50 * i:800 + 50 * (i + 1)],
                           z[656 + 41 * i:656 + 41 * (i + 1)], w[544 + 34 * i:544 + 34 * (i + 1)],
                           l[480 + 30 * i:480 + 30 * (i + 1)], resource_check)

def Clean_ancilla_two(eng, x0, x1, x2, x3, temp_k, y, t, z, z_two, w, w_two, l, flag, k_i, resource_check):
    for i in range(4):
        Uncompute_sbox_two(eng, x0[8 * i:8 * (i + 1)], y[27 * i:27 * (i + 1)], t[50 * i:50 * (i + 1)],
                           z[41 * i:41 * (i + 1)], z_two[41 * i:41 * (i + 1)], w[34 * i:34 * (i + 1)],
                           w_two[34 * i:34 * (i + 1)], l[30 * i:30 * (i + 1)], resource_check)

        Uncompute_sbox_two(eng, x1[8 * i:8 * (i + 1)], y[27 * (i + 4):27 * (i + 5)],
                           t[50 * (i + 4):50 * (i + 5)], z[41 * (i + 4):41 * (i + 5)], z_two[41 * (i + 4):41 * (i + 5)],
                           w[34 * (i + 4):34 * (i + 5)], w_two[34 * (i + 4):34 * (i + 5)], l[30 * (i + 4):30 * (i + 5)],
                           resource_check)
        Uncompute_sbox_two(eng, x2[8 * i:8 * (i + 1)], y[27 * (i + 8):27 * (i + 9)],
                           t[50 * (i + 8):50 * (i + 9)], z[41 * (i + 8):41 * (i + 9)], z_two[41 * (i + 8):41 * (i + 9)],
                           w[34 * (i + 8):34 * (i + 9)], w_two[34 * (i + 8):34 * (i + 9)],
                           l[30 * (i + 8):30 * (i + 9)],
                           resource_check)

        Uncompute_sbox_two(eng, x3[8 * i:8 * (i + 1)], y[27 * (i + 12):27 * (i + 13)],
                           t[50 * (i + 12):50 * (i + 13)], z[41 * (i + 12):41 * (i + 13)],
                           z_two[41 * (i + 12):41 * (i + 13)],
                           w[34 * (i + 12):34 * (i + 13)], w_two[34 * (i + 12):34 * (i + 13)],
                           l[30 * (i + 12):30 * (i + 13)], resource_check)

    if(flag != 1):
        new_k0 = []
        if (k_i % 2 == 0):
            for j in range(32):
                new_k0.append(temp_k[j])
        else:
            for j in range(32):
                new_k0.append(temp_k[(24 + j) % 32])

        for i in range(4):
            Uncompute_sbox_two(eng, new_k0[8 * i:8 * (i + 1)], y[432 + 27 * i:432 + 27 * (i + 1)],
                           t[800 + 50 * i:800 + 50 * (i + 1)],
                           z[656 + 41 * i:656 + 41 * (i + 1)], z_two[656 + 41 * i:656 + 41 * (i + 1)], w[544 + 34 * i:544 + 34 * (i + 1)], w_two[544 + 34 * i:544 + 34 * (i + 1)],
                           l[480 + 30 * i:480 + 30 * (i + 1)], resource_check)

def Keyshedule(eng, k, i, y, t, z, w, l, round, k_i, resource_check):

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
             k[224 + 8 * j: 224 + 8 * (j + 1)] = Sbox(eng, new_k0[8 * j:8 * (j + 1)], y[432 + 27 * j:432 + 27 * (j + 1)],
                                               t[800 + 50 * j:800 + 50 * (j + 1)],
                                               z[656 + 41 * j:656 + 41 * (j + 1)], w[544 + 34 * j:544 + 34 * (j + 1)],
                                               l[480 + 30 * j:480 + 30 * (j + 1)], k[224 + 8 * j: 224 + 8 * (j + 1)],
                                               1, round, resource_check)
    else:
        for j in range(4): #22 68 18
             k[96 + 8 * j: 96 + 8 * (j + 1)] = Sbox(eng, new_k0[8 * j:8 * (j + 1)], y[432 + 27 * j:432 + 27 * (j + 1)],
                                               t[800 + 50 * j:800 + 50 * (j + 1)],
                                               z[656 + 41 * j:656 + 41 * (j + 1)], w[544 + 34 * j:544 + 34 * (j + 1)],
                                               l[480 + 30 * j:480 + 30 * (j + 1)], k[96 + 8 * j: 96 + 8 * (j + 1)],
                                               1, round, resource_check)
    if (k_i % 2 == 0):
        for j in range(8):
            if ((Rcon[int(k_i/2)] >> j) & 1):
                X | k[248+j]

def Keyshedule_two(eng, k, i, y, t, z, z_two, w, w_two, l, round, k_i, resource_check):

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
             k[224 + 8 * j: 224 + 8 * (j + 1)] = Sbox_two(eng, new_k0[8 * j:8 * (j + 1)], y[432 + 27 * j:432 + 27 * (j + 1)],
                                               t[800 + 50 * j:800 + 50 * (j + 1)],
                                               z[656 + 41 * j:656 + 41 * (j + 1)], z_two[656 + 41 * j:656 + 41 * (j + 1)], w[544 + 34 * j:544 + 34 * (j + 1)], w_two[544 + 34 * j:544 + 34 * (j + 1)],
                                               l[480 + 30 * j:480 + 30 * (j + 1)], k[224 + 8 * j: 224 + 8 * (j + 1)],
                                               1, round, resource_check)
    else:
        for j in range(4): #22 68 18
             k[96 + 8 * j: 96 + 8 * (j + 1)] = Sbox_two(eng, new_k0[8 * j:8 * (j + 1)], y[432 + 27 * j:432 + 27 * (j + 1)],
                                               t[800 + 50 * j:800 + 50 * (j + 1)],
                                               z[656 + 41 * j:656 + 41 * (j + 1)], z_two[656 + 41 * j:656 + 41 * (j + 1)], w[544 + 34 * j:544 + 34 * (j + 1)], w_two[544 + 34 * j:544 + 34 * (j + 1)],
                                               l[480 + 30 * j:480 + 30 * (j + 1)], k[96 + 8 * j: 96 + 8 * (j + 1)],
                                               1, round, resource_check)
    if (k_i % 2 == 0):
        for j in range(8):
            if ((Rcon[int(k_i/2)] >> j) & 1):
                X | k[248+j]

def SBox_bp12_all(eng, x0, x1, x2, x3, y, t, z, w, l, s, round, resource_check):
    for i in range(4):
        x0[8 * i:8 * (i + 1)] = Sbox(eng, x0[8 * i:8 * (i + 1)], y[27 * i:27 * (i + 1)], t[50 * i:50 * (i + 1)],
                                     z[41 * i:41 * (i + 1)], w[34 * i:34 * (i + 1)], l[30 * i:30 * (i + 1)],
                                     s[8 * i:8 * (i + 1)], 0, round, resource_check)

        x1[8 * i:8 * (i + 1)] = Sbox(eng, x1[8 * i:8 * (i + 1)], y[27 * (i + 4):27 * (i + 5)],
                                     t[50 * (i + 4):50 * (i + 5)], z[41 * (i + 4):41 * (i + 5)],
                                     w[34 * (i + 4):34 * (i + 5)], l[30 * (i + 4):30 * (i + 5)],
                                     s[8 * (i + 4):8 * (i + 5)], 0, round, resource_check)
        x2[8 * i:8 * (i + 1)] = Sbox(eng, x2[8 * i:8 * (i + 1)], y[27 * (i + 8):27 * (i + 9)],
                                     t[50 * (i + 8):50 * (i + 9)], z[41 * (i + 8):41 * (i + 9)],
                                     w[34 * (i + 8):34 * (i + 9)], l[30 * (i + 8):30 * (i + 9)],
                                     s[8 * (i + 8):8 * (i + 9)], 0, round, resource_check)

        x3[8 * i:8 * (i + 1)] = Sbox(eng, x3[8 * i:8 * (i + 1)], y[27 * (i + 12):27 * (i + 13)],
                                     t[50 * (i + 12):50 * (i + 13)], z[41 * (i + 12):41 * (i + 13)],
                                     w[34 * (i + 12):34 * (i + 13)], l[30 * (i + 12):30 * (i + 13)],
                                     s[8 * (i + 12):8 * (i + 13)], 0, round, resource_check)

def SBox_bp12_all_two(eng, x0, x1, x2, x3, y, t, z, z_two, w, w_two, l, s, round, resource_check):
    for i in range(4):
        x0[8 * i:8 * (i + 1)] = Sbox_two(eng, x0[8 * i:8 * (i + 1)], y[27 * i:27 * (i + 1)], t[50 * i:50 * (i + 1)],
                                     z[41 * i:41 * (i + 1)], z_two[41 * i:41 * (i + 1)], w[34 * i:34 * (i + 1)], w_two[34 * i:34 * (i + 1)], l[30 * i:30 * (i + 1)],
                                     s[8 * i:8 * (i + 1)], 0, round, resource_check)

        x1[8 * i:8 * (i + 1)] = Sbox_two(eng, x1[8 * i:8 * (i + 1)], y[27 * (i + 4):27 * (i + 5)],
                                     t[50 * (i + 4):50 * (i + 5)], z[41 * (i + 4):41 * (i + 5)], z_two[41 * (i + 4):41 * (i + 5)],
                                     w[34 * (i + 4):34 * (i + 5)], w_two[34 * (i + 4):34 * (i + 5)], l[30 * (i + 4):30 * (i + 5)],
                                     s[8 * (i + 4):8 * (i + 5)], 0, round, resource_check)
        x2[8 * i:8 * (i + 1)] = Sbox_two(eng, x2[8 * i:8 * (i + 1)], y[27 * (i + 8):27 * (i + 9)],
                                     t[50 * (i + 8):50 * (i + 9)], z[41 * (i + 8):41 * (i + 9)], z_two[41 * (i + 8):41 * (i + 9)],
                                     w[34 * (i + 8):34 * (i + 9)], w_two[34 * (i + 8):34 * (i + 9)], l[30 * (i + 8):30 * (i + 9)],
                                     s[8 * (i + 8):8 * (i + 9)], 0, round, resource_check)

        x3[8 * i:8 * (i + 1)] = Sbox_two(eng, x3[8 * i:8 * (i + 1)], y[27 * (i + 12):27 * (i + 13)],
                                     t[50 * (i + 12):50 * (i + 13)], z[41 * (i + 12):41 * (i + 13)], z_two[41 * (i + 12):41 * (i + 13)],
                                     w[34 * (i + 12):34 * (i + 13)], w_two[34 * (i + 12):34 * (i + 13)],  l[30 * (i + 12):30 * (i + 13)],
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

def reverse_CNOT(eng, a, b):
    CNOT | (b, a)

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

    if(i!=8):
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

def CNOT2_mc(eng, a, b, c):
    CNOT | (b, a)
    CNOT | (c, a)

def CNOT2(eng, a, b, c):
    CNOT | (a, c)
    CNOT | (b, c)

def Uncompute_sbox(eng, u_in, t, m, n, w, l, resource_check):

    u = []
    for i in range(8):
        u.append(u_in[7 - i])

    with Dagger(eng):
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

        # CNOT | (u[2], t[11])
        # CNOT | (u[5], t[11])

        CNOT | (u[2], t[15])
        CNOT | (u[5], t[15])
        CNOT | (u[2], t[26])
        CNOT | (u[5], t[26])

        CNOT | (t[2], t[12])
        CNOT | (t[3], t[12])
        CNOT | (t[4], t[14])

        CNOT | (t[4], t[15])
        # CNOT | (t[11], t[15])

        CNOT | (t[8], t[16])
        CNOT | (t[15], t[16])

        CNOT | (u[3], t[18])
        CNOT | (u[7], t[18])

        CNOT | (t[6], t[18])
        # CNOT | (t[17], t[18])
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

        Toffoli_gate(eng, t[12], t[5], m[0], resource_check)
        Toffoli_gate(eng, t[22], t[7], m[19], resource_check)

        Toffoli_gate(eng, t[18], u[7], m[20], resource_check)
        CNOT | (m[0], m[20])
        Toffoli_gate(eng, t[2], t[15], m[5], resource_check)
        Toffoli_gate(eng, t[21], t[8], m[21], resource_check)

        Toffoli_gate(eng, t[19], t[16], m[22], resource_check)
        CNOT | (m[5], m[22])
        CNOT | (m[5], m[21])
        Toffoli_gate(eng, t[0], t[14], m[10], resource_check)
        Toffoli_gate(eng, t[3], t[26], m[12], resource_check)

        CNOT | (m[10], m[12])
        Toffoli_gate(eng, t[1], t[9], m[13], resource_check)  # Here

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

        # ** ** ** ** ** ** *Layer

        # 41

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

        # # # # # # # # # # # # # # # # # # # # # # # /

        Toffoli_gate(eng, m[21], m[19], m[24], resource_check)

        CNOT2(eng, m[22], m[24], m[27])

        CNOT2(eng, m[20], m[24], m[25])

        Toffoli_gate(eng, m[44], m[22], m[28], resource_check)
        CNOT2(eng, m[26], m[24], m[29])

        Toffoli_gate(eng, m[20], m[47], m[30], resource_check)
        CNOT2(eng, m[23], m[24], m[31])

        # Toffoli_gate(eng, m[27], m[26], m[28])
        # Toffoli_gate(eng, m[25], m[23], m[29])
        # Toffoli_gate(eng, l[2], m[28], m[31])
        # Toffoli_gate(eng, l[3], m[30], m[34])

        Toffoli_gate(eng, m[23], t[5], n[0], resource_check)  # 2
        CNOT2(eng, m[22], m[31], n[1])
        CNOT2(eng, m[25], m[30], n[2])

        Toffoli_gate(eng, l[0], t[7], n[3], resource_check)  # 2

        Toffoli_gate(eng, l[1], u[7], n[5], resource_check)  # 2
        Toffoli_gate(eng, m[48], m[32], n[6], resource_check)  # 2

        CNOT2(eng, m[20], m[29], n[7])
        CNOT2(eng, m[27], m[28], n[8])
        Toffoli_gate(eng, m[26], t[15], n[9], resource_check)  # 2

        Toffoli_gate(eng, l[11], t[8], n[10], resource_check)  # 2

        Toffoli_gate(eng, m[45], t[16], n[12], resource_check)  # 2
        Toffoli_gate(eng, l[12], m[40], n[13], resource_check)  # 2

        # ** ** ** ** ** ** ** ** ** ** ** ** ** **

        Toffoli_gate(eng, l[13], t[14], n[15], resource_check)  # 2
        Toffoli_gate(eng, l[2], m[38], n[16], resource_check)  # 2
        Toffoli_gate(eng, n[14], m[39], w[8], resource_check)  # 2

        CNOT2(eng, m[29], m[31], n[17])
        CNOT2(eng, n[14], n[17], n[18])
        CNOT2(eng, m[27], m[28], n[19])
        CNOT2(eng, m[25], m[30], n[20])
        Toffoli_gate(eng, l[14], t[26], n[21], resource_check)  # 2
        Toffoli_gate(eng, l[3], m[43], n[22], resource_check)  # 2

        Toffoli_gate(eng, l[15], t[9], n[23], resource_check)  # 2
        Toffoli_gate(eng, l[4], m[37], n[24], resource_check)  # 2

        Toffoli_gate(eng, l[5], t[12], n[25], resource_check)  # 2

        Toffoli_gate(eng, l[6], t[22], n[26], resource_check)  # 2

        Toffoli_gate(eng, l[7], t[18], n[28], resource_check)  # 2
        Toffoli_gate(eng, m[49], m[41], n[29], resource_check)  # 2

        Toffoli_gate(eng, l[16], t[2], n[30], resource_check)  # 2

        Toffoli_gate(eng, l[17], t[21], n[31], resource_check)  # 2

        Toffoli_gate(eng, m[46], t[19], n[33], resource_check)  # 2
        Toffoli_gate(eng, l[18], m[42], n[34], resource_check)  # 2

        Toffoli_gate(eng, l[19], t[0], n[35], resource_check)  # 2
        Toffoli_gate(eng, l[8], m[33], n[36], resource_check)  # 2
        Toffoli_gate(eng, l[22], m[34], w[25], resource_check)  # 2

        Toffoli_gate(eng, l[20], t[3], n[37], resource_check)  # 2
        Toffoli_gate(eng, l[9], m[36], n[38], resource_check)  # 2

        Toffoli_gate(eng, l[21], t[1], n[39], resource_check)  # 2
        Toffoli_gate(eng, l[10], m[35], n[40], resource_check)  # 2

        # Clean

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

        # ** ** ** ** ** ** ** *Layer

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

        # l22 ~ 29 are idle state

        Toffoli_gate(eng, n[2], n[0], m[32], resource_check)  # 3
        Toffoli_gate(eng, n[1], t[5], w[1], resource_check)  # 3
        CNOT | (w[1], m[32])

        Toffoli_gate(eng, m[31], t[7], m[33], resource_check)  # 3
        Toffoli_gate(eng, n[3], m[30], w[2], resource_check)  # 3
        CNOT | (w[2], m[33])

        Toffoli_gate(eng, n[5], m[25], m[34], resource_check)  # 3
        # CNOT2(eng, w[3], n[6], m[34])
        CNOT | (n[6], m[34])

        Toffoli_gate(eng, n[7], t[15], m[35], resource_check)  # 3
        Toffoli_gate(eng, n[8], n[9], w[5], resource_check)  # 3
        # CNOT2(eng, w[4], w[5], m[35])
        CNOT | (w[5], m[35])

        Toffoli_gate(eng, m[29], t[8], m[36], resource_check)  # 3
        Toffoli_gate(eng, m[28], n[10], w[6], resource_check)  # 3

        CNOT | (w[6], m[36])

        Toffoli_gate(eng, m[27], n[13], m[37], resource_check)  # 3
        # CNOT2(eng, w[7], n[12], m[37])
        CNOT | (n[12], m[37])

        Toffoli_gate(eng, n[15], l[3], m[38], resource_check)  # 3
        Toffoli_gate(eng, n[16], l[0], w[10], resource_check)  # 3
        # CNOT2(eng, w[8], w[9], m[38])
        CNOT | (w[8], m[38])
        CNOT | (w[10], m[38])

        Toffoli_gate(eng, n[18], t[26], m[39], resource_check)  # 3
        Toffoli_gate(eng, n[19], n[21], w[12], resource_check)  # 3
        Toffoli_gate(eng, n[20], n[22], w[13], resource_check)  # 3
        # CNOT2(eng, w[11], w[12], m[39])
        CNOT | (w[12], m[39])
        CNOT | (w[13], m[39])

        Toffoli_gate(eng, l[6], n[23], m[40], resource_check)  # 3
        Toffoli_gate(eng, n[17], t[9], w[15], resource_check)  # 3
        Toffoli_gate(eng, l[10], n[24], w[16], resource_check)  # 3
        # CNOT2(eng, w[14], w[15], m[40])
        CNOT | (w[15], m[40])
        CNOT | (w[16], m[40])

        Toffoli_gate(eng, l[15], n[25], m[41], resource_check)  # 3
        Toffoli_gate(eng, l[14], t[12], w[18], resource_check)  # 3
        # CNOT2(eng, w[17], w[18], m[41])
        CNOT | (w[18], m[41])

        Toffoli_gate(eng, l[13], t[22], m[42], resource_check)  # 3
        Toffoli_gate(eng, n[26], l[11], w[19], resource_check)  # 3
        CNOT | (w[19], m[42])

        Toffoli_gate(eng, n[28], l[1], m[43], resource_check)  # 3
        # CNOT2(eng, w[20], n[29], m[43])
        CNOT | (n[29], m[43])

        Toffoli_gate(eng, l[16], t[2], m[44], resource_check)  # 3
        Toffoli_gate(eng, l[17], n[30], w[22], resource_check)  # 3
        # CNOT2(eng, w[21], w[22], m[44])
        CNOT | (w[22], m[44])

        Toffoli_gate(eng, l[9], t[21], m[45], resource_check)  # 3
        Toffoli_gate(eng, l[7], n[31], w[23], resource_check)  # 3
        # CNOT2(eng, w[23], n[32], m[45])
        CNOT | (w[23], m[45])

        Toffoli_gate(eng, l[4], n[34], m[46], resource_check)  # 3
        # CNOT2(eng, w[24], n[33], m[46])
        CNOT | (n[33], m[46])

        Toffoli_gate(eng, n[35], l[5], m[47], resource_check)  # 3
        Toffoli_gate(eng, n[36], l[2], w[27], resource_check)  # 3

        # CNOT2(eng, w[25], w[26], m[47])
        CNOT | (w[25], m[47])
        CNOT | (w[27], m[47])

        Toffoli_gate(eng, l[19], t[3], m[48], resource_check)  # 3
        Toffoli_gate(eng, l[20], n[37], w[29], resource_check)  # 3
        Toffoli_gate(eng, l[21], n[38], w[30], resource_check)  # 3
        # CNOT2(eng, w[28], w[29], m[48])
        CNOT | (w[29], m[48])
        CNOT | (w[30], m[48])

        Toffoli_gate(eng, l[8], n[39], m[49], resource_check)  # 3
        Toffoli_gate(eng, l[18], t[1], w[32], resource_check)  # 3
        Toffoli_gate(eng, l[12], n[40], w[33], resource_check)  # 3
        # CNOT2(eng, w[31], w[32], m[49])
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

def Uncompute_sbox_special(eng, u_in, t, m, n, w, l, resource_check):

    u = []
    for i in range(8):
        u.append(u_in[7 - i])

    with Dagger(eng):
        CNOT | (l[12], l[15])  #
        CNOT | (m[26], l[16])  #
        CNOT | (l[11], l[17])  #
        CNOT | (l[12], l[18])  #
        CNOT | (l[13], l[19])  #
        CNOT | (l[14], l[20])  #
        CNOT | (l[15], l[21])  #

        CNOT | (n[14], l[22])  #

        # # # # # # # # # # # # # # # # # # # # # # # /

        Toffoli_gate(eng, m[21], m[19], m[24], resource_check)

        CNOT2(eng, m[22], m[24], m[27])

        CNOT2(eng, m[20], m[24], m[25])

        Toffoli_gate(eng, m[44], m[22], m[28], resource_check)
        CNOT2(eng, m[26], m[24], m[29])

        Toffoli_gate(eng, m[20], m[47], m[30], resource_check)
        CNOT2(eng, m[23], m[24], m[31])

        # Toffoli_gate(eng, m[27], m[26], m[28])
        # Toffoli_gate(eng, m[25], m[23], m[29])
        # Toffoli_gate(eng, l[2], m[28], m[31])
        # Toffoli_gate(eng, l[3], m[30], m[34])

        Toffoli_gate(eng, m[23], t[5], n[0], resource_check)  # 2
        CNOT2(eng, m[22], m[31], n[1])
        CNOT2(eng, m[25], m[30], n[2])

        Toffoli_gate(eng, l[0], t[7], n[3], resource_check)  # 2

        Toffoli_gate(eng, l[1], u[7], n[5], resource_check)  # 2
        Toffoli_gate(eng, m[48], m[32], n[6], resource_check)  # 2

        CNOT2(eng, m[20], m[29], n[7])
        CNOT2(eng, m[27], m[28], n[8])
        Toffoli_gate(eng, m[26], t[15], n[9], resource_check)  # 2

        Toffoli_gate(eng, l[11], t[8], n[10], resource_check)  # 2

        Toffoli_gate(eng, m[45], t[16], n[12], resource_check)  # 2
        Toffoli_gate(eng, l[12], m[40], n[13], resource_check)  # 2

        # ** ** ** ** ** ** ** ** ** ** ** ** ** **

        Toffoli_gate(eng, l[13], t[14], n[15], resource_check)  # 2
        Toffoli_gate(eng, l[2], m[38], n[16], resource_check)  # 2
        Toffoli_gate(eng, n[14], m[39], w[8], resource_check)  # 2

        CNOT2(eng, m[29], m[31], n[17])
        CNOT2(eng, n[14], n[17], n[18])
        CNOT2(eng, m[27], m[28], n[19])
        CNOT2(eng, m[25], m[30], n[20])
        Toffoli_gate(eng, l[14], t[26], n[21], resource_check)  # 2
        Toffoli_gate(eng, l[3], m[43], n[22], resource_check)  # 2

        Toffoli_gate(eng, l[15], t[9], n[23], resource_check)  # 2
        Toffoli_gate(eng, l[4], m[37], n[24], resource_check)  # 2

        Toffoli_gate(eng, l[5], t[12], n[25], resource_check)  # 2

        Toffoli_gate(eng, l[6], t[22], n[26], resource_check)  # 2

        Toffoli_gate(eng, l[7], t[18], n[28], resource_check)  # 2
        Toffoli_gate(eng, m[49], m[41], n[29], resource_check)  # 2

        Toffoli_gate(eng, l[16], t[2], n[30], resource_check)  # 2

        Toffoli_gate(eng, l[17], t[21], n[31], resource_check)  # 2

        Toffoli_gate(eng, m[46], t[19], n[33], resource_check)  # 2
        Toffoli_gate(eng, l[18], m[42], n[34], resource_check)  # 2

        Toffoli_gate(eng, l[19], t[0], n[35], resource_check)  # 2
        Toffoli_gate(eng, l[8], m[33], n[36], resource_check)  # 2
        Toffoli_gate(eng, l[22], m[34], w[25], resource_check)  # 2

        Toffoli_gate(eng, l[20], t[3], n[37], resource_check)  # 2
        Toffoli_gate(eng, l[9], m[36], n[38], resource_check)  # 2

        Toffoli_gate(eng, l[21], t[1], n[39], resource_check)  # 2
        Toffoli_gate(eng, l[10], m[35], n[40], resource_check)  # 2

        # Clean

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

        # ** ** ** ** ** ** ** *Layer

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

        # l22 ~ 29 are idle state

        Toffoli_gate(eng, n[2], n[0], m[32], resource_check)  # 3
        Toffoli_gate(eng, n[1], t[5], w[1], resource_check)  # 3
        CNOT | (w[1], m[32])

        Toffoli_gate(eng, m[31], t[7], m[33], resource_check)  # 3
        Toffoli_gate(eng, n[3], m[30], w[2], resource_check)  # 3
        CNOT | (w[2], m[33])

        Toffoli_gate(eng, n[5], m[25], m[34], resource_check)  # 3
        # CNOT2(eng, w[3], n[6], m[34])
        CNOT | (n[6], m[34])

        Toffoli_gate(eng, n[7], t[15], m[35], resource_check)  # 3
        Toffoli_gate(eng, n[8], n[9], w[5], resource_check)  # 3
        # CNOT2(eng, w[4], w[5], m[35])
        CNOT | (w[5], m[35])

        Toffoli_gate(eng, m[29], t[8], m[36], resource_check)  # 3
        Toffoli_gate(eng, m[28], n[10], w[6], resource_check)  # 3

        CNOT | (w[6], m[36])

        Toffoli_gate(eng, m[27], n[13], m[37], resource_check)  # 3
        # CNOT2(eng, w[7], n[12], m[37])
        CNOT | (n[12], m[37])

        Toffoli_gate(eng, n[15], l[3], m[38], resource_check)  # 3
        Toffoli_gate(eng, n[16], l[0], w[10], resource_check)  # 3
        # CNOT2(eng, w[8], w[9], m[38])
        CNOT | (w[8], m[38])
        CNOT | (w[10], m[38])

        Toffoli_gate(eng, n[18], t[26], m[39], resource_check)  # 3
        Toffoli_gate(eng, n[19], n[21], w[12], resource_check)  # 3
        Toffoli_gate(eng, n[20], n[22], w[13], resource_check)  # 3
        # CNOT2(eng, w[11], w[12], m[39])
        CNOT | (w[12], m[39])
        CNOT | (w[13], m[39])

        Toffoli_gate(eng, l[6], n[23], m[40], resource_check)  # 3
        Toffoli_gate(eng, n[17], t[9], w[15], resource_check)  # 3
        Toffoli_gate(eng, l[10], n[24], w[16], resource_check)  # 3
        # CNOT2(eng, w[14], w[15], m[40])
        CNOT | (w[15], m[40])
        CNOT | (w[16], m[40])

        Toffoli_gate(eng, l[15], n[25], m[41], resource_check)  # 3
        Toffoli_gate(eng, l[14], t[12], w[18], resource_check)  # 3
        # CNOT2(eng, w[17], w[18], m[41])
        CNOT | (w[18], m[41])

        Toffoli_gate(eng, l[13], t[22], m[42], resource_check)  # 3
        Toffoli_gate(eng, n[26], l[11], w[19], resource_check)  # 3
        CNOT | (w[19], m[42])

        Toffoli_gate(eng, n[28], l[1], m[43], resource_check)  # 3
        # CNOT2(eng, w[20], n[29], m[43])
        CNOT | (n[29], m[43])

        Toffoli_gate(eng, l[16], t[2], m[44], resource_check)  # 3
        Toffoli_gate(eng, l[17], n[30], w[22], resource_check)  # 3
        # CNOT2(eng, w[21], w[22], m[44])
        CNOT | (w[22], m[44])

        Toffoli_gate(eng, l[9], t[21], m[45], resource_check)  # 3
        Toffoli_gate(eng, l[7], n[31], w[23], resource_check)  # 3
        # CNOT2(eng, w[23], n[32], m[45])
        CNOT | (w[23], m[45])

        Toffoli_gate(eng, l[4], n[34], m[46], resource_check)  # 3
        # CNOT2(eng, w[24], n[33], m[46])
        CNOT | (n[33], m[46])

        Toffoli_gate(eng, n[35], l[5], m[47], resource_check)  # 3
        Toffoli_gate(eng, n[36], l[2], w[27], resource_check)  # 3

        # CNOT2(eng, w[25], w[26], m[47])
        CNOT | (w[25], m[47])
        CNOT | (w[27], m[47])

        Toffoli_gate(eng, l[19], t[3], m[48], resource_check)  # 3
        Toffoli_gate(eng, l[20], n[37], w[29], resource_check)  # 3
        Toffoli_gate(eng, l[21], n[38], w[30], resource_check)  # 3
        # CNOT2(eng, w[28], w[29], m[48])
        CNOT | (w[29], m[48])
        CNOT | (w[30], m[48])

        Toffoli_gate(eng, l[8], n[39], m[49], resource_check)  # 3
        Toffoli_gate(eng, l[18], t[1], w[32], resource_check)  # 3
        Toffoli_gate(eng, l[12], n[40], w[33], resource_check)  # 3
        # CNOT2(eng, w[31], w[32], m[49])
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

def Uncompute_sbox_two(eng, u_in, t, m, n, n_two, w, w_two, l, resource_check):

    u = []
    for i in range(8):
        u.append(u_in[7 - i])

    with Dagger(eng):
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

        # CNOT | (u[2], t[11])
        # CNOT | (u[5], t[11])

        CNOT | (u[2], t[15])
        CNOT | (u[5], t[15])
        CNOT | (u[2], t[26])
        CNOT | (u[5], t[26])

        CNOT | (t[2], t[12])
        CNOT | (t[3], t[12])
        CNOT | (t[4], t[14])

        CNOT | (t[4], t[15])
        # CNOT | (t[11], t[15])

        CNOT | (t[8], t[16])
        CNOT | (t[15], t[16])

        CNOT | (u[3], t[18])
        CNOT | (u[7], t[18])

        CNOT | (t[6], t[18])
        # CNOT | (t[17], t[18])
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

        Toffoli_gate(eng, t[12], t[5], m[0], resource_check)
        Toffoli_gate(eng, t[22], t[7], m[19], resource_check)

        Toffoli_gate(eng, t[18], u[7], m[20], resource_check)
        CNOT | (m[0], m[20])
        Toffoli_gate(eng, t[2], t[15], m[5], resource_check)
        Toffoli_gate(eng, t[21], t[8], m[21], resource_check)

        Toffoli_gate(eng, t[19], t[16], m[22], resource_check)
        CNOT | (m[5], m[22])
        CNOT | (m[5], m[21])
        Toffoli_gate(eng, t[0], t[14], m[10], resource_check)
        Toffoli_gate(eng, t[3], t[26], m[12], resource_check)

        CNOT | (m[10], m[12])
        Toffoli_gate(eng, t[1], t[9], m[13], resource_check)  # Here
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

        # ** ** ** ** ** ** *Layer

        # 41

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

        # # # # # # # # # # # # # # # # # # # # # # #

        Toffoli_gate(eng, m[21], m[19], w_two[33], resource_check)

        CNOT2(eng, m[22], w_two[33], m[27])

        CNOT2(eng, m[20], w_two[33], m[25])

        Toffoli_gate(eng, m[44], m[22], w_two[32], resource_check)
        CNOT2(eng, m[26], w_two[33], m[29])

        Toffoli_gate(eng, m[20], m[47], w_two[30], resource_check)
        CNOT2(eng, m[23], w_two[33], m[31])

        # Toffoli_gate(eng, m[27], m[26], w_two[32])
        # Toffoli_gate(eng, m[25], m[23], m[29])
        # Toffoli_gate(eng, l[2], w_two[32], m[31])
        # Toffoli_gate(eng, l[3], w_two[30], m[34])

        Toffoli_gate(eng, m[23], t[5], w_two[29], resource_check)  # 2
        CNOT2(eng, m[22], m[31], n[1])
        CNOT2(eng, m[25], w_two[30], n[2])

        Toffoli_gate(eng, l[0], t[7], w_two[27], resource_check)  # 2

        Toffoli_gate(eng, l[1], u[7], w_two[23], resource_check)  # 2
        Toffoli_gate(eng, m[48], m[32], w_two[22], resource_check)  # 2

        CNOT2(eng, m[20], m[29], n[7])
        CNOT2(eng, m[27], w_two[32], n[8])
        Toffoli_gate(eng, m[26], t[15], w_two[19], resource_check)  # 2

        Toffoli_gate(eng, l[11], t[8], w_two[18], resource_check)  # 2

        Toffoli_gate(eng, m[45], t[16], w_two[16], resource_check)  # 2
        Toffoli_gate(eng, l[12], m[40], w_two[15], resource_check)  # 2

        # ** ** ** ** ** ** ** ** ** ** ** ** ** **

        Toffoli_gate(eng, l[13], t[14], w_two[13], resource_check)  # 2
        Toffoli_gate(eng, l[2], m[38], w_two[12], resource_check)  # 2
        Toffoli_gate(eng, n[14], m[39], w_two[10], resource_check)  # 2

        CNOT2(eng, m[29], m[31], n[17])
        CNOT2(eng, n[14], n[17], n[18])
        CNOT2(eng, m[27], w_two[32], n[19])
        CNOT2(eng, m[25], w_two[30], n[20])
        Toffoli_gate(eng, l[14], t[26], w_two[6], resource_check)  # 2
        Toffoli_gate(eng, l[3], m[43], w_two[5], resource_check)  # 2

        Toffoli_gate(eng, l[15], t[9], w_two[2], resource_check)  # 2
        Toffoli_gate(eng, l[4], m[37], w_two[1], resource_check)  # 2

        Toffoli_gate(eng, l[5], t[12], n[25], resource_check)  # 2

        Toffoli_gate(eng, l[6], t[22], n[26], resource_check)  # 2

        Toffoli_gate(eng, l[7], t[18], n[28], resource_check)  # 2
        Toffoli_gate(eng, m[49], m[41], n[29], resource_check)  # 2

        Toffoli_gate(eng, l[16], t[2], n[30], resource_check)  # 2

        Toffoli_gate(eng, l[17], t[21], n[31], resource_check)  # 2

        Toffoli_gate(eng, m[46], t[19], n[33], resource_check)  # 2
        Toffoli_gate(eng, l[18], m[42], n[34], resource_check)  # 2

        Toffoli_gate(eng, l[19], t[0], n[35], resource_check)  # 2
        Toffoli_gate(eng, l[8], m[33], n[36], resource_check)  # 2
        Toffoli_gate(eng, l[22], m[34], w[25], resource_check)  # 2

        Toffoli_gate(eng, l[20], t[3], n[37], resource_check)  # 2
        Toffoli_gate(eng, l[9], m[36], n[38], resource_check)  # 2

        Toffoli_gate(eng, l[21], t[1], n[39], resource_check)  # 2
        Toffoli_gate(eng, l[10], m[35], n[40], resource_check)  # 2

        # Clean

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

        # ** ** ** ** ** ** ** *Layer

        CNOT | (m[25], l[0])
        CNOT | (m[25], l[1])
        CNOT | (m[25], l[2])

        CNOT | (m[27], l[3])
        CNOT | (m[27], l[4])
        CNOT | (m[27], l[5])

        CNOT | (w_two[32], l[6])
        CNOT | (w_two[32], l[7])
        CNOT | (w_two[32], l[8])

        CNOT | (m[29], l[9])

        CNOT | (w_two[30], l[10])
        CNOT | (w_two[30], l[11])
        CNOT | (w_two[30], l[12])

        CNOT | (m[31], l[13])
        CNOT | (n[1], l[14])
        CNOT | (n[2], l[15])
        CNOT | (n[7], l[16])
        CNOT | (n[8], l[17])

        CNOT | (n[17], l[18])
        CNOT | (n[18], l[19])
        CNOT | (n[19], l[20])
        CNOT | (n[20], l[21])



        Toffoli_gate(eng, n[2], w_two[29], m[32], resource_check)  # 3
        Toffoli_gate(eng, n[1], t[5], n_two[40], resource_check)  # 3
        CNOT | (n_two[40], m[32])

        Toffoli_gate(eng, m[31], t[7], m[33], resource_check)  # 3
        Toffoli_gate(eng, w_two[27], w_two[30], n_two[39], resource_check)  # 3
        CNOT | (n_two[39], m[33])

        Toffoli_gate(eng, w_two[23], m[25], m[34], resource_check)  # 3
        # CNOT2(eng, w[3], w_two[22], m[34])
        CNOT | (w_two[22], m[34])

        Toffoli_gate(eng, n[7], t[15], m[35], resource_check)  # 3
        Toffoli_gate(eng, n[8], w_two[19], n_two[38], resource_check)  # 3
        # CNOT2(eng, w[4], n_two[38], m[35])
        CNOT | (n_two[38], m[35])

        Toffoli_gate(eng, m[29], t[8], m[36], resource_check)  # 3
        Toffoli_gate(eng, w_two[32], w_two[18], n_two[37], resource_check)  # 3

        CNOT | (n_two[37], m[36])

        Toffoli_gate(eng, m[27], w_two[15], m[37], resource_check)  # 3
        # CNOT2(eng, w[7], w_two[16], m[37])
        CNOT | (w_two[16], m[37])

        Toffoli_gate(eng, w_two[13], l[3], m[38], resource_check)  # 3
        Toffoli_gate(eng, w_two[12], l[0], n_two[36], resource_check)  # 3
        # CNOT2(eng, w_two[10], w[9], m[38])
        CNOT | (w_two[10], m[38])
        CNOT | (n_two[36], m[38])

        Toffoli_gate(eng, n[18], t[26], m[39], resource_check)  # 3
        Toffoli_gate(eng, n[19], w_two[6], n_two[35], resource_check)  # 3
        Toffoli_gate(eng, n[20], w_two[5], n_two[34], resource_check)  # 3
        # CNOT2(eng, w[11], n_two[35], m[39])
        CNOT | (n_two[35], m[39])
        CNOT | (n_two[34], m[39])

        Toffoli_gate(eng, l[6], w_two[2], m[40], resource_check)  # 3
        Toffoli_gate(eng, n[17], t[9], n_two[33], resource_check)  # 3
        Toffoli_gate(eng, l[10], w_two[1], n_two[31], resource_check)  # 3
        # CNOT2(eng, w[14], n_two[33], m[40])
        CNOT | (n_two[33], m[40])
        CNOT | (n_two[31], m[40])

        Toffoli_gate(eng, l[15], n[25], m[41], resource_check)  # 3
        Toffoli_gate(eng, l[14], t[12], n_two[30], resource_check)  # 3
        # CNOT2(eng, w[17], n_two[30], m[41])
        CNOT | (n_two[30], m[41])

        Toffoli_gate(eng, l[13], t[22], m[42], resource_check)  # 3
        Toffoli_gate(eng, n[26], l[11], n_two[29], resource_check)  # 3
        CNOT | (n_two[29], m[42])

        Toffoli_gate(eng, n[28], l[1], m[43], resource_check)  # 3
        # CNOT2(eng, w[20], n[29], m[43])
        CNOT | (n[29], m[43])

        Toffoli_gate(eng, l[16], t[2], m[44], resource_check)  # 3
        Toffoli_gate(eng, l[17], n[30], n_two[28], resource_check)  # 3
        # CNOT2(eng, w[21], n_two[28], m[44])
        CNOT | (n_two[28], m[44])

        Toffoli_gate(eng, l[9], t[21], m[45], resource_check)  # 3
        Toffoli_gate(eng, l[7], n[31], n_two[26], resource_check)  # 3
        # CNOT2(eng, n_two[26], n[32], m[45])
        CNOT | (n_two[26], m[45])

        Toffoli_gate(eng, l[4], n[34], m[46], resource_check)  # 3
        # CNOT2(eng, w[24], n[33], m[46])
        CNOT | (n[33], m[46])

        Toffoli_gate(eng, n[35], l[5], m[47], resource_check)  # 3
        Toffoli_gate(eng, n[36], l[2], n_two[25], resource_check)  # 3

        # CNOT2(eng, w[25], w[26], m[47])
        CNOT | (w[25], m[47])
        CNOT | (n_two[25], m[47])

        Toffoli_gate(eng, l[19], t[3], m[48], resource_check)  # 3
        Toffoli_gate(eng, l[20], n[37], n_two[24], resource_check)  # 3
        Toffoli_gate(eng, l[21], n[38], n_two[23], resource_check)  # 3
        # CNOT2(eng, w[28], n_two[24], m[48])
        CNOT | (n_two[24], m[48])
        CNOT | (n_two[23], m[48])

        Toffoli_gate(eng, l[8], n[39], m[49], resource_check)  # 3
        Toffoli_gate(eng, l[18], t[1], n_two[22], resource_check)  # 3
        Toffoli_gate(eng, l[12], n[40], n_two[21], resource_check)  # 3
        # CNOT2(eng, w[31], n_two[22], m[49])
        CNOT | (n_two[22], m[49])
        CNOT | (n_two[21], m[49])

        CNOT | (m[25], l[0])
        CNOT | (m[25], l[1])
        CNOT | (m[25], l[2])

        CNOT | (m[27], l[3])
        CNOT | (m[27], l[4])
        CNOT | (m[27], l[5])

        CNOT | (w_two[32], l[6])
        CNOT | (w_two[32], l[7])
        CNOT | (w_two[32], l[8])

        CNOT | (m[29], l[9])

        CNOT | (w_two[30], l[10])
        CNOT | (w_two[30], l[11])
        CNOT | (w_two[30], l[12])

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

def Sbox(eng, u_in, t, m, n, w, l, s, flag, round, resource_check):
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

        # CNOT | (u[2], t[11])
        # CNOT | (u[5], t[11])

        CNOT | (u[2], t[15])
        CNOT | (u[5], t[15])
        CNOT | (u[2], t[26])
        CNOT | (u[5], t[26])

        CNOT | (t[2], t[12])
        CNOT | (t[3], t[12])
        CNOT | (t[4], t[14])

        CNOT | (t[4], t[15])
        # CNOT | (t[11], t[15])

        CNOT | (t[8], t[16])
        CNOT | (t[15], t[16])

        CNOT | (u[3], t[18])
        CNOT | (u[7], t[18])

        CNOT | (t[6], t[18])
        # CNOT | (t[17], t[18])
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

        Toffoli_gate(eng, t[12], t[5], m[0], resource_check)
        Toffoli_gate(eng, t[22], t[7], m[19], resource_check)

        Toffoli_gate(eng, t[18], u[7], m[20], resource_check)
        CNOT | (m[0], m[20])
        Toffoli_gate(eng, t[2], t[15], m[5], resource_check)
        Toffoli_gate(eng, t[21], t[8], m[21], resource_check)

        Toffoli_gate(eng, t[19], t[16], m[22], resource_check)
        CNOT | (m[5], m[22])
        CNOT | (m[5], m[21])
        Toffoli_gate(eng, t[0], t[14], m[10], resource_check)
        Toffoli_gate(eng, t[3], t[26], m[12], resource_check)

        CNOT | (m[10], m[12])
        Toffoli_gate(eng, t[1], t[9], m[13], resource_check)  # Here

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

        # ** ** ** ** ** ** *Layer

        # 41

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

        # # # # # # # # # # # # # # # # # # # # # # # /

        Toffoli_gate(eng, m[21], m[19], m[24], resource_check)

        CNOT2(eng, m[22], m[24], m[27])

        CNOT2(eng, m[20], m[24], m[25])

        Toffoli_gate(eng, m[44], m[22], m[28], resource_check)
        CNOT2(eng, m[26], m[24], m[29])

        Toffoli_gate(eng, m[20], m[47], m[30], resource_check)
        CNOT2(eng, m[23], m[24], m[31])

        # Toffoli_gate(eng, m[27], m[26], m[28])
        # Toffoli_gate(eng, m[25], m[23], m[29])
        # Toffoli_gate(eng, l[2], m[28], m[31])
        # Toffoli_gate(eng, l[3], m[30], m[34])

        Toffoli_gate(eng, m[23], t[5], n[0], resource_check)  # 2
        CNOT2(eng, m[22], m[31], n[1])
        CNOT2(eng, m[25], m[30], n[2])

        Toffoli_gate(eng, l[0], t[7], n[3], resource_check)  # 2

        Toffoli_gate(eng, l[1], u[7], n[5], resource_check)  # 2
        Toffoli_gate(eng, m[48], m[32], n[6], resource_check)  # 2

        CNOT2(eng, m[20], m[29], n[7])
        CNOT2(eng, m[27], m[28], n[8])
        Toffoli_gate(eng, m[26], t[15], n[9], resource_check)  # 2

        Toffoli_gate(eng, l[11], t[8], n[10], resource_check)  # 2

        Toffoli_gate(eng, m[45], t[16], n[12], resource_check)  # 2
        Toffoli_gate(eng, l[12], m[40], n[13], resource_check)  # 2

        # ** ** ** ** ** ** ** ** ** ** ** ** ** **

        Toffoli_gate(eng, l[13], t[14], n[15], resource_check)  # 2
        Toffoli_gate(eng, l[2], m[38], n[16], resource_check)  # 2
        Toffoli_gate(eng, n[14], m[39], w[8], resource_check)  # 2

        CNOT2(eng, m[29], m[31], n[17])
        CNOT2(eng, n[14], n[17], n[18])
        CNOT2(eng, m[27], m[28], n[19])
        CNOT2(eng, m[25], m[30], n[20])
        Toffoli_gate(eng, l[14], t[26], n[21], resource_check)  # 2
        Toffoli_gate(eng, l[3], m[43], n[22], resource_check)  # 2

        Toffoli_gate(eng, l[15], t[9], n[23], resource_check)  # 2
        Toffoli_gate(eng, l[4], m[37], n[24], resource_check)  # 2

        Toffoli_gate(eng, l[5], t[12], n[25], resource_check)  # 2

        Toffoli_gate(eng, l[6], t[22], n[26], resource_check)  # 2

        Toffoli_gate(eng, l[7], t[18], n[28], resource_check)  # 2
        Toffoli_gate(eng, m[49], m[41], n[29], resource_check)  # 2

        Toffoli_gate(eng, l[16], t[2], n[30], resource_check)  # 2

        Toffoli_gate(eng, l[17], t[21], n[31], resource_check)  # 2

        Toffoli_gate(eng, m[46], t[19], n[33], resource_check)  # 2
        Toffoli_gate(eng, l[18], m[42], n[34], resource_check)  # 2

        Toffoli_gate(eng, l[19], t[0], n[35], resource_check)  # 2
        Toffoli_gate(eng, l[8], m[33], n[36], resource_check)  # 2
        Toffoli_gate(eng, l[22], m[34], w[25], resource_check)  # 2

        Toffoli_gate(eng, l[20], t[3], n[37], resource_check)  # 2
        Toffoli_gate(eng, l[9], m[36], n[38], resource_check)  # 2

        Toffoli_gate(eng, l[21], t[1], n[39], resource_check)  # 2
        Toffoli_gate(eng, l[10], m[35], n[40], resource_check)  # 2

        # Clean

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

        # ** ** ** ** ** ** ** *Layer

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

        # l22 ~ 29 are idle state

        Toffoli_gate(eng, n[2], n[0], m[32], resource_check)  # 3
        Toffoli_gate(eng, n[1], t[5], w[1], resource_check)  # 3
        CNOT | (w[1], m[32])

        Toffoli_gate(eng, m[31], t[7], m[33], resource_check)  # 3
        Toffoli_gate(eng, n[3], m[30], w[2], resource_check)  # 3
        CNOT | (w[2], m[33])

        Toffoli_gate(eng, n[5], m[25], m[34], resource_check)  # 3
        # CNOT2(eng, w[3], n[6], m[34])
        CNOT | (n[6], m[34])

        Toffoli_gate(eng, n[7], t[15], m[35], resource_check)  # 3
        Toffoli_gate(eng, n[8], n[9], w[5], resource_check)  # 3
        # CNOT2(eng, w[4], w[5], m[35])
        CNOT | (w[5], m[35])

        Toffoli_gate(eng, m[29], t[8], m[36], resource_check)  # 3
        Toffoli_gate(eng, m[28], n[10], w[6], resource_check)  # 3

        CNOT | (w[6], m[36])

        Toffoli_gate(eng, m[27], n[13], m[37], resource_check)  # 3
        # CNOT2(eng, w[7], n[12], m[37])
        CNOT | (n[12], m[37])

        Toffoli_gate(eng, n[15], l[3], m[38], resource_check)  # 3
        Toffoli_gate(eng, n[16], l[0], w[10], resource_check)  # 3
        # CNOT2(eng, w[8], w[9], m[38])
        CNOT | (w[8], m[38])
        CNOT | (w[10], m[38])

        Toffoli_gate(eng, n[18], t[26], m[39], resource_check)  # 3
        Toffoli_gate(eng, n[19], n[21], w[12], resource_check)  # 3
        Toffoli_gate(eng, n[20], n[22], w[13], resource_check)  # 3
        # CNOT2(eng, w[11], w[12], m[39])
        CNOT | (w[12], m[39])
        CNOT | (w[13], m[39])

        Toffoli_gate(eng, l[6], n[23], m[40], resource_check)  # 3
        Toffoli_gate(eng, n[17], t[9], w[15], resource_check)  # 3
        Toffoli_gate(eng, l[10], n[24], w[16], resource_check)  # 3
        # CNOT2(eng, w[14], w[15], m[40])
        CNOT | (w[15], m[40])
        CNOT | (w[16], m[40])

        Toffoli_gate(eng, l[15], n[25], m[41], resource_check)  # 3
        Toffoli_gate(eng, l[14], t[12], w[18], resource_check)  # 3
        # CNOT2(eng, w[17], w[18], m[41])
        CNOT | (w[18], m[41])

        Toffoli_gate(eng, l[13], t[22], m[42], resource_check)  # 3
        Toffoli_gate(eng, n[26], l[11], w[19], resource_check)  # 3
        CNOT | (w[19], m[42])

        Toffoli_gate(eng, n[28], l[1], m[43], resource_check)  # 3
        # CNOT2(eng, w[20], n[29], m[43])
        CNOT | (n[29], m[43])

        Toffoli_gate(eng, l[16], t[2], m[44], resource_check)  # 3
        Toffoli_gate(eng, l[17], n[30], w[22], resource_check)  # 3
        # CNOT2(eng, w[21], w[22], m[44])
        CNOT | (w[22], m[44])

        Toffoli_gate(eng, l[9], t[21], m[45], resource_check)  # 3
        Toffoli_gate(eng, l[7], n[31], w[23], resource_check)  # 3
        # CNOT2(eng, w[23], n[32], m[45])
        CNOT | (w[23], m[45])

        Toffoli_gate(eng, l[4], n[34], m[46], resource_check)  # 3
        # CNOT2(eng, w[24], n[33], m[46])
        CNOT | (n[33], m[46])

        Toffoli_gate(eng, n[35], l[5], m[47], resource_check)  # 3
        Toffoli_gate(eng, n[36], l[2], w[27], resource_check)  # 3

        # CNOT2(eng, w[25], w[26], m[47])
        CNOT | (w[25], m[47])
        CNOT | (w[27], m[47])

        Toffoli_gate(eng, l[19], t[3], m[48], resource_check)  # 3
        Toffoli_gate(eng, l[20], n[37], w[29], resource_check)  # 3
        Toffoli_gate(eng, l[21], n[38], w[30], resource_check)  # 3
        # CNOT2(eng, w[28], w[29], m[48])
        CNOT | (w[29], m[48])
        CNOT | (w[30], m[48])

        Toffoli_gate(eng, l[8], n[39], m[49], resource_check)  # 3
        Toffoli_gate(eng, l[18], t[1], w[32], resource_check)  # 3
        Toffoli_gate(eng, l[12], n[40], w[33], resource_check)  # 3
        # CNOT2(eng, w[31], w[32], m[49])
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

def Sbox_two(eng, u_in, t, m, n, n_two, w, w_two, l, s, flag, round, resource_check):
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

        # CNOT | (u[2], t[11])
        # CNOT | (u[5], t[11])

        CNOT | (u[2], t[15])
        CNOT | (u[5], t[15])
        CNOT | (u[2], t[26])
        CNOT | (u[5], t[26])

        CNOT | (t[2], t[12])
        CNOT | (t[3], t[12])
        CNOT | (t[4], t[14])

        CNOT | (t[4], t[15])
        # CNOT | (t[11], t[15])

        CNOT | (t[8], t[16])
        CNOT | (t[15], t[16])

        CNOT | (u[3], t[18])
        CNOT | (u[7], t[18])

        CNOT | (t[6], t[18])
        # CNOT | (t[17], t[18])
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

        Toffoli_gate(eng, t[12], t[5], m[0], resource_check)
        Toffoli_gate(eng, t[22], t[7], m[19], resource_check)

        Toffoli_gate(eng, t[18], u[7], m[20], resource_check)
        CNOT | (m[0], m[20])
        Toffoli_gate(eng, t[2], t[15], m[5], resource_check)
        Toffoli_gate(eng, t[21], t[8], m[21], resource_check)

        Toffoli_gate(eng, t[19], t[16], m[22], resource_check)
        CNOT | (m[5], m[22])
        CNOT | (m[5], m[21])
        Toffoli_gate(eng, t[0], t[14], m[10], resource_check)
        Toffoli_gate(eng, t[3], t[26], m[12], resource_check)

        CNOT | (m[10], m[12])
        Toffoli_gate(eng, t[1], t[9], m[13], resource_check)  # Here

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

        # ** ** ** ** ** ** *Layer

        # 41

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

        # # # # # # # # # # # # # # # # # # # # # # #

        Toffoli_gate(eng, m[21], m[19], w_two[33], resource_check)

        CNOT2(eng, m[22], w_two[33], m[27])

        CNOT2(eng, m[20], w_two[33], m[25])

        Toffoli_gate(eng, m[44], m[22], w_two[32], resource_check)
        CNOT2(eng, m[26], w_two[33], m[29])

        Toffoli_gate(eng, m[20], m[47], w_two[30], resource_check)
        CNOT2(eng, m[23], w_two[33], m[31])

        # Toffoli_gate(eng, m[27], m[26], w_two[32])
        # Toffoli_gate(eng, m[25], m[23], m[29])
        # Toffoli_gate(eng, l[2], w_two[32], m[31])
        # Toffoli_gate(eng, l[3], w_two[30], m[34])

        Toffoli_gate(eng, m[23], t[5], w_two[29], resource_check)  # 2
        CNOT2(eng, m[22], m[31], n[1])
        CNOT2(eng, m[25], w_two[30], n[2])

        Toffoli_gate(eng, l[0], t[7], w_two[27], resource_check)  # 2

        Toffoli_gate(eng, l[1], u[7], w_two[23], resource_check)  # 2
        Toffoli_gate(eng, m[48], m[32], w_two[22], resource_check)  # 2

        CNOT2(eng, m[20], m[29], n[7])
        CNOT2(eng, m[27], w_two[32], n[8])
        Toffoli_gate(eng, m[26], t[15], w_two[19], resource_check)  # 2

        Toffoli_gate(eng, l[11], t[8], w_two[18], resource_check)  # 2

        Toffoli_gate(eng, m[45], t[16], w_two[16], resource_check)  # 2
        Toffoli_gate(eng, l[12], m[40], w_two[15], resource_check)  # 2

        # ** ** ** ** ** ** ** ** ** ** ** ** ** **

        Toffoli_gate(eng, l[13], t[14], w_two[13], resource_check)  # 2
        Toffoli_gate(eng, l[2], m[38], w_two[12], resource_check)  # 2
        Toffoli_gate(eng, n[14], m[39], w_two[10], resource_check)  # 2

        CNOT2(eng, m[29], m[31], n[17])
        CNOT2(eng, n[14], n[17], n[18])
        CNOT2(eng, m[27], w_two[32], n[19])
        CNOT2(eng, m[25], w_two[30], n[20])
        Toffoli_gate(eng, l[14], t[26], w_two[6], resource_check)  # 2
        Toffoli_gate(eng, l[3], m[43], w_two[5], resource_check)  # 2

        Toffoli_gate(eng, l[15], t[9], w_two[2], resource_check)  # 2
        Toffoli_gate(eng, l[4], m[37], w_two[1], resource_check)  # 2

        Toffoli_gate(eng, l[5], t[12], n[25], resource_check)  # 2

        Toffoli_gate(eng, l[6], t[22], n[26], resource_check)  # 2

        Toffoli_gate(eng, l[7], t[18], n[28], resource_check)  # 2
        Toffoli_gate(eng, m[49], m[41], n[29], resource_check)  # 2

        Toffoli_gate(eng, l[16], t[2], n[30], resource_check)  # 2

        Toffoli_gate(eng, l[17], t[21], n[31], resource_check)  # 2

        Toffoli_gate(eng, m[46], t[19], n[33], resource_check)  # 2
        Toffoli_gate(eng, l[18], m[42], n[34], resource_check)  # 2

        Toffoli_gate(eng, l[19], t[0], n[35], resource_check)  # 2
        Toffoli_gate(eng, l[8], m[33], n[36], resource_check)  # 2
        Toffoli_gate(eng, l[22], m[34], w[25], resource_check)  # 2

        Toffoli_gate(eng, l[20], t[3], n[37], resource_check)  # 2
        Toffoli_gate(eng, l[9], m[36], n[38], resource_check)  # 2

        Toffoli_gate(eng, l[21], t[1], n[39], resource_check)  # 2
        Toffoli_gate(eng, l[10], m[35], n[40], resource_check)  # 2

        # Clean

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

        # ** ** ** ** ** ** ** *Layer

        CNOT | (m[25], l[0])
        CNOT | (m[25], l[1])
        CNOT | (m[25], l[2])

        CNOT | (m[27], l[3])
        CNOT | (m[27], l[4])
        CNOT | (m[27], l[5])

        CNOT | (w_two[32], l[6])
        CNOT | (w_two[32], l[7])
        CNOT | (w_two[32], l[8])

        CNOT | (m[29], l[9])

        CNOT | (w_two[30], l[10])
        CNOT | (w_two[30], l[11])
        CNOT | (w_two[30], l[12])

        CNOT | (m[31], l[13])
        CNOT | (n[1], l[14])
        CNOT | (n[2], l[15])
        CNOT | (n[7], l[16])
        CNOT | (n[8], l[17])

        CNOT | (n[17], l[18])
        CNOT | (n[18], l[19])
        CNOT | (n[19], l[20])
        CNOT | (n[20], l[21])

        Toffoli_gate(eng, n[2], w_two[29], m[32], resource_check)  # 3
        Toffoli_gate(eng, n[1], t[5], n_two[40], resource_check)  # 3
        CNOT | (n_two[40], m[32])

        Toffoli_gate(eng, m[31], t[7], m[33], resource_check)  # 3
        Toffoli_gate(eng, w_two[27], w_two[30], n_two[39], resource_check)  # 3
        CNOT | (n_two[39], m[33])

        Toffoli_gate(eng, w_two[23], m[25], m[34], resource_check)  # 3
        # CNOT2(eng, w[3], w_two[22], m[34])
        CNOT | (w_two[22], m[34])

        Toffoli_gate(eng, n[7], t[15], m[35], resource_check)  # 3
        Toffoli_gate(eng, n[8], w_two[19], n_two[38], resource_check)  # 3
        # CNOT2(eng, w[4], n_two[38], m[35])
        CNOT | (n_two[38], m[35])

        Toffoli_gate(eng, m[29], t[8], m[36], resource_check)  # 3
        Toffoli_gate(eng, w_two[32], w_two[18], n_two[37], resource_check)  # 3

        CNOT | (n_two[37], m[36])

        Toffoli_gate(eng, m[27], w_two[15], m[37], resource_check)  # 3
        # CNOT2(eng, w[7], w_two[16], m[37])
        CNOT | (w_two[16], m[37])

        Toffoli_gate(eng, w_two[13], l[3], m[38], resource_check)  # 3
        Toffoli_gate(eng, w_two[12], l[0], n_two[36], resource_check)  # 3
        # CNOT2(eng, w_two[10], w[9], m[38])
        CNOT | (w_two[10], m[38])
        CNOT | (n_two[36], m[38])

        Toffoli_gate(eng, n[18], t[26], m[39], resource_check)  # 3
        Toffoli_gate(eng, n[19], w_two[6], n_two[35], resource_check)  # 3
        Toffoli_gate(eng, n[20], w_two[5], n_two[34], resource_check)  # 3
        # CNOT2(eng, w[11], n_two[35], m[39])
        CNOT | (n_two[35], m[39])
        CNOT | (n_two[34], m[39])

        Toffoli_gate(eng, l[6], w_two[2], m[40], resource_check)  # 3
        Toffoli_gate(eng, n[17], t[9], n_two[33], resource_check)  # 3
        Toffoli_gate(eng, l[10], w_two[1], n_two[31], resource_check)  # 3
        # CNOT2(eng, w[14], n_two[33], m[40])
        CNOT | (n_two[33], m[40])
        CNOT | (n_two[31], m[40])

        Toffoli_gate(eng, l[15], n[25], m[41], resource_check)  # 3
        Toffoli_gate(eng, l[14], t[12], n_two[30], resource_check)  # 3
        # CNOT2(eng, w[17], n_two[30], m[41])
        CNOT | (n_two[30], m[41])

        Toffoli_gate(eng, l[13], t[22], m[42], resource_check)  # 3
        Toffoli_gate(eng, n[26], l[11], n_two[29], resource_check)  # 3
        CNOT | (n_two[29], m[42])

        Toffoli_gate(eng, n[28], l[1], m[43], resource_check)  # 3
        # CNOT2(eng, w[20], n[29], m[43])
        CNOT | (n[29], m[43])

        Toffoli_gate(eng, l[16], t[2], m[44], resource_check)  # 3
        Toffoli_gate(eng, l[17], n[30], n_two[28], resource_check)  # 3
        # CNOT2(eng, w[21], n_two[28], m[44])
        CNOT | (n_two[28], m[44])

        Toffoli_gate(eng, l[9], t[21], m[45], resource_check)  # 3
        Toffoli_gate(eng, l[7], n[31], n_two[26], resource_check)  # 3
        # CNOT2(eng, n_two[26], n[32], m[45])
        CNOT | (n_two[26], m[45])

        Toffoli_gate(eng, l[4], n[34], m[46], resource_check)  # 3
        # CNOT2(eng, w[24], n[33], m[46])
        CNOT | (n[33], m[46])

        Toffoli_gate(eng, n[35], l[5], m[47], resource_check)  # 3
        Toffoli_gate(eng, n[36], l[2], n_two[25], resource_check)  # 3

        # CNOT2(eng, w[25], w[26], m[47])
        CNOT | (w[25], m[47])
        CNOT | (n_two[25], m[47])

        Toffoli_gate(eng, l[19], t[3], m[48], resource_check)  # 3
        Toffoli_gate(eng, l[20], n[37], n_two[24], resource_check)  # 3
        Toffoli_gate(eng, l[21], n[38], n_two[23], resource_check)  # 3
        # CNOT2(eng, w[28], n_two[24], m[48])
        CNOT | (n_two[24], m[48])
        CNOT | (n_two[23], m[48])

        Toffoli_gate(eng, l[8], n[39], m[49], resource_check)  # 3
        Toffoli_gate(eng, l[18], t[1], n_two[22], resource_check)  # 3
        Toffoli_gate(eng, l[12], n[40], n_two[21], resource_check)  # 3
        # CNOT2(eng, w[31], n_two[22], m[49])
        CNOT | (n_two[22], m[49])
        CNOT | (n_two[21], m[49])

        CNOT | (m[25], l[0])
        CNOT | (m[25], l[1])
        CNOT | (m[25], l[2])

        CNOT | (m[27], l[3])
        CNOT | (m[27], l[4])
        CNOT | (m[27], l[5])

        CNOT | (w_two[32], l[6])
        CNOT | (w_two[32], l[7])
        CNOT | (w_two[32], l[8])

        CNOT | (m[29], l[9])

        CNOT | (w_two[30], l[10])
        CNOT | (w_two[30], l[11])
        CNOT | (w_two[30], l[12])

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
