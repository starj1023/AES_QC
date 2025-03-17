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
    ancilla = eng.allocate_qureg(720)  # 36 * 20

    k_i = 0
    for i in range(14):

        if(i%2 == 0):
            AddRoundkey(eng, x0, x1, x2, x3, k)
        else:
            AddRoundkey_2(eng, x0, x1, x2, x3, k)

        print('Round', i)

        if (i == 1):
            Clean_ancilla(eng, t0, t1, t2, t3, k, y, t, z, w, l, 1, k_i, ancilla)

        if(i!= 0 and i!= 1 and i!= 13 and i % 2 == 0):
            Clean_ancilla_two(eng, t0, t1, t2, t3, k[0:32], y_two, t_two, z_two, z, w_two, w, l_two, 0, k_i, ancilla)

        if (i != 0 and i != 1 and i!= 13 and i % 2 == 1):
            Clean_ancilla(eng, t0, t1, t2, t3, k[128:160], y, t, z, w, l, 0, k_i, ancilla)

        if(i == 13):
            Clean_ancilla_special(eng, t0, t1, t2, t3, k[128:160], y, t, z, w, l, 0, k_i, ancilla)

        if(i!=0):
            if(i%2 == 0):
                Keyshedule(eng, k, i, y, t, z, w, l, i, k_i, ancilla) #i=2, k_i=1, _one
                CNOT32(eng, k[96:128], k[64:96])
                CNOT32(eng, k[64:96], k[32:64])
                CNOT32(eng, k[32:64], k[0:32])
            else:
                Keyshedule_two(eng, k, i, y_two, t_two, z_two, z, w_two, w, l_two, i, k_i, ancilla) #i=1, k_i=0, _two, i=3, k_i=2, _two
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
            SBox_bp12_all(eng, x0, x1, x2, x3, y, t, z, w, l, s, i, ancilla)
        else:
            SBox_bp12_all_two(eng, x0, x1, x2, x3, y_two, t_two, z_two, z, w_two, w, l_two, s, i, ancilla)

        x0, x1, x2, x3 = Shiftrow(eng, x0, x1, x2, x3)

        if(i!=13):
            x0 = Mixcolumns(eng, x0)
            x1 = Mixcolumns(eng, x1)
            x2 = Mixcolumns(eng, x2)
            x3 = Mixcolumns(eng, x3)

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

def Clean_ancilla(eng, x0, x1, x2, x3, temp_k, y, t, z, w, l, flag, k_i, ancilla):

    for i in range(4):
        Uncompute_sbox(eng, x0[8 * i:8 * (i + 1)], y[27 * i:27 * (i + 1)], t[50 * i:50 * (i + 1)],
                       z[41 * i:41 * (i + 1)], w[34 * i:34 * (i + 1)], l[30 * i:30 * (i + 1)], ancilla)

        Uncompute_sbox(eng, x1[8 * i:8 * (i + 1)], y[27 * (i + 4):27 * (i + 5)],
                       t[50 * (i + 4):50 * (i + 5)], z[41 * (i + 4):41 * (i + 5)],
                       w[34 * (i + 4):34 * (i + 5)], l[30 * (i + 4):30 * (i + 5)], ancilla)
        Uncompute_sbox(eng, x2[8 * i:8 * (i + 1)], y[27 * (i + 8):27 * (i + 9)],
                       t[50 * (i + 8):50 * (i + 9)], z[41 * (i + 8):41 * (i + 9)], w[34 * (i + 8):34 * (i + 9)],
                       l[30 * (i + 8):30 * (i + 9)],
                       ancilla)

        Uncompute_sbox(eng, x3[8 * i:8 * (i + 1)], y[27 * (i + 12):27 * (i + 13)],
                       t[50 * (i + 12):50 * (i + 13)], z[41 * (i + 12):41 * (i + 13)],
                       w[34 * (i + 12):34 * (i + 13)], l[30 * (i + 12):30 * (i + 13)], ancilla)

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
                           l[480 + 30 * i:480 + 30 * (i + 1)], ancilla)

def Clean_ancilla_special(eng, x0, x1, x2, x3, temp_k, y, t, z, w, l, flag, k_i, ancilla):

    for i in range(4):
        Uncompute_sbox_special(eng, x0[8 * i:8 * (i + 1)], y[27 * i:27 * (i + 1)], t[50 * i:50 * (i + 1)],
                       z[41 * i:41 * (i + 1)], w[34 * i:34 * (i + 1)], l[30 * i:30 * (i + 1)], ancilla)

        Uncompute_sbox_special(eng, x1[8 * i:8 * (i + 1)], y[27 * (i + 4):27 * (i + 5)],
                       t[50 * (i + 4):50 * (i + 5)], z[41 * (i + 4):41 * (i + 5)],
                       w[34 * (i + 4):34 * (i + 5)], l[30 * (i + 4):30 * (i + 5)], ancilla)
        Uncompute_sbox_special(eng, x2[8 * i:8 * (i + 1)], y[27 * (i + 8):27 * (i + 9)],
                       t[50 * (i + 8):50 * (i + 9)], z[41 * (i + 8):41 * (i + 9)], w[34 * (i + 8):34 * (i + 9)],
                       l[30 * (i + 8):30 * (i + 9)],
                       ancilla)

        Uncompute_sbox_special(eng, x3[8 * i:8 * (i + 1)], y[27 * (i + 12):27 * (i + 13)],
                       t[50 * (i + 12):50 * (i + 13)], z[41 * (i + 12):41 * (i + 13)],
                       w[34 * (i + 12):34 * (i + 13)], l[30 * (i + 12):30 * (i + 13)], ancilla)

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
                           l[480 + 30 * i:480 + 30 * (i + 1)], ancilla)

def Clean_ancilla_two(eng, x0, x1, x2, x3, temp_k, y, t, z, z_two, w, w_two, l, flag, k_i, ancilla):
    for i in range(4):
        Uncompute_sbox_two(eng, x0[8 * i:8 * (i + 1)], y[27 * i:27 * (i + 1)], t[50 * i:50 * (i + 1)],
                           z[41 * i:41 * (i + 1)], z_two[41 * i:41 * (i + 1)], w[34 * i:34 * (i + 1)],
                           w_two[34 * i:34 * (i + 1)], l[30 * i:30 * (i + 1)], ancilla)

        Uncompute_sbox_two(eng, x1[8 * i:8 * (i + 1)], y[27 * (i + 4):27 * (i + 5)],
                           t[50 * (i + 4):50 * (i + 5)], z[41 * (i + 4):41 * (i + 5)], z_two[41 * (i + 4):41 * (i + 5)],
                           w[34 * (i + 4):34 * (i + 5)], w_two[34 * (i + 4):34 * (i + 5)], l[30 * (i + 4):30 * (i + 5)],
                           ancilla)
        Uncompute_sbox_two(eng, x2[8 * i:8 * (i + 1)], y[27 * (i + 8):27 * (i + 9)],
                           t[50 * (i + 8):50 * (i + 9)], z[41 * (i + 8):41 * (i + 9)], z_two[41 * (i + 8):41 * (i + 9)],
                           w[34 * (i + 8):34 * (i + 9)], w_two[34 * (i + 8):34 * (i + 9)],
                           l[30 * (i + 8):30 * (i + 9)],
                           ancilla)

        Uncompute_sbox_two(eng, x3[8 * i:8 * (i + 1)], y[27 * (i + 12):27 * (i + 13)],
                           t[50 * (i + 12):50 * (i + 13)], z[41 * (i + 12):41 * (i + 13)],
                           z_two[41 * (i + 12):41 * (i + 13)],
                           w[34 * (i + 12):34 * (i + 13)], w_two[34 * (i + 12):34 * (i + 13)],
                           l[30 * (i + 12):30 * (i + 13)], ancilla)

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
                           l[480 + 30 * i:480 + 30 * (i + 1)], ancilla)

def Keyshedule(eng, k, i, y, t, z, w, l, round, k_i, ancilla):

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
                                               1, round, ancilla[576 + 36 * j: 576 + 36 * (j + 1)])
    else:
        for j in range(4): #22 68 18
             k[96 + 8 * j: 96 + 8 * (j + 1)] = Sbox(eng, new_k0[8 * j:8 * (j + 1)], y[432 + 27 * j:432 + 27 * (j + 1)],
                                               t[800 + 50 * j:800 + 50 * (j + 1)],
                                               z[656 + 41 * j:656 + 41 * (j + 1)], w[544 + 34 * j:544 + 34 * (j + 1)],
                                               l[480 + 30 * j:480 + 30 * (j + 1)], k[96 + 8 * j: 96 + 8 * (j + 1)],
                                               1, round, ancilla[576 + 36 * j: 576 + 36 * (j + 1)])
    if (k_i % 2 == 0):
        for j in range(8):
            if ((Rcon[int(k_i/2)] >> j) & 1):
                X | k[248+j]

