from projectq import MainEngine
from projectq.ops import H, CNOT, Measure, Toffoli, X, All, Swap
from projectq.backends import ResourceCounter, ClassicalSimulator

def main(eng):
    x0 = eng.allocate_qureg(32)
    x1 = eng.allocate_qureg(32)
    x2 = eng.allocate_qureg(32)
    x3 = eng.allocate_qureg(32)
    x4 = eng.allocate_qureg(32)
    x5 = eng.allocate_qureg(32)
    x6 = eng.allocate_qureg(32)
    x7 = eng.allocate_qureg(32)
    x8 = eng.allocate_qureg(32)
    x9 = eng.allocate_qureg(32)

    y1 = eng.allocate_qureg(32)
    y2 = eng.allocate_qureg(32)

    x_naive = eng.allocate_qureg(32)
    x_naive_matrix = eng.allocate_qureg(32)
    x_naive2 = eng.allocate_qureg(32)
    out_naive2 = eng.allocate_qureg(32)
    out_naive_matrix = eng.allocate_qureg(32)

    x_euro = eng.allocate_qureg(32)
    x_eprint = eng.allocate_qureg(32)
    x_2023 = eng.allocate_qureg(32)
    new_240703 = eng.allocate_qureg(200)
    new_1120 = eng.allocate_qureg(32)
    new_1213 = eng.allocate_qureg(32)
    new_0104 = eng.allocate_qureg(32)
    new_0114 = eng.allocate_qureg(32)
    new_0221 = eng.allocate_qureg(32)
    new_0221_2 = eng.allocate_qureg(32)
    asia_23 = eng.allocate_qureg(32)
    peerj = eng.allocate_qureg(32)

    if (not resource_check):
        Round_constant_XOR(eng, x0, 0xcd38df63, 32)
        Round_constant_XOR(eng, x1, 0xcd38df63, 32)
        Round_constant_XOR(eng, x2, 0xcd38df63, 32)
        Round_constant_XOR(eng, x3, 0xcd38df63, 32)
        Round_constant_XOR(eng, x4, 0xcd38df63, 32)
        Round_constant_XOR(eng, x5, 0xcd38df63, 32)
        Round_constant_XOR(eng, x6, 0xcd38df63, 32)
        Round_constant_XOR(eng, x7, 0xcd38df63, 32)
        Round_constant_XOR(eng, x_naive, 0xcd38df63, 32)
        Round_constant_XOR(eng, x_naive_matrix, 0xcd38df63, 32)
        Round_constant_XOR(eng, x_naive2, 0xcd38df63, 32)
        Round_constant_XOR(eng, x_euro, 0xcd38df63, 32) # index issue
        Round_constant_XOR(eng, x_eprint, 0xcd38df63, 32)
        Round_constant_XOR(eng, x_2023, 0xcd38df63, 32)
        Round_constant_XOR(eng, asia_23, 0xcd38df63, 32)
        Round_constant_XOR(eng, new_240703[0:32], 0xcd38df63, 32)
        Round_constant_XOR(eng, x8, 0xcd38df63, 32)
        Round_constant_XOR(eng, x9, 0xcd38df63, 32)
        Round_constant_XOR(eng, new_1120, 0xcd38df63, 32)
        Round_constant_XOR(eng, new_1213, 0xcd38df63, 32)
        Round_constant_XOR(eng, new_0104, 0xcd38df63, 32)
        Round_constant_XOR(eng, new_0114, 0xcd38df63, 32)
        Round_constant_XOR(eng, new_0221, 0xcd38df63, 32)
        Round_constant_XOR(eng, new_0221_2, 0xcd38df63, 32)
        Round_constant_XOR(eng, peerj, 0xcd38df63, 32)

    x0 = Mixcolumns(eng, x0) # Ours [56]
    y1 = AES_97xor(eng, x1, y1) # [41]
    y2 = XOR94(eng, x2, y2)  # [53]
    out1 = XOR105_newnew(eng, x3) #[44]
    out2 = IP_mc(eng, x4) #[38]
    out3 = Maxi_mc(eng, x5)  # [47]
    out4 = AES_MC5(eng, x6) #[46] Towards Low-Latency Implementation of LinearLayers
    out5 = AES_MC_45(eng, x7) #[45]
    out_euro = Euro_plu_mix(eng, x_euro)
    out_naive = mix_naive(eng, x_naive)
    out_naive_matrix = mix_naive_matrix(eng, x_naive_matrix, out_naive_matrix)
    out_naive2 = Mix_naive_2(eng, x_naive2, out_naive2)
    out_zhu_eprint = zhu_eprint(eng, x_eprint)
    out_2023 = AES_102xor_2023(eng, x_2023)
    out_asia_23 = asia_23_mc(eng, asia_23)
    new_240703_out = Mix_240703(eng, new_240703)
    asia_24_out = asia_24_Mixcolumn(eng, x8)
    out_1213 = Mix_1213(eng, new_1213)
    out_0104 = Mix_0104(eng, new_0104)
    out_0114 = CNOT_0114(eng, new_0114)
    out_ches = ches_mc(eng, new_0221)
    xor98 = XOR91(eng, x9)
    peerj_out = Peerj_mc(eng, peerj)  # Optimizing implementations of linear layers using two and higher input XOR gates

    if (not resource_check):
        print("AES_ours[56]")
        print_state(eng, x0, 8)

        print("AES_97xor[41]")
        print_state(eng, y1, 8)

        print("94xor[53]")
        print_state(eng, y2, 8)

        print("105xor[44]")
        print_state(eng, out1, 8)

        print("IP_mc[38]")
        print_state(eng, out2, 8)

        print("Maxi_mc[47]")
        print_state(eng, out3, 8)

        print("new_mix [46]")
        print_state(eng, out4, 8)

        print("Mix_Song [45]")
        print_state(eng, out5, 8)

        ### Index issue) ###
        # print("Euro")
        # print_state(eng, out_euro, 8)

        print("ePrint")
        print_state(eng, out_zhu_eprint, 8)

        print("Mix_naive")
        print_state(eng, out_naive, 8)

        print("Mix_naive2")
        print_state(eng, out_naive2, 8)

        print("Mix_naive_matrix")
        print_state(eng, out_naive_matrix, 8)

        print("Mix_eprint_zhu")
        print_state(eng, out_zhu_eprint, 8)

        print("Mix_eprint_zhu")
        print_state(eng, out_2023, 8)
        #
        print("Mix_asia")
        print_state(eng, out_asia_23, 8)

        print("Mix_asi240723")
        print_state(eng, new_240703_out, 8)

        print("asia24")
        print_state(eng, asia_24_out, 8)

        print('xor98')
        print_state(eng, xor98, 8)

        print('mc_1213')
        print_state(eng, out_1213, 8)

        print('mc_0104')
        print_state(eng, out_0104, 8)

        print('mc_0114')
        print_state(eng, out_0114, 8)

        print('ches')
        print_state(eng, out_ches, 8)

def reverse_CNOT(eng, a, b):
    CNOT | (b, a)

def logical_swap(eng, a, b):
    temp = a
    a = b
    b = temp

    return a, b

def ches_mc(eng, x_in):
    x = []
    for i in range(8):
        x.append(x_in[24 + i])
    for i in range(8):
        x.append(x_in[16 + i])
    for i in range(8):
        x.append(x_in[8 + i])
    for i in range(8):
        x.append(x_in[i])
    for i in range(100):
        new = eng.allocate_qubit()
        x.append(new)

    CNOT2(eng, x[32], x[2], x[10])
    CNOT2(eng, x[33], x[1], x[25])
    CNOT2(eng, x[34], x[18], x[33])
    CNOT2(eng, x[35], x[9], x[25])
    CNOT2(eng, x[36], x[10], x[26])
    CNOT2(eng, x[37], x[35], x[36])
    CNOT2(eng, x[38], x[9], x[17])
    CNOT2(eng, x[39], x[2], x[38])
    CNOT2(eng, x[40], x[37], x[39])  # y[18]
    CNOT2(eng, x[41], x[18], x[26])
    CNOT2(eng, x[42], x[39], x[41])  # y[10]
    CNOT2(eng, x[43], x[7], x[31])
    CNOT2(eng, x[44], x[8], x[16])
    CNOT2(eng, x[45], x[0], x[43])
    CNOT2(eng, x[46], x[44], x[45])  # y[24]
    CNOT2(eng, x[47], x[7], x[15])
    CNOT2(eng, x[48], x[24], x[44])
    CNOT2(eng, x[49], x[47], x[48])  # y[0]
    CNOT2(eng, x[50], x[14], x[22])
    CNOT2(eng, x[51], x[23], x[43])
    CNOT2(eng, x[52], x[50], x[51])  # y[15]
    CNOT2(eng, x[53], x[6], x[30])
    CNOT2(eng, x[54], x[47], x[53])
    CNOT2(eng, x[55], x[23], x[54])  # y[31]
    CNOT2(eng, x[56], x[21], x[29])
    CNOT2(eng, x[57], x[14], x[56])
    CNOT2(eng, x[58], x[53], x[57])  # y[22]
    CNOT2(eng, x[59], x[4], x[12])
    CNOT2(eng, x[60], x[13], x[59])
    CNOT2(eng, x[61], x[56], x[60])  # y[5]
    CNOT2(eng, x[62], x[5], x[13])
    CNOT2(eng, x[63], x[30], x[62])
    CNOT2(eng, x[64], x[50], x[63])  # y[6]
    CNOT2(eng, x[65], x[20], x[28])
    CNOT2(eng, x[66], x[29], x[65])
    CNOT2(eng, x[67], x[62], x[66])  # y[21]
    CNOT2(eng, x[68], x[1], x[24])
    CNOT2(eng, x[69], x[38], x[68])
    CNOT2(eng, x[70], x[45], x[69])  # y[25]
    CNOT2(eng, x[71], x[6], x[22])
    CNOT2(eng, x[72], x[31], x[71])
    CNOT2(eng, x[73], x[54], x[72])  # y[23]
    CNOT2(eng, x[74], x[15], x[23])
    CNOT2(eng, x[75], x[50], x[74])
    CNOT2(eng, x[76], x[72], x[75])  # y[7]
    CNOT2(eng, x[77], x[0], x[8])
    CNOT2(eng, x[78], x[74], x[77])
    CNOT2(eng, x[79], x[48], x[78])  # y[8]
    CNOT2(eng, x[80], x[23], x[31])
    CNOT2(eng, x[81], x[24], x[80])
    CNOT2(eng, x[82], x[77], x[81])  # y[16]
    CNOT2(eng, x[83], x[5], x[21])
    CNOT2(eng, x[84], x[71], x[83])
    CNOT2(eng, x[85], x[57], x[84])  # y[30]
    CNOT2(eng, x[86], x[63], x[84])  # y[14]
    CNOT2(eng, x[87], x[12], x[28])
    CNOT2(eng, x[88], x[83], x[87])
    CNOT2(eng, x[89], x[60], x[88])  # y[29]
    CNOT2(eng, x[90], x[66], x[88])  # y[13]
    CNOT2(eng, x[91], x[68], x[80])
    CNOT2(eng, x[92], x[16], x[35])
    CNOT2(eng, x[93], x[91], x[92])  # y[17]
    CNOT2(eng, x[94], x[17], x[35])
    CNOT2(eng, x[95], x[47], x[77])
    CNOT2(eng, x[96], x[94], x[95])  # y[1]
    CNOT2(eng, x[97], x[17], x[44])
    CNOT2(eng, x[98], x[33], x[74])
    CNOT2(eng, x[99], x[97], x[98])  # y[9]
    CNOT2(eng, x[100], x[19], x[27])
    CNOT2(eng, x[101], x[11], x[47])
    CNOT2(eng, x[102], x[32], x[100])
    CNOT2(eng, x[103], x[101], x[102])  # y[3]
    CNOT2(eng, x[104], x[3], x[20])
    CNOT2(eng, x[105], x[87], x[104])
    CNOT2(eng, x[106], x[101], x[105])  # y[4]
    CNOT2(eng, x[107], x[80], x[100])
    CNOT2(eng, x[108], x[4], x[87])
    CNOT2(eng, x[109], x[107], x[108])  # y[20]
    CNOT2(eng, x[110], x[27], x[104])
    CNOT2(eng, x[111], x[43], x[59])
    CNOT2(eng, x[112], x[110], x[111])  # y[28]
    CNOT2(eng, x[113], x[11], x[19])
    CNOT2(eng, x[114], x[65], x[113])
    CNOT2(eng, x[115], x[4], x[74])
    CNOT2(eng, x[116], x[114], x[115])  # y[12]
    CNOT2(eng, x[117], x[2], x[26])
    CNOT2(eng, x[118], x[3], x[43])
    CNOT2(eng, x[119], x[113], x[117])
    CNOT2(eng, x[120], x[118], x[119])  # y[27]
    CNOT2(eng, x[121], x[10], x[74])
    CNOT2(eng, x[122], x[3], x[18])
    CNOT2(eng, x[123], x[100], x[122])
    CNOT2(eng, x[124], x[121], x[123])  # y[11]
    CNOT2(eng, x[125], x[41], x[80])
    CNOT2(eng, x[126], x[11], x[27])
    CNOT2(eng, x[127], x[3], x[126])
    CNOT2(eng, x[128], x[125], x[127])  # y[19]
    CNOT2(eng, x[129], x[34], x[37])  # y[2]
    CNOT2(eng, x[130], x[32], x[34])  # y[26]

    y = []

    y.append(x[49])  # y[0]
    y.append(x[96])  # y[1]
    y.append(x[129])  # y[2]
    y.append(x[103])  # y[3]
    y.append(x[106])  # y[4]
    y.append(x[61])  # y[5]
    y.append(x[64])  # y[6]
    y.append(x[76])  # y[7]
    y.append(x[79])  # y[8]
    y.append(x[99])  # y[9]
    y.append(x[42])  # y[10]
    y.append(x[124])  # y[11]
    y.append(x[116])  # y[12]
    y.append(x[90])  # y[13]
    y.append(x[86])  # y[14]
    y.append(x[52])  # y[15]
    y.append(x[82])  # y[16]
    y.append(x[93])  # y[17]
    y.append(x[40])  # y[18]
    y.append(x[128])  # y[19]
    y.append(x[109])  # y[20]
    y.append(x[67])  # y[21]
    y.append(x[58])  # y[22]
    y.append(x[73])  # y[23]
    y.append(x[46])  # y[24]
    y.append(x[70])  # y[25]
    y.append(x[130])  # y[26]
    y.append(x[120])  # y[27]
    y.append(x[112])  # y[28]
    y.append(x[89])  # y[29]
    y.append(x[85])  # y[30]
    y.append(x[55])  # y[31]

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

