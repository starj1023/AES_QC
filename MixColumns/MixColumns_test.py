from projectq import MainEngine
from projectq.ops import H, CNOT, Measure, Toffoli, X, All, Swap
from projectq.backends import ResourceCounter, ClassicalSimulator
from projectq.meta import Loop, Compute, Uncompute, Control


def main(eng):
    x0 = eng.allocate_qureg(32)

    x1 = eng.allocate_qureg(32)
    t1 = eng.allocate_qureg(150)
    y1 = eng.allocate_qureg(32)

    x2 = eng.allocate_qureg(32)
    t2 = eng.allocate_qureg(150)
    y2 = eng.allocate_qureg(32)

    x3 = eng.allocate_qureg(32)
    t3 = eng.allocate_qureg(150)
    y3 = eng.allocate_qureg(32)

    x4 = eng.allocate_qureg(32)
    t4 = eng.allocate_qureg(150)
    y4 = eng.allocate_qureg(32)

    x5 = eng.allocate_qureg(32)
    t5 = eng.allocate_qureg(150)
    y5 = eng.allocate_qureg(32)

    x6 = eng.allocate_qureg(32)
    t6 = eng.allocate_qureg(150)
    y6 = eng.allocate_qureg(32)

    x7 = eng.allocate_qureg(32)
    t7 = eng.allocate_qureg(150)
    y7 = eng.allocate_qureg(32)

    out1 = []
    out2 = []
    out3 = []
    out4 = []
    out5 = []

    x_naive = eng.allocate_qureg(32)
    x_naive2 = eng.allocate_qureg(32)
    x_euro = eng.allocate_qureg(32)
    out_naive2 = eng.allocate_qureg(32)
    x_eprint = eng.allocate_qureg(32)

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
        Round_constant_XOR(eng, x_naive2, 0xcd38df63, 32)
        Round_constant_XOR(eng, x_euro, 0xcd38df63, 32)
        Round_constant_XOR(eng, x_eprint, 0xcd38df63, 32)

    #x0 = Mixcolumns(eng, x0) # Ours [56]
    # y1 = AES_97xor(eng, x1, y1, t1) # [41]
    # y2 = XOR94(eng, x2, t2, y2)  # [53]
    # out1 = XOR105_newnew(eng, x3, t3) #[44] # MixColumn From Baksi's email
    # out2 = IP_mc(eng, x4) #[38]
    # out3 = Maxi_mc(eng, x5, t4)  # [47] CNOT: 184, qubits 124, depth 16 --> CNOT 188, qubits 126, depth 13 (Need to edit overleaf)
    # out4 = AES_MC5(eng, t5, x6) #[46] # Towards Low-Latency Implementation of LinearLayers
    # out5 = AES_MC_Song(eng, t6, x7) #[45]
    # Euro_plu_mix(eng, x_euro)
    # out_naive = []
    # out_naive = mix_naive(eng, x_naive)
    # out_naive2 = Mix_naive_2(eng, x_naive2, out_naive2)
    out_zhu_eprint = []
    out_zhu_eprint = zhu_eprint(eng, x_eprint)

    if (not resource_check):
        #print('resource_c')
        #print("AES_ours[56]")
        #print_state(eng, x0, 8)

        # print("AES_97xor[41]")
        # print_state(eng, y1, 8)

        # print("94xor[53]")
        # print_state(eng, y2, 8)

        # print("105xor[44]")
        # print_state(eng, out1, 8)

        # print("IP_mc[38]")
        # print_state(eng, out2, 8)

        # print("Maxi_mc[47]")
        # print_state(eng, out3, 8)

        # print("new_mix [46]")
        # print_state(eng, out4, 8)

        # print("Mix_Song [45]")
        # print_state(eng, out5, 8)

        # print("Mix_naive")
        # print_state(eng, out_naive, 8)

        #print("Mix_naive2")
        #print_state(eng, out_naive2, 8)

        print("Mix_eprint_zhu")
        print_state(eng, out_zhu_eprint, 8)


def AES_97xor(eng, x_in, y, t):

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

def XOR94(eng, x_in, t, y):

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

def XOR105_newnew(eng, x_in, t):
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
    CNOT2(eng, t[100], x[18], x[26])
    CNOT2(eng, t[101], t[95], t[100])
    CNOT2(eng, t[102], t[96], t[101])  # y19  (3)
    CNOT2(eng, t[103], x[19], x[28])
    CNOT2(eng, t[104], t[15], t[103])
    CNOT2(eng, t[105], t[96], t[104])  # y20  (3)

    out = []

    #out.append(t[25])
    #out.append(t[50])
    #out.append(t[43])
    #out.append(t[94])

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


def zhu_eprint(eng, x_in): # 1은 0 절대 아님 + 1은 8 절대 아님 + 1은 16 절대 아님

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
    '''
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
    '''
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

def AES_MC5(eng, t, x_in):
    x = []
    for i in range(8):
        x.append(x_in[24 + i])
    for i in range(8):
        x.append(x_in[16 + i])
    for i in range(8):
        x.append(x_in[8 + i])
    for i in range(8):
        x.append(x_in[0 + i])


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

def AES_MC_Song(eng, t, x_in):

    x = []
    for i in range(8):
        x.append(x_in[24 + i])
    for i in range(8):
        x.append(x_in[16 + i])
    for i in range(8):
        x.append(x_in[8 + i])
    for i in range(8):
        x.append(x_in[0 + i])

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

#  7 6 5 4 3 2 1 0
#  6 5 4 3 2 1 0
#        7 7   7 7
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
        x0.append(x[i+24])
        x1.append(x[i+16])
        x2.append(x[i+8])
        x3.append(x[i])

    y0 = eng.allocate_qureg(8)
    y1 = eng.allocate_qureg(8)
    y2 = eng.allocate_qureg(8)
    y3 = eng.allocate_qureg(8)

    #first row
    mx_02(eng, x0, y0)
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
    x2 = []
    #x = in_x

    #for i in range(32):
    #    x2.append(in_x[31-i])

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


def CNOT2(eng, a, b, c):
    CNOT | (b, a)
    CNOT | (c, a)

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