def Keyshedule_two(eng, k, i, y, t, z, z_two, w, w_two, l, round, k_i, ancilla):

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
                                               1, round, ancilla[576 + 36 * j: 576 + 36 * (j + 1)])
    else:
        for j in range(4): #22 68 18
             k[96 + 8 * j: 96 + 8 * (j + 1)] = Sbox_two(eng, new_k0[8 * j:8 * (j + 1)], y[432 + 27 * j:432 + 27 * (j + 1)],
                                               t[800 + 50 * j:800 + 50 * (j + 1)],
                                               z[656 + 41 * j:656 + 41 * (j + 1)], z_two[656 + 41 * j:656 + 41 * (j + 1)], w[544 + 34 * j:544 + 34 * (j + 1)], w_two[544 + 34 * j:544 + 34 * (j + 1)],
                                               l[480 + 30 * j:480 + 30 * (j + 1)], k[96 + 8 * j: 96 + 8 * (j + 1)],
                                               1, round, ancilla[576 + 36 * j: 576 + 36 * (j + 1)])
    if (k_i % 2 == 0):
        for j in range(8):
            if ((Rcon[int(k_i/2)] >> j) & 1):
                X | k[248+j]

def SBox_bp12_all(eng, x0, x1, x2, x3, y, t, z, w, l, s, round, ancilla):
    for i in range(4):
        x0[8 * i:8 * (i + 1)] = Sbox(eng, x0[8 * i:8 * (i + 1)], y[27 * i:27 * (i + 1)], t[50 * i:50 * (i + 1)],
                                     z[41 * i:41 * (i + 1)], w[34 * i:34 * (i + 1)], l[30 * i:30 * (i + 1)],
                                     s[8 * i:8 * (i + 1)], 0, round, ancilla[36 * i:36 * (i + 1)])

        x1[8 * i:8 * (i + 1)] = Sbox(eng, x1[8 * i:8 * (i + 1)], y[27 * (i + 4):27 * (i + 5)],
                                     t[50 * (i + 4):50 * (i + 5)], z[41 * (i + 4):41 * (i + 5)],
                                     w[34 * (i + 4):34 * (i + 5)], l[30 * (i + 4):30 * (i + 5)],
                                     s[8 * (i + 4):8 * (i + 5)], 0, round, ancilla[36 * (i + 4):36 * (i + 5)])
        x2[8 * i:8 * (i + 1)] = Sbox(eng, x2[8 * i:8 * (i + 1)], y[27 * (i + 8):27 * (i + 9)],
                                     t[50 * (i + 8):50 * (i + 9)], z[41 * (i + 8):41 * (i + 9)],
                                     w[34 * (i + 8):34 * (i + 9)], l[30 * (i + 8):30 * (i + 9)],
                                     s[8 * (i + 8):8 * (i + 9)], 0, round, ancilla[36 * (i + 8):36 * (i + 9)])

        x3[8 * i:8 * (i + 1)] = Sbox(eng, x3[8 * i:8 * (i + 1)], y[27 * (i + 12):27 * (i + 13)],
                                     t[50 * (i + 12):50 * (i + 13)], z[41 * (i + 12):41 * (i + 13)],
                                     w[34 * (i + 12):34 * (i + 13)], l[30 * (i + 12):30 * (i + 13)],
                                     s[8 * (i + 12):8 * (i + 13)], 0, round, ancilla[36 * (i + 12):36 * (i + 13)])

def SBox_bp12_all_two(eng, x0, x1, x2, x3, y, t, z, z_two, w, w_two, l, s, round, ancilla):
    for i in range(4):
        x0[8 * i:8 * (i + 1)] = Sbox_two(eng, x0[8 * i:8 * (i + 1)], y[27 * i:27 * (i + 1)], t[50 * i:50 * (i + 1)],
                                     z[41 * i:41 * (i + 1)], z_two[41 * i:41 * (i + 1)], w[34 * i:34 * (i + 1)], w_two[34 * i:34 * (i + 1)], l[30 * i:30 * (i + 1)],
                                     s[8 * i:8 * (i + 1)], 0, round, ancilla[36 * i:36 * (i + 1)])

        x1[8 * i:8 * (i + 1)] = Sbox_two(eng, x1[8 * i:8 * (i + 1)], y[27 * (i + 4):27 * (i + 5)],
                                     t[50 * (i + 4):50 * (i + 5)], z[41 * (i + 4):41 * (i + 5)], z_two[41 * (i + 4):41 * (i + 5)],
                                     w[34 * (i + 4):34 * (i + 5)], w_two[34 * (i + 4):34 * (i + 5)], l[30 * (i + 4):30 * (i + 5)],
                                     s[8 * (i + 4):8 * (i + 5)], 0, round, ancilla[36 * (i + 4):36 * (i + 5)])
        x2[8 * i:8 * (i + 1)] = Sbox_two(eng, x2[8 * i:8 * (i + 1)], y[27 * (i + 8):27 * (i + 9)],
                                     t[50 * (i + 8):50 * (i + 9)], z[41 * (i + 8):41 * (i + 9)], z_two[41 * (i + 8):41 * (i + 9)],
                                     w[34 * (i + 8):34 * (i + 9)], w_two[34 * (i + 8):34 * (i + 9)], l[30 * (i + 8):30 * (i + 9)],
                                     s[8 * (i + 8):8 * (i + 9)], 0, round, ancilla[36 * (i + 8):36 * (i + 9)])

        x3[8 * i:8 * (i + 1)] = Sbox_two(eng, x3[8 * i:8 * (i + 1)], y[27 * (i + 12):27 * (i + 13)],
                                     t[50 * (i + 12):50 * (i + 13)], z[41 * (i + 12):41 * (i + 13)], z_two[41 * (i + 12):41 * (i + 13)],
                                     w[34 * (i + 12):34 * (i + 13)], w_two[34 * (i + 12):34 * (i + 13)],  l[30 * (i + 12):30 * (i + 13)],
                                     s[8 * (i + 12):8 * (i + 13)], 0, round, ancilla[36 * (i + 12):36 * (i + 13)])

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

def Mixcolumns(eng, x_in):
    # Changing the index of qubit

    x = []
    for i in range(8):
        x.append(x_in[24 + i])
    for i in range(8):
        x.append(x_in[16 + i])
    for i in range(8):
        x.append(x_in[8 + i])
    for i in range(8):
        x.append(x_in[i])

    CNOT | (x[12], x[28])
    CNOT | (x[20], x[4])
    CNOT | (x[19], x[3])
    CNOT | (x[27], x[11])
    CNOT | (x[21], x[5])
    CNOT | (x[13], x[29])
    CNOT | (x[6], x[22])
    CNOT | (x[30], x[14])
    CNOT | (x[23], x[31])
    CNOT | (x[15], x[7])
    CNOT | (x[18], x[2])
    CNOT | (x[26], x[10])
    CNOT | (x[24], x[1])
    CNOT | (x[0], x[8])
    CNOT | (x[9], x[25])
    CNOT | (x[16], x[17])
    CNOT | (x[31], x[7])
    CNOT | (x[19], x[27])
    CNOT | (x[12], x[20])
    CNOT | (x[13], x[21])
    CNOT | (x[4], x[28])
    CNOT | (x[30], x[6])
    CNOT | (x[16], x[0])
    CNOT | (x[24], x[8])
    CNOT | (x[26], x[18])
    CNOT | (x[15], x[23])
    CNOT | (x[2], x[10])
    CNOT | (x[29], x[5])
    CNOT | (x[3], x[11])
    CNOT | (x[25], x[17])
    CNOT | (x[1], x[9])
    CNOT | (x[22], x[14])
    CNOT | (x[17], x[26])
    CNOT | (x[18], x[19])
    CNOT | (x[20], x[13])
    CNOT | (x[31], x[12])
    CNOT | (x[11], x[3])
    CNOT | (x[8], x[9])
    CNOT | (x[21], x[30])
    CNOT | (x[28], x[4])
    CNOT | (x[2], x[27])
    CNOT | (x[7], x[25])
    CNOT | (x[14], x[6])
    CNOT | (x[29], x[15])
    CNOT | (x[24], x[16])
    CNOT | (x[22], x[23])
    CNOT | (x[20], x[27])
    CNOT | (x[22], x[31])
    CNOT | (x[16], x[17])
    CNOT | (x[10], x[18])
    CNOT | (x[4], x[21])
    CNOT | (x[25], x[9])
    CNOT | (x[7], x[0])
    CNOT | (x[29], x[6])
    CNOT | (x[2], x[26])
    CNOT | (x[11], x[19])
    CNOT | (x[3], x[23])
    CNOT | (x[8], x[24])
    CNOT | (x[18], x[26])
    CNOT | (x[27], x[12])
    CNOT | (x[17], x[9])
    CNOT | (x[7], x[3])
    CNOT | (x[31], x[15])
    CNOT | (x[22], x[8])
    CNOT | (x[23], x[20])
    CNOT | (x[24], x[16])
    CNOT | (x[3], x[23])
    CNOT | (x[8], x[24])
    CNOT | (x[17], x[1])
    CNOT | (x[31], x[19])
    CNOT | (x[22], x[30])
    CNOT | (x[7], x[4])
    CNOT | (x[2], x[12])
    CNOT | (x[25], x[18])
    CNOT | (x[5], x[21])
    CNOT | (x[23], x[24])
    CNOT | (x[7], x[18])
    CNOT | (x[1], x[2])
    CNOT | (x[16], x[9])
    CNOT | (x[22], x[19])
    CNOT | (x[31], x[20])
    CNOT | (x[10], x[27])
    CNOT | (x[5], x[13])
    CNOT | (x[28], x[29])
    CNOT | (x[25], x[26])
    CNOT | (x[5], x[22])
    CNOT | (x[7], x[17])
    CNOT | (x[1], x[18])
    CNOT | (x[9], x[26])
    CNOT | (x[14], x[23])
    CNOT | (x[31], x[8])
    CNOT | (x[29], x[13])
    CNOT | (x[28], x[12])
    CNOT | (x[11], x[4])
    CNOT | (x[6], x[15])
    CNOT | (x[20], x[27])
    CNOT | (x[16], x[25])
    CNOT | (x[0], x[24])
    CNOT | (x[10], x[3])
    CNOT | (x[31], x[7])
    CNOT | (x[29], x[5])
    CNOT | (x[2], x[10])
    CNOT | (x[22], x[14])
    CNOT | (x[15], x[23])
    CNOT | (x[4], x[28])
    CNOT | (x[3], x[11])
    CNOT | (x[25], x[1])
    CNOT | (x[30], x[6])
    CNOT | (x[0], x[16])
    CNOT | (x[13], x[21])
    CNOT | (x[12], x[20])
    CNOT | (x[24], x[9])
    CNOT | (x[19], x[27])
    CNOT | (x[8], x[17])
    CNOT | (x[26], x[18])
    CNOT | (x[21], x[5])
    CNOT | (x[13], x[29])
    CNOT | (x[30], x[14])
    CNOT | (x[6], x[22])
    CNOT | (x[15], x[7])
    CNOT | (x[23], x[31])
    CNOT | (x[27], x[3])
    CNOT | (x[20], x[4])
    CNOT | (x[19], x[11])
    CNOT | (x[12], x[28])
    CNOT | (x[9], x[25])
    CNOT | (x[26], x[2])
    CNOT | (x[18], x[10])
    CNOT | (x[24], x[16])
    CNOT | (x[8], x[0])
    CNOT | (x[17], x[1])

    x_out = [None] * 32

    x_out[0] = x[0]
    x_out[17] = x[1]
    x_out[18] = x[2]
    x_out[27] = x[3]
    x_out[28] = x[4]
    x_out[21] = x[5]
    x_out[22] = x[6]
    x_out[15] = x[7]
    x_out[16] = x[8]
    x_out[25] = x[9]
    x_out[26] = x[10]
    x_out[3] = x[11]

    x_out[20] = x[12]
    x_out[29] = x[13]
    x_out[30] = x[14]
    x_out[7] = x[15]
    x_out[24] = x[16]
    x_out[1] = x[17]
    x_out[10] = x[18]
    x_out[19] = x[19]
    x_out[12] = x[20]
    x_out[5] = x[21]
    x_out[6] = x[22]
    x_out[31] = x[23]
    x_out[8] = x[24]
    x_out[9] = x[25]
    x_out[2] = x[26]
    x_out[11] = x[27]
    x_out[4] = x[28]
    x_out[13] = x[29]
    x_out[14] = x[30]
    x_out[23] = x[31]

    out_x = []
    for i in range(8):
        out_x.append(x_out[24 + i])
    for i in range(8):
        out_x.append(x_out[16 + i])
    for i in range(8):
        out_x.append(x_out[8 + i])
    for i in range(8):
        out_x.append(x_out[0 + i])

    return out_x