def CNOT_0114(eng, x_in):
    t = eng.allocate_qureg(100)
    y = eng.allocate_qureg(100)

    x = []
    for i in range(32):
        x.append(x_in[31-i])

    CNOT | (x[8], t[0])
    CNOT | (x[16], t[0])
    CNOT | (x[24], t[1])
    CNOT | (x[0], t[1])
    CNOT | (x[28], t[2])
    CNOT | (x[24], t[2])
    CNOT | (x[16], t[2])
    CNOT | (x[12], t[3])
    CNOT | (x[8], t[3])
    CNOT | (x[0], t[3])
    CNOT | (x[22], t[4])
    CNOT | (x[14], t[4])
    CNOT | (x[7], t[4])
    CNOT | (x[23], t[5])
    CNOT | (x[6], t[5])
    CNOT | (x[30], t[5])
    CNOT | (x[20], t[6])
    CNOT | (x[27], t[6])
    CNOT | (x[3], t[6])
    CNOT | (x[11], y[19])
    CNOT | (t[2], y[19])
    CNOT | (t[6], y[19])
    CNOT | (x[11], t[8])
    CNOT | (x[4], t[8])
    CNOT | (x[19], t[8])
    CNOT | (x[27], y[3])
    CNOT | (t[3], y[3])
    CNOT | (t[8], y[3])
    CNOT | (x[13], t[10])
    CNOT | (x[20], t[10])
    CNOT | (x[28], t[10])
    CNOT | (x[5], y[4])
    CNOT | (t[3], y[4])
    CNOT | (t[10], y[4])
    CNOT | (x[12], t[12])
    CNOT | (x[4], t[12])
    CNOT | (x[29], t[12])
    CNOT | (x[21], y[20])
    CNOT | (t[2], y[20])
    CNOT | (t[12], y[20])
    CNOT | (x[18], t[14])
    CNOT | (x[26], t[14])
    CNOT | (x[11], t[14])
    CNOT | (x[10], y[2])
    CNOT | (x[3], y[2])
    CNOT | (t[14], y[2])
    CNOT | (x[2], y[10])
    CNOT | (x[19], y[10])
    CNOT | (t[14], y[10])
    CNOT | (x[18], t[17])
    CNOT | (x[10], t[17])
    CNOT | (x[27], t[17])
    CNOT | (x[11], y[18])
    CNOT | (y[10], y[18])
    CNOT | (t[17], y[18])
    CNOT | (x[3], y[26])
    CNOT | (x[2], y[26])
    CNOT | (t[17], y[26])
    CNOT | (x[22], t[20])
    CNOT | (x[5], t[20])
    CNOT | (x[29], t[20])
    CNOT | (x[13], y[21])
    CNOT | (x[30], y[21])
    CNOT | (t[20], y[21])
    CNOT | (x[14], y[13])
    CNOT | (x[21], y[13])
    CNOT | (t[20], y[13])
    CNOT | (x[18], t[23])
    CNOT | (x[1], t[23])
    CNOT | (x[25], t[23])
    CNOT | (x[10], y[9])
    CNOT | (x[17], y[9])
    CNOT | (t[23], y[9])
    CNOT | (x[9], y[17])
    CNOT | (x[26], y[17])
    CNOT | (t[23], y[17])
    CNOT | (x[6], t[26])
    CNOT | (x[21], t[26])
    CNOT | (x[29], t[26])
    CNOT | (x[22], y[29])
    CNOT | (y[21], y[29])
    CNOT | (t[26], y[29])
    CNOT | (x[13], y[5])
    CNOT | (x[14], y[5])
    CNOT | (t[26], y[5])
    CNOT | (x[24], t[29])
    CNOT | (x[16], t[29])
    CNOT | (x[31], t[29])
    CNOT | (x[7], y[23])
    CNOT | (x[15], y[23])
    CNOT | (t[29], y[23])
    CNOT | (x[14], y[22])
    CNOT | (t[5], y[22])
    CNOT | (t[29], y[22])
    CNOT | (x[2], t[32])
    CNOT | (y[9], t[32])
    CNOT | (y[17], t[32])
    CNOT | (x[10], y[25])
    CNOT | (x[1], y[25])
    CNOT | (t[32], y[25])
    CNOT | (x[26], y[1])
    CNOT | (x[25], y[1])
    CNOT | (t[32], y[1])
    CNOT | (x[8], t[35])
    CNOT | (x[15], t[35])
    CNOT | (x[0], t[35])
    CNOT | (x[30], y[6])
    CNOT | (t[4], y[6])
    CNOT | (t[35], y[6])
    CNOT | (x[23], y[7])
    CNOT | (x[31], y[7])
    CNOT | (t[35], y[7])
    CNOT | (x[23], t[38])
    CNOT | (t[1], t[38])
    CNOT | (y[23], t[38])
    CNOT | (t[35], y[15])
    CNOT | (t[38], y[15])
    CNOT | (t[29], y[31])
    CNOT | (t[38], y[31])
    CNOT | (x[17], t[41])
    CNOT | (x[16], t[41])
    CNOT | (t[1], t[41])
    CNOT | (x[25], y[16])
    CNOT | (t[0], y[16])
    CNOT | (t[41], y[16])
    CNOT | (x[9], y[8])
    CNOT | (t[41], y[8])
    CNOT | (x[1], t[44])
    CNOT | (x[0], t[44])
    CNOT | (t[0], t[44])
    CNOT | (x[9], y[0])
    CNOT | (t[1], y[0])
    CNOT | (t[44], y[0])
    CNOT | (x[25], y[24])
    CNOT | (t[44], y[24])
    CNOT | (t[1], t[47])
    CNOT | (y[6], t[47])
    CNOT | (y[7], t[47])
    CNOT | (t[5], y[30])
    CNOT | (t[47], y[30])
    CNOT | (x[4], t[49])
    CNOT | (x[21], t[49])
    CNOT | (t[10], t[49])
    CNOT | (t[0], y[12])
    CNOT | (t[49], y[12])
    CNOT | (x[19], t[51])
    CNOT | (t[0], t[51])
    CNOT | (t[6], t[51])
    CNOT | (x[12], y[11])
    CNOT | (t[51], y[11])
    CNOT | (x[20], t[53])
    CNOT | (x[5], t[53])
    CNOT | (t[1], t[53])
    CNOT | (t[12], y[28])
    CNOT | (t[53], y[28])
    CNOT | (x[28], t[55])
    CNOT | (x[3], t[55])
    CNOT | (t[1], t[55])
    CNOT | (t[8], y[27])
    CNOT | (t[55], y[27])
    CNOT | (t[0], t[57])
    CNOT | (y[23], t[57])
    CNOT | (y[22], t[57])
    CNOT | (t[4], y[14])
    CNOT | (t[57], y[14])

    y2 = []
    for i in range(32):
        y2.append(y[31 - i])

    out_y = []

    # out_y = []
    # for i in range(8):
    #     out_y.append(y[24 + i])
    # for i in range(8):
    #     out_y.append(y[16 + i])
    # for i in range(8):
    #     out_y.append(y[8 + i])
    # for i in range(8):
    #     out_y.append(y[0 + i])

    # for i in range(8):
    #     out_y.append(y2[i])
    # for i in range(8):
    #     out_y.append(y2[8 + i])
    # for i in range(8):
    #     out_y.append(y2[16 + i])
    # for i in range(8):
    #     out_y.append(y2[24 + i])

    # out_x = []
    # for i in range(8):
    #     out_x.append(y[8 + i])
    # for i in range(8):
    #     out_x.append(y[24 + i])
    # for i in range(8):
    #     out_x.append(y[0 + i])
    # for i in range(8):
    #     out_x.append(y[16 + i])
    #
    # for i in range(8):
    #     out_x.append(y[24 + i])
    # for i in range(8):
    #     out_x.append(y[16 + i])
    # for i in range(8):
    #     out_x.append(y[8 + i])
    # for i in range(8):
    #     out_x.append(y[0 + i])


    return y2

def Mix_0104(eng, x_in):
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

    x[17], x[1] = logical_swap(eng, x[17], x[1])
    x[26], x[2] = logical_swap(eng, x[26], x[2])
    x[11], x[3] = logical_swap(eng, x[11], x[3])
    x[28], x[4] = logical_swap(eng, x[28], x[4])
    x[21], x[5] = logical_swap(eng, x[21], x[5])
    x[22], x[6] = logical_swap(eng, x[22], x[6])
    x[15], x[7] = logical_swap(eng, x[15], x[7])
    x[24], x[8] = logical_swap(eng, x[24], x[8])
    x[25], x[9] = logical_swap(eng, x[25], x[9])
    x[18], x[10] = logical_swap(eng, x[18], x[10])
    x[20], x[12] = logical_swap(eng, x[20], x[12])
    x[29], x[13] = logical_swap(eng, x[29], x[13])
    x[30], x[14] = logical_swap(eng, x[30], x[14])
    x[24], x[16] = logical_swap(eng, x[24], x[16])
    x[31], x[23] = logical_swap(eng, x[31], x[23])
    x[18], x[26] = logical_swap(eng, x[18], x[26])
    x[11], x[27] = logical_swap(eng, x[11], x[27])

    out_x = []
    for i in range(8):
        out_x.append(x[24 + i])
    for i in range(8):
        out_x.append(x[16 + i])
    for i in range(8):
        out_x.append(x[8 + i])
    for i in range(8):
        out_x.append(x[0 + i])

    return out_x

def Mix_1213(eng, x_in):

    x = []
    for i in range(8):
        x.append(x_in[24 + i])
    for i in range(8):
        x.append(x_in[16 + i])
    for i in range(8):
        x.append(x_in[8 + i])
    for i in range(8):
        x.append(x_in[i])

    #x01, x09 = x09, x01
    #x16, x24 = x24, x16
    #x13, x29 = x29, x13
    x[1], x[9] =logical_swap(eng, x[1], x[9])
    x[16], x[24] =logical_swap(eng, x[16], x[24])
    x[13], x[29] =logical_swap(eng, x[13], x[29])

    #x11 = x11 + x27
    CNOT | (x[27], x[11])

    # x02 = x02 + x18
    CNOT | (x[18], x[2])

    # x21 = x21 + x05
    CNOT | (x[5], x[21])

    # x09, x17 = x17, x09
    x[9], x[17] = logical_swap(eng, x[9], x[17])

    # x04 = x12 + x04
    CNOT | (x[12], x[4])

    # x10, x26 = x26, x10
    x[10], x[26] =logical_swap(eng, x[10], x[26])

    #x13 = x13 + x29
    # x26 = x26 + x10
    # x22 = x22 + x06
    CNOT | (x[29], x[13])
    CNOT | (x[10], x[26])
    CNOT | (x[6], x[22])

    #x00, x08 = x08, x00
    x[0], x[8] =logical_swap(eng, x[0], x[8])

    # x28 = x28 + x04
    # x15 = x15 + x31
    # x23 = x23 + x07
    # x07 = x07 + x23
    # x31 = x31 + x07
    # x07 = x07 + x15

    CNOT | (x[4], x[28])
    CNOT | (x[31], x[15])
    CNOT | (x[7], x[23])
    CNOT | (x[23], x[7])
    CNOT | (x[7], x[31])
    CNOT | (x[15], x[7])

    # x17, x25 = x25, x17
    x[17], x[25] =logical_swap(eng, x[17], x[25])

    # x17 = x17 + x25
    # x09 = x09 + x17
    # x25 = x25 + x09
    # x09 = x09 + x01
    CNOT | (x[25], x[17])
    CNOT | (x[17], x[9])
    CNOT | (x[9], x[25])
    CNOT | (x[1], x[9])

    # x03, x19 = x19, x03
    x[3], x[19] =logical_swap(eng, x[3], x[19])

    # x19 = x19 + x03
    # x08 = x00 + x08
    # x16 = x16 + x08
    # x01 = x01 + x16
    # x30 = x30 + x14
    # x14 = x14 + x06

    CNOT | (x[3], x[19])
    CNOT | (x[0], x[8])
    CNOT | (x[8], x[16])
    CNOT | (x[16], x[1])
    CNOT | (x[14], x[30])
    CNOT | (x[6], x[14])

    # x07 = x07 + x14
    # x06 = x06 + x05
    # x05 = x05 + x04
    # x04 = x04 + x19
    # x19 = x19 + x11
    # x11 = x11 + x15

    CNOT | (x[14], x[7])
    CNOT | (x[5], x[6])
    CNOT | (x[4], x[5])
    CNOT | (x[19], x[4])
    CNOT | (x[11], x[19])
    CNOT | (x[15], x[11])

    # x06 = x29 + x06
    # x14 = x21 + x14
    # x08 = x08 + x23
    # x24 = x24 + x08
    # x16 = x16 + x31
    # x00 = x00 + x24

    CNOT | (x[29], x[6])
    CNOT | (x[21], x[14])
    CNOT | (x[23], x[8])
    CNOT | (x[8], x[24])
    CNOT | (x[31], x[16])
    CNOT | (x[24], x[0])

    # x24 = x24 + x31
    # x27 = x03 + x27
    # x03 = x03 + x18
    # x18 = x18 + x25
    # x03 = x03 + x10
    # x10 = x10 + x17

    CNOT | (x[31], x[24])
    CNOT | (x[3], x[27])
    CNOT | (x[18], x[3])
    CNOT | (x[25], x[18])
    CNOT | (x[10], x[3])
    CNOT | (x[17], x[10])

    # x17 = x17 + x23
    # x17 = x17 + x24
    # x17 = x17 + x01
    # x03 = x03 + x31
    # x19 = x19 + x03
    # x12 = x12 + x20

    CNOT | (x[23], x[17])
    CNOT | (x[24], x[17])
    CNOT | (x[1], x[17])
    CNOT | (x[31], x[3])
    CNOT | (x[3], x[19])
    CNOT | (x[20], x[12])

    # x29 = x29 + x12
    # x12 = x12 + x11
    # x11 = x11 + x23
    # x11 = x11 + x18
    # x20 = x20 + x28
    # x28 = x28 + x27

    CNOT | (x[12], x[29])
    CNOT | (x[11], x[12])
    CNOT | (x[23], x[11])
    CNOT | (x[18], x[11])
    CNOT | (x[28], x[20])
    CNOT | (x[27], x[28])

    # x27 = x27 + x02
    # x02 = x02 + x09
    # x10 = x10 + x02
    # x28 = x28 + x31
    # x31 = x31 + x22
    # x27 = x27 + x23

    CNOT | (x[2], x[27])
    CNOT | (x[9], x[2])
    CNOT | (x[2], x[10])
    CNOT | (x[31], x[28])
    CNOT | (x[22], x[31])
    CNOT | (x[23], x[27])


    # x27 = x27 + x19
    # x22 = x22 + x30
    # x06 = x06 + x22
    # x14 = x06 + x14
    # x26 = x26 + x09
    # x18 = x18 + x26

    CNOT | (x[19], x[27])
    CNOT | (x[30], x[22])
    CNOT | (x[22], x[6])
    CNOT | (x[6], x[14])
    CNOT | (x[9], x[26])
    CNOT | (x[26], x[18])

    # x02 = x02 + x18
    # x11 = x11 + x02
    # x26 = x26 + x10
    # x03 = x03 + x11
    # x11 = x11 + x27
    # x25 = x25 + x00

    CNOT | (x[18], x[2])
    CNOT | (x[2], x[11])
    CNOT | (x[10], x[26])
    CNOT | (x[11], x[3])
    CNOT | (x[27], x[11])
    CNOT | (x[0], x[25])

    # x00 = x00 + x15
    # x15 = x15 + x22
    # x00 = x00 + x16
    # x08 = x08 + x00
    # x01 = x01 + x08
    # x09 = x09 + x01

    CNOT | (x[15], x[0])
    CNOT | (x[22], x[15])
    CNOT | (x[16], x[0])
    CNOT | (x[0], x[8])
    CNOT | (x[8], x[1])
    CNOT | (x[1], x[9])


    # x01 = x01 + x25
    # x25 = x25 + x17
    # x13 = x13 + x21
    # x21 = x21 + x20
    # x20 = x20 + x12
    # x05 = x05 + x13

    CNOT | (x[25], x[1])
    CNOT | (x[17], x[25])
    CNOT | (x[21], x[13])
    CNOT | (x[20], x[21])
    CNOT | (x[12], x[20])
    CNOT | (x[13], x[5])

    # x12 = x12 + x28
    # x04 = x04 + x12
    # x30 = x30 + x13
    # x13 = x13 + x29
    # x29 = x29 + x21
    # x21 = x21 + x05

    CNOT | (x[28], x[12])
    CNOT | (x[12], x[4])
    CNOT | (x[13], x[30])
    CNOT | (x[29], x[13])
    CNOT | (x[21], x[29])
    CNOT | (x[5], x[21])

    # x04 = x04 + x23
    # x20 = x20 + x04
    # x23 = x23 + x22
    # x22 = x22 + x30
    # x23 = x23 + x07
    # x22 = x22 + x06

    CNOT | (x[23], x[4])
    CNOT | (x[4], x[20])
    CNOT | (x[22], x[23])
    CNOT | (x[30], x[22])
    CNOT | (x[7], x[23])
    CNOT | (x[6], x[22])

    # x31 = x31 + x23
    # x15 = x15 + x31
    # x30 = x30 + x14

    CNOT | (x[23], x[31])
    CNOT | (x[31], x[15])
    CNOT | (x[14], x[30])

    # x02, x18 = x18, x02
    # x20, x28 = x28, x20
    x[2], x[18] = logical_swap(eng, x[2], x[18])
    x[20], x[28] = logical_swap(eng, x[20], x[28])

    out_x = []
    for i in range(8):
        out_x.append(x[24 + i])
    for i in range(8):
        out_x.append(x[16 + i])
    for i in range(8):
        out_x.append(x[8 + i])
    for i in range(8):
        out_x.append(x[0 + i])


    return out_x

def XOR91(eng, x_in):

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

    y.append(x[12]) #4
    y.append(x[21]) #5
    y.append(x[30]) #6
    y.append(x[31]) #7

    y.append(x[24]) #8
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

def XOR98(eng, x_in):

    x = []
    for i in range(8):
        x.append(x_in[24 + i])
    for i in range(8):
        x.append(x_in[16 + i])
    for i in range(8):
        x.append(x_in[8 + i])
    for i in range(8):
        x.append(x_in[i])

    CNOT | (x[26], x[18])
    CNOT | (x[12], x[20])
    CNOT | (x[5], x[21])
    CNOT | (x[31], x[23])
    CNOT | (x[27], x[11])
    CNOT | (x[24], x[8])
    CNOT | (x[6], x[22])
    CNOT | (x[1], x[25])
    CNOT | (x[15], x[31])
    CNOT | (x[20], x[4])
    CNOT | (x[29], x[5])
    CNOT | (x[3], x[27])
    CNOT | (x[14], x[6])
    CNOT | (x[18], x[19])
    CNOT | (x[28], x[12])
    CNOT | (x[9], x[1])
    CNOT | (x[14], x[30])
    CNOT | (x[7], x[15])
    CNOT | (x[18], x[3])
    CNOT | (x[21], x[29])
    CNOT | (x[20], x[13])
    CNOT | (x[31], x[27])
    CNOT | (x[4], x[28])
    CNOT | (x[24], x[9])
    CNOT | (x[5], x[14])
    CNOT | (x[6], x[7])
    CNOT | (x[2], x[18])
    CNOT | (x[23], x[3])
    CNOT | (x[27], x[4])
    CNOT | (x[15], x[19])
    CNOT | (x[24], x[17])
    CNOT | (x[20], x[29])
    CNOT | (x[22], x[30])
    CNOT | (x[21], x[6])
    CNOT | (x[23], x[16])
    CNOT | (x[12], x[5])
    CNOT | (x[15], x[4])
    CNOT | (x[10], x[27])
    CNOT | (x[11], x[20])

    CNOT | (x[1], x[2])
    CNOT | (x[0], x[24])
    CNOT | (x[18], x[10])
    CNOT | (x[11], x[3])
    CNOT | (x[28], x[21])
    CNOT | (x[26], x[27])
    CNOT | (x[15], x[0])
    CNOT | (x[16], x[24])
    CNOT | (x[4], x[12])
    CNOT | (x[31], x[20])
    CNOT | (x[9], x[18])
    CNOT | (x[25], x[26])
    CNOT | (x[23], x[15])
    CNOT | (x[19], x[12])
    CNOT | (x[0], x[1])
    CNOT | (x[31], x[24])
    CNOT | (x[20], x[28])
    CNOT | (x[13], x[21])
    CNOT | (x[25], x[9])
    CNOT | (x[22], x[23])
    CNOT | (x[19], x[11])
    CNOT | (x[10], x[26])
    CNOT | (x[31], x[1])
    CNOT | (x[17], x[18])
    CNOT | (x[3], x[12])
    CNOT | (x[4], x[28])
    CNOT | (x[16], x[9])
    CNOT | (x[14], x[22])
    CNOT | (x[8], x[25])
    CNOT | (x[7], x[23])
    CNOT | (x[10], x[11])
    CNOT | (x[15], x[19])
    CNOT | (x[1], x[17])
    CNOT | (x[12], x[20])
    CNOT | (x[31], x[25])
    CNOT | (x[27], x[19])
    CNOT | (x[30], x[14])
    CNOT | (x[16], x[1])
    CNOT | (x[15], x[8])

    CNOT | (x[2], x[10])
    CNOT | (x[13], x[14])
    CNOT | (x[30], x[31])
    CNOT | (x[17], x[25])
    CNOT | (x[8], x[0])
    CNOT | (x[18], x[2])
    CNOT | (x[7], x[15])
    CNOT | (x[11], x[27])
    CNOT | (x[5], x[13])
    CNOT | (x[29], x[14])
    CNOT | (x[8], x[16])
    CNOT | (x[31], x[7])
    CNOT | (x[6], x[30])
    CNOT | (x[25], x[1])
    CNOT | (x[26], x[2])
    CNOT | (x[23], x[31])
    CNOT | (x[21], x[5])
    CNOT | (x[22], x[30])
    CNOT | (x[24], x[8])
    CNOT | (x[14], x[6])

    x_out = []

    x_out.append(x[16])
    x_out.append(x[25])
    x_out.append(x[10])
    x_out.append(x[11])

    x_out.append(x[28])
    x_out.append(x[5])
    x_out.append(x[6])
    x_out.append(x[15])

    x_out.append(x[24])
    x_out.append(x[1])
    x_out.append(x[18])
    x_out.append(x[19])

    x_out.append(x[12])
    x_out.append(x[29])
    x_out.append(x[14])
    x_out.append(x[23])

    x_out.append(x[0])
    x_out.append(x[9])
    x_out.append(x[2])
    x_out.append(x[3])

    x_out.append(x[20])
    x_out.append(x[13])
    x_out.append(x[30])
    x_out.append(x[7])

    x_out.append(x[8])
    x_out.append(x[17])
    x_out.append(x[26])
    x_out.append(x[27])

    x_out.append(x[4])
    x_out.append(x[21])
    x_out.append(x[22])
    x_out.append(x[31])

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

