from projectq.ops import H, CNOT, Measure, Toffoli, X, All, Swap, Z, T, Tdagger, S, Tdag
from projectq import MainEngine
from projectq.backends import ResourceCounter, ClassicalSimulator, IBMBackend
from projectq.meta import Loop, Compute, Uncompute, Control

def Sbox(eng):

    n = 8
    a = eng.allocate_qureg(n) # input
    s = eng.allocate_qureg(n) # output

    # Ancilla qubits
    y = eng.allocate_qureg(100)  #
    t = eng.allocate_qureg(100)  #
    z = eng.allocate_qureg(100)  #

    if(resource_check != 1):
        Round_constant_XOR(eng, a, 0xff, n)

    s = Sbox_bp10(eng, a, y, t, z, s)

    if (resource_check != 1):
        print('Sbox: ')
        All(Measure) | s
        for i in range(8):
            print(int(s[n - 1 - i]), end=' ')

def Sbox_bp10(eng, x_in, y, t, z, s):
    x = []
    x.append(x_in[7])
    x.append(x_in[6])
    x.append(x_in[5])
    x.append(x_in[4])
    x.append(x_in[3])
    x.append(x_in[2])
    x.append(x_in[1])
    x.append(x_in[0])

    CNOT | (x[3], y[13])
    CNOT | (x[5], y[13])

    CNOT | (x[0], y[12])
    CNOT | (x[6], y[12])

    CNOT | (x[0], y[8])
    CNOT | (x[3], y[8])

    CNOT | (x[0], y[7])
    CNOT | (x[5], y[7])

    CNOT | (x[1], t[0])
    CNOT | (x[2], t[0])

    CNOT | (t[0], y[0])
    CNOT | (x[7], y[0])

    CNOT | (y[0], y[3])
    CNOT | (x[3], y[3])

    CNOT | (y[12], y[11])
    CNOT | (y[13], y[11])

    CNOT | (y[0], y[1])
    CNOT | (x[0], y[1])

    CNOT | (y[0], y[4])
    CNOT | (x[6], y[4])

    CNOT | (y[4], y[2])
    CNOT | (y[7], y[2])

    CNOT | (x[4], t[1])
    CNOT | (y[11], t[1])

    CNOT | (t[1], y[14])
    CNOT | (x[5], y[14])

    CNOT | (t[1], y[19])
    CNOT | (x[1], y[19])

    CNOT | (y[14], y[5])
    CNOT | (x[7], y[5])

    CNOT | (y[14], y[9])
    CNOT | (t[0], y[9])

    CNOT | (y[19], y[10])
    CNOT | (y[8], y[10])

    CNOT | (x[7], y[6])
    CNOT | (y[10], y[6])

    CNOT | (y[9], y[16])
    CNOT | (y[10], y[16])

    CNOT | (y[9], y[18])
    CNOT | (y[7], y[18])

    CNOT | (t[0], y[15])
    CNOT | (y[10], y[15])

    CNOT | (y[12], y[20])
    CNOT | (y[15], y[20])

    CNOT | (x[0], y[17])
    CNOT | (y[15], y[17])

    #####################
    Toffoli_gate(eng, y[11], y[14], t[2])
    Toffoli_gate(eng, y[2], y[5], t[3])
    CNOT2(eng, t[3], t[2], t[4])

    Toffoli_gate(eng, y[3], x[7], t[5])
    CNOT2(eng, t[5], t[2], t[6])
    Toffoli_gate(eng, y[12], y[15], t[7])

    Toffoli_gate(eng, y[4], y[0], t[8])
    CNOT2(eng, t[8], t[7], t[9])
    Toffoli_gate(eng, y[1], y[6], t[10])

    CNOT2(eng, t[10], t[7], t[11])
    Toffoli_gate(eng, y[8], y[10], t[12])
    Toffoli_gate(eng, y[13], y[16], t[13])

    CNOT2(eng, t[13], t[12], t[14])
    Toffoli_gate(eng, y[7], y[9], t[15])
    CNOT2(eng, t[15], t[12], t[16])

    CNOT2(eng, t[4], t[14], t[17])
    CNOT2(eng, t[6], t[16], t[18])
    CNOT2(eng, t[9], t[14], t[19])

    CNOT2(eng, t[11], t[16], t[20])
    CNOT2(eng, t[17], y[19], t[21])
    CNOT2(eng, t[18], y[18], t[22])

    CNOT2(eng, t[19], y[20], t[23])
    CNOT2(eng, t[20], y[17], t[24])
    #######################

    CNOT2(eng, t[21], t[22], t[25])
    Toffoli_gate(eng, t[21], t[23], t[26])
    CNOT2(eng, t[24], t[26], t[27])

    Toffoli_gate(eng, t[25], t[27], t[28])
    CNOT2(eng, t[28], t[22], t[29])
    CNOT2(eng, t[23], t[24], t[30])

    CNOT2(eng, t[22], t[26], t[31])
    Toffoli_gate(eng, t[31], t[30], t[32])
    CNOT2(eng, t[32], t[24], t[33])

    CNOT2(eng, t[23], t[33], t[34])
    CNOT2(eng, t[27], t[33], t[35])
    Toffoli_gate(eng, t[24], t[35], t[36])

    CNOT2(eng, t[36], t[34], t[37])
    CNOT2(eng, t[27], t[36], t[38])
    Toffoli_gate(eng, t[29], t[38], t[39])

    CNOT2(eng, t[25], t[39], t[40])
    #########################

    CNOT2(eng, t[40], t[37], t[41])
    CNOT2(eng, t[29], t[33], t[42])
    CNOT2(eng, t[29], t[40], t[43])

    CNOT2(eng, t[33], t[37], t[44])
    CNOT2(eng, t[42], t[41], t[45])
    Toffoli_gate(eng, t[44], y[14], z[0])

    Toffoli_gate(eng, t[37], y[5], z[1])
    Toffoli_gate(eng, t[33], x[7], z[2])
    Toffoli_gate(eng, t[43], y[15], z[3])

    Toffoli_gate(eng, t[40], y[0], z[4])
    Toffoli_gate(eng, t[29], y[6], z[5])
    Toffoli_gate(eng, t[42], y[10], z[6])

    Toffoli_gate(eng, t[45], y[16], z[7])
    Toffoli_gate(eng, t[41], y[9], z[8])
    Toffoli_gate(eng, t[44], y[11], z[9])

    Toffoli_gate(eng, t[37], y[2], z[10])
    Toffoli_gate(eng, t[33], y[3], z[11])
    Toffoli_gate(eng, t[43], y[12], z[12])

    Toffoli_gate(eng, t[40], y[4], z[13])
    Toffoli_gate(eng, t[29], y[1], z[14])
    Toffoli_gate(eng, t[42], y[8], z[15])

    Toffoli_gate(eng, t[45], y[13], z[16])
    Toffoli_gate(eng, t[41], y[7], z[17])
    ##########################

    CNOT2(eng, z[15], z[16], t[46])
    CNOT2(eng, z[10], z[11], t[47])
    CNOT2(eng, z[5], z[13], t[48])

    CNOT2(eng, z[9], z[10], t[49])
    CNOT2(eng, z[2], z[12], t[50])
    CNOT2(eng, z[2], z[5], t[51])

    CNOT2(eng, z[7], z[8], t[52])
    CNOT2(eng, z[0], z[3], t[53])
    CNOT2(eng, z[6], z[7], t[54])

    CNOT2(eng, z[16], z[17], t[55])
    CNOT2(eng, z[12], t[48], t[56])
    CNOT2(eng, t[50], t[53], t[57])

    CNOT2(eng, z[4], t[46], t[58])
    CNOT2(eng, z[3], t[54], t[59])
    CNOT2(eng, t[46], t[57], t[60])

    CNOT2(eng, z[14], t[57], t[61])
    CNOT2(eng, t[52], t[58], t[62])
    CNOT2(eng, t[49], t[58], t[63])

    CNOT2(eng, z[4], t[59], t[64])
    CNOT2(eng, t[61], t[62], t[65])
    CNOT2(eng, z[1], t[63], t[66])

    CNOT2(eng, t[59], t[63], s[7])
    CNOT2(eng, t[56], t[62], s[1])
    X | s[1]
    CNOT2(eng, t[48], t[60], s[0])
    X | s[0]

    CNOT2(eng, t[64], t[65], t[67])
    CNOT2(eng, t[53], t[66], s[4])
    CNOT2(eng, t[51], t[66], s[3])

    CNOT2(eng, t[47], t[65], s[2])
    CNOT2(eng, t[64], s[4], s[6])

    X | s[6]
    CNOT2(eng, t[55], t[67], s[5])
    X | s[5]



    return s

def CNOT2(eng, a, b, c):
    CNOT | (a, c)
    CNOT | (b, c)

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

global resource_check

resource_check = 0
Resource = ClassicalSimulator()
eng = MainEngine(Resource)
Sbox(eng)
eng.flush()
print()

resource_check = 1
Resource = ResourceCounter()
eng = MainEngine(Resource)
Sbox(eng)
print(Resource)
eng.flush()