def CNOT2(eng, a, b, c):
    CNOT | (a, c)
    CNOT | (b, c)

def Uncompute_sbox(eng, u_in, t, m, n, w, l, ancilla):

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

        AND_gate_dag(eng, t[12], t[5], m[0], ancilla[0])
        AND_gate_dag(eng, t[22], t[7], m[19], ancilla[0])

        AND_gate_dag(eng, t[18], u[7], m[20], ancilla[0])
        CNOT | (m[0], m[20])
        AND_gate_dag(eng, t[2], t[15], m[5], ancilla[0])
        AND_gate_dag(eng, t[21], t[8], m[21], ancilla[0])

        AND_gate_dag(eng, t[19], t[16], m[22], ancilla[0])
        CNOT | (m[5], m[22])
        CNOT | (m[5], m[21])
        AND_gate_dag(eng, t[0], t[14], m[10], ancilla[0])
        AND_gate_dag(eng, t[3], t[26], m[12], ancilla[0])

        CNOT | (m[10], m[12])
        AND_gate_dag(eng, t[1], t[9], m[13], ancilla[0])  # Here

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

        AND_gate_dag(eng, m[21], m[19], m[24], ancilla[0])

        CNOT2(eng, m[22], m[24], m[27])

        CNOT2(eng, m[20], m[24], m[25])

        AND_gate_dag(eng, m[44], m[22], m[28], ancilla[0])
        CNOT2(eng, m[26], m[24], m[29])

        AND_gate_dag(eng, m[20], m[47], m[30], ancilla[0])
        CNOT2(eng, m[23], m[24], m[31])

        # AND_gate_dag(eng, m[27], m[26], m[28])
        # AND_gate_dag(eng, m[25], m[23], m[29])
        # AND_gate_dag(eng, l[2], m[28], m[31])
        # AND_gate_dag(eng, l[3], m[30], m[34])

        AND_gate_dag(eng, m[23], t[5], n[0], ancilla[0])  # 2
        CNOT2(eng, m[22], m[31], n[1])
        CNOT2(eng, m[25], m[30], n[2])

        AND_gate_dag(eng, l[0], t[7], n[3], ancilla[0])  # 2

        AND_gate_dag(eng, l[1], u[7], n[5], ancilla[0])  # 2
        AND_gate_dag(eng, m[48], m[32], n[6], ancilla[0])  # 2

        CNOT2(eng, m[20], m[29], n[7])
        CNOT2(eng, m[27], m[28], n[8])
        AND_gate_dag(eng, m[26], t[15], n[9], ancilla[0])  # 2

        AND_gate_dag(eng, l[11], t[8], n[10], ancilla[0])  # 2

        AND_gate_dag(eng, m[45], t[16], n[12], ancilla[0])  # 2
        AND_gate_dag(eng, l[12], m[40], n[13], ancilla[0])  # 2

        # ** ** ** ** ** ** ** ** ** ** ** ** ** **

        AND_gate_dag(eng, l[13], t[14], n[15], ancilla[0])  # 2
        AND_gate_dag(eng, l[2], m[38], n[16], ancilla[0])  # 2
        AND_gate_dag(eng, n[14], m[39], w[8], ancilla[0])  # 2

        CNOT2(eng, m[29], m[31], n[17])
        CNOT2(eng, n[14], n[17], n[18])
        CNOT2(eng, m[27], m[28], n[19])
        CNOT2(eng, m[25], m[30], n[20])
        AND_gate_dag(eng, l[14], t[26], n[21], ancilla[0])  # 2
        AND_gate_dag(eng, l[3], m[43], n[22], ancilla[0])  # 2

        AND_gate_dag(eng, l[15], t[9], n[23], ancilla[0])  # 2
        AND_gate_dag(eng, l[4], m[37], n[24], ancilla[0])  # 2

        AND_gate_dag(eng, l[5], t[12], n[25], ancilla[0])  # 2

        AND_gate_dag(eng, l[6], t[22], n[26], ancilla[0])  # 2

        AND_gate_dag(eng, l[7], t[18], n[28], ancilla[0])  # 2
        AND_gate_dag(eng, m[49], m[41], n[29], ancilla[0])  # 2

        AND_gate_dag(eng, l[16], t[2], n[30], ancilla[0])  # 2

        AND_gate_dag(eng, l[17], t[21], n[31], ancilla[0])  # 2

        AND_gate_dag(eng, m[46], t[19], n[33], ancilla[0])  # 2
        AND_gate_dag(eng, l[18], m[42], n[34], ancilla[0])  # 2

        AND_gate_dag(eng, l[19], t[0], n[35], ancilla[0])  # 2
        AND_gate_dag(eng, l[8], m[33], n[36], ancilla[0])  # 2
        AND_gate_dag(eng, l[22], m[34], w[25], ancilla[0])  # 2

        AND_gate_dag(eng, l[20], t[3], n[37], ancilla[0])  # 2
        AND_gate_dag(eng, l[9], m[36], n[38], ancilla[0])  # 2

        AND_gate_dag(eng, l[21], t[1], n[39], ancilla[0])  # 2
        AND_gate_dag(eng, l[10], m[35], n[40], ancilla[0])  # 2

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

        AND_gate_dag(eng, n[2], n[0], m[32], ancilla[0])  # 3
        AND_gate_dag(eng, n[1], t[5], w[1], ancilla[0])  # 3
        CNOT | (w[1], m[32])

        AND_gate_dag(eng, m[31], t[7], m[33], ancilla[0])  # 3
        AND_gate_dag(eng, n[3], m[30], w[2], ancilla[0])  # 3
        CNOT | (w[2], m[33])

        AND_gate_dag(eng, n[5], m[25], m[34], ancilla[0])  # 3
        # CNOT2(eng, w[3], n[6], m[34])
        CNOT | (n[6], m[34])

        AND_gate_dag(eng, n[7], t[15], m[35], ancilla[0])  # 3
        AND_gate_dag(eng, n[8], n[9], w[5], ancilla[0])  # 3
        # CNOT2(eng, w[4], w[5], m[35])
        CNOT | (w[5], m[35])

        AND_gate_dag(eng, m[29], t[8], m[36], ancilla[0])  # 3
        AND_gate_dag(eng, m[28], n[10], w[6], ancilla[0])  # 3

        CNOT | (w[6], m[36])

        AND_gate_dag(eng, m[27], n[13], m[37], ancilla[0])  # 3
        # CNOT2(eng, w[7], n[12], m[37])
        CNOT | (n[12], m[37])

        AND_gate_dag(eng, n[15], l[3], m[38], ancilla[0])  # 3
        AND_gate_dag(eng, n[16], l[0], w[10], ancilla[0])  # 3
        # CNOT2(eng, w[8], w[9], m[38])
        CNOT | (w[8], m[38])
        CNOT | (w[10], m[38])

        AND_gate_dag(eng, n[18], t[26], m[39], ancilla[0])  # 3
        AND_gate_dag(eng, n[19], n[21], w[12], ancilla[0])  # 3
        AND_gate_dag(eng, n[20], n[22], w[13], ancilla[0])  # 3
        # CNOT2(eng, w[11], w[12], m[39])
        CNOT | (w[12], m[39])
        CNOT | (w[13], m[39])

        AND_gate_dag(eng, l[6], n[23], m[40], ancilla[0])  # 3
        AND_gate_dag(eng, n[17], t[9], w[15], ancilla[0])  # 3
        AND_gate_dag(eng, l[10], n[24], w[16], ancilla[0])  # 3
        # CNOT2(eng, w[14], w[15], m[40])
        CNOT | (w[15], m[40])
        CNOT | (w[16], m[40])

        AND_gate_dag(eng, l[15], n[25], m[41], ancilla[0])  # 3
        AND_gate_dag(eng, l[14], t[12], w[18], ancilla[0])  # 3
        # CNOT2(eng, w[17], w[18], m[41])
        CNOT | (w[18], m[41])

        AND_gate_dag(eng, l[13], t[22], m[42], ancilla[0])  # 3
        AND_gate_dag(eng, n[26], l[11], w[19], ancilla[0])  # 3
        CNOT | (w[19], m[42])

        AND_gate_dag(eng, n[28], l[1], m[43], ancilla[0])  # 3
        # CNOT2(eng, w[20], n[29], m[43])
        CNOT | (n[29], m[43])

        AND_gate_dag(eng, l[16], t[2], m[44], ancilla[0])  # 3
        AND_gate_dag(eng, l[17], n[30], w[22], ancilla[0])  # 3
        # CNOT2(eng, w[21], w[22], m[44])
        CNOT | (w[22], m[44])

        AND_gate_dag(eng, l[9], t[21], m[45], ancilla[0])  # 3
        AND_gate_dag(eng, l[7], n[31], w[23], ancilla[0])  # 3
        # CNOT2(eng, w[23], n[32], m[45])
        CNOT | (w[23], m[45])

        AND_gate_dag(eng, l[4], n[34], m[46], ancilla[0])  # 3
        # CNOT2(eng, w[24], n[33], m[46])
        CNOT | (n[33], m[46])

        AND_gate_dag(eng, n[35], l[5], m[47], ancilla[0])  # 3
        AND_gate_dag(eng, n[36], l[2], w[27], ancilla[0])  # 3

        # CNOT2(eng, w[25], w[26], m[47])
        CNOT | (w[25], m[47])
        CNOT | (w[27], m[47])

        AND_gate_dag(eng, l[19], t[3], m[48], ancilla[0])  # 3
        AND_gate_dag(eng, l[20], n[37], w[29], ancilla[0])  # 3
        AND_gate_dag(eng, l[21], n[38], w[30], ancilla[0])  # 3
        # CNOT2(eng, w[28], w[29], m[48])
        CNOT | (w[29], m[48])
        CNOT | (w[30], m[48])

        AND_gate_dag(eng, l[8], n[39], m[49], ancilla[0])  # 3
        AND_gate_dag(eng, l[18], t[1], w[32], ancilla[0])  # 3
        AND_gate_dag(eng, l[12], n[40], w[33], ancilla[0])  # 3
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