def XOR98_improving(eng, x_in):

    x = []
    for i in range(8):
        x.append(x_in[24 + i])
    for i in range(8):
        x.append(x_in[16 + i])
    for i in range(8):
        x.append(x_in[8 + i])
    for i in range(8):
        x.append(x_in[i])

    CNOT | (x[26], x[18])
    CNOT | (x[12], x[20])
    CNOT | (x[5], x[21])
    CNOT | (x[31], x[23])
    CNOT | (x[27], x[11])
    CNOT | (x[24], x[8])
    CNOT | (x[6], x[22])
    CNOT | (x[1], x[25])
    CNOT | (x[15], x[31])
    CNOT | (x[20], x[4])
    CNOT | (x[29], x[5])
    CNOT | (x[3], x[27])
    CNOT | (x[14], x[6])
    CNOT | (x[18], x[19])
    CNOT | (x[28], x[12])
    CNOT | (x[9], x[1])
    CNOT | (x[14], x[30])
    CNOT | (x[7], x[15])
    CNOT | (x[18], x[3])
    CNOT | (x[21], x[29])
    CNOT | (x[20], x[13])
    CNOT | (x[31], x[27])
    CNOT | (x[4], x[28])
    CNOT | (x[24], x[9])
    CNOT | (x[5], x[14])
    CNOT | (x[6], x[7])
    CNOT | (x[2], x[18])
    CNOT | (x[23], x[3])
    CNOT | (x[27], x[4])
    CNOT | (x[15], x[19])
    CNOT | (x[24], x[17])
    CNOT | (x[20], x[29])
    CNOT | (x[22], x[30])
    CNOT | (x[21], x[6])
    CNOT | (x[23], x[16])
    CNOT | (x[12], x[5])
    CNOT | (x[15], x[4])
    CNOT | (x[10], x[27])
    CNOT | (x[11], x[20])

    CNOT | (x[1], x[2])
    CNOT | (x[0], x[24])
    CNOT | (x[18], x[10])
    CNOT | (x[11], x[3])
    CNOT | (x[28], x[21])
    CNOT | (x[26], x[27])
    CNOT | (x[15], x[0])
    CNOT | (x[16], x[24])
    CNOT | (x[4], x[12])
    CNOT | (x[31], x[20])
    CNOT | (x[9], x[18])
    CNOT | (x[25], x[26])
    CNOT | (x[23], x[15])
    CNOT | (x[19], x[12])
    CNOT | (x[0], x[1])
    CNOT | (x[31], x[24])
    CNOT | (x[20], x[28])
    CNOT | (x[13], x[21])
    CNOT | (x[25], x[9])
    CNOT | (x[22], x[23])
    CNOT | (x[19], x[11])
    CNOT | (x[10], x[26])
    CNOT | (x[31], x[1])
    CNOT | (x[17], x[18])
    CNOT | (x[3], x[12])
    CNOT | (x[4], x[28])
    CNOT | (x[16], x[9])
    CNOT | (x[14], x[22])
    CNOT | (x[8], x[25])
    CNOT | (x[7], x[23])
    CNOT | (x[10], x[11])
    CNOT | (x[15], x[19])
    CNOT | (x[1], x[17])
    CNOT | (x[12], x[20])
    CNOT | (x[31], x[25])
    CNOT | (x[27], x[19])
    CNOT | (x[30], x[14])
    CNOT | (x[16], x[1])
    CNOT | (x[15], x[8])

    CNOT | (x[2], x[10])
    CNOT | (x[13], x[14])
    CNOT | (x[30], x[31])
    CNOT | (x[17], x[25])
    CNOT | (x[8], x[0])
    CNOT | (x[18], x[2])
    CNOT | (x[7], x[15])
    CNOT | (x[11], x[27])
    CNOT | (x[5], x[13])
    CNOT | (x[29], x[14])
    CNOT | (x[8], x[16])
    CNOT | (x[31], x[7])
    CNOT | (x[6], x[30])
    CNOT | (x[25], x[1])
    CNOT | (x[26], x[2])
    CNOT | (x[23], x[31])
    CNOT | (x[21], x[5])
    CNOT | (x[22], x[30])
    CNOT | (x[24], x[8])
    CNOT | (x[14], x[6])

    x_out = []

    x_out.append(x[16])
    x_out.append(x[25])
    x_out.append(x[10])
    x_out.append(x[11])

    x_out.append(x[28])
    x_out.append(x[5])
    x_out.append(x[6])
    x_out.append(x[15])

    x_out.append(x[24])
    x_out.append(x[1])
    x_out.append(x[18])
    x_out.append(x[19])

    x_out.append(x[12])
    x_out.append(x[29])
    x_out.append(x[14])
    x_out.append(x[23])

    x_out.append(x[0])
    x_out.append(x[9])
    x_out.append(x[2])
    x_out.append(x[3])

    x_out.append(x[20])
    x_out.append(x[13])
    x_out.append(x[30])
    x_out.append(x[7])

    x_out.append(x[8])
    x_out.append(x[17])
    x_out.append(x[26])
    x_out.append(x[27])

    x_out.append(x[4])
    x_out.append(x[21])
    x_out.append(x[22])
    x_out.append(x[31])

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

def asia_24_Mixcolumn(eng, x_in):
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

def asia_23_mc(eng, x_in):

    # Changing the index of qubits
    x = []
    for i in range(8):
        x.append(x_in[24 + i])
    for i in range(8):
        x.append(x_in[16 + i])
    for i in range(8):
        x.append(x_in[8 + i])
    for i in range(8):
        x.append(x_in[i])

    reverse_CNOT(eng, x[31], x[23])
    reverse_CNOT(eng, x[24], x[8])
    reverse_CNOT(eng, x[21], x[29])
    reverse_CNOT(eng, x[26], x[18])
    reverse_CNOT(eng, x[1], x[17])
    reverse_CNOT(eng, x[11], x[3])
    reverse_CNOT(eng, x[10], x[2])
    reverse_CNOT(eng, x[28], x[20])
    reverse_CNOT(eng, x[14], x[22])
    reverse_CNOT(eng, x[27], x[19])
    reverse_CNOT(eng, x[13], x[5])

    reverse_CNOT(eng, x[23], x[7])
    reverse_CNOT(eng, x[25], x[1])
    reverse_CNOT(eng, x[22], x[6])
    reverse_CNOT(eng, x[20], x[4])
    reverse_CNOT(eng, x[17], x[9])
    reverse_CNOT(eng, x[29], x[13])
    reverse_CNOT(eng, x[12], x[28])

    reverse_CNOT(eng, x[7], x[15])
    reverse_CNOT(eng, x[8], x[23])
    reverse_CNOT(eng, x[9], x[25])
    reverse_CNOT(eng, x[4], x[12])
    reverse_CNOT(eng, x[6], x[13])
    reverse_CNOT(eng, x[2], x[17])
    reverse_CNOT(eng, x[5], x[28])

    reverse_CNOT(eng, x[25], x[8])
    reverse_CNOT(eng, x[16], x[7])
    reverse_CNOT(eng, x[12], x[11])
    reverse_CNOT(eng, x[30], x[13])
    reverse_CNOT(eng, x[15], x[14])
    reverse_CNOT(eng, x[29], x[28])
    reverse_CNOT(eng, x[17], x[23])

    reverse_CNOT(eng, x[8], x[0])
    reverse_CNOT(eng, x[11], x[27])
    reverse_CNOT(eng, x[13], x[21])
    reverse_CNOT(eng, x[30], x[14])
    reverse_CNOT(eng, x[18], x[17])
    reverse_CNOT(eng, x[28], x[23])

    reverse_CNOT(eng, x[0], x[31])
    reverse_CNOT(eng, x[14], x[5])
    reverse_CNOT(eng, x[27], x[2])
    reverse_CNOT(eng, x[21], x[20])
    reverse_CNOT(eng, x[28], x[19])
    reverse_CNOT(eng, x[17], x[24])

    reverse_CNOT(eng, x[0], x[24])
    reverse_CNOT(eng, x[14], x[29])
    reverse_CNOT(eng, x[27], x[18])
    reverse_CNOT(eng, x[20], x[12])
    reverse_CNOT(eng, x[2], x[26])
    reverse_CNOT(eng, x[28], x[3])
    reverse_CNOT(eng, x[5], x[4])

    reverse_CNOT(eng, x[18], x[23])
    reverse_CNOT(eng, x[20], x[11])
    reverse_CNOT(eng, x[19], x[26])
    reverse_CNOT(eng, x[3], x[10])
    reverse_CNOT(eng, x[12], x[7])
    reverse_CNOT(eng, x[24], x[16])

    reverse_CNOT(eng, x[23], x[30])
    reverse_CNOT(eng, x[26], x[1])
    reverse_CNOT(eng, x[18], x[10])
    reverse_CNOT(eng, x[3], x[7])
    reverse_CNOT(eng, x[20], x[31])
    reverse_CNOT(eng, x[4], x[12])

    reverse_CNOT(eng, x[23], x[15])
    reverse_CNOT(eng, x[18], x[9])
    reverse_CNOT(eng, x[10], x[1])
    reverse_CNOT(eng, x[7], x[31])
    reverse_CNOT(eng, x[4], x[28])

    reverse_CNOT(eng, x[23], x[6])
    reverse_CNOT(eng, x[1], x[25])
    reverse_CNOT(eng, x[19], x[31])
    reverse_CNOT(eng, x[17], x[7])
    reverse_CNOT(eng, x[10], x[2])
    reverse_CNOT(eng, x[28], x[20])
    reverse_CNOT(eng, x[26], x[18])

    reverse_CNOT(eng, x[31], x[22])
    reverse_CNOT(eng, x[25], x[16])
    reverse_CNOT(eng, x[6], x[14])
    reverse_CNOT(eng, x[19], x[11])
    reverse_CNOT(eng, x[1], x[0])

    reverse_CNOT(eng, x[22], x[13])
    reverse_CNOT(eng, x[16], x[7])
    reverse_CNOT(eng, x[11], x[3])
    reverse_CNOT(eng, x[9], x[1])

    reverse_CNOT(eng, x[22], x[30])
    reverse_CNOT(eng, x[13], x[5])
    reverse_CNOT(eng, x[7], x[15])
    reverse_CNOT(eng, x[16], x[8])
    reverse_CNOT(eng, x[3], x[27])
    reverse_CNOT(eng, x[1], x[17])

    reverse_CNOT(eng, x[14], x[22])
    reverse_CNOT(eng, x[5], x[21])
    reverse_CNOT(eng, x[15], x[31])
    reverse_CNOT(eng, x[27], x[19])
    reverse_CNOT(eng, x[8], x[24])
    reverse_CNOT(eng, x[17], x[25])

    reverse_CNOT(eng, x[31], x[23])
    reverse_CNOT(eng, x[21], x[29])

    x_out = []
    x_out.append(x[24])
    x_out.append(x[1])
    x_out.append(x[10])
    x_out.append(x[11])
    x_out.append(x[12])
    x_out.append(x[13])
    x_out.append(x[30])
    x_out.append(x[15])
    x_out.append(x[8])
    x_out.append(x[25])
    x_out.append(x[2])
    x_out.append(x[3])
    x_out.append(x[4])
    x_out.append(x[5])
    x_out.append(x[14])
    x_out.append(x[7])
    x_out.append(x[0])
    x_out.append(x[17])
    x_out.append(x[26])
    x_out.append(x[19])
    x_out.append(x[20])
    x_out.append(x[29])
    x_out.append(x[22])
    x_out.append(x[31])
    x_out.append(x[16])
    x_out.append(x[9])
    x_out.append(x[18])
    x_out.append(x[27])
    x_out.append(x[28])
    x_out.append(x[21])
    x_out.append(x[6])
    x_out.append(x[23])

    y_out = []
    for i in range(8):
        y_out.append(x_out[24 + i])
    for i in range(8):
        y_out.append(x_out[16 + i])
    for i in range(8):
        y_out.append(x_out[8 + i])
    for i in range(8):
        y_out.append(x_out[0 + i])

    return y_out

def AES_102xor_2023(eng, x_in):

    t_in = eng.allocate_qureg(109)
    x_out = []
    t = []

    for i in range(8):
        t.append(x_in[24 + i])
    for i in range(8):
        t.append(x_in[16 + i])
    for i in range(8):
        t.append(x_in[8 + i])
    for i in range(8):
        t.append(x_in[i])

    for i in range(109):
        t.append(t_in[i])

    CNOT2(eng, t[140], t[18], t[9])
    CNOT2(eng, t[32], t[5], t[13])
    CNOT2(eng, t[33], t[21], t[29])
    CNOT2(eng, t[34], t[15], t[30])
    CNOT2(eng, t[35], t[7], t[16])
    CNOT2(eng, t[36], t[23], t[24])
    CNOT2(eng, t[37], t[1], t[18])
    CNOT2(eng, t[38], t[17], t[26])
    CNOT2(eng, t[137], t[38], t[140])
    CNOT2(eng, t[39], t[6], t[22])
    CNOT2(eng, t[40], t[39], t[33])
    CNOT2(eng, t[41], t[14], t[31])
    CNOT2(eng, t[42], t[41], t[39])
    CNOT2(eng, t[43], t[7], t[15])
    CNOT2(eng, t[44], t[43], t[41])
    CNOT2(eng, t[45], t[0], t[17])
    CNOT2(eng, t[46], t[7], t[45])
    CNOT2(eng, t[47], t[6], t[23])
    CNOT2(eng, t[48], t[7], t[47])
    CNOT2(eng, t[49], t[48], t[44])
    CNOT2(eng, t[50], t[42], t[48])
    CNOT2(eng, t[51], t[34], t[48])
    CNOT2(eng, t[52], t[12], t[28])
    CNOT2(eng, t[53], t[3], t[7])
    CNOT2(eng, t[54], t[52], t[53])
    CNOT2(eng, t[55], t[13], t[29])
    CNOT2(eng, t[56], t[52], t[55])
    CNOT2(eng, t[57], t[30], t[55])
    CNOT2(eng, t[58], t[57], t[40])
    CNOT2(eng, t[59], t[14], t[22])
    CNOT2(eng, t[60], t[59], t[30])
    CNOT2(eng, t[61], t[32], t[60])
    CNOT2(eng, t[62], t[40], t[60])
    CNOT2(eng, t[63], t[44], t[60])
    CNOT2(eng, t[64], t[4], t[20])
    CNOT2(eng, t[65], t[64], t[53])
    CNOT2(eng, t[66], t[12], t[20])
    CNOT2(eng, t[67], t[5], t[66])
    CNOT2(eng, t[68], t[33], t[67])
    CNOT2(eng, t[69], t[67], t[56])
    CNOT2(eng, t[70], t[14], t[21])
    CNOT2(eng, t[71], t[5], t[70])
    CNOT2(eng, t[72], t[71], t[40])
    CNOT2(eng, t[73], t[18], t[23])
    CNOT2(eng, t[74], t[11], t[27])
    CNOT2(eng, t[75], t[73], t[74])
    CNOT2(eng, t[76], t[3], t[19])
    CNOT2(eng, t[77], t[73], t[76])
    CNOT2(eng, t[78], t[16], t[23])
    CNOT2(eng, t[79], t[78], t[25])
    CNOT2(eng, t[80], t[0], t[8])
    CNOT2(eng, t[81], t[31], t[80])
    CNOT2(eng, t[82], t[81], t[36])
    CNOT2(eng, t[83], t[81], t[35])
    CNOT2(eng, t[84], t[78], t[80])
    CNOT2(eng, t[85], t[2], t[10])
    CNOT2(eng, t[86], t[85], t[25])
    CNOT2(eng, t[87], t[86], t[38])
    CNOT2(eng, t[88], t[86], t[37])
    CNOT2(eng, t[89], t[3], t[26])
    CNOT2(eng, t[90], t[89], t[31])
    CNOT2(eng, t[91], t[75], t[90])
    CNOT2(eng, t[92], t[12], t[27])
    CNOT2(eng, t[93], t[92], t[31])
    CNOT2(eng, t[94], t[65], t[93])
    CNOT2(eng, t[95], t[8], t[15])
    CNOT2(eng, t[96], t[24], t[95])
    CNOT2(eng, t[97], t[96], t[35])
    CNOT2(eng, t[98], t[84], t[96])
    CNOT2(eng, t[99], t[9], t[25])
    CNOT2(eng, t[100], t[95], t[99])
    CNOT2(eng, t[101], t[100], t[46])
    CNOT2(eng, t[102], t[1], t[17])
    CNOT2(eng, t[138], t[10], t[102])
    CNOT2(eng, t[103], t[95], t[102])
    CNOT2(eng, t[104], t[103], t[79])
    CNOT2(eng, t[105], t[4], t[28])
    CNOT2(eng, t[106], t[105], t[21])
    CNOT2(eng, t[107], t[56], t[106])
    CNOT2(eng, t[108], t[32], t[106])
    CNOT2(eng, t[109], t[19], t[23])
    CNOT2(eng, t[110], t[105], t[109])
    CNOT2(eng, t[111], t[110], t[93])
    CNOT2(eng, t[114], t[137], t[138])
    CNOT2(eng, t[117], t[2], t[137])
    CNOT2(eng, t[118], t[10], t[27])
    CNOT2(eng, t[119], t[15], t[118])
    CNOT2(eng, t[120], t[77], t[119])
    CNOT2(eng, t[121], t[11], t[20])
    CNOT2(eng, t[122], t[15], t[121])
    CNOT2(eng, t[123], t[54], t[122])
    CNOT2(eng, t[124], t[110], t[122])
    CNOT2(eng, t[125], t[11], t[19])
    CNOT2(eng, t[126], t[2], t[7])
    CNOT2(eng, t[127], t[125], t[126])
    CNOT2(eng, t[128], t[127], t[119])
    CNOT2(eng, t[129], t[127], t[90])
    CNOT2(eng, t[130], t[9], t[31])
    CNOT2(eng, t[131], t[1], t[24])
    CNOT2(eng, t[132], t[130], t[131])
    CNOT2(eng, t[133], t[132], t[79])
    CNOT2(eng, t[134], t[132], t[46])

    x_out.append(t[97]);
    x_out.append(t[101])
    x_out.append(t[114]);
    x_out.append(t[128])
    x_out.append(t[123]);
    x_out.append(t[107])
    x_out.append(t[61]);
    x_out.append(t[49])

    x_out.append(t[98]);
    x_out.append(t[104])
    x_out.append(t[117]);
    x_out.append(t[120])
    x_out.append(t[124]);
    x_out.append(t[68])
    x_out.append(t[58]);
    x_out.append(t[50])

    x_out.append(t[82]);
    x_out.append(t[133])
    x_out.append(t[87]);
    x_out.append(t[91])
    x_out.append(t[111]);
    x_out.append(t[69])
    x_out.append(t[62]);
    x_out.append(t[63])

    x_out.append(t[83]);
    x_out.append(t[134])
    x_out.append(t[88]);
    x_out.append(t[129])
    x_out.append(t[94]);
    x_out.append(t[108])
    x_out.append(t[72]);
    x_out.append(t[51])

    y_out = []
    for i in range(8):
        y_out.append(x_out[24 + i])
    for i in range(8):
        y_out.append(x_out[16 + i])
    for i in range(8):
        y_out.append(x_out[8 + i])
    for i in range(8):
        y_out.append(x_out[0 + i])

    return y_out

def AES_97xor(eng, x_in, y):

    t = eng.allocate_qureg(100)
    x = []
    for i in range(8):
        x.append(x_in[24 + i])
    for i in range(8):
        x.append(x_in[16 + i])
    for i in range(8):
        x.append(x_in[8 + i])
    for i in range(8):
        x.append(x_in[0 + i])

    CNOT2(eng, t[0] , x[7] , x[15])
    CNOT2(eng, t[1] , x[23] , x[31])
    CNOT2(eng, t[2] , x[7] , x[31])
    CNOT2(eng, t[3] , x[15] , x[23])
    CNOT2(eng, t[4] , x[0] , x[8])
    CNOT2(eng, t[5] , x[6] , x[14])
    CNOT2(eng, t[6] , x[5] , x[29])
    CNOT2(eng, t[7] , x[16] , x[24])
    CNOT2(eng, t[8] , x[22] , x[30])
    CNOT2(eng, t[9] , x[13] , x[21])
    CNOT2(eng, t[10] , x[1] , x[9])
    CNOT2(eng, t[11], x[10] , x[18])
    CNOT2(eng, t[12] , x[2] , x[26])
    CNOT2(eng, t[13] , x[17] , x[25])
    CNOT2(eng, t[14] , x[4] , x[12])
    CNOT2(eng, t[15] , x[3] , x[27])
    CNOT2(eng, t[16] , x[20] , x[28])
    CNOT2(eng, t[17] , x[11] , x[19])
    CNOT2(eng, t[18] , x[0] , t[3])
    CNOT2(eng, y[8] , t[7] , t[18])
    CNOT2(eng, t[20] , x[16] , t[4])
    CNOT2(eng, y[24] , t[2] , t[20])
    CNOT2(eng, t[22] , t[1] , t[7])
    CNOT2(eng, y[16] , t[20] , t[22])
    CNOT2(eng, t[24] , x[8] , t[7])
    CNOT2(eng, y[0] , t[0], t[24])
    CNOT2(eng, t[26] , x[6] , t[8])
    CNOT2(eng, y[14] , t[9] , t[26])
    CNOT2(eng, t[28] , x[7] , x[22])
    CNOT2(eng, t[29] , x[21] , t[5])
    CNOT2(eng, t[30] , x[5] , y[14])
    CNOT2(eng, y[6] , t[29] , t[30])
    CNOT2(eng, t[32] , x[10] , t[12])
    CNOT2(eng, y[18] , t[13] , t[32])
    CNOT2(eng, t[34] , x[25] , t[11])
    CNOT2(eng, t[35] , x[1] , x[2])
    CNOT2(eng, y[26] , t[34] , t[35])
    CNOT2(eng, t[37] , x[9] , y[18])
    CNOT2(eng, y[10] , t[34] , t[37])
    CNOT2(eng, t[39] , t[0] , t[32])
    CNOT2(eng, t[40] , x[13] , t[6])
    CNOT2(eng, y[21] , t[16] , t[40])
    CNOT2(eng, t[42] , x[28] , t[9])
    CNOT2(eng, t[43] , x[4] , x[5])
    CNOT2(eng, y[29] , t[42] , t[43])
    CNOT2(eng, t[45] , x[12] , y[21])
    CNOT2(eng, y[13] , t[42] , t[45])
    CNOT2(eng, t[47] , x[14] , t[1])
    CNOT2(eng, y[15] , t[28] , t[47])
    CNOT2(eng, t[49] , x[6] , x[15])
    CNOT2(eng, y[7] , t[47] , t[49])
    CNOT2(eng, t[51] , x[15] , t[2])
    CNOT2(eng, y[23] , t[8] , t[51])
    CNOT2(eng, t[53] , x[22] , t[5])
    CNOT2(eng, y[30] , t[6] , t[53])
    CNOT2(eng, t[55] , x[25] , t[10])
    CNOT2(eng, y[17] , t[22] , t[55])
    CNOT2(eng, t[57] , x[26] , t[10])
    CNOT2(eng, y[2] , t[11] , t[57])
    CNOT2(eng, t[59] , x[29] , x[30])
    CNOT2(eng, y[22] , t[29] , t[59])
    CNOT2(eng, t[61] , x[29] , t[9])
    CNOT2(eng, y[5] , t[14] , t[61])
    CNOT2(eng, t[63] , t[3] , t[26])
    CNOT2(eng, y[31] , t[28] , t[63])
    CNOT2(eng, t[65] , t[4] , t[37])
    CNOT2(eng, y[1] , t[39] , t[65])
    CNOT2(eng, t[67] , x[1] , t[13])
    CNOT2(eng, t[68] , t[18] , t[20])
    CNOT2(eng, y[9] , t[67] , t[68])
    CNOT2(eng, t[70] , x[3] , t[2])
    CNOT2(eng, t[71] , x[27] , t[14])
    CNOT2(eng, t[72] , x[20] , t[70])
    CNOT2(eng, y[28] , t[71] , t[72])
    CNOT2(eng, t[74] , t[12] , t[17])
    CNOT2(eng, y[27] , t[70] , t[74])
    CNOT2(eng, t[76] , x[2] , x[27])
    CNOT2(eng, t[77] , t[39] , t[74])
    CNOT2(eng, y[3] , t[76] , t[77])
    CNOT2(eng, t[79] , t[3] , t[11])
    CNOT2(eng, t[80] , x[19] , t[15])
    CNOT2(eng, y[11] , t[79] , t[80])
    CNOT2(eng, t[82] , x[4] , t[3])
    CNOT2(eng, t[83] , t[16] , t[17])
    CNOT2(eng, y[12] , t[82] , t[83])
    CNOT2(eng, t[85] , x[19] , t[1])
    CNOT2(eng, t[86] , x[28] , t[71])
    CNOT2(eng, y[20] , t[85] , t[86])
    CNOT2(eng, t[88] , x[9] , y[17])
    CNOT2(eng, t[89] , y[1] , t[68])
    CNOT2(eng, y[25] , t[88] , t[89])
    CNOT2(eng, t[91] , x[11] , y[27])
    CNOT2(eng, t[92] , y[3] , t[79])
    CNOT2(eng, y[19] , t[91] , t[92])
    CNOT2(eng, t[94] , t[14] , t[70])
    CNOT2(eng, t[95] , y[12] , t[85])
    CNOT2(eng, y[4] , t[94] , t[95])

    out = []
    for i in range(8):
        out.append(y[24 + i])
    for i in range(8):
        out.append(y[16 + i])
    for i in range(8):
        out.append(y[8 + i])
    for i in range(8):
        out.append(y[0 + i])

    return out

def Mixcolumns(eng, x_in):

    # Changing the index of qubits
    x = []
    for i in range(8):
        x.append(x_in[24 + i])
    for i in range(8):
        x.append(x_in[16 + i])
    for i in range(8):
        x.append(x_in[8 + i])
    for i in range(8):
        x.append(x_in[i])

    CNOT | (x[31], x[23]); CNOT | (x[15], x[31])
    CNOT | (x[4], x[12]); CNOT | (x[21], x[13])
    CNOT | (x[9], x[17]); CNOT | (x[27], x[11])
    CNOT | (x[28], x[4]); CNOT | (x[5], x[21])
    CNOT | (x[24], x[0]); CNOT | (x[7], x[15])
    CNOT | (x[1], x[9]); CNOT | (x[6], x[14])
    CNOT | (x[16], x[24]); CNOT | (x[22], x[6])
    CNOT | (x[31], x[16]); CNOT | (x[8], x[24])
    CNOT | (x[26], x[18]); CNOT | (x[30], x[22])
    CNOT | (x[10], x[26]); CNOT | (x[23], x[8])
    CNOT | (x[13], x[30]); CNOT | (x[29], x[13])
    CNOT | (x[13], x[5]); CNOT | (x[4], x[29])
    CNOT | (x[11], x[4]); CNOT | (x[19], x[11])

    CNOT | (x[12], x[13]); CNOT | (x[23], x[19])
    CNOT | (x[31], x[4]); CNOT | (x[20], x[12])
    CNOT | (x[12], x[28]); CNOT | (x[27], x[20])
    CNOT | (x[19], x[20]); CNOT | (x[31], x[27])
    CNOT | (x[15], x[12]); CNOT | (x[3], x[27])
    CNOT | (x[11], x[3]); CNOT | (x[2], x[11])
    CNOT | (x[18], x[19]); CNOT | (x[10], x[11])
    CNOT | (x[18], x[10]); CNOT | (x[2], x[18])
    CNOT | (x[9], x[10]); CNOT | (x[9], x[2])
    CNOT | (x[17], x[18]); CNOT | (x[25], x[17])
    CNOT | (x[17], x[1]); CNOT | (x[24], x[25])
    CNOT | (x[8], x[9]); CNOT | (x[15], x[24])
    CNOT | (x[15], x[11]); CNOT | (x[0], x[8])
    CNOT | (x[23], x[15]); CNOT | (x[16], x[17])
    CNOT | (x[0], x[16]); CNOT | (x[31], x[0])
    CNOT | (x[23], x[16]); CNOT | (x[6], x[23])
    CNOT | (x[7], x[31]); CNOT | (x[22], x[31])
    CNOT | (x[6], x[30]); CNOT | (x[14], x[7])
    CNOT | (x[21], x[14]); CNOT | (x[5], x[6])
    CNOT | (x[21], x[22]); CNOT | (x[29], x[5])
    CNOT | (x[28], x[21]); CNOT | (x[21], x[29])
    CNOT | (x[13], x[21]); CNOT | (x[27], x[12])
    CNOT | (x[26], x[27]); CNOT | (x[20], x[28])

    CNOT | (x[4], x[20]); CNOT | (x[1], x[26])
    CNOT | (x[30], x[14]); CNOT | (x[12], x[4])
    CNOT | (x[19], x[3]); CNOT | (x[27], x[19])
    CNOT | (x[25], x[1]); CNOT | (x[24], x[0])
    CNOT | (x[0], x[1]); CNOT | (x[26], x[2])

    CNOT | (x[9], x[25]); CNOT | (x[7], x[15])
    CNOT | (x[23], x[7]); CNOT | (x[14], x[6])
    CNOT | (x[17], x[9]); CNOT | (x[31], x[23])
    CNOT | (x[18], x[26]); CNOT | (x[6], x[22])
    CNOT | (x[0], x[17]); CNOT | (x[11], x[27])

    x_out = []
    x_out.append(x[0]); x_out.append(x[1])
    x_out.append(x[26]); x_out.append(x[27])
    x_out.append(x[12]); x_out.append(x[5])
    x_out.append(x[22]); x_out.append(x[23])

    x_out.append(x[8]); x_out.append(x[25])
    x_out.append(x[2]); x_out.append(x[3])
    x_out.append(x[28]); x_out.append(x[21])
    x_out.append(x[6]); x_out.append(x[31])

    x_out.append(x[16]); x_out.append(x[9])
    x_out.append(x[18]); x_out.append(x[19])
    x_out.append(x[20]); x_out.append(x[29])
    x_out.append(x[30]); x_out.append(x[7])

    x_out.append(x[24]); x_out.append(x[17])
    x_out.append(x[10]); x_out.append(x[11])
    x_out.append(x[4]); x_out.append(x[13])
    x_out.append(x[14]); x_out.append(x[15])

    return x_out

def XOR94(eng, x_in, y):

    t = eng.allocate_qureg(100)
    x= []
    for i in range(32):
        x.append(x_in[31 - i])

    CNOT2(eng, t[0], x[8], x[16])
    CNOT2(eng, t[1], x[7], x[31])
    CNOT2(eng, t[2], x[23], t[0])
    CNOT2(eng,y[15], t[1], t[2])
    CNOT2(eng,t[4], x[16], x[24])
    CNOT2(eng,t[5], x[15], t[4])
    CNOT2(eng,y[23], t[1], t[5])
    CNOT2(eng,t[7], x[1], x[25])
    CNOT2(eng,t[8], x[0], t[0])
    CNOT2(eng,y[24], t[7], t[8])
    CNOT2(eng,t[10], x[10], x[18])
    CNOT2(eng,t[11], x[17], t[10])
    CNOT2(eng,y[9], t[7], t[11])
    CNOT2(eng,t[13], x[3], x[27])
    CNOT2(eng,t[14], x[2], t[13])
    CNOT2(eng,y[26], t[10], t[14])
    CNOT2(eng,t[16], x[1], x[9])
    CNOT2(eng,t[17], x[8], t[16])
    CNOT2(eng,y[0], t[4], t[17])
    CNOT2(eng,t[19], x[18], x[26])
    CNOT2(eng,t[20], x[25], t[19])
    CNOT2(eng,y[17], t[16], t[20])
    CNOT2(eng,t[22], x[11], x[19])
    CNOT2(eng,t[23], x[2], t[19])
    CNOT2(eng,y[10], t[22], t[23])
    CNOT2(eng,t[25], x[11], t[10])
    CNOT2(eng,t[26], x[3], t[25])
    CNOT2(eng,y[2], x[26], t[26])
    CNOT2(eng,t[28], x[27], y[10])
    CNOT2(eng,y[18], t[25], t[28])
    CNOT2(eng,t[30], x[26], t[16])
    CNOT2(eng,t[31], y[9], t[23])

    CNOT2(eng,y[1], t[30], t[31])
    CNOT2(eng,t[33], x[2], t[30])
    CNOT2(eng,y[25], x[17], t[33])
    CNOT2(eng,t[35], x[17], t[4])
    CNOT2(eng,t[36], x[1], t[35])
    CNOT2(eng,y[16], y[24], t[36])
    CNOT2(eng,t[38], x[0], t[16])
    CNOT2(eng,y[8], t[36], t[38])
    CNOT2(eng,t[40], x[0], x[8])
    CNOT2(eng,t[41], x[31], t[40])
    CNOT2(eng,t[42], x[15], t[41])
    CNOT2(eng,y[7], x[23], t[42])
    CNOT2(eng,t[44], y[15], t[41])
    CNOT2(eng,y[31], t[5], t[44])
    CNOT2(eng,t[46], x[14], x[22])
    CNOT2(eng,t[47], x[21], x[29])
    CNOT2(eng,t[48], x[5], t[46])
    CNOT2(eng,y[13], t[47], t[48])
    CNOT2(eng,t[50], t[1], t[46])
    CNOT2(eng,t[51], x[30], t[42])
    CNOT2(eng,y[6], t[50], t[51])
    CNOT2(eng,t[53], x[6], x[14])
    CNOT2(eng,t[54], t[47], t[53])
    CNOT2(eng,y[5], x[13], t[54])
    CNOT2(eng,t[56], y[6], t[53])
    CNOT2(eng,y[14], t[44], t[56])
    CNOT2(eng,t[58], x[0], x[24])
    CNOT2(eng,t[59], x[6], t[50])
    CNOT2(eng,y[30], t[58], t[59])
    CNOT2(eng,t[61], x[22], x[30])
    CNOT2(eng,t[62], t[44], y[30])

    CNOT2(eng, y[22], t[61], t[62])
    CNOT2(eng,t[64], x[5], x[29])
    CNOT2(eng,t[65], t[61], t[64])
    CNOT2(eng,y[21], x[13], t[65])
    CNOT2(eng,t[67], t[46], t[65])
    CNOT2(eng,y[29], y[5], t[67])
    CNOT2(eng, t[69], x[4], x[12])
    CNOT2(eng, t[70], x[28], t[4])
    CNOT2(eng,t[71], t[47], t[69])
    CNOT2(eng, y[20], t[70], t[71])
    CNOT2(eng,t[73], x[20], t[13])
    CNOT2(eng,t[74], x[11], t[70])
    CNOT2(eng,y[19], t[73], t[74])
    CNOT2(eng,t[76], t[58], t[64])
    CNOT2(eng, t[77], t[69], t[76])
    CNOT2(eng, y[28], x[20], t[77])
    CNOT2(eng,t[79], x[12], t[0])
    CNOT2(eng,t[80], x[19], t[79])
    CNOT2(eng,y[11], t[73], t[80])
    CNOT2(eng,t[82], t[40], t[69])
    CNOT2(eng,t[83], t[28], t[82])
    CNOT2(eng,y[3], t[23], t[83])
    CNOT2(eng,t[85], x[3], y[19])
    CNOT2(eng, t[86], y[11], t[85])
    CNOT2(eng, y[27], t[82], t[86])
    CNOT2(eng,t[88], y[28], t[79])
    CNOT2(eng,t[89], x[13], t[88])
    CNOT2(eng,t[90], x[21], t[89])
    CNOT2(eng, y[4], y[20], t[90])
    CNOT2(eng, t[92], x[28], t[90])
    CNOT2(eng,y[12], t[76], t[92])

    y_out = []
    for i in range(32):
        y_out.append(y[31-i])

    return y_out