def Uncompute_sbox_special(eng, u_in, t, m, n, w, l, ancilla):

    u = []
    for i in range(8):
        u.append(u_in[7 - i])

    with Dagger(eng):
        # # # # # # # # # # # # # # # # # # # # # # # /

        AND_gate_dag(eng, m[21], m[19], m[24], ancilla[0])

        CNOT2(eng, m[22], m[24], m[27])

        CNOT2(eng, m[20], m[24], m[25])

        AND_gate_dag(eng, m[44], m[22], m[28], ancilla[0])
        CNOT2(eng, m[26], m[24], m[29])

        AND_gate_dag(eng, m[20], m[47], m[30], ancilla[0])
        CNOT2(eng, m[23], m[24], m[31])

        # AND_gate_dag(eng, m[27], m[26], m[28])
        # AND_gate_dag(eng, m[25], m[23], m[29])
        # AND_gate_dag(eng, l[2], m[28], m[31])
        # AND_gate_dag(eng, l[3], m[30], m[34])

        AND_gate_dag(eng, m[23], t[5], n[0], ancilla[0])  # 2
        CNOT2(eng, m[22], m[31], n[1])
        CNOT2(eng, m[25], m[30], n[2])

        AND_gate_dag(eng, l[0], t[7], n[3], ancilla[0])  # 2

        AND_gate_dag(eng, l[1], u[7], n[5], ancilla[0])  # 2
        AND_gate_dag(eng, m[48], m[32], n[6], ancilla[0])  # 2

        CNOT2(eng, m[20], m[29], n[7])
        CNOT2(eng, m[27], m[28], n[8])
        AND_gate_dag(eng, m[26], t[15], n[9], ancilla[0])  # 2

        AND_gate_dag(eng, l[11], t[8], n[10], ancilla[0])  # 2

        AND_gate_dag(eng, m[45], t[16], n[12], ancilla[0])  # 2
        AND_gate_dag(eng, l[12], m[40], n[13], ancilla[0])  # 2

        # ** ** ** ** ** ** ** ** ** ** ** ** ** **

        AND_gate_dag(eng, l[13], t[14], n[15], ancilla[0])  # 2
        AND_gate_dag(eng, l[2], m[38], n[16], ancilla[0])  # 2
        AND_gate_dag(eng, n[14], m[39], w[8], ancilla[0])  # 2

        CNOT2(eng, m[29], m[31], n[17])
        CNOT2(eng, n[14], n[17], n[18])
        CNOT2(eng, m[27], m[28], n[19])
        CNOT2(eng, m[25], m[30], n[20])
        AND_gate_dag(eng, l[14], t[26], n[21], ancilla[0])  # 2
        AND_gate_dag(eng, l[3], m[43], n[22], ancilla[0])  # 2

        AND_gate_dag(eng, l[15], t[9], n[23], ancilla[0])  # 2
        AND_gate_dag(eng, l[4], m[37], n[24], ancilla[0])  # 2

        AND_gate_dag(eng, l[5], t[12], n[25], ancilla[0])  # 2

        AND_gate_dag(eng, l[6], t[22], n[26], ancilla[0])  # 2

        AND_gate_dag(eng, l[7], t[18], n[28], ancilla[0])  # 2
        AND_gate_dag(eng, m[49], m[41], n[29], ancilla[0])  # 2

        AND_gate_dag(eng, l[16], t[2], n[30], ancilla[0])  # 2

        AND_gate_dag(eng, l[17], t[21], n[31], ancilla[0])  # 2

        AND_gate_dag(eng, m[46], t[19], n[33], ancilla[0])  # 2
        AND_gate_dag(eng, l[18], m[42], n[34], ancilla[0])  # 2

        AND_gate_dag(eng, l[19], t[0], n[35], ancilla[0])  # 2
        AND_gate_dag(eng, l[8], m[33], n[36], ancilla[0])  # 2
        AND_gate_dag(eng, l[22], m[34], w[25], ancilla[0])  # 2

        AND_gate_dag(eng, l[20], t[3], n[37], ancilla[0])  # 2
        AND_gate_dag(eng, l[9], m[36], n[38], ancilla[0])  # 2

        AND_gate_dag(eng, l[21], t[1], n[39], ancilla[0])  # 2
        AND_gate_dag(eng, l[10], m[35], n[40], ancilla[0])  # 2

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

        AND_gate_dag(eng, n[2], n[0], m[32], ancilla[0])  # 3
        AND_gate_dag(eng, n[1], t[5], w[1], ancilla[0])  # 3
        CNOT | (w[1], m[32])

        AND_gate_dag(eng, m[31], t[7], m[33], ancilla[0])  # 3
        AND_gate_dag(eng, n[3], m[30], w[2], ancilla[0])  # 3
        CNOT | (w[2], m[33])

        AND_gate_dag(eng, n[5], m[25], m[34], ancilla[0])  # 3
        # CNOT2(eng, w[3], n[6], m[34])
        CNOT | (n[6], m[34])

        AND_gate_dag(eng, n[7], t[15], m[35], ancilla[0])  # 3
        AND_gate_dag(eng, n[8], n[9], w[5], ancilla[0])  # 3
        # CNOT2(eng, w[4], w[5], m[35])
        CNOT | (w[5], m[35])

        AND_gate_dag(eng, m[29], t[8], m[36], ancilla[0])  # 3
        AND_gate_dag(eng, m[28], n[10], w[6], ancilla[0])  # 3

        CNOT | (w[6], m[36])

        AND_gate_dag(eng, m[27], n[13], m[37], ancilla[0])  # 3
        # CNOT2(eng, w[7], n[12], m[37])
        CNOT | (n[12], m[37])

        AND_gate_dag(eng, n[15], l[3], m[38], ancilla[0])  # 3
        AND_gate_dag(eng, n[16], l[0], w[10], ancilla[0])  # 3
        # CNOT2(eng, w[8], w[9], m[38])
        CNOT | (w[8], m[38])
        CNOT | (w[10], m[38])

        AND_gate_dag(eng, n[18], t[26], m[39], ancilla[0])  # 3
        AND_gate_dag(eng, n[19], n[21], w[12], ancilla[0])  # 3
        AND_gate_dag(eng, n[20], n[22], w[13], ancilla[0])  # 3
        # CNOT2(eng, w[11], w[12], m[39])
        CNOT | (w[12], m[39])
        CNOT | (w[13], m[39])

        AND_gate_dag(eng, l[6], n[23], m[40], ancilla[0])  # 3
        AND_gate_dag(eng, n[17], t[9], w[15], ancilla[0])  # 3
        AND_gate_dag(eng, l[10], n[24], w[16], ancilla[0])  # 3
        # CNOT2(eng, w[14], w[15], m[40])
        CNOT | (w[15], m[40])
        CNOT | (w[16], m[40])

        AND_gate_dag(eng, l[15], n[25], m[41], ancilla[0])  # 3
        AND_gate_dag(eng, l[14], t[12], w[18], ancilla[0])  # 3
        # CNOT2(eng, w[17], w[18], m[41])
        CNOT | (w[18], m[41])

        AND_gate_dag(eng, l[13], t[22], m[42], ancilla[0])  # 3
        AND_gate_dag(eng, n[26], l[11], w[19], ancilla[0])  # 3
        CNOT | (w[19], m[42])

        AND_gate_dag(eng, n[28], l[1], m[43], ancilla[0])  # 3
        # CNOT2(eng, w[20], n[29], m[43])
        CNOT | (n[29], m[43])

        AND_gate_dag(eng, l[16], t[2], m[44], ancilla[0])  # 3
        AND_gate_dag(eng, l[17], n[30], w[22], ancilla[0])  # 3
        # CNOT2(eng, w[21], w[22], m[44])
        CNOT | (w[22], m[44])

        AND_gate_dag(eng, l[9], t[21], m[45], ancilla[0])  # 3
        AND_gate_dag(eng, l[7], n[31], w[23], ancilla[0])  # 3
        # CNOT2(eng, w[23], n[32], m[45])
        CNOT | (w[23], m[45])

        AND_gate_dag(eng, l[4], n[34], m[46], ancilla[0])  # 3
        # CNOT2(eng, w[24], n[33], m[46])
        CNOT | (n[33], m[46])

        AND_gate_dag(eng, n[35], l[5], m[47], ancilla[0])  # 3
        AND_gate_dag(eng, n[36], l[2], w[27], ancilla[0])  # 3

        # CNOT2(eng, w[25], w[26], m[47])
        CNOT | (w[25], m[47])
        CNOT | (w[27], m[47])

        AND_gate_dag(eng, l[19], t[3], m[48], ancilla[0])  # 3
        AND_gate_dag(eng, l[20], n[37], w[29], ancilla[0])  # 3
        AND_gate_dag(eng, l[21], n[38], w[30], ancilla[0])  # 3
        # CNOT2(eng, w[28], w[29], m[48])
        CNOT | (w[29], m[48])
        CNOT | (w[30], m[48])

        AND_gate_dag(eng, l[8], n[39], m[49], ancilla[0])  # 3
        AND_gate_dag(eng, l[18], t[1], w[32], ancilla[0])  # 3
        AND_gate_dag(eng, l[12], n[40], w[33], ancilla[0])  # 3
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