def XOR105_newnew(eng, x_in):
    y = eng.allocate_qureg(32)
    t = eng.allocate_qureg(120)
    x = []
    for i in range(8):
        x.append(x_in[24 + i])
    for i in range(8):
        x.append(x_in[16 + i])
    for i in range(8):
        x.append(x_in[8 + i])
    for i in range(8):
        x.append(x_in[i])

    CNOT2(eng, t[1], x[7], x[15])
    CNOT2(eng, t[2], x[23], x[31])
    CNOT2(eng, t[3], x[7], x[31])
    CNOT2(eng, t[4], x[15], x[23])
    CNOT2(eng, t[5], x[0], x[8])
    CNOT2(eng, t[6], x[6], x[14])
    CNOT2(eng, t[7], x[5], x[29])
    CNOT2(eng, t[8], x[16], x[24])
    CNOT2(eng, t[9], x[22], x[30])
    CNOT2(eng, t[10], x[13], x[21])
    CNOT2(eng, t[11], x[1], x[9])
    CNOT2(eng, t[12], x[10], x[18])
    CNOT2(eng, t[13], x[2], x[26])
    CNOT2(eng, t[14], x[17], x[25])
    CNOT2(eng, t[15], x[4], x[12])
    CNOT2(eng, t[16], x[3], x[27])
    CNOT2(eng, t[17], x[20], x[28])
    CNOT2(eng, t[18], x[11], x[19])
    CNOT2(eng, t[19], x[0], t[4])
    CNOT2(eng, t[20], t[8], t[19]) # y8  (3)
    CNOT2(eng, t[21], x[6], t[9])
    CNOT2(eng, t[22], t[10], t[21])  # y14  (3)
    CNOT2(eng, t[23], x[7], x[22])
    CNOT2(eng, t[24], x[8], t[1])
    CNOT2(eng, t[25], t[8], t[24])  # y0  (3)
    CNOT2(eng, t[26], x[10], t[13])
    CNOT2(eng, t[27], t[14], t[26])  # y18  (3)
    CNOT2(eng, t[28], x[13], t[7])
    CNOT2(eng, t[29], t[17], t[28])  # y21  (3)
    CNOT2(eng, t[30], x[14], t[2])
    CNOT2(eng, t[31], t[23], t[30])  # y15  (3)
    CNOT2(eng, t[32], x[6], x[15])
    CNOT2(eng, t[33], t[30], t[32])  # y7  (3)
    CNOT2(eng, t[34], x[15], t[3])
    CNOT2(eng, t[35], t[9], t[34])
    CNOT2(eng, t[36], x[16], t[3])
    CNOT2(eng, t[37], t[5], t[36])
    CNOT2(eng, t[38], x[22], t[6])
    CNOT2(eng, t[39], t[7], t[38])
    CNOT2(eng, t[40], x[24], t[2])
    CNOT2(eng, t[41], t[5], t[40])  # y16  (3)
    CNOT2(eng, t[42], x[26], t[11])
    CNOT2(eng, t[43], t[12], t[42])  # y2  (3)
    CNOT2(eng, t[44], x[29], t[10])
    CNOT2(eng, t[45], t[15], t[44])  # y5  (3)
    CNOT2(eng, t[46], t[4], t[23])
    CNOT2(eng, t[47], t[21], t[46])  # y31  (3)
    CNOT2(eng, t[48], x[0], x[9])
    CNOT2(eng, t[49], t[14], t[48])
    CNOT2(eng, t[50], t[24], t[49])  # y1  (3)
    CNOT2(eng, t[51], x[1], x[2])
    CNOT2(eng, t[52], x[25], t[12])
    CNOT2(eng, t[53], t[51], t[52])  # y26  (3)
    CNOT2(eng, t[54], x[3], t[3])
    CNOT2(eng, t[55], t[13], t[18])
    CNOT2(eng, t[56], t[54], t[55])  # y27  (3)
    CNOT2(eng, t[57], x[4], x[5])
    CNOT2(eng, t[58], x[28], t[10])
    CNOT2(eng, t[59], t[57], t[58])  # y29  (3)
    CNOT2(eng, t[60], x[4], t[4])
    CNOT2(eng, t[61], t[17], t[18])
    CNOT2(eng, t[62], t[60], t[61])  # y12  (3)
    CNOT2(eng, t[63], x[5], x[13])
    CNOT2(eng, t[64], x[14], t[9])
    CNOT2(eng, t[65], t[63], t[64])  # y6  (3)
    CNOT2(eng, t[66], x[9], x[17])
    CNOT2(eng, t[67], x[18], t[13])
    CNOT2(eng, t[68], t[66], t[67])  # y10  (3)
    CNOT2(eng, t[69], x[12], x[20])
    CNOT2(eng, t[70], x[21], t[7])
    CNOT2(eng, t[71], t[69], t[70])  # y13  (3)
    CNOT2(eng, t[72], x[4], x[27])
    CNOT2(eng, t[73], t[69], t[72])
    CNOT2(eng, t[74], t[54], t[73])  # y28  (3)
    CNOT2(eng, t[75], x[5], x[30])
    CNOT2(eng, t[76], t[6], t[75])
    CNOT2(eng, t[77], t[70], t[76])  # y22  (3)
    CNOT2(eng, t[78], x[16], x[25])
    CNOT2(eng, t[79], x[1], x[17])
    CNOT2(eng, t[80], t[11], t[78])
    CNOT2(eng, t[81], t[40], t[80])  # y17  (3)
    CNOT2(eng, t[82], x[8], t[4])
    CNOT2(eng, t[83], t[78], t[79])
    CNOT2(eng, t[84], t[82], t[83])  # y9  (3)
    CNOT2(eng, t[85], x[19], t[4])
    CNOT2(eng, t[86], t[12], t[16])
    CNOT2(eng, t[87], t[85], t[86])  # y11  (3)
    CNOT2(eng, t[88], x[24], t[3])
    CNOT2(eng, t[89], t[48], t[79])
    CNOT2(eng, t[90], t[88], t[89])  # y25  (3)
    CNOT2(eng, t[91], x[2], x[10])
    CNOT2(eng, t[92], x[27], t[1])
    CNOT2(eng, t[93], t[18], t[91])
    CNOT2(eng, t[94], t[92], t[93])  # y3  (3)
    CNOT2(eng, t[95], x[3], x[11])
    CNOT2(eng, t[96], x[27], t[2])
    CNOT2(eng, t[97], x[12], t[1])
    CNOT2(eng, t[98], t[17], t[95])
    CNOT2(eng, t[99], t[97], t[98])  # y4  (3)
    CNOT2(eng, t[101], x[18], x[26])
    CNOT | (t[95], t[101])

    CNOT2(eng, t[102], t[96], t[101])  # y19  (3)
    CNOT2(eng, t[105], x[19], x[28])

    CNOT | (t[15], t[105])
    CNOT | (t[96], t[105])


    out = []

    out.append(t[37])
    out.append(t[90])
    out.append(t[53])
    out.append(t[56])

    out.append(t[74])
    out.append(t[59])
    out.append(t[39])
    out.append(t[47])

    out.append(t[41])
    out.append(t[81])
    out.append(t[27])
    out.append(t[102])

    out.append(t[105])
    out.append(t[29])
    out.append(t[77])
    out.append(t[35])

    out.append(t[20])
    out.append(t[84])
    out.append(t[68])
    out.append(t[87])

    out.append(t[62])
    out.append(t[71])
    out.append(t[22])
    out.append(t[31])

    out.append(t[25])
    out.append(t[50])
    out.append(t[43])
    out.append(t[94])

    out.append(t[99])
    out.append(t[45])
    out.append(t[65])
    out.append(t[33])

    return out

def zhu_eprint(eng, x_in):

    x = []
    for i in range(8):
        x.append(x_in[24 + i])
    for i in range(8):
        x.append(x_in[16 + i])
    for i in range(8):
        x.append(x_in[8 + i])
    for i in range(8):
        x.append(x_in[i])

    # here
    CNOT | (x[6], x[14])
    CNOT | (x[22], x[6])
    CNOT | (x[30], x[22])
    CNOT | (x[21], x[13])
    CNOT | (x[13], x[30])
    CNOT | (x[29], x[13])
    CNOT | (x[5], x[21])
    CNOT | (x[4], x[12])
    CNOT | (x[13], x[5])
    CNOT | (x[28], x[4])
    CNOT | (x[12], x[13])
    CNOT | (x[4], x[29])
    CNOT | (x[27], x[11])
    CNOT | (x[20], x[12])
    CNOT | (x[11], x[4])
    CNOT | (x[27], x[20])
    CNOT | (x[19], x[11])
    CNOT | (x[31], x[23])
    CNOT | (x[3], x[27])
    CNOT | (x[23], x[19])
    CNOT | (x[26], x[18])
    CNOT | (x[11], x[3])
    CNOT | (x[19], x[20])
    CNOT | (x[10], x[26])
    CNOT | (x[10], x[11])
    CNOT | (x[18], x[19])
    CNOT | (x[18], x[10])
    CNOT | (x[9], x[17])
    CNOT | (x[2], x[18])
    CNOT | (x[1], x[9])
    CNOT | (x[24], x[0])
    CNOT | (x[17], x[18])
    CNOT | (x[9], x[10])
    CNOT | (x[2], x[11])
    CNOT | (x[8], x[24])
    CNOT | (x[25], x[17])
    CNOT | (x[9], x[2])
    CNOT | (x[23], x[8])
    CNOT | (x[16], x[24])
    CNOT | (x[15], x[31])
    CNOT | (x[17], x[1])
    CNOT | (x[8], x[9])
    CNOT | (x[31], x[16])
    CNOT | (x[16], x[17])
    CNOT | (x[0], x[8])
    CNOT | (x[12], x[28])
    CNOT | (x[31], x[4])
    CNOT | (x[7], x[15])
    CNOT | (x[0], x[16])
    CNOT | (x[15], x[12])
    CNOT | (x[31], x[27])
    CNOT | (x[31], x[0])
    CNOT | (x[24], x[25])
    CNOT | (x[15], x[11])
    CNOT | (x[7], x[31])
    CNOT | (x[15], x[24])
    CNOT | (x[14], x[7])
    CNOT | (x[23], x[15])
    CNOT | (x[27], x[12])
    CNOT | (x[21], x[14])
    CNOT | (x[22], x[31])
    CNOT | (x[23], x[16])
    CNOT | (x[26], x[27])
    CNOT | (x[6], x[30])
    CNOT | (x[21], x[22])
    CNOT | (x[6], x[23])
    CNOT | (x[1], x[26])
    CNOT | (x[28], x[21])
    CNOT | (x[5], x[6])
    CNOT | (x[25], x[1])
    CNOT | (x[20], x[28])
    CNOT | (x[30], x[14])
    CNOT | (x[7], x[15])
    CNOT | (x[29], x[5])
    CNOT | (x[24], x[0])
    CNOT | (x[9], x[25])
    CNOT | (x[19], x[3])
    CNOT | (x[4], x[20])
    CNOT | (x[21], x[29])
    CNOT | (x[14], x[6])
    CNOT | (x[23], x[7])
    CNOT | (x[0], x[1])
    CNOT | (x[17], x[9])
    CNOT | (x[26], x[2])
    CNOT | (x[27], x[19])
    CNOT | (x[12], x[4])
    CNOT | (x[13], x[21])
    CNOT | (x[6], x[22])
    CNOT | (x[31], x[23])
    CNOT | (x[0], x[17])
    CNOT | (x[18], x[26])
    CNOT | (x[11], x[27])

    x_out = []
    x_out.append(x[0]);
    x_out.append(x[1])
    x_out.append(x[26]);
    x_out.append(x[27])
    x_out.append(x[12]);
    x_out.append(x[5])
    x_out.append(x[22]);
    x_out.append(x[23])

    x_out.append(x[8]);
    x_out.append(x[25])
    x_out.append(x[2]);
    x_out.append(x[3])
    x_out.append(x[28]);
    x_out.append(x[21])
    x_out.append(x[6]);
    x_out.append(x[31])

    x_out.append(x[16]);
    x_out.append(x[9])
    x_out.append(x[18]);
    x_out.append(x[19])
    x_out.append(x[20]);
    x_out.append(x[29])
    x_out.append(x[30]);
    x_out.append(x[7])

    x_out.append(x[24]);
    x_out.append(x[17])
    x_out.append(x[10]);
    x_out.append(x[11])
    x_out.append(x[4]);
    x_out.append(x[13])
    x_out.append(x[14]);
    x_out.append(x[15])

    return x_out

def IP_mc(eng, x_in):
    x = []
    for i in range(8):
        x.append(x_in[24 + i])
    for i in range(8):
        x.append(x_in[16 + i])
    for i in range(8):
        x.append(x_in[8 + i])
    for i in range(8):
        x.append(x_in[i])

    CNOT | (x[7], x[0])
    CNOT | (x[8], x[0])
    CNOT | (x[9], x[0])
    CNOT | (x[15], x[0])
    CNOT | (x[17], x[0])
    CNOT | (x[25], x[0])
    CNOT | (x[9], x[1])
    CNOT | (x[10], x[1])
    CNOT | (x[18], x[1])
    CNOT | (x[26], x[1])
    CNOT | (x[7], x[2])
    CNOT | (x[10], x[2])
    CNOT | (x[11], x[2])
    CNOT | (x[15], x[2])
    CNOT | (x[19], x[2])
    CNOT | (x[27], x[2])
    CNOT | (x[7], x[3])
    CNOT | (x[11], x[3])
    CNOT | (x[12], x[3])
    CNOT | (x[15], x[3])
    CNOT | (x[20], x[3])
    CNOT | (x[28], x[3])
    CNOT | (x[12], x[4])
    CNOT | (x[13], x[4])
    CNOT | (x[21], x[4])
    CNOT | (x[29], x[4])
    CNOT | (x[13], x[5])
    CNOT | (x[14], x[5])
    CNOT | (x[22], x[5])
    CNOT | (x[30], x[5])
    CNOT | (x[14], x[6])
    CNOT | (x[15], x[6])
    CNOT | (x[23], x[6])
    CNOT | (x[31], x[6])
    CNOT | (x[8], x[7])
    CNOT | (x[15], x[7])
    CNOT | (x[16], x[7])
    CNOT | (x[24], x[7])
    CNOT | (x[9], x[8])
    CNOT | (x[10], x[8])
    CNOT | (x[15], x[8])
    CNOT | (x[16], x[8])
    CNOT | (x[17], x[8])
    CNOT | (x[18], x[8])
    CNOT | (x[23], x[8])
    CNOT | (x[25], x[8])
    CNOT | (x[26], x[8])
    CNOT | (x[15], x[9])
    CNOT | (x[17], x[9])
    CNOT | (x[23], x[9])
    CNOT | (x[25], x[9])
    CNOT | (x[14], x[10])
    CNOT | (x[15], x[10])
    CNOT | (x[18], x[10])
    CNOT | (x[22], x[10])
    CNOT | (x[23], x[10])
    CNOT | (x[24], x[10])
    CNOT | (x[26], x[10])
    CNOT | (x[31], x[10])
    CNOT | (x[12], x[11])
    CNOT | (x[15], x[11])
    CNOT | (x[19], x[11])
    CNOT | (x[20], x[11])
    CNOT | (x[23], x[11])
    CNOT | (x[24], x[11])
    CNOT | (x[26], x[11])
    CNOT | (x[27], x[11])
    CNOT | (x[28], x[11])
    CNOT | (x[13], x[12])
    CNOT | (x[14], x[12])
    CNOT | (x[20], x[12])
    CNOT | (x[21], x[12])
    CNOT | (x[22], x[12])
    CNOT | (x[29], x[12])
    CNOT | (x[30], x[12])
    CNOT | (x[21], x[13])
    CNOT | (x[24], x[13])
    CNOT | (x[26], x[13])
    CNOT | (x[27], x[13])
    CNOT | (x[29], x[13])
    CNOT | (x[15], x[14])
    CNOT | (x[22], x[14])
    CNOT | (x[23], x[14])
    CNOT | (x[24], x[14])
    CNOT | (x[26], x[14])
    CNOT | (x[27], x[14])
    CNOT | (x[29], x[14])
    CNOT | (x[30], x[14])
    CNOT | (x[31], x[14])
    CNOT | (x[23], x[15])
    CNOT | (x[25], x[15])
    CNOT | (x[26], x[15])
    CNOT | (x[28], x[15])
    CNOT | (x[29], x[15])
    CNOT | (x[31], x[15])
    CNOT | (x[23], x[16])
    CNOT | (x[24], x[16])
    CNOT | (x[25], x[16])
    CNOT | (x[26], x[16])
    CNOT | (x[27], x[16])
    CNOT | (x[29], x[16])
    CNOT | (x[30], x[16])
    CNOT | (x[31], x[16])
    CNOT | (x[25], x[17])
    CNOT | (x[26], x[17])
    CNOT | (x[27], x[17])
    CNOT | (x[28], x[17])
    CNOT | (x[30], x[17])
    CNOT | (x[31], x[17])
    CNOT | (x[23], x[18])
    CNOT | (x[24], x[18])
    CNOT | (x[25], x[18])
    CNOT | (x[26], x[18])
    CNOT | (x[29], x[18])
    CNOT | (x[30], x[18])
    CNOT | (x[31], x[18])
    CNOT | (x[23], x[19])
    CNOT | (x[24], x[19])
    CNOT | (x[26], x[19])
    CNOT | (x[28], x[19])
    CNOT | (x[31], x[19])
    CNOT | (x[24], x[20])
    CNOT | (x[25], x[20])
    CNOT | (x[27], x[20])
    CNOT | (x[29], x[20])
    CNOT | (x[25], x[21])
    CNOT | (x[26], x[21])
    CNOT | (x[28], x[21])
    CNOT | (x[30], x[21])
    CNOT | (x[24], x[22])
    CNOT | (x[26], x[22])
    CNOT | (x[27], x[22])
    CNOT | (x[29], x[22])
    CNOT | (x[31], x[22])
    CNOT | (x[25], x[23])
    CNOT | (x[27], x[23])
    CNOT | (x[28], x[23])
    CNOT | (x[30], x[23])
    CNOT | (x[25], x[24])
    CNOT | (x[26], x[24])
    CNOT | (x[27], x[24])
    CNOT | (x[29], x[24])
    CNOT | (x[30], x[24])
    CNOT | (x[26], x[25])
    CNOT | (x[27], x[25])
    CNOT | (x[27], x[26])
    CNOT | (x[29], x[26])
    CNOT | (x[31], x[26])
    CNOT | (x[28], x[27])
    CNOT | (x[29], x[27])
    CNOT | (x[29], x[28])
    CNOT | (x[31], x[28])
    CNOT | (x[31], x[29])

    CNOT | (x[5], x[31])
    CNOT | (x[6], x[31])
    CNOT | (x[13], x[31])
    CNOT | (x[14], x[31])
    CNOT | (x[21], x[31])
    CNOT | (x[22], x[31])
    CNOT | (x[24], x[31])
    CNOT | (x[26], x[31])
    CNOT | (x[27], x[31])
    CNOT | (x[29], x[31])
    CNOT | (x[6], x[30])
    CNOT | (x[7], x[30])
    CNOT | (x[8], x[30])
    CNOT | (x[9], x[30])
    CNOT | (x[10], x[30])
    CNOT | (x[22], x[30])
    CNOT | (x[23], x[30])
    CNOT | (x[24], x[30])
    CNOT | (x[27], x[30])
    CNOT | (x[29], x[30])
    CNOT | (x[4], x[29])
    CNOT | (x[5], x[29])
    CNOT | (x[12], x[29])
    CNOT | (x[20], x[29])
    CNOT | (x[21], x[29])
    CNOT | (x[24], x[29])
    CNOT | (x[25], x[29])
    CNOT | (x[26], x[29])
    CNOT | (x[0], x[28])
    CNOT | (x[1], x[28])
    CNOT | (x[8], x[28])
    CNOT | (x[16], x[28])
    CNOT | (x[17], x[28])
    CNOT | (x[3], x[27])
    CNOT | (x[4], x[27])
    CNOT | (x[11], x[27])
    CNOT | (x[13], x[27])
    CNOT | (x[19], x[27])
    CNOT | (x[20], x[27])
    CNOT | (x[25], x[27])
    CNOT | (x[2], x[26])
    CNOT | (x[3], x[26])
    CNOT | (x[7], x[26])
    CNOT | (x[8], x[26])
    CNOT | (x[9], x[26])
    CNOT | (x[11], x[26])
    CNOT | (x[18], x[26])
    CNOT | (x[19], x[26])
    CNOT | (x[23], x[26])
    CNOT | (x[1], x[25])
    CNOT | (x[2], x[25])
    CNOT | (x[7], x[25])
    CNOT | (x[8], x[25])
    CNOT | (x[11], x[25])
    CNOT | (x[12], x[25])
    CNOT | (x[13], x[25])
    CNOT | (x[14], x[25])
    CNOT | (x[15], x[25])
    CNOT | (x[17], x[25])
    CNOT | (x[18], x[25])
    CNOT | (x[23], x[25])
    CNOT | (x[24], x[25])
    CNOT | (x[0], x[24])
    CNOT | (x[9], x[24])
    CNOT | (x[16], x[24])
    CNOT | (x[0], x[23])
    CNOT | (x[7], x[23])
    CNOT | (x[8], x[23])
    CNOT | (x[10], x[23])
    CNOT | (x[14], x[23])
    CNOT | (x[15], x[23])
    CNOT | (x[7], x[22])
    CNOT | (x[8], x[22])
    CNOT | (x[9], x[22])
    CNOT | (x[10], x[22])
    CNOT | (x[14], x[22])
    CNOT | (x[6], x[21])
    CNOT | (x[15], x[21])
    CNOT | (x[5], x[20])
    CNOT | (x[14], x[20])
    CNOT | (x[15], x[20])
    CNOT | (x[4], x[19])
    CNOT | (x[13], x[19])
    CNOT | (x[3], x[18])
    CNOT | (x[7], x[18])
    CNOT | (x[8], x[18])
    CNOT | (x[9], x[18])
    CNOT | (x[10], x[18])
    CNOT | (x[12], x[18])
    CNOT | (x[13], x[18])
    CNOT | (x[15], x[18])
    CNOT | (x[2], x[17])
    CNOT | (x[7], x[17])
    CNOT | (x[8], x[17])
    CNOT | (x[9], x[17])
    CNOT | (x[10], x[17])
    CNOT | (x[11], x[17])
    CNOT | (x[12], x[17])
    CNOT | (x[13], x[17])
    CNOT | (x[1], x[16])
    CNOT | (x[10], x[16])
    CNOT | (x[14], x[16])
    CNOT | (x[2], x[15])
    CNOT | (x[7], x[15])
    CNOT | (x[8], x[15])
    CNOT | (x[11], x[15])
    CNOT | (x[12], x[15])
    CNOT | (x[13], x[15])
    CNOT | (x[14], x[15])
    CNOT | (x[6], x[14])
    CNOT | (x[13], x[14])
    CNOT | (x[4], x[13])
    CNOT | (x[11], x[13])
    CNOT | (x[5], x[12])
    CNOT | (x[3], x[11])
    CNOT | (x[7], x[11])
    CNOT | (x[8], x[11])
    CNOT | (x[9], x[11])
    CNOT | (x[7], x[10])
    CNOT | (x[8], x[10])
    CNOT | (x[9], x[10])
    CNOT | (x[0], x[9])
    CNOT | (x[7], x[9])
    CNOT | (x[1], x[8])

    if (resource_check != 1):
        Swap | (x[30], x[31])
        Swap | (x[27], x[28])
        Swap | (x[26], x[27])
        Swap | (x[25], x[26])
        Swap | (x[22], x[23])
        Swap | (x[21], x[22])
        Swap | (x[20], x[21])
        Swap | (x[19], x[20])
        Swap | (x[18], x[19])
        Swap | (x[17], x[18])
        Swap | (x[16], x[17])
        Swap | (x[12], x[13])
        Swap | (x[10], x[15])
        Swap | (x[8], x[9])
        Swap | (x[6], x[7])
        Swap | (x[5], x[6])
        Swap | (x[4], x[5])
        Swap | (x[3], x[4])
        Swap | (x[2], x[3])
        Swap | (x[1], x[2])
        Swap | (x[0], x[1])

    out = []
    for i in range(8):
        out.append(x[24 + i])
    for i in range(8):
        out.append(x[16 + i])
    for i in range(8):
        out.append(x[8 + i])
    for i in range(8):
        out.append(x[i])

    return out

def Maxi_mc(eng, x_in):

    x = []
    for i in range(8):
        x.append(x_in[24 + i])
    for i in range(8):
        x.append(x_in[16 + i])
    for i in range(8):
        x.append(x_in[8 + i])
    for i in range(8):
        x.append(x_in[i])

    t = eng.allocate_qureg(100)
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

def AES_MC5(eng, x_in):
    x = []
    for i in range(8):
        x.append(x_in[24 + i])
    for i in range(8):
        x.append(x_in[16 + i])
    for i in range(8):
        x.append(x_in[8 + i])
    for i in range(8):
        x.append(x_in[0 + i])

    t = eng.allocate_qureg(110)

    CNOT2_euro(eng, x[5], x[13], t[32])
    CNOT2_euro(eng, x[21], x[29], t[43])
    CNOT2_euro(eng, x[15], x[30], t[44])
    CNOT2_euro(eng, x[7], x[16], t[46])
    CNOT2_euro(eng, x[23], x[24], t[47])
    CNOT2_euro(eng, x[1], x[18], t[56])
    CNOT2_euro(eng, x[17], x[26], t[57])
    CNOT2_euro(eng, x[6], x[22], t[70])

    CNOT2_euro(eng, t[70], t[43], t[35])

    CNOT2_euro(eng, x[14], x[31], t[71])

    CNOT2_euro(eng, t[71], t[70], t[42])

    CNOT2_euro(eng, x[7], x[15], t[72])

    CNOT2_euro(eng, t[72], t[71], t[37])

    CNOT2_euro(eng, x[0], x[17], t[73])
    CNOT2_euro(eng, x[7], t[73], t[51])
    CNOT2_euro(eng, x[6], x[23], t[74])
    CNOT2_euro(eng, x[7], t[74], t[39])

    CNOT2_euro(eng, t[39], t[37], t[7])
    CNOT2_euro(eng, t[42], t[39], t[15])
    CNOT2_euro(eng, t[44], t[39], t[31])

    CNOT2_euro(eng, x[12], x[28], t[75])
    CNOT2_euro(eng, x[3], x[7], t[76])

    CNOT2_euro(eng, t[75], t[76], t[63])

    CNOT2_euro(eng, x[13], x[29], t[77])

    CNOT2_euro(eng, t[75], t[77], t[36])

    CNOT2_euro(eng, x[30], t[77], t[38])

    CNOT2_euro(eng, t[38], t[35], t[14])

    CNOT2_euro(eng, x[14], x[22], t[78])

    CNOT2_euro(eng, t[78], x[30], t[34])
    CNOT2_euro(eng, t[32], t[34], t[6])
    CNOT2_euro(eng, t[35], t[34], t[22])
    CNOT2_euro(eng, t[37], t[34], t[23])

    CNOT2_euro(eng, x[4], x[20], t[79])

    CNOT2_euro(eng, t[79], t[76], t[64])

    CNOT2_euro(eng, x[12], x[20], t[80])
    CNOT2_euro(eng, x[5], t[80], t[41])

    CNOT2_euro(eng, t[43], t[41], t[13])
    CNOT2_euro(eng, t[41], t[36], t[21])
    CNOT2_euro(eng, x[14], x[21], t[81])
    CNOT2_euro(eng, x[5], t[81], t[40])
    CNOT2_euro(eng, t[40], t[35], t[30])
    CNOT2_euro(eng, x[18], x[23], t[82])
    CNOT2_euro(eng, x[11], x[27], t[83])
    CNOT2_euro(eng, t[82], t[83], t[69])

    CNOT2_euro(eng, x[3], x[19], t[84])
    CNOT2_euro(eng, t[82], t[84], t[68])
    CNOT2_euro(eng, x[16], x[23], t[85])
    CNOT2_euro(eng, t[85], x[25], t[52])
    CNOT2_euro(eng, x[0], x[8], t[86])
    CNOT2_euro(eng, x[31], t[86], t[45])
    CNOT2_euro(eng, t[45], t[47], t[16])
    CNOT2_euro(eng, t[45], t[46], t[24])

    CNOT2_euro(eng, t[85], t[86], t[49])
    CNOT2_euro(eng, x[2], x[10], t[87])
    CNOT2_euro(eng, t[87], x[25], t[55])
    CNOT2_euro(eng, t[55], t[57], t[18])

    CNOT2_euro(eng, t[55], t[56], t[26])
    CNOT2_euro(eng, x[3], x[26], t[88])
    CNOT2_euro(eng, t[88], x[31], t[66])

    CNOT2_euro(eng, t[69], t[66], t[19])
    CNOT2_euro(eng, x[12], x[27], t[89])
    CNOT2_euro(eng, t[89], x[31], t[61])

    CNOT2_euro(eng, t[64], t[61], t[28])
    CNOT2_euro(eng, x[8], x[15], t[90])
    CNOT2_euro(eng, x[24], t[90], t[48])
    CNOT2_euro(eng, t[48], t[46], t[0])

    CNOT2_euro(eng, t[49], t[48], t[8])

    CNOT2_euro(eng, x[9], x[25], t[91])
    CNOT2_euro(eng, t[90], t[91], t[53])

    CNOT2_euro(eng, t[53], t[51], t[1])
    CNOT2_euro(eng, x[1], x[17], t[92])

    CNOT2_euro(eng, t[90], t[92], t[54])
    CNOT2_euro(eng, t[54], t[52], t[9])
    CNOT2_euro(eng, x[4], x[28], t[93])
    CNOT2_euro(eng, t[93], x[21], t[33])
    CNOT2_euro(eng, t[36], t[33], t[5])
    CNOT2_euro(eng, t[32], t[33], t[29])
    CNOT2_euro(eng, x[19], x[23], t[94])

    CNOT2_euro(eng, t[93], t[94], t[60])
    CNOT2_euro(eng, t[60], t[61], t[20])
    CNOT2_euro(eng, x[10], x[26], t[95])
    CNOT2_euro(eng, x[9], t[95], t[59])

    CNOT2_euro(eng, t[59], t[56], t[2])
    CNOT2_euro(eng, x[2], x[18], t[96])
    CNOT2_euro(eng, x[9], t[96], t[58])
    CNOT2_euro(eng, t[58], t[57], t[10])

    CNOT2_euro(eng, x[10], x[27], t[97])
    CNOT2_euro(eng, x[15], t[97], t[67])
    CNOT2_euro(eng, t[68], t[67], t[11])
    CNOT2_euro(eng, x[11], x[20], t[98])
    CNOT2_euro(eng, x[15], t[98], t[62])

    CNOT2_euro(eng, t[63], t[62], t[4])
    CNOT2_euro(eng, t[60], t[62], t[12])
    CNOT2_euro(eng, x[11], x[19], t[99])
    CNOT2_euro(eng, x[2], x[7], t[100])

    CNOT2_euro(eng, t[99], t[100], t[65])
    CNOT2_euro(eng, t[65], t[67], t[3])
    CNOT2_euro(eng, t[65], t[66], t[27])
    CNOT2_euro(eng, x[9], x[31], t[101])
    CNOT2_euro(eng, x[1], x[24], t[102])
    CNOT2_euro(eng, t[101], t[102], t[50])
    CNOT2_euro(eng, t[50], t[52], t[17])
    CNOT2_euro(eng, t[50], t[51], t[25])

    out = []
    for i in range(8):
        out.append(t[24 + i])
    for i in range(8):
        out.append(t[16 + i])
    for i in range(8):
        out.append(t[8 + i])
    for i in range(8):
        out.append(t[0 + i])

    return out