def Uncompute_sbox_two(eng, u_in, t, m, n, n_two, w, w_two, l, ancilla):

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

        AND_gate_dag(eng, t[12], t[5], m[0], ancilla[0])
        AND_gate_dag(eng, t[22], t[7], m[19], ancilla[0])

        AND_gate_dag(eng, t[18], u[7], m[20], ancilla[0])
        CNOT | (m[0], m[20])
        AND_gate_dag(eng, t[2], t[15], m[5], ancilla[0])
        AND_gate_dag(eng, t[21], t[8], m[21], ancilla[0])

        AND_gate_dag(eng, t[19], t[16], m[22], ancilla[0])
        CNOT | (m[5], m[22])
        CNOT | (m[5], m[21])
        AND_gate_dag(eng, t[0], t[14], m[10], ancilla[0])
        AND_gate_dag(eng, t[3], t[26], m[12], ancilla[0])

        CNOT | (m[10], m[12])
        AND_gate_dag(eng, t[1], t[9], m[13], ancilla[0])  # Here

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

        # ## can be used after 1st Toffoli operation -->  w[33 32 30 29 27 23 22 19 18 16 15 13 12 10 6 5 2 1]

        AND_gate_dag(eng, m[21], m[19], w_two[33], ancilla[0])

        CNOT2(eng, m[22], w_two[33], m[27])

        CNOT2(eng, m[20], w_two[33], m[25])

        AND_gate_dag(eng, m[44], m[22], w_two[32], ancilla[0])
        CNOT2(eng, m[26], w_two[33], m[29])

        AND_gate_dag(eng, m[20], m[47], w_two[30], ancilla[0])
        CNOT2(eng, m[23], w_two[33], m[31])

        # AND_gate_dag(eng, m[27], m[26], w_two[32])
        # AND_gate_dag(eng, m[25], m[23], m[29])
        # AND_gate_dag(eng, l[2], w_two[32], m[31])
        # AND_gate_dag(eng, l[3], w_two[30], m[34])

        AND_gate_dag(eng, m[23], t[5], w_two[29], ancilla[0])  # 2
        CNOT2(eng, m[22], m[31], n[1])
        CNOT2(eng, m[25], w_two[30], n[2])

        AND_gate_dag(eng, l[0], t[7], w_two[27], ancilla[0])  # 2

        AND_gate_dag(eng, l[1], u[7], w_two[23], ancilla[0])  # 2
        AND_gate_dag(eng, m[48], m[32], w_two[22], ancilla[0])  # 2

        CNOT2(eng, m[20], m[29], n[7])
        CNOT2(eng, m[27], w_two[32], n[8])
        AND_gate_dag(eng, m[26], t[15], w_two[19], ancilla[0])  # 2

        AND_gate_dag(eng, l[11], t[8], w_two[18], ancilla[0])  # 2

        AND_gate_dag(eng, m[45], t[16], w_two[16], ancilla[0])  # 2
        AND_gate_dag(eng, l[12], m[40], w_two[15], ancilla[0])  # 2

        # ** ** ** ** ** ** ** ** ** ** ** ** ** **

        AND_gate_dag(eng, l[13], t[14], w_two[13], ancilla[0])  # 2
        AND_gate_dag(eng, l[2], m[38], w_two[12], ancilla[0])  # 2
        AND_gate_dag(eng, n[14], m[39], w_two[10], ancilla[0])  # 2

        CNOT2(eng, m[29], m[31], n[17])
        CNOT2(eng, n[14], n[17], n[18])
        CNOT2(eng, m[27], w_two[32], n[19])
        CNOT2(eng, m[25], w_two[30], n[20])
        AND_gate_dag(eng, l[14], t[26], w_two[6], ancilla[0])  # 2
        AND_gate_dag(eng, l[3], m[43], w_two[5], ancilla[0])  # 2

        AND_gate_dag(eng, l[15], t[9], w_two[2], ancilla[0])  # 2
        AND_gate_dag(eng, l[4], m[37], w_two[1], ancilla[0])  # 2

        AND_gate_dag(eng, l[5], t[12], n[25], ancilla[0])  # 2

        AND_gate_dag(eng, l[6], t[22], n[26], ancilla[0])  # 2

        AND_gate_dag(eng, l[7], t[18], n[28], ancilla[0])  # 2
        AND_gate_dag(eng, m[49], m[41], n[29], ancilla[0])  # 2

        AND_gate_dag(eng, l[16], t[2], n[30], ancilla[0])  # 2

        AND_gate_dag(eng, l[17], t[21], n[31], ancilla[0])  # 2

        AND_gate_dag(eng, m[46], t[19], n[33], ancilla[0])  # 2
        AND_gate_dag(eng, l[18], m[42], n[34], ancilla[0])  # 2

        AND_gate_dag(eng, l[19], t[0], n[35], ancilla[0])  # 2
        AND_gate_dag(eng, l[8], m[33], n[36], ancilla[0])  # 2
        AND_gate_dag(eng, l[22], m[34], w[25], ancilla[0])  # 2

        AND_gate_dag(eng, l[20], t[3], n[37], ancilla[0])  # 2
        AND_gate_dag(eng, l[9], m[36], n[38], ancilla[0])  # 2

        AND_gate_dag(eng, l[21], t[1], n[39], ancilla[0])  # 2
        AND_gate_dag(eng, l[10], m[35], n[40], ancilla[0])  # 2

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

        # l22 ~ 29 are idle state
        # ## can be used after 1st Toffoli operation -->  w[33 32 30 29 27 23 22 19 18 16 15 13 12 10 6 5 2 1]
        # Can be used after 2st Tofoli operation -> n[40 39 38 37 36 35 34 33 31 30 29 28 26 25 24 23 22 21]  -> Can be used after S-box operation n[20 19 18 17 16 15 13 12 10 9 8 7 6 5 3 2 1 0] w[25] m[24 25 27 28 29 30 31]

        AND_gate_dag(eng, n[2], w_two[29], m[32], ancilla[0])  # 3
        AND_gate_dag(eng, n[1], t[5], n_two[40], ancilla[0])  # 3
        CNOT | (n_two[40], m[32])

        AND_gate_dag(eng, m[31], t[7], m[33], ancilla[0])  # 3
        AND_gate_dag(eng, w_two[27], w_two[30], n_two[39], ancilla[0])  # 3
        CNOT | (n_two[39], m[33])

        AND_gate_dag(eng, w_two[23], m[25], m[34], ancilla[0])  # 3
        # CNOT2(eng, w[3], w_two[22], m[34])
        CNOT | (w_two[22], m[34])

        AND_gate_dag(eng, n[7], t[15], m[35], ancilla[0])  # 3
        AND_gate_dag(eng, n[8], w_two[19], n_two[38], ancilla[0])  # 3
        # CNOT2(eng, w[4], n_two[38], m[35])
        CNOT | (n_two[38], m[35])

        AND_gate_dag(eng, m[29], t[8], m[36], ancilla[0])  # 3
        AND_gate_dag(eng, w_two[32], w_two[18], n_two[37], ancilla[0])  # 3

        CNOT | (n_two[37], m[36])

        AND_gate_dag(eng, m[27], w_two[15], m[37], ancilla[0])  # 3
        # CNOT2(eng, w[7], w_two[16], m[37])
        CNOT | (w_two[16], m[37])

        AND_gate_dag(eng, w_two[13], l[3], m[38], ancilla[0])  # 3
        AND_gate_dag(eng, w_two[12], l[0], n_two[36], ancilla[0])  # 3
        # CNOT2(eng, w_two[10], w[9], m[38])
        CNOT | (w_two[10], m[38])
        CNOT | (n_two[36], m[38])

        AND_gate_dag(eng, n[18], t[26], m[39], ancilla[0])  # 3
        AND_gate_dag(eng, n[19], w_two[6], n_two[35], ancilla[0])  # 3
        AND_gate_dag(eng, n[20], w_two[5], n_two[34], ancilla[0])  # 3
        # CNOT2(eng, w[11], n_two[35], m[39])
        CNOT | (n_two[35], m[39])
        CNOT | (n_two[34], m[39])

        AND_gate_dag(eng, l[6], w_two[2], m[40], ancilla[0])  # 3
        AND_gate_dag(eng, n[17], t[9], n_two[33], ancilla[0])  # 3
        AND_gate_dag(eng, l[10], w_two[1], n_two[31], ancilla[0])  # 3
        # CNOT2(eng, w[14], n_two[33], m[40])
        CNOT | (n_two[33], m[40])
        CNOT | (n_two[31], m[40])

        AND_gate_dag(eng, l[15], n[25], m[41], ancilla[0])  # 3
        AND_gate_dag(eng, l[14], t[12], n_two[30], ancilla[0])  # 3
        # CNOT2(eng, w[17], n_two[30], m[41])
        CNOT | (n_two[30], m[41])

        AND_gate_dag(eng, l[13], t[22], m[42], ancilla[0])  # 3
        AND_gate_dag(eng, n[26], l[11], n_two[29], ancilla[0])  # 3
        CNOT | (n_two[29], m[42])

        AND_gate_dag(eng, n[28], l[1], m[43], ancilla[0])  # 3
        # CNOT2(eng, w[20], n[29], m[43])
        CNOT | (n[29], m[43])

        AND_gate_dag(eng, l[16], t[2], m[44], ancilla[0])  # 3
        AND_gate_dag(eng, l[17], n[30], n_two[28], ancilla[0])  # 3
        # CNOT2(eng, w[21], n_two[28], m[44])
        CNOT | (n_two[28], m[44])

        AND_gate_dag(eng, l[9], t[21], m[45], ancilla[0])  # 3
        AND_gate_dag(eng, l[7], n[31], n_two[26], ancilla[0])  # 3
        # CNOT2(eng, n_two[26], n[32], m[45])
        CNOT | (n_two[26], m[45])

        AND_gate_dag(eng, l[4], n[34], m[46], ancilla[0])  # 3
        # CNOT2(eng, w[24], n[33], m[46])
        CNOT | (n[33], m[46])

        AND_gate_dag(eng, n[35], l[5], m[47], ancilla[0])  # 3
        AND_gate_dag(eng, n[36], l[2], n_two[25], ancilla[0])  # 3

        # CNOT2(eng, w[25], w[26], m[47])
        CNOT | (w[25], m[47])
        CNOT | (n_two[25], m[47])

        AND_gate_dag(eng, l[19], t[3], m[48], ancilla[0])  # 3
        AND_gate_dag(eng, l[20], n[37], n_two[24], ancilla[0])  # 3
        AND_gate_dag(eng, l[21], n[38], n_two[23], ancilla[0])  # 3
        # CNOT2(eng, w[28], n_two[24], m[48])
        CNOT | (n_two[24], m[48])
        CNOT | (n_two[23], m[48])

        AND_gate_dag(eng, l[8], n[39], m[49], ancilla[0])  # 3
        AND_gate_dag(eng, l[18], t[1], n_two[22], ancilla[0])  # 3
        AND_gate_dag(eng, l[12], n[40], n_two[21], ancilla[0])  # 3
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