def AES_MC_45(eng, x_in):

    x = []
    for i in range(8):
        x.append(x_in[24 + i])
    for i in range(8):
        x.append(x_in[16 + i])
    for i in range(8):
        x.append(x_in[8 + i])
    for i in range(8):
        x.append(x_in[0 + i])

    t = eng.allocate_qureg(125)

    CNOT2_euro(eng, x[23], x[31], t[32])
    CNOT2_euro(eng, x[15], x[31], t[33])
    CNOT2_euro(eng, x[4], x[12], t[34])
    CNOT2_euro(eng, x[13], x[21], t[35])
    CNOT2_euro(eng, x[9], x[17], t[36])
    CNOT2_euro(eng, x[11], x[27], t[37])
    CNOT2_euro(eng, x[4], x[28], t[38])
    CNOT2_euro(eng, x[5], x[21], t[39])
    CNOT2_euro(eng, x[0], x[24], t[40])
    CNOT2_euro(eng, x[7], x[15], t[41])
    CNOT2_euro(eng, x[1], x[9], t[42])
    CNOT2_euro(eng, x[6], x[14], t[43])
    CNOT2_euro(eng, x[16], x[24], t[44])
    CNOT2_euro(eng, x[6], x[22], t[45])
    CNOT2_euro(eng, x[16], t[33], t[46])
    CNOT2_euro(eng, x[8], t[44], t[47])
    CNOT2_euro(eng, x[18], x[26], t[48])
    CNOT2_euro(eng, x[22], x[30], t[49])
    CNOT2_euro(eng, x[10], x[26], t[50])

    CNOT2_euro(eng, x[2], t[42], t[51])
    CNOT2_euro(eng, x[25], t[47], t[52])
    CNOT2_euro(eng, t[41], t[47], t[53])
    CNOT2_euro(eng, t[32], t[41], t[54])
    CNOT2_euro(eng, t[33], t[40], t[55])
    CNOT2_euro(eng, t[32], t[45], t[56])
    CNOT2_euro(eng, x[7], t[43], t[57])
    CNOT2_euro(eng, t[39], t[49], t[58])
    CNOT2_euro(eng, x[3], x[27], t[59])
    CNOT2_euro(eng, x[25], t[36], t[60])
    CNOT2_euro(eng, x[1], t[60], t[61])
    CNOT2_euro(eng, t[46], t[60], t[62])
    CNOT2_euro(eng, t[50], t[61], t[63])
    CNOT2_euro(eng, t[35], t[45], t[64])
    CNOT2_euro(eng, x[30], t[64], t[65])
    CNOT2_euro(eng, t[33], t[59], t[66])
    CNOT2_euro(eng, t[50], t[66], t[67])
    CNOT2_euro(eng, x[19], t[32], t[68])
    CNOT2_euro(eng, x[20], t[34], t[69])

    CNOT2_euro(eng, t[32], t[40], t[70])
    CNOT2_euro(eng, x[8], t[70], t[71])
    CNOT2_euro(eng, t[46], t[70], t[72])
    CNOT2_euro(eng, t[41], t[69], t[73])
    CNOT2_euro(eng, t[66], t[73], t[74])
    CNOT2_euro(eng, x[29], t[35], t[75])
    CNOT2_euro(eng, t[34], t[75], t[76])
    CNOT2_euro(eng, x[28], t[69], t[77])
    CNOT2_euro(eng, t[39], t[77], t[78])
    CNOT2_euro(eng, t[76], t[78], t[79])
    CNOT2_euro(eng, t[33], t[37], t[80])
    CNOT2_euro(eng, t[38], t[80], t[81])
    CNOT2_euro(eng, t[74], t[81], t[82])
    CNOT2_euro(eng, x[27], t[68], t[83])
    CNOT2_euro(eng, x[20], t[83], t[84])
    CNOT2_euro(eng, t[77], t[84], t[85])
    CNOT2_euro(eng, t[81], t[84], t[86])
    CNOT2_euro(eng, x[5], t[75], t[87])
    CNOT2_euro(eng, t[45], t[87], t[88])

    CNOT2_euro(eng, x[29], t[38], t[89])
    CNOT2_euro(eng, t[87], t[89], t[90])
    CNOT2_euro(eng, t[78], t[89], t[91])
    CNOT2_euro(eng, x[2], t[48], t[92])
    CNOT2_euro(eng, t[36], t[92], t[93])
    CNOT2_euro(eng, t[33], t[49], t[94])
    CNOT2_euro(eng, x[7], t[94], t[95])
    CNOT2_euro(eng, t[40], t[71], t[96])
    CNOT2_euro(eng, t[42], t[96], t[97])
    CNOT2_euro(eng, x[10], t[92], t[98])
    CNOT2_euro(eng, t[51], t[98], t[99])
    CNOT2_euro(eng, t[48], t[68], t[100])
    CNOT2_euro(eng, t[67], t[100], t[101])
    CNOT2_euro(eng, t[37], t[100], t[102])
    CNOT2_euro(eng, x[19], t[102], t[103])
    CNOT2_euro(eng, x[3], t[103], t[104])
    CNOT2_euro(eng, t[39], t[65], t[105])
    CNOT2_euro(eng, t[43], t[105], t[106])
    CNOT2_euro(eng, t[54], t[98], t[107])

    CNOT2_euro(eng, t[102], t[107], t[108])
    CNOT2_euro(eng, t[61], t[52], t[109])
    CNOT2_euro(eng, t[53], t[55], t[110])
    CNOT2_euro(eng, t[109], t[110], t[111])
    CNOT2_euro(eng, t[51], t[63], t[112])
    CNOT2_euro(eng, t[52], t[97], t[113])
    CNOT2_euro(eng, t[54], t[57], t[114])
    CNOT2_euro(eng, t[56], t[57], t[115])
    CNOT2_euro(eng, t[88], t[106], t[116])
    CNOT2_euro(eng, t[97], t[62], t[117])
    CNOT2_euro(eng, t[56], t[95], t[118])
    CNOT2_euro(eng, t[93], t[63], t[119])
    CNOT2_euro(eng, t[58], t[116], t[120])
    CNOT2_euro(eng, t[62], t[110], t[121])
    CNOT2_euro(eng, t[108], t[67], t[122])

    out = []

    out.append(t[53])
    out.append(t[121])
    out.append(t[99])
    out.append(t[108])
    out.append(t[82])
    out.append(t[76])
    out.append(t[106])
    out.append(t[114])
    out.append(t[72])
    out.append(t[117])
    out.append(t[93])
    out.append(t[101])
    out.append(t[86])
    out.append(t[91])
    out.append(t[65])
    out.append(t[115])
    out.append(t[71])
    out.append(t[113])
    out.append(t[112])
    out.append(t[104])
    out.append(t[85])
    out.append(t[79])
    out.append(t[116])
    out.append(t[95])
    out.append(t[110])
    out.append(t[111])
    out.append(t[119])
    out.append(t[122])
    out.append(t[74])
    out.append(t[90])
    out.append(t[120])
    out.append(t[118])

    out2 = []
    for i in range(8):
        out2.append(out[24 + i])
    for i in range(8):
        out2.append(out[16 + i])
    for i in range(8):
        out2.append(out[8 + i])
    for i in range(8):
        out2.append(out[0 + i])

    return out2

def mx_03(eng, x, y):

    CNOT | (x[0], y[0])
    CNOT | (x[1], y[1])
    CNOT | (x[2], y[2])
    CNOT | (x[3], y[3])
    CNOT | (x[4], y[4])
    CNOT | (x[5], y[5])
    CNOT | (x[6], y[6])
    CNOT | (x[7], y[7])

    CNOT | (x[0], y[1])
    CNOT | (x[1], y[2])
    CNOT | (x[2], y[3])
    CNOT | (x[3], y[4])
    CNOT | (x[4], y[5])
    CNOT | (x[5], y[6])
    CNOT | (x[6], y[7])

    #modular
    CNOT | (x[7], y[0])
    CNOT | (x[7], y[1])
    CNOT | (x[7], y[3])
    CNOT | (x[7], y[4])

def mx_01(eng, x, y):
    for i in range(8):
        CNOT | (x[i], y[i])

def mx_02(eng, x, y):
    CNOT | (x[0], y[1])
    CNOT | (x[1], y[2])
    CNOT | (x[2], y[3])
    CNOT | (x[3], y[4])
    CNOT | (x[4], y[5])
    CNOT | (x[5], y[6])
    CNOT | (x[6], y[7])

    #modular
    CNOT | (x[7], y[0])
    CNOT | (x[7], y[1])
    CNOT | (x[7], y[3])
    CNOT | (x[7], y[4])

def mix_naive(eng, x):

    x0 = []
    x1 = []
    x2 = []
    x3 = []

    for i in range(8):
        x0.append(x[i+24]) # x0 = x[24 ~ 31]
        x1.append(x[i+16]) # x1 = x[16 ~ 23]
        x2.append(x[i+8]) # x2 = x[8 ~ 15]
        x3.append(x[i])   # x3 = x[0 ~ 7]

    y0 = eng.allocate_qureg(8)
    y1 = eng.allocate_qureg(8)
    y2 = eng.allocate_qureg(8)
    y3 = eng.allocate_qureg(8)

    #first row
    mx_02(eng, x0, y0) #
    mx_03(eng, x1, y0)
    mx_01(eng, x2, y0)
    mx_01(eng, x3, y0)

    #second row
    mx_01(eng, x0, y1)
    mx_02(eng, x1, y1)
    mx_03(eng, x2, y1)
    mx_01(eng, x3, y1)

    #third row
    mx_01(eng, x0, y2)
    mx_01(eng, x1, y2)
    mx_02(eng, x2, y2)
    mx_03(eng, x3, y2)

    #fourth row=
    mx_03(eng, x0, y3)
    mx_01(eng, x1, y3)
    mx_01(eng, x2, y3)
    mx_02(eng, x3, y3)

    out = []
    for i in range(8):
        out.append(y3[i])
    for i in range(8):
        out.append(y2[i])
    for i in range(8):
        out.append(y1[i])
    for i in range(8):
        out.append(y0[i])

    return out

def Mix_naive_2(eng, in_x, y):

    x = []

    for i in range(8):
        x.append(in_x[i + 0])
    for i in range(8):
        x.append(in_x[i + 24])
    for i in range(8):
        x.append(in_x[i + 16])
    for i in range(8):
        x.append(in_x[i + 8])


    MixColumn= [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
                 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
                 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
                 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
                 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,
                 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
                 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0,
                 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1 ,
                 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0,
                 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0,
                 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
                 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0,
                 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0,
                 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
                 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0,
                 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1 ,
                 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1,
                 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1,
                 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0,
                 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1,
                 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1,
                 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0,
                 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0,
                 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1 ,
                 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 ,
                 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1,
                 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
                 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1,
                 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1,
                 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,
                 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0,
                 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0]

    for i in range(32):
        for j in range(32):
            if(MixColumn[i*32+j] == 1):
                CNOT | (x[j], y[i])

    out = []
    for i in range(8):
        out.append(y[i+0])
    for i in range(8):
        out.append(y[i+24])
    for i in range(8):
        out.append(y[i+16])
    for i in range(8):
        out.append(y[i+8])

    return out

def mix_naive_matrix(eng, x, y):

    MixColumn =[0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1,
        1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1,
        0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0,
        0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1,
        0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1,
        0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0,
        0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0,
        0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1,
        1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
        1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
        0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
        0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
        0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,
        0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
        0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0,
        0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1,
        1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0,
        0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0,
        0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
        0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0,
        0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0,
        0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
        0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,
        0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1,
        1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1,
        0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1,
        0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1,
        0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1,
        0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0,
        0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1,
        1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1,
        0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0,
        0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1,
        0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1,
        0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0,
        0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0,
        0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1,
        1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
        1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
        0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
        0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
        0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,
        0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
        0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0,
        0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1,
        1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0,
        0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0,
        0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
        0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0,
        0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0,
        0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
        0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,
        0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1,
        1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1,
        0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1,
        0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1,
        0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1,
        0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0]

    for i in range(32):
        for j in range(32):
            if(MixColumn[i*32+j] == 1):
                CNOT | (x[j], y[i])

    return y

def Euro_plu_mix(eng, word):

    CNOT | (word[7], word[0]);
    CNOT | (word[8], word[0]);
    CNOT | (word[9], word[0]);
    CNOT | (word[15], word[0]);
    CNOT | (word[17], word[0]);
    CNOT | (word[25], word[0]);
    CNOT | (word[9], word[1]);
    CNOT | (word[10], word[1]);
    CNOT | (word[18], word[1]);
    CNOT | (word[26], word[1]);
    CNOT | (word[7], word[2]);
    CNOT | (word[10], word[2]);
    CNOT | (word[11], word[2]);
    CNOT | (word[15], word[2]);
    CNOT | (word[19], word[2]);
    CNOT | (word[27], word[2]);
    CNOT | (word[7], word[3]);
    CNOT | (word[11], word[3]);
    CNOT | (word[12], word[3]);
    CNOT | (word[15], word[3]);
    CNOT | (word[20], word[3]);
    CNOT | (word[28], word[3]);
    CNOT | (word[12], word[4]);
    CNOT | (word[13], word[4]);
    CNOT | (word[21], word[4]);
    CNOT | (word[29], word[4]);
    CNOT | (word[13], word[5]);
    CNOT | (word[14], word[5]);
    CNOT | (word[22], word[5]);
    CNOT | (word[30], word[5]);
    CNOT | (word[14], word[6]);
    CNOT | (word[15], word[6]);
    CNOT | (word[23], word[6]);
    CNOT | (word[31], word[6]);
    CNOT | (word[8], word[7]);
    CNOT | (word[15], word[7]);
    CNOT | (word[16], word[7]);
    CNOT | (word[24], word[7]);
    CNOT | (word[9], word[8]);
    CNOT | (word[10], word[8]);
    CNOT | (word[15], word[8]);
    CNOT | (word[16], word[8]);
    CNOT | (word[17], word[8]);
    CNOT | (word[18], word[8]);
    CNOT | (word[23], word[8]);
    CNOT | (word[25], word[8]);
    CNOT | (word[26], word[8]);
    CNOT | (word[15], word[9]);
    CNOT | (word[17], word[9]);
    CNOT | (word[23], word[9]);
    CNOT | (word[25], word[9]);
    CNOT | (word[14], word[10]);
    CNOT | (word[15], word[10]);
    CNOT | (word[18], word[10]);
    CNOT | (word[22], word[10]);
    CNOT | (word[23], word[10]);
    CNOT | (word[24], word[10]);
    CNOT | (word[26], word[10]);
    CNOT | (word[31], word[10]);
    CNOT | (word[12], word[11]);
    CNOT | (word[15], word[11]);
    CNOT | (word[19], word[11]);
    CNOT | (word[20], word[11]);
    CNOT | (word[23], word[11]);
    CNOT | (word[24], word[11]);
    CNOT | (word[26], word[11]);
    CNOT | (word[27], word[11]);
    CNOT | (word[28], word[11]);
    CNOT | (word[13], word[12]);
    CNOT | (word[14], word[12]);
    CNOT | (word[20], word[12]);
    CNOT | (word[21], word[12]);
    CNOT | (word[22], word[12]);
    CNOT | (word[29], word[12]);
    CNOT | (word[30], word[12]);
    CNOT | (word[21], word[13]);
    CNOT | (word[24], word[13]);
    CNOT | (word[26], word[13]);
    CNOT | (word[27], word[13]);
    CNOT | (word[29], word[13]);
    CNOT | (word[15], word[14]);
    CNOT | (word[22], word[14]);
    CNOT | (word[23], word[14]);
    CNOT | (word[24], word[14]);
    CNOT | (word[26], word[14]);
    CNOT | (word[27], word[14]);
    CNOT | (word[29], word[14]);
    CNOT | (word[30], word[14]);
    CNOT | (word[31], word[14]);
    CNOT | (word[23], word[15]);
    CNOT | (word[25], word[15]);
    CNOT | (word[26], word[15]);
    CNOT | (word[28], word[15]);
    CNOT | (word[29], word[15]);
    CNOT | (word[31], word[15]);
    CNOT | (word[23], word[16]);
    CNOT | (word[24], word[16]);
    CNOT | (word[25], word[16]);
    CNOT | (word[26], word[16]);
    CNOT | (word[27], word[16]);
    CNOT | (word[29], word[16]);
    CNOT | (word[30], word[16]);
    CNOT | (word[31], word[16]);
    CNOT | (word[25], word[17]);
    CNOT | (word[26], word[17]);
    CNOT | (word[27], word[17]);
    CNOT | (word[28], word[17]);
    CNOT | (word[30], word[17]);
    CNOT | (word[31], word[17]);
    CNOT | (word[23], word[18]);
    CNOT | (word[24], word[18]);
    CNOT | (word[25], word[18]);
    CNOT | (word[26], word[18]);
    CNOT | (word[29], word[18]);
    CNOT | (word[30], word[18]);
    CNOT | (word[31], word[18]);
    CNOT | (word[23], word[19]);
    CNOT | (word[24], word[19]);
    CNOT | (word[26], word[19]);
    CNOT | (word[28], word[19]);
    CNOT | (word[31], word[19]);
    CNOT | (word[24], word[20]);
    CNOT | (word[25], word[20]);
    CNOT | (word[27], word[20]);
    CNOT | (word[29], word[20]);
    CNOT | (word[25], word[21]);
    CNOT | (word[26], word[21]);
    CNOT | (word[28], word[21]);
    CNOT | (word[30], word[21]);
    CNOT | (word[24], word[22]);
    CNOT | (word[26], word[22]);
    CNOT | (word[27], word[22]);
    CNOT | (word[29], word[22]);
    CNOT | (word[31], word[22]);
    CNOT | (word[25], word[23]);
    CNOT | (word[27], word[23]);
    CNOT | (word[28], word[23]);
    CNOT | (word[30], word[23]);
    CNOT | (word[25], word[24]);
    CNOT | (word[26], word[24]);
    CNOT | (word[27], word[24]);
    CNOT | (word[29], word[24]);
    CNOT | (word[30], word[24]);
    CNOT | (word[26], word[25]);
    CNOT | (word[27], word[25]);
    CNOT | (word[27], word[26]);
    CNOT | (word[29], word[26]);
    CNOT | (word[31], word[26]);
    CNOT | (word[28], word[27]);
    CNOT | (word[29], word[27]);
    CNOT | (word[29], word[28]);
    CNOT | (word[31], word[28]);
    CNOT | (word[31], word[29]);

    # L
    CNOT | (word[5], word[31]);
    CNOT | (word[6], word[31]);
    CNOT | (word[13], word[31]);
    CNOT | (word[14], word[31]);
    CNOT | (word[21], word[31]);
    CNOT | (word[22], word[31]);
    CNOT | (word[24], word[31]);
    CNOT | (word[26], word[31]);
    CNOT | (word[27], word[31]);
    CNOT | (word[29], word[31]);
    CNOT | (word[6], word[30]);
    CNOT | (word[7], word[30]);
    CNOT | (word[8], word[30]);
    CNOT | (word[9], word[30]);
    CNOT | (word[10], word[30]);
    CNOT | (word[22], word[30]);
    CNOT | (word[23], word[30]);
    CNOT | (word[24], word[30]);
    CNOT | (word[27], word[30]);
    CNOT | (word[29], word[30]);
    CNOT | (word[4], word[29]);
    CNOT | (word[5], word[29]);
    CNOT | (word[12], word[29]);
    CNOT | (word[20], word[29]);
    CNOT | (word[21], word[29]);
    CNOT | (word[24], word[29]);
    CNOT | (word[25], word[29]);
    CNOT | (word[26], word[29]);
    CNOT | (word[0], word[28]);
    CNOT | (word[1], word[28]);
    CNOT | (word[8], word[28]);
    CNOT | (word[16], word[28]);
    CNOT | (word[17], word[28]);
    CNOT | (word[3], word[27]);
    CNOT | (word[4], word[27]);
    CNOT | (word[11], word[27]);
    CNOT | (word[13], word[27]);
    CNOT | (word[19], word[27]);
    CNOT | (word[20], word[27]);
    CNOT | (word[25], word[27]);
    CNOT | (word[2], word[26]);
    CNOT | (word[3], word[26]);
    CNOT | (word[7], word[26]);
    CNOT | (word[8], word[26]);
    CNOT | (word[9], word[26]);
    CNOT | (word[11], word[26]);
    CNOT | (word[18], word[26]);
    CNOT | (word[19], word[26]);
    CNOT | (word[23], word[26]);
    CNOT | (word[1], word[25]);
    CNOT | (word[2], word[25]);
    CNOT | (word[7], word[25]);
    CNOT | (word[8], word[25]);
    CNOT | (word[11], word[25]);
    CNOT | (word[12], word[25]);
    CNOT | (word[13], word[25]);
    CNOT | (word[14], word[25]);
    CNOT | (word[15], word[25]);
    CNOT | (word[17], word[25]);
    CNOT | (word[18], word[25]);
    CNOT | (word[23], word[25]);
    CNOT | (word[24], word[25]);
    CNOT | (word[0], word[24]);
    CNOT | (word[9], word[24]);
    CNOT | (word[16], word[24]);
    CNOT | (word[0], word[23]);
    CNOT | (word[7], word[23]);
    CNOT | (word[8], word[23]);
    CNOT | (word[10], word[23]);
    CNOT | (word[14], word[23]);
    CNOT | (word[15], word[23]);
    CNOT | (word[7], word[22]);
    CNOT | (word[8], word[22]);
    CNOT | (word[9], word[22]);
    CNOT | (word[10], word[22]);
    CNOT | (word[14], word[22]);
    CNOT | (word[6], word[21]);
    CNOT | (word[15], word[21]);
    CNOT | (word[5], word[20]);
    CNOT | (word[14], word[20]);
    CNOT | (word[15], word[20]);
    CNOT | (word[4], word[19]);
    CNOT | (word[13], word[19]);
    CNOT | (word[3], word[18]);
    CNOT | (word[7], word[18]);
    CNOT | (word[8], word[18]);
    CNOT | (word[9], word[18]);
    CNOT | (word[10], word[18]);
    CNOT | (word[12], word[18]);
    CNOT | (word[13], word[18]);
    CNOT | (word[15], word[18]);
    CNOT | (word[2], word[17]);
    CNOT | (word[7], word[17]);
    CNOT | (word[8], word[17]);
    CNOT | (word[9], word[17]);
    CNOT | (word[10], word[17]);
    CNOT | (word[11], word[17]);
    CNOT | (word[12], word[17]);
    CNOT | (word[13], word[17]);
    CNOT | (word[1], word[16]);
    CNOT | (word[10], word[16]);
    CNOT | (word[14], word[16]);
    CNOT | (word[2], word[15]);
    CNOT | (word[7], word[15]);
    CNOT | (word[8], word[15]);
    CNOT | (word[11], word[15]);
    CNOT | (word[12], word[15]);
    CNOT | (word[13], word[15]);
    CNOT | (word[14], word[15]);
    CNOT | (word[6], word[14]);
    CNOT | (word[13], word[14]);
    CNOT | (word[4], word[13]);
    CNOT | (word[11], word[13]);
    CNOT | (word[5], word[12]);
    CNOT | (word[3], word[11]);
    CNOT | (word[7], word[11]);
    CNOT | (word[8], word[11]);
    CNOT | (word[9], word[11]);
    CNOT | (word[7], word[10]);
    CNOT | (word[8], word[10]);
    CNOT | (word[9], word[10]);
    CNOT | (word[0], word[9]);
    CNOT | (word[7], word[9]);
    CNOT | (word[1], word[8]);

    out = []
    for i in range(32):
        out.append(word[31-i])

    return out