def Sbox(eng, u_in, t, m, n, w, l, s, flag, round, ancilla):
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

        AND_gate(eng, t[12], t[5], m[0], ancilla[0])
        AND_gate(eng, t[22], t[7], m[19], ancilla[1])

        AND_gate(eng, t[18], u[7], m[20], ancilla[2])
        CNOT | (m[0], m[20])
        AND_gate(eng, t[2], t[15], m[5], ancilla[3])
        AND_gate(eng, t[21], t[8], m[21], ancilla[4])

        AND_gate(eng, t[19], t[16], m[22], ancilla[5])
        CNOT | (m[5], m[22])
        CNOT | (m[5], m[21])
        AND_gate(eng, t[0], t[14], m[10], ancilla[6])
        AND_gate(eng, t[3], t[26], m[12], ancilla[7])

        CNOT | (m[10], m[12])
        AND_gate(eng, t[1], t[9], m[13], ancilla[8])  # Here

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

        AND_gate(eng, m[21], m[19], m[24], ancilla[0])

        CNOT2(eng, m[22], m[24], m[27])

        CNOT2(eng, m[20], m[24], m[25])

        AND_gate(eng, m[44], m[22], m[28], ancilla[1])
        CNOT2(eng, m[26], m[24], m[29])

        AND_gate(eng, m[20], m[47], m[30], ancilla[2])
        CNOT2(eng, m[23], m[24], m[31])

        # AND_gate_dag(eng, m[27], m[26], m[28])
        # AND_gate_dag(eng, m[25], m[23], m[29])
        # AND_gate_dag(eng, l[2], m[28], m[31])
        # AND_gate_dag(eng, l[3], m[30], m[34])

        AND_gate(eng, m[23], t[5], n[0], ancilla[3])  # 2
        CNOT2(eng, m[22], m[31], n[1])
        CNOT2(eng, m[25], m[30], n[2])

        AND_gate(eng, l[0], t[7], n[3], ancilla[4])  # 2

        AND_gate(eng, l[1], u[7], n[5], ancilla[5])  # 2
        AND_gate(eng, m[48], m[32], n[6], ancilla[6])  # 2

        CNOT2(eng, m[20], m[29], n[7])
        CNOT2(eng, m[27], m[28], n[8])
        AND_gate(eng, m[26], t[15], n[9], ancilla[7])  # 2

        AND_gate(eng, l[11], t[8], n[10], ancilla[8])  # 2

        AND_gate(eng, m[45], t[16], n[12], ancilla[9])  # 2
        AND_gate(eng, l[12], m[40], n[13], ancilla[10])  # 2

        # ** ** ** ** ** ** ** ** ** ** ** ** ** **

        AND_gate(eng, l[13], t[14], n[15], ancilla[11])  # 2
        AND_gate(eng, l[2], m[38], n[16], ancilla[12])  # 2
        AND_gate(eng, n[14], m[39], w[8], ancilla[13])  # 2

        CNOT2(eng, m[29], m[31], n[17])
        CNOT2(eng, n[14], n[17], n[18])
        CNOT2(eng, m[27], m[28], n[19])
        CNOT2(eng, m[25], m[30], n[20])
        AND_gate(eng, l[14], t[26], n[21], ancilla[14])  # 2
        AND_gate(eng, l[3], m[43], n[22], ancilla[15])  # 2

        AND_gate(eng, l[15], t[9], n[23], ancilla[16])  # 2
        AND_gate(eng, l[4], m[37], n[24], ancilla[17])  # 2

        AND_gate(eng, l[5], t[12], n[25], ancilla[18])  # 2

        AND_gate(eng, l[6], t[22], n[26], ancilla[19])  # 2

        AND_gate(eng, l[7], t[18], n[28], ancilla[20])  # 2
        AND_gate(eng, m[49], m[41], n[29], ancilla[21])  # 2

        AND_gate(eng, l[16], t[2], n[30], ancilla[22])  # 2

        AND_gate(eng, l[17], t[21], n[31], ancilla[23])  # 2

        AND_gate(eng, m[46], t[19], n[33], ancilla[24])  # 2
        AND_gate(eng, l[18], m[42], n[34], ancilla[32])  # 2

        AND_gate(eng, l[19], t[0], n[35], ancilla[25])  # 2
        AND_gate(eng, l[8], m[33], n[36], ancilla[26])  # 2
        AND_gate(eng, l[22], m[34], w[25], ancilla[27])  # 2

        if(flag == 1):
            AND_gate(eng, l[20], t[3], n[37], ancilla[28])  # 2
            AND_gate(eng, l[9], m[36], n[38], ancilla[29])  # 2

            AND_gate(eng, l[21], t[1], n[39], ancilla[30])  # 2
            AND_gate(eng, l[10], m[35], n[40], ancilla[31])  # 2
        else:
            AND_gate(eng, l[20], t[3], n[37], s[0])  # 2
            AND_gate(eng, l[9], m[36], n[38], s[1])  # 2

            AND_gate(eng, l[21], t[1], n[39], s[2])  # 2
            AND_gate(eng, l[10], m[35], n[40], s[3])  # 2

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

        AND_gate(eng, n[2], n[0], m[32], ancilla[0])  # 3
        AND_gate(eng, n[1], t[5], w[1], ancilla[1])  # 3
        CNOT | (w[1], m[32])

        AND_gate(eng, m[31], t[7], m[33], ancilla[2])  # 3
        AND_gate(eng, n[3], m[30], w[2], ancilla[3])  # 3
        CNOT | (w[2], m[33])

        AND_gate(eng, n[5], m[25], m[34], ancilla[4])  # 3
        # CNOT2(eng, w[3], n[6], m[34])
        CNOT | (n[6], m[34])

        AND_gate(eng, n[7], t[15], m[35], ancilla[5])  # 3
        AND_gate(eng, n[8], n[9], w[5], ancilla[6])  # 3
        # CNOT2(eng, w[4], w[5], m[35])
        CNOT | (w[5], m[35])

        AND_gate(eng, m[29], t[8], m[36], ancilla[7])  # 3
        AND_gate(eng, m[28], n[10], w[6], ancilla[8])  # 3

        CNOT | (w[6], m[36])

        AND_gate(eng, m[27], n[13], m[37], ancilla[9])  # 3
        # CNOT2(eng, w[7], n[12], m[37])
        CNOT | (n[12], m[37])

        AND_gate(eng, n[15], l[3], m[38], ancilla[10])  # 3
        AND_gate(eng, n[16], l[0], w[10], ancilla[11])  # 3
        # CNOT2(eng, w[8], w[9], m[38])
        CNOT | (w[8], m[38])
        CNOT | (w[10], m[38])

        AND_gate(eng, n[18], t[26], m[39], ancilla[12])  # 3
        AND_gate(eng, n[19], n[21], w[12], ancilla[13])  # 3
        AND_gate(eng, n[20], n[22], w[13], ancilla[14])  # 3
        # CNOT2(eng, w[11], w[12], m[39])
        CNOT | (w[12], m[39])
        CNOT | (w[13], m[39])

        AND_gate(eng, l[6], n[23], m[40], ancilla[15])  # 3
        AND_gate(eng, n[17], t[9], w[15], ancilla[16])  # 3
        AND_gate(eng, l[10], n[24], w[16], ancilla[17])  # 3
        # CNOT2(eng, w[14], w[15], m[40])
        CNOT | (w[15], m[40])
        CNOT | (w[16], m[40])

        AND_gate(eng, l[15], n[25], m[41], ancilla[18])  # 3
        AND_gate(eng, l[14], t[12], w[18], ancilla[19])  # 3
        # CNOT2(eng, w[17], w[18], m[41])
        CNOT | (w[18], m[41])

        AND_gate(eng, l[13], t[22], m[42], ancilla[20])  # 3
        AND_gate(eng, n[26], l[11], w[19], ancilla[21])  # 3
        CNOT | (w[19], m[42])

        AND_gate(eng, n[28], l[1], m[43], ancilla[22])  # 3
        # CNOT2(eng, w[20], n[29], m[43])
        CNOT | (n[29], m[43])

        AND_gate(eng, l[16], t[2], m[44], ancilla[23])  # 3
        AND_gate(eng, l[17], n[30], w[22], ancilla[24])  # 3
        # CNOT2(eng, w[21], w[22], m[44])
        CNOT | (w[22], m[44])

        AND_gate(eng, l[9], t[21], m[45], ancilla[25])  # 3
        AND_gate(eng, l[7], n[31], w[23], ancilla[26])  # 3
        # CNOT2(eng, w[23], n[32], m[45])
        CNOT | (w[23], m[45])

        AND_gate(eng, l[4], n[34], m[46], ancilla[27])  # 3
        # CNOT2(eng, w[24], n[33], m[46])
        CNOT | (n[33], m[46])

        if(flag ==1):
            AND_gate(eng, n[35], l[5], m[47], ancilla[28])  # 3
            AND_gate(eng, n[36], l[2], w[27], ancilla[29])  # 3

            # CNOT2(eng, w[25], w[26], m[47])
            CNOT | (w[25], m[47])
            CNOT | (w[27], m[47])

            AND_gate(eng, l[19], t[3], m[48], ancilla[30])  # 3
            AND_gate(eng, l[20], n[37], w[29], ancilla[31])  # 3
            AND_gate(eng, l[21], n[38], w[30], ancilla[32])  # 3
            # CNOT2(eng, w[28], w[29], m[48])
            CNOT | (w[29], m[48])
            CNOT | (w[30], m[48])

            AND_gate(eng, l[8], n[39], m[49], ancilla[33])  # 3
            AND_gate(eng, l[18], t[1], w[32], ancilla[34])  # 3
            AND_gate(eng, l[12], n[40], w[33], ancilla[35])  # 3 (36)
        else:
            AND_gate(eng, n[35], l[5], m[47], s[0])  # 3
            AND_gate(eng, n[36], l[2], w[27], s[1])  # 3

            # CNOT2(eng, w[25], w[26], m[47])
            CNOT | (w[25], m[47])
            CNOT | (w[27], m[47])

            AND_gate(eng, l[19], t[3], m[48], s[2])  # 3
            AND_gate(eng, l[20], n[37], w[29], s[3])  # 3
            AND_gate(eng, l[21], n[38], w[30], s[4])  # 3
            # CNOT2(eng, w[28], w[29], m[48])
            CNOT | (w[29], m[48])
            CNOT | (w[30], m[48])

            AND_gate(eng, l[8], n[39], m[49], s[5])  # 3
            AND_gate(eng, l[18], t[1], w[32], s[6])  # 3
            AND_gate(eng, l[12], n[40], w[33], s[7])  # 3 (36)
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