def Mix_240703(eng, r_in):
    r = []
    r_temp = []

    for i in range(32):
        r_temp.append(r_in[31-i])

    for i in range(8):
        r.append(r_temp[24 + i])
    for i in range(8):
        r.append(r_temp[16 + i])
    for i in range(8):
        r.append(r_temp[8 + i])
    for i in range(8):
        r.append(r_temp[i])

    for i in range(129):
        r.append(r_in[32+i])

    CNOT2(eng, r[64], r[8], r[0])  # 00000101], 00000100], 00000001
    CNOT2(eng, r[65], r[10], r[2])  # 00000404], 00000400], 00000004
    CNOT2(eng, r[66], r[14], r[6])  # 00004040], 00004000], 00000040
    CNOT2(eng, r[67], r[15], r[7])  # 00008080], 00008000], 00000080
    CNOT2(eng, r[68], r[16], r[8])  # 00010100], 00010000], 00000100
    CNOT2(eng, r[69], r[17], r[9])  # 00020200], 00020000], 00000200
    CNOT2(eng, r[70], r[19], r[11])  # 00080800], 00080000], 00000800
    CNOT2(eng, r[71], r[19], r[18])  # 000c0000], 00080000], 00040000
    CNOT2(eng, r[72], r[20], r[11])  # 00100800], 00100000], 00000800
    CNOT2(eng, r[73], r[21], r[6])  # 00200040], 00200000], 00000040
    CNOT2(eng, r[74], r[21], r[13])  # 00202000], 00200000], 00002000
    CNOT2(eng, r[75], r[22], r[13])  # 00402000], 00400000], 00002000
    CNOT2(eng, r[76], r[24], r[0])  # 01000001], 01000000], 00000001
    CNOT2(eng, r[77], r[24], r[16])  # 01010000], 01000000], 00010000
    CNOT2(eng, r[78], r[25], r[0])  # 02000001], 02000000], 00000001
    CNOT2(eng, r[79], r[25], r[1])  # 02000002], 02000000], 00000002
    CNOT2(eng, r[80], r[26], r[18])  # 04040000], 04000000], 00040000
    CNOT2(eng, r[81], r[26], r[25])  # 06000000], 04000000], 02000000
    CNOT2(eng, r[82], r[27], r[3])  # 08000008], 08000000], 00000008
    CNOT2(eng, r[83], r[28], r[4])  # 10000010], 10000000], 00000010
    CNOT2(eng, r[84], r[28], r[20])  # 10100000], 10000000], 00100000
    CNOT2(eng, r[85], r[29], r[5])  # 20000020], 20000000], 00000020
    CNOT2(eng, r[86], r[30], r[22])  # 40400000], 40000000], 00400000
    CNOT2(eng, r[87], r[31], r[23])  # 80800000], 80000000], 00800000
    CNOT2(eng, r[88], r[64], r[4])  # 00000111], 00000101], 00000010
    CNOT2(eng, r[89], r[64], r[24])  # 01000101], 00000101], 01000000
    CNOT2(eng, r[90], r[65], r[26])  # 04000404], 00000404], 04000000
    CNOT2(eng, r[91], r[65], r[27])  # 08000404], 00000404], 08000000
    CNOT2(eng, r[92], r[66], r[30])  # 40004040], 00004040], 40000000
    CNOT2(eng, r[93], r[67], r[23])  # 00808080], 00008080], 00800000
    CNOT2(eng, r[94], r[67], r[64])  # 00008181], 00008080], 00000101
    CNOT2(eng, r[95], r[68], r[17])  # 00030100], 00010100], 00020000
    CNOT2(eng, r[96], r[68], r[24])  # 01010100], 00010100], 01000000
    CNOT2(eng, r[97], r[68], r[31])  # 80010100], 00010100], 80000000
    CNOT2(eng, r[98], r[69], r[2])  # 00020204], 00020200], 00000004
    CNOT2(eng, r[99], r[70], r[3])  # 00080808], 00080800], 00000008
    CNOT2(eng, r[100], r[70], r[27])  # 08080800], 00080800], 08000000
    CNOT2(eng, r[101], r[74], r[5])  # 00202020], 00202000], 00000020
    CNOT2(eng, r[102], r[74], r[68])  # 00212100], 00202000], 00010100
    CNOT2(eng, r[103], r[77], r[66])  # 01014040], 01010000], 00004040
    CNOT2(eng, r[104], r[79], r[9])  # 02000202], 02000002], 00000200
    CNOT2(eng, r[105], r[80], r[1])  # 04040002], 04040000], 00000002
    CNOT2(eng, r[106], r[80], r[3])  # 04040008], 04040000], 00000008
    CNOT2(eng, r[107], r[82], r[12])  # 08001008], 08000008], 00001000
    CNOT2(eng, r[108], r[83], r[12])  # 10001010], 10000010], 00001000
    CNOT2(eng, r[109], r[83], r[76])  # 11000011], 10000010], 01000001
    CNOT2(eng, r[110], r[84], r[5])  # 10100020], 10100000], 00000020
    CNOT2(eng, r[111], r[84], r[77])  # 11110000], 10100000], 01010000
    CNOT2(eng, r[112], r[85], r[14])  # 20004020], 20000020], 00004000
    CNOT2(eng, r[113], r[86], r[6])  # 40400040], 40400000], 00000040
    CNOT2(eng, r[114], r[86], r[14])  # 40404000], 40400000], 00004000
    CNOT2(eng, r[115], r[87], r[15])  # 80808000], 80800000], 00008000
    CNOT2(eng, r[116], r[87], r[22])  # 80c00000], 80800000], 00400000
    CNOT2(eng, r[117], r[88], r[13])  # 00002111], 00000111], 00002000
    CNOT2(eng, r[118], r[88], r[19])  # 00080111], 00000111], 00080000
    CNOT2(eng, r[119], r[89], r[69])  # 01020301], 01000101], 00020200
    CNOT2(eng, r[120], r[90], r[70])  # 04080c04], 04000404], 00080800
    CNOT2(eng, r[121], r[91], r[71])  # 080c0404], 08000404], 000c0000
    CNOT2(eng, r[122], r[93], r[77])  # 01818080], 00808080], 01010000
    CNOT2(eng, r[123], r[95], r[78])  # 02030101], 00030100], 02000001
    CNOT2(eng, r[124], r[96], r[79])  # 03010102], 01010100], 02000002
    CNOT2(eng, r[125], r[97], r[67])  # 80018180], 80010100], 00008080
    CNOT2(eng, r[126], r[98], r[81])  # 06020204], 00020204], 06000000
    CNOT2(eng, r[127], r[101], r[86])  # 40602020], 00202020], 40400000
    CNOT2(eng, r[128], r[101], r[92])  # 40206060], 00202020], 40004040
    CNOT2(eng, r[129], r[104], r[10])  # 02000602], 02000202], 00000400
    CNOT2(eng, r[130], r[104], r[77])  # 03010202], 02000202], 01010000
    CNOT2(eng, r[131], r[105], r[69])  # 04060202], 04040002], 00020200
    CNOT2(eng, r[132], r[106], r[2])  # 0404000c], 04040008], 00000004
    CNOT2(eng, r[133], r[107], r[68])  # 08011108], 08001008], 00010100
    CNOT2(eng, r[134], r[108], r[29])  # 30001010], 10001010], 20000000
    CNOT2(eng, r[135], r[108], r[102])  # 10213110], 10001010], 00212100
    CNOT2(eng, r[136], r[109], r[100])  # 19080811], 11000011], 08080800
    CNOT2(eng, r[137], r[110], r[109])  # 01100031], 10100020], 11000011
    CNOT2(eng, r[138], r[111], r[21])  # 11310000], 11110000], 00200000
    CNOT2(eng, r[139], r[111], r[99])  # 11190808], 11110000], 00080808
    CNOT2(eng, r[140], r[112], r[73])  # 20204060], 20004020], 00200040
    CNOT2(eng, r[141], r[112], r[75])  # 20406020], 20004020], 00402000
    CNOT2(eng, r[142], r[113], r[94])  # 404081c1], 40400040], 00008181
    CNOT2(eng, r[143], r[114], r[93])  # 40c0c080], 40404000], 00808080
    CNOT2(eng, r[144], r[115], r[76])  # 81808001], 80808000], 01000001
    CNOT2(eng, r[145], r[115], r[94])  # 80800181], 80808000], 00008181
    CNOT2(eng, r[146], r[115], r[97])  # 00818100], 80808000], 80010100
    CNOT2(eng, r[147], r[116], r[103])  # 81c14040], 80c00000], 01014040
    CNOT2(eng, r[148], r[117], r[110])  # 10102131], 00002111], 10100020
    CNOT2(eng, r[149], r[118], r[107])  # 08081119], 00080111], 08001008
    CNOT2(eng, r[150], r[128], r[112])  # 60202040], 40206060], 20004020
    CNOT2(eng, r[151], r[129], r[18])  # 02040602], 02000602], 00040000
    CNOT2(eng, r[152], r[129], r[98])  # 02020406], 02000602], 00020204
    CNOT2(eng, r[153], r[130], r[78])  # 01010203], 03010202], 02000001
    CNOT2(eng, r[154], r[132], r[11])  # 0404080c], 0404000c], 00000800
    CNOT2(eng, r[155], r[132], r[91])  # 0c040408], 0404000c], 08000404
    CNOT2(eng, r[156], r[133], r[72])  # 08111908], 08011108], 00100800
    CNOT2(eng, r[157], r[137], r[134])  # 31101021], 01100031], 30001010
    CNOT2(eng, r[158], r[138], r[134])  # 21311010], 11310000], 30001010
    CNOT2(eng, r[159], r[144], r[143])  # c1404081], 81808001], 40c0c080
    CNOT2(eng, r[160], r[146], r[92])  # 4081c140], 00818100], 40004040

    out = []
    out.append(r[122])
    out.append(r[147])
    out.append(r[127])
    out.append(r[158])
    out.append(r[139])
    out.append(r[121])
    out.append(r[131])
    out.append(r[123])

    out.append(r[125])
    out.append(r[160])
    out.append(r[141])
    out.append(r[135])
    out.append(r[156])
    out.append(r[120])
    out.append(r[151])
    out.append(r[119])

    # out.append(r[143])
    out.append(r[145])  ##
    out.append(r[142])  ##
    out.append(r[140])  ##
    out.append(r[148])
    out.append(r[149])
    out.append(r[154])
    out.append(r[152])
    out.append(r[153])

    out.append(r[144])
    out.append(r[159])
    out.append(r[150])
    out.append(r[157])
    out.append(r[136])
    out.append(r[155])
    out.append(r[126])
    out.append(r[124])  ##

    oout = []
    for i in range(8):
        oout.append(out[24 + i])
    for i in range(8):
        oout.append(out[16 + i])
    for i in range(8):
        oout.append(out[8 + i])
    for i in range(8):
        oout.append(out[i])

    return oout
    
def Peerj_mc(eng, x_in):

    t = eng.allocate_qureg(100)
    y = eng.allocate_qureg(100)

    x = []
    for i in range(8):
        x.append(x_in[24 + i])
    for i in range(8):
        x.append(x_in[16 + i])
    for i in range(8):
        x.append(x_in[8 + i])
    for i in range(8):
        x.append(x_in[i])

    CNOT2(eng, t[0], x[15], x[23])
    CNOT4(eng, y[31], x[6], x[7], x[30], t[0])
    CNOT4(eng, y[7], x[6], x[14], x[31], t[0])
    CNOT4(eng, y[8], x[0], x[16], x[24], t[0])
    CNOT2(eng, t[4], x[7], x[15])
    CNOT4(eng, y[15], x[6], x[22], y[7], t[4])
    CNOT4(eng, y[0], x[8], x[16], x[24], t[4])
    CNOT4(eng, y[23], x[22], x[31], x[30], t[4])
    CNOT4(eng, t[8], x[0], x[15], x[24], x[31])
    CNOT2(eng, y[24], y[0], t[8])
    CNOT3(eng, y[16], x[8], t[0], t[8])
    CNOT4(eng, t[11], x[3], x[11], x[26], x[31])
    CNOT4(eng, y[27], x[2], x[7], x[19], t[11])
    CNOT4(eng, y[19], x[18], x[23], x[27], t[11])
    CNOT4(eng, t[14], x[4], x[12], x[27], x[31])
    CNOT4(eng, y[20], x[19], x[23], x[28], t[14])
    CNOT4(eng, y[28], x[3], x[7], x[20], t[14])
    CNOT2(eng, t[17], x[2], x[10])
    CNOT4(eng, y[26], x[1], x[18], x[25], t[17])
    CNOT4(eng, y[18], x[17], x[25], x[26], t[17])
    CNOT4(eng, t[20], x[1], x[9], x[17], x[25])
    CNOT4(eng, y[10], x[10], x[26], y[26], t[20])
    CNOT4(eng, y[25], x[25], t[4], t[8], t[20])
    CNOT4(eng, y[2], x[2], x[18], y[18], t[20])
    CNOT3(eng, t[24], x[11], x[20], x[28])
    CNOT4(eng, y[12], x[4], x[19], t[0], t[24])
    CNOT4(eng, y[4], x[3], x[12], t[4], t[24])
    CNOT3(eng, t[27], x[0], x[8], t[20])
    CNOT4(eng, y[17], x[16], x[17], y[16], t[27])
    CNOT3(eng, y[1], x[1], t[4], t[27])
    CNOT4(eng, y[9], x[9], x[24], y[8], t[27])
    CNOT3(eng, t[31], x[6], x[14], x[29])
    CNOT3(eng, y[22], x[21], x[30], t[31])
    CNOT3(eng, y[30], x[5], x[22], t[31])
    CNOT4(eng, t[34], x[5], x[13], x[21], x[29])
    CNOT4(eng, y[14], x[14], x[30], y[30], t[34])
    CNOT4(eng, y[21], x[11], x[21], t[24], t[34])
    CNOT4(eng, y[13], x[13], x[12], x[20], t[34])
    CNOT4(eng, y[6], x[6], x[22], y[22], t[34])
    CNOT4(eng, y[5], x[4], x[5], x[12], t[34])
    CNOT4(eng, y[29], x[4], x[29], x[28], t[34])
    CNOT2(eng, t[41], t[4], t[17])
    CNOT4(eng, y[11], x[3], y[27], y[19], t[41])
    CNOT4(eng, y[3], x[11], x[27], x[19], t[41])

    y_out = []
    for i in range(8):
        y_out.append(y[24 + i])
    for i in range(8):
        y_out.append(y[16 + i])
    for i in range(8):
        y_out.append(y[8 + i])
    for i in range(8):
        y_out.append(y[i])

    return y_out

def CNOT2(eng, a, b, c):
    CNOT | (b, a)
    CNOT | (c, a)

def CNOT3(eng, a, b, c, d):
    CNOT | (b, a)
    CNOT | (c, a)
    CNOT | (d, a)

def CNOT4(eng, a, b, c, d, e):
    CNOT | (b, a)
    CNOT | (c, a)
    CNOT | (d, a)
    CNOT | (e, a)

def CNOT2_euro(eng, a, b, c):
    CNOT | (a, c)
    CNOT | (b, c)

def print_qubit(eng, a):
    All(Measure) | a
    for i in range(len(a)):
        print(int(a[i], end=''))
    print('\n')

def Round_constant_XOR(eng, k, rc, bit):
    for i in range(bit):
        if (rc >> i & 1):
            X | k[i]

def print_input(eng, b, k):
    All(Measure) | b
    All(Measure) | k
    print('Plaintext : 0x', end='')
    print_hex(eng, b)
    print('\nKey : 0x', end='')
    print_hex(eng, k)
    print('\n')

def print_state(eng, b, n):
    All(Measure) | b
    print('0x', end='')
    print_hex(eng, b, n)
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
main(eng)
eng.flush()

resource_check = 1
Resource = ResourceCounter()
eng = MainEngine(Resource)
main(eng)
print(Resource)