def Sbox_two(eng, u_in, t, m, n, n_two, w, w_two, l, s, flag, round, ancilla):
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

        AND_gate(eng, t[12], t[5], m[0], ancilla[0])
        AND_gate(eng, t[22], t[7], m[19], ancilla[1])

        AND_gate(eng, t[18], u[7], m[20], ancilla[2])
        CNOT | (m[0], m[20])
        AND_gate(eng, t[2], t[15], m[5], ancilla[3])
        AND_gate(eng, t[21], t[8], m[21], ancilla[4])

        AND_gate(eng, t[19], t[16], m[22], ancilla[5])
        CNOT | (m[5], m[22])
        CNOT | (m[5], m[21])
        AND_gate(eng, t[0], t[14], m[10], ancilla[6])
        AND_gate(eng, t[3], t[26], m[12], ancilla[7])

        CNOT | (m[10], m[12])
        AND_gate(eng, t[1], t[9], m[13], ancilla[8])  # Here

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

        # ## can be used after 1st Toffoli operation -->  w[33 32 30 29 27 23 22 19 18 16 15 13 12 10 6 5 2 1]

        AND_gate(eng, m[21], m[19], w_two[33], ancilla[0])

        CNOT2(eng, m[22], w_two[33], m[27])

        CNOT2(eng, m[20], w_two[33], m[25])

        AND_gate(eng, m[44], m[22], w_two[32], ancilla[1])
        CNOT2(eng, m[26], w_two[33], m[29])

        AND_gate(eng, m[20], m[47], w_two[30], ancilla[2])
        CNOT2(eng, m[23], w_two[33], m[31])

        # AND_gate(eng, m[27], m[26], w_two[32])
        # AND_gate(eng, m[25], m[23], m[29])
        # AND_gate(eng, l[2], w_two[32], m[31])
        # AND_gate(eng, l[3], w_two[30], m[34])

        AND_gate(eng, m[23], t[5], w_two[29], ancilla[3])  # 2
        CNOT2(eng, m[22], m[31], n[1])
        CNOT2(eng, m[25], w_two[30], n[2])

        AND_gate(eng, l[0], t[7], w_two[27], ancilla[4])  # 2

        AND_gate(eng, l[1], u[7], w_two[23], ancilla[5])  # 2
        AND_gate(eng, m[48], m[32], w_two[22], ancilla[6])  # 2

        CNOT2(eng, m[20], m[29], n[7])
        CNOT2(eng, m[27], w_two[32], n[8])
        AND_gate(eng, m[26], t[15], w_two[19], ancilla[7])  # 2

        AND_gate(eng, l[11], t[8], w_two[18], ancilla[8])  # 2

        AND_gate(eng, m[45], t[16], w_two[16], ancilla[9])  # 2
        AND_gate(eng, l[12], m[40], w_two[15], ancilla[10])  # 2

        # ** ** ** ** ** ** ** ** ** ** ** ** ** **

        AND_gate(eng, l[13], t[14], w_two[13], ancilla[11])  # 2
        AND_gate(eng, l[2], m[38], w_two[12], ancilla[12])  # 2
        AND_gate(eng, n[14], m[39], w_two[10], ancilla[13])  # 2

        CNOT2(eng, m[29], m[31], n[17])
        CNOT2(eng, n[14], n[17], n[18])
        CNOT2(eng, m[27], w_two[32], n[19])
        CNOT2(eng, m[25], w_two[30], n[20])
        AND_gate(eng, l[14], t[26], w_two[6], ancilla[14])  # 2
        AND_gate(eng, l[3], m[43], w_two[5], ancilla[15])  # 2

        AND_gate(eng, l[15], t[9], w_two[2], ancilla[16])  # 2
        AND_gate(eng, l[4], m[37], w_two[1], ancilla[17])  # 2

        AND_gate(eng, l[5], t[12], n[25], ancilla[18])  # 2

        AND_gate(eng, l[6], t[22], n[26], ancilla[19])  # 2

        AND_gate(eng, l[7], t[18], n[28], ancilla[20])  # 2
        AND_gate(eng, m[49], m[41], n[29], ancilla[21])  # 2

        AND_gate(eng, l[16], t[2], n[30], ancilla[22])  # 2

        AND_gate(eng, l[17], t[21], n[31], ancilla[23])  # 2

        AND_gate(eng, m[46], t[19], n[33], ancilla[24])  # 2
        AND_gate(eng, l[18], m[42], n[34], ancilla[25])  # 2

        AND_gate(eng, l[19], t[0], n[35], ancilla[26])  # 2
        AND_gate(eng, l[8], m[33], n[36], ancilla[27])  # 2

        if(flag==1):
            AND_gate(eng, l[22], m[34], w[25], ancilla[28])  # 2

            AND_gate(eng, l[20], t[3], n[37], ancilla[29])  # 2
            AND_gate(eng, l[9], m[36], n[38], ancilla[30])  # 2

            AND_gate(eng, l[21], t[1], n[39], ancilla[31])  # 2
            AND_gate(eng, l[10], m[35], n[40], ancilla[32])  # 2
        else:
            AND_gate(eng, l[22], m[34], w[25], s[0])  # 2

            AND_gate(eng, l[20], t[3], n[37], s[1])  # 2
            AND_gate(eng, l[9], m[36], n[38], s[2])  # 2

            AND_gate(eng, l[21], t[1], n[39], s[3])  # 2
            AND_gate(eng, l[10], m[35], n[40], s[4])  # 2
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

        # l22 ~ 29 are idle state
        # ## can be used after 1st Toffoli operation -->  w[33 32 30 29 27 23 22 19 18 16 15 13 12 10 6 5 2 1]
        # Can be used after 2st Tofoli operation -> n[40 39 38 37 36 35 34 33 31 30 29 28 26 25 24 23 22 21]  -> Can be used after S-box operation n[20 19 18 17 16 15 13 12 10 9 8 7 6 5 3 2 1 0] w[25] m[24 25 27 28 29 30 31]

        AND_gate(eng, n[2], w_two[29], m[32], ancilla[0])  # 3
        AND_gate(eng, n[1], t[5], n_two[40], ancilla[1])  # 3
        CNOT | (n_two[40], m[32])

        AND_gate(eng, m[31], t[7], m[33], ancilla[2])  # 3
        AND_gate(eng, w_two[27], w_two[30], n_two[39], ancilla[3])  # 3
        CNOT | (n_two[39], m[33])

        AND_gate(eng, w_two[23], m[25], m[34], ancilla[4])  # 3
        # CNOT2(eng, w[3], w_two[22], m[34])
        CNOT | (w_two[22], m[34])

        AND_gate(eng, n[7], t[15], m[35], ancilla[5])  # 3
        AND_gate(eng, n[8], w_two[19], n_two[38], ancilla[6])  # 3
        # CNOT2(eng, w[4], n_two[38], m[35])
        CNOT | (n_two[38], m[35])

        AND_gate(eng, m[29], t[8], m[36], ancilla[7])  # 3
        AND_gate(eng, w_two[32], w_two[18], n_two[37], ancilla[8])  # 3

        CNOT | (n_two[37], m[36])

        AND_gate(eng, m[27], w_two[15], m[37], ancilla[9])  # 3
        # CNOT2(eng, w[7], w_two[16], m[37])
        CNOT | (w_two[16], m[37])

        AND_gate(eng, w_two[13], l[3], m[38], ancilla[10])  # 3
        AND_gate(eng, w_two[12], l[0], n_two[36], ancilla[11])  # 3
        # CNOT2(eng, w_two[10], w[9], m[38])
        CNOT | (w_two[10], m[38])
        CNOT | (n_two[36], m[38])

        AND_gate(eng, n[18], t[26], m[39], ancilla[12])  # 3
        AND_gate(eng, n[19], w_two[6], n_two[35], ancilla[13])  # 3
        AND_gate(eng, n[20], w_two[5], n_two[34], ancilla[14])  # 3
        # CNOT2(eng, w[11], n_two[35], m[39])
        CNOT | (n_two[35], m[39])
        CNOT | (n_two[34], m[39])

        AND_gate(eng, l[6], w_two[2], m[40], ancilla[15])  # 3
        AND_gate(eng, n[17], t[9], n_two[33], ancilla[16])  # 3
        AND_gate(eng, l[10], w_two[1], n_two[31], ancilla[17])  # 3
        # CNOT2(eng, w[14], n_two[33], m[40])
        CNOT | (n_two[33], m[40])
        CNOT | (n_two[31], m[40])

        AND_gate(eng, l[15], n[25], m[41], ancilla[18])  # 3
        AND_gate(eng, l[14], t[12], n_two[30], ancilla[19])  # 3
        # CNOT2(eng, w[17], n_two[30], m[41])
        CNOT | (n_two[30], m[41])

        AND_gate(eng, l[13], t[22], m[42], ancilla[20])  # 3
        AND_gate(eng, n[26], l[11], n_two[29], ancilla[21])  # 3
        CNOT | (n_two[29], m[42])

        AND_gate(eng, n[28], l[1], m[43], ancilla[22])  # 3
        # CNOT2(eng, w[20], n[29], m[43])
        CNOT | (n[29], m[43])

        AND_gate(eng, l[16], t[2], m[44], ancilla[23])  # 3
        AND_gate(eng, l[17], n[30], n_two[28], ancilla[24])  # 3
        # CNOT2(eng, w[21], n_two[28], m[44])
        CNOT | (n_two[28], m[44])

        AND_gate(eng, l[9], t[21], m[45], ancilla[25])  # 3
        AND_gate(eng, l[7], n[31], n_two[26], ancilla[26])  # 3
        # CNOT2(eng, n_two[26], n[32], m[45])
        CNOT | (n_two[26], m[45])

        AND_gate(eng, l[4], n[34], m[46], ancilla[27])  # 3
        # CNOT2(eng, w[24], n[33], m[46])
        CNOT | (n[33], m[46])

        if(flag == 1):
            AND_gate(eng, n[35], l[5], m[47], ancilla[28])  # 3
            AND_gate(eng, n[36], l[2], n_two[25], ancilla[29])  # 3

            # CNOT2(eng, w[25], w[26], m[47])
            CNOT | (w[25], m[47])
            CNOT | (n_two[25], m[47])

            AND_gate(eng, l[19], t[3], m[48], ancilla[30])  # 3
            AND_gate(eng, l[20], n[37], n_two[24], ancilla[31])  # 3
            AND_gate(eng, l[21], n[38], n_two[23], ancilla[32])  # 3
            # CNOT2(eng, w[28], n_two[24], m[48])
            CNOT | (n_two[24], m[48])
            CNOT | (n_two[23], m[48])

            AND_gate(eng, l[8], n[39], m[49], ancilla[33])  # 3
            AND_gate(eng, l[18], t[1], n_two[22], ancilla[34])  # 3
            AND_gate(eng, l[12], n[40], n_two[21], ancilla[35])  # 3
        else:
            AND_gate(eng, n[35], l[5], m[47], s[0])  # 3
            AND_gate(eng, n[36], l[2], n_two[25], s[1])  # 3

            # CNOT2(eng, w[25], w[26], m[47])
            CNOT | (w[25], m[47])
            CNOT | (n_two[25], m[47])

            AND_gate(eng, l[19], t[3], m[48], s[2])  # 3
            AND_gate(eng, l[20], n[37], n_two[24], s[3])  # 3
            AND_gate(eng, l[21], n[38], n_two[23], s[4])  # 3
            # CNOT2(eng, w[28], n_two[24], m[48])
            CNOT | (n_two[24], m[48])
            CNOT | (n_two[23], m[48])

            AND_gate(eng, l[8], n[39], m[49], s[5])  # 3
            AND_gate(eng, l[18], t[1], n_two[22], s[6])  # 3
            AND_gate(eng, l[12], n[40], n_two[21], s[7])  # 3
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
    H | b
    CNOT | (a, b)
    X | c

    with Dagger(eng):
        Measure | c
    H | b
    H | c

print('Estimate cost...')
Resource = ResourceCounter()
eng = MainEngine(Resource)
AES(eng, 1)
print(Resource)
print('\n')
eng.flush()

