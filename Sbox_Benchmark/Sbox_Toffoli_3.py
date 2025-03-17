from projectq.ops import H, CNOT, Measure, Toffoli, X, All, Swap, Z, T, Tdagger, S, Tdag, Sdag
from projectq import MainEngine
from projectq.backends import ResourceCounter, ClassicalSimulator, IBMBackend
from projectq.meta import Loop, Compute, Uncompute, Control, Dagger

def Sbox(eng):

    n = 8
    a = eng.allocate_qureg(n) # input
    s = eng.allocate_qureg(n) # output

    a1 = eng.allocate_qureg(n)  # input
    s1 = eng.allocate_qureg(n)  # output

    # Ancilla qubits
    y = eng.allocate_qureg(27)  # 27 * 20
    t = eng.allocate_qureg(50)  # 50 * 20
    z = eng.allocate_qureg(41)  # 41 * 20
    w = eng.allocate_qureg(34)  # 34 * 20
    l = eng.allocate_qureg(30)  # 30 * 20

    y1 = eng.allocate_qureg(27)  # 27 * 20
    t1 = eng.allocate_qureg(50)  # 50 * 20
    z1 = eng.allocate_qureg(41)  # 41 * 20
    w1 = eng.allocate_qureg(34)  # 34 * 20
    l1 = eng.allocate_qureg(30)  # 30 * 20

    and_ancilla = eng.allocate_qureg(20)

    if(resource_check != 1):
        Round_constant_XOR(eng, a, 0xff, n)

    round = 1

    s = Sbox_T3(eng, a, y, t, z, w, l, s, round)
    #s1 = AND_Sbox_T3(eng, a1, y1, t1, z1, w1, l1, s1, and_ancilla, round)

    if (resource_check != 1):
        print('Sbox: ')
        All(Measure) | s
        for i in range(8):
            print(int(s[n - 1 - i]), end=' ')
            print(int(s1[n - 1 - i]), end=' ')

def Sbox_T3(eng, u_in, t, m, n, w, l, s, round):

    u = []
    for i in range(8):
        u.append(u_in[7 - i])
    with Compute(eng):
        CNOT2(eng, u[0], u[3], t[1 - 1])
        CNOT2(eng, u[0], u[5], t[2 - 1])
        CNOT2(eng, u[0], u[6], t[3 - 1])
        CNOT2(eng, u[3], u[5], t[4 - 1])
        CNOT2(eng, u[4], u[6], t[5 - 1])
        CNOT2(eng, t[1 - 1], t[5 - 1], t[6 - 1])
        CNOT2(eng, u[1], u[2], t[7 - 1])
        CNOT2(eng, u[7], t[6 - 1], t[8 - 1])
        CNOT2(eng, u[7], t[7 - 1], t[9 - 1])
        CNOT2(eng, t[6 - 1], t[7 - 1], t[10 - 1])
        CNOT2(eng, u[1], u[5], t[11 - 1])
        CNOT2(eng, u[2], u[5], t[12 - 1])
        CNOT2(eng, t[3 - 1], t[4 - 1], t[13 - 1])
        CNOT2(eng, t[6 - 1], t[11 - 1], t[14 - 1])
        CNOT2(eng, t[5 - 1], t[11 - 1], t[15 - 1])
        CNOT2(eng, t[5 - 1], t[12 - 1], t[16 - 1])
        CNOT2(eng, t[9 - 1], t[16 - 1], t[17 - 1])
        CNOT2(eng, u[3], u[7], t[18 - 1])
        CNOT2(eng, t[7 - 1], t[18 - 1], t[19 - 1])
        CNOT2(eng, t[1 - 1], t[19 - 1], t[20 - 1])
        CNOT2(eng, u[6], u[7], t[21 - 1])
        CNOT2(eng, t[7 - 1], t[21 - 1], t[22 - 1])
        CNOT2(eng, t[2 - 1], t[22 - 1], t[23 - 1])
        CNOT2(eng, t[2 - 1], t[10 - 1], t[24 - 1])
        CNOT2(eng, t[20 - 1], t[17 - 1], t[25 - 1])
        CNOT2(eng, t[3 - 1], t[16 - 1], t[26 - 1])
        CNOT2(eng, t[1 - 1], t[12 - 1], t[27 - 1])

        Toffoli_gate(eng, t[13 - 1], t[6 - 1], m[1 - 1] )
        Toffoli_gate(eng, t[23 - 1], t[8 - 1], m[2 - 1] )
        CNOT2(eng, t[14 - 1], m[1 - 1], m[3 - 1])
        Toffoli_gate(eng, t[19 - 1], u[7], m[4 - 1] )
        CNOT2(eng, m[4 - 1], m[1 - 1], m[5 - 1])
        Toffoli_gate(eng, t[3 - 1], t[16 - 1], m[6 - 1] )
        Toffoli_gate(eng, t[22 - 1], t[9 - 1], m[7 - 1] )
        CNOT2(eng, t[26 - 1], m[6 - 1], m[8 - 1])
        Toffoli_gate(eng, t[20 - 1], t[17 - 1], m[9 - 1] )
        CNOT2(eng, m[9 - 1], m[6 - 1], m[10 - 1])
        Toffoli_gate(eng, t[1 - 1], t[15 - 1], m[11 - 1] )
        Toffoli_gate(eng, t[4 - 1], t[27 - 1], m[12 - 1] )
        CNOT2(eng, m[12 - 1], m[11 - 1], m[13 - 1])
        Toffoli_gate(eng, t[2 - 1], t[10 - 1], m[14 - 1] )
        CNOT2(eng, m[14 - 1], m[11 - 1], m[15 - 1])
        CNOT2(eng, m[3 - 1], m[2 - 1], m[16 - 1])
        CNOT2(eng, m[5 - 1], t[24 - 1], m[17 - 1])
        CNOT2(eng, m[8 - 1], m[7 - 1], m[18 - 1])
        CNOT2(eng, m[10 - 1], m[15 - 1], m[19 - 1])
        CNOT2(eng, m[16 - 1], m[13 - 1], m[20 - 1])
        CNOT2(eng, m[17 - 1], m[15 - 1], m[21 - 1])
        CNOT2(eng, m[18 - 1], m[13 - 1], m[22 - 1])
        CNOT2(eng, m[19 - 1], t[25 - 1], m[23 - 1])
        CNOT2(eng, m[22 - 1], m[23 - 1], m[24 - 1])

        # ** ** ** ** ** ** *Layer

        # 41

        CNOT | (u[7], m[33 - 1])
        CNOT | (t[1 - 1], m[34 - 1])
        CNOT | (t[1 - 1], m[35 - 1])
        CNOT | (t[2 - 1], m[36 - 1])
        CNOT | (t[4 - 1], m[37 - 1])
        CNOT | (t[10 - 1], m[38 - 1])
        CNOT | (t[15 - 1], m[39 - 1])
        CNOT | (t[15 - 1], m[40 - 1])
        CNOT2(eng, m[20 - 1], m[21 - 1], m[27 - 1])
        CNOT | (t[17 - 1], m[41 - 1])
        CNOT | (t[19 - 1], m[42 - 1])
        CNOT | (t[20 - 1], m[43 - 1])
        CNOT | (t[27 - 1], m[44 - 1])
        CNOT | (m[20 - 1], m[45 - 1])
        CNOT | (m[21 - 1], m[46 - 1])
        CNOT | (m[21 - 1], m[47 - 1])
        CNOT | (m[22 - 1], m[48 - 1])
        CNOT | (m[23 - 1], m[49 - 1])
        CNOT | (m[23 - 1], m[50 - 1])

        CNOT | (m[24 - 1], l[1 - 1])

        CNOT | (m[24 - 1], l[2 - 1])

        CNOT2(eng, m[21 - 1], m[23 - 1], n[15 - 1])

        CNOT | (m[24 - 1], l[3 - 1])
        CNOT | (l[1 - 1], l[4 - 1])
        CNOT | (l[2 - 1], l[5 - 1])
        CNOT | (m[24 - 1], l[6 - 1])
        CNOT | (l[1 - 1], l[7 - 1])
        CNOT | (l[2 - 1], l[8 - 1])
        CNOT | (l[3 - 1], l[9 - 1])
        CNOT | (l[4 - 1], l[10 - 1])
        CNOT | (l[5 - 1], l[11 - 1])

        CNOT | (m[27 - 1], l[12 - 1])
        CNOT | (m[27 - 1], l[13 - 1])
        CNOT | (m[27 - 1], l[14 - 1])
        CNOT | (l[12 - 1], l[15 - 1])
        CNOT | (l[13 - 1], l[16 - 1])
        CNOT | (m[27 - 1], l[17 - 1])
        CNOT | (l[12 - 1], l[18 - 1])
        CNOT | (l[13 - 1], l[19 - 1])
        CNOT | (l[14 - 1], l[20 - 1])
        CNOT | (l[15 - 1], l[21 - 1])
        CNOT | (l[16 - 1], l[22 - 1])

        CNOT | (n[15 - 1], l[23 - 1])

        # # # # # # # # # # # # # # # # # # # # # # # /

        Toffoli_gate(eng, m[22 - 1], m[20 - 1], m[25 - 1] )

        CNOT2(eng, m[23 - 1], m[25 - 1], m[28 - 1])

        CNOT2(eng, m[21 - 1], m[25 - 1], m[26 - 1])

        Toffoli_gate(eng, m[45 - 1], m[23 - 1], m[29 - 1] )
        CNOT2(eng, m[27 - 1], m[25 - 1], m[30 - 1])

        Toffoli_gate(eng, m[21 - 1], m[48 - 1], m[31 - 1] )
        CNOT2(eng, m[24 - 1], m[25 - 1], m[32 - 1])

        # Toffoli_gate(eng, m[28 - 1], m[27 - 1], m[29 - 1])
        # Toffoli_gate(eng, m[26 - 1], m[24 - 1], m[30 - 1])
        # Toffoli_gate(eng, l[2], m[29 - 1], m[32 - 1])
        # Toffoli_gate(eng, l[3], m[31 - 1], m[35 - 1])

        Toffoli_gate(eng, m[24 - 1], t[6 - 1], n[1 - 1] )  # 2
        CNOT2(eng, m[23 - 1], m[32 - 1], n[2 - 1])
        CNOT2(eng, m[26 - 1], m[31 - 1], n[3 - 1])

        Toffoli_gate(eng, l[1 - 1], t[8 - 1], n[4 - 1] )  # 2

        Toffoli_gate(eng, l[2 - 1], u[7], n[6 - 1] )  # 2
        Toffoli_gate(eng, m[49 - 1], m[33 - 1], n[7 - 1] )  # 2

        CNOT2(eng, m[21 - 1], m[30 - 1], n[8 - 1])
        CNOT2(eng, m[28 - 1], m[29 - 1], n[9 - 1])
        Toffoli_gate(eng, m[27 - 1], t[16 - 1], n[10 - 1] )  # 2

        Toffoli_gate(eng, l[12 - 1], t[9 - 1], n[11 - 1] )  # 2

        Toffoli_gate(eng, m[46 - 1], t[17 - 1], n[13 - 1] )  # 2
        Toffoli_gate(eng, l[13 - 1], m[41 - 1], n[14 - 1] )  # 2

        # ** ** ** ** ** ** ** ** ** ** ** ** ** **

        Toffoli_gate(eng, l[14 - 1], t[15 - 1], n[16 - 1] )  # 2
        Toffoli_gate(eng, l[3 - 1], m[39 - 1], n[17 - 1] )  # 2
        Toffoli_gate(eng, n[15 - 1], m[40 - 1], w[9 - 1] )  # 2

        CNOT2(eng, m[30 - 1], m[32 - 1], n[18 - 1])
        CNOT2(eng, n[15 - 1], n[18 - 1], n[19 - 1])
        CNOT2(eng, m[28 - 1], m[29 - 1], n[20 - 1])
        CNOT2(eng, m[26 - 1], m[31 - 1], n[21 - 1])
        Toffoli_gate(eng, l[15 - 1], t[27 - 1], n[22 - 1] )  # 2
        Toffoli_gate(eng, l[4 - 1], m[44 - 1], n[23 - 1] )  # 2

        Toffoli_gate(eng, l[16 - 1], t[10 - 1], n[24 - 1] )  # 2
        Toffoli_gate(eng, l[5 - 1], m[38 - 1], n[25 - 1] )  # 2

        Toffoli_gate(eng, l[6 - 1], t[13 - 1], n[26 - 1] )  # 2

        Toffoli_gate(eng, l[7 - 1], t[23 - 1], n[27 - 1] )  # 2

        Toffoli_gate(eng, l[8 - 1], t[19 - 1], n[29 - 1] )  # 2
        Toffoli_gate(eng, m[50 - 1], m[42 - 1], n[30 - 1] )  # 2

        Toffoli_gate(eng, l[17 - 1], t[3 - 1], n[31 - 1] )  # 2

        Toffoli_gate(eng, l[18 - 1], t[22 - 1], n[32 - 1] )  # 2

        Toffoli_gate(eng, m[47 - 1], t[20 - 1], n[34 - 1] )  # 2
        Toffoli_gate(eng, l[19 - 1], m[43 - 1], n[35 - 1] )  # 2

        Toffoli_gate(eng, l[20 - 1], t[1 - 1], n[36 - 1] )  # 2
        Toffoli_gate(eng, l[9 - 1], m[34 - 1], n[37 - 1] )  # 2
        Toffoli_gate(eng, l[23 - 1], m[35 - 1], w[26 - 1] )  # 2

        Toffoli_gate(eng, l[21 - 1], t[4 - 1], n[38 - 1] )  # 2
        Toffoli_gate(eng, l[10 - 1], m[37 - 1], n[39 - 1] )  # 2

        Toffoli_gate(eng, l[22 - 1], t[2 - 1], n[40 - 1] )  # 2
        Toffoli_gate(eng, l[11 - 1], m[36 - 1], n[41 - 1] )  # 2

        # Clean

        CNOT | (n[15 - 1], l[23 - 1])
        CNOT | (l[16 - 1], l[22 - 1])
        CNOT | (l[15 - 1], l[21 - 1])
        CNOT | (l[14 - 1], l[20 - 1])
        CNOT | (l[13 - 1], l[19 - 1])
        CNOT | (l[12 - 1], l[18 - 1])
        CNOT | (m[27 - 1], l[17 - 1])
        CNOT | (l[13 - 1], l[16 - 1])
        CNOT | (l[12 - 1], l[15 - 1])
        CNOT | (m[27 - 1], l[14 - 1])
        CNOT | (m[27 - 1], l[13 - 1])
        CNOT | (m[27 - 1], l[12 - 1])
        CNOT | (l[5 - 1], l[11 - 1])
        CNOT | (l[4 - 1], l[10 - 1])
        CNOT | (l[3 - 1], l[9 - 1])
        CNOT | (l[2 - 1], l[8 - 1])
        CNOT | (l[1 - 1], l[7 - 1])
        CNOT | (m[24 - 1], l[6 - 1])
        CNOT | (l[2 - 1], l[5 - 1])
        CNOT | (l[1 - 1], l[4 - 1])
        CNOT | (m[24 - 1], l[3 - 1])
        CNOT | (m[24 - 1], l[2 - 1])
        CNOT | (m[24 - 1], l[1 - 1])

        CNOT | (m[23 - 1], m[50 - 1])
        CNOT | (m[23 - 1], m[49 - 1])
        CNOT | (m[22 - 1], m[48 - 1])
        CNOT | (m[21 - 1], m[47 - 1])
        CNOT | (m[21 - 1], m[46 - 1])
        CNOT | (m[20 - 1], m[45 - 1])
        CNOT | (t[27 - 1], m[44 - 1])
        CNOT | (t[20 - 1], m[43 - 1])
        CNOT | (t[19 - 1], m[42 - 1])
        CNOT | (t[17 - 1], m[41 - 1])
        CNOT | (t[15 - 1], m[40 - 1])
        CNOT | (t[15 - 1], m[39 - 1])
        CNOT | (t[10 - 1], m[38 - 1])
        CNOT | (t[4 - 1], m[37 - 1])
        CNOT | (t[2 - 1], m[36 - 1])
        CNOT | (t[1 - 1], m[35 - 1])
        CNOT | (t[1 - 1], m[34 - 1])
        CNOT | (u[7], m[33 - 1])

        # ** ** ** ** ** ** ** *Layer

        CNOT | (m[26 - 1], l[1 - 1])
        CNOT | (m[26 - 1], l[2 - 1])
        CNOT | (m[26 - 1], l[3 - 1])

        CNOT | (m[28 - 1], l[4 - 1])
        CNOT | (m[28 - 1], l[5 - 1])
        CNOT | (m[28 - 1], l[6 - 1])

        CNOT | (m[29 - 1], l[7 - 1])
        CNOT | (m[29 - 1], l[8 - 1])
        CNOT | (m[29 - 1], l[9 - 1])

        CNOT | (m[30 - 1], l[10 - 1])

        CNOT | (m[31 - 1], l[11 - 1])
        CNOT | (m[31 - 1], l[12 - 1])
        CNOT | (m[31 - 1], l[13 - 1])

        CNOT | (m[32 - 1], l[14 - 1])
        CNOT | (n[2 - 1], l[15 - 1])
        CNOT | (n[3 - 1], l[16 - 1])
        CNOT | (n[8 - 1], l[17 - 1])
        CNOT | (n[9 - 1], l[18 - 1])

        CNOT | (n[18 - 1], l[19 - 1])
        CNOT | (n[19 - 1], l[20 - 1])
        CNOT | (n[20 - 1], l[21 - 1])
        CNOT | (n[21 - 1], l[22 - 1])

        # l22 ~ 29 are idle state

        Toffoli_gate(eng, n[3 - 1], n[1 - 1], w[1 - 1] )  # 3
        Toffoli_gate(eng, n[2 - 1], t[6 - 1], w[2 - 1] )  # 3
        CNOT2(eng, w[1 - 1], w[2 - 1], m[33 - 1])

        Toffoli_gate(eng, m[32 - 1], t[8 - 1], n[5 - 1] )  # 3
        Toffoli_gate(eng, n[4 - 1], m[31 - 1], w[3 - 1] )  # 3
        CNOT2(eng, w[3 - 1], n[5 - 1], m[34 - 1])

        Toffoli_gate(eng, n[6 - 1], m[26 - 1], w[4 - 1] )  # 3
        CNOT2(eng, w[4 - 1], n[7 - 1], m[35 - 1])

        Toffoli_gate(eng, n[8 - 1], t[16 - 1], w[5 - 1] )  # 3
        Toffoli_gate(eng, n[9 - 1], n[10 - 1], w[6 - 1] )  # 3
        CNOT2(eng, w[5 - 1], w[6 - 1], m[36 - 1])

        Toffoli_gate(eng, m[30 - 1], t[9 - 1], n[12 - 1] )  # 3
        Toffoli_gate(eng, m[29 - 1], n[11 - 1], w[7 - 1] )  # 3
        CNOT2(eng, w[7 - 1], n[12 - 1], m[37 - 1])

        Toffoli_gate(eng, m[28 - 1], n[14 - 1], w[8 - 1] )  # 3
        CNOT2(eng, w[8 - 1], n[13 - 1], m[38 - 1])

        Toffoli_gate(eng, n[16 - 1], l[4 - 1], w[10 - 1] )  # 3
        Toffoli_gate(eng, n[17 - 1], l[1 - 1], w[11 - 1] )  # 3
        CNOT2(eng, w[9 - 1], w[10 - 1], m[39 - 1])
        CNOT | (w[11 - 1], m[39 - 1])

        Toffoli_gate(eng, n[19 - 1], t[27 - 1], w[12 - 1] )  # 3
        Toffoli_gate(eng, n[20 - 1], n[22 - 1], w[13 - 1] )  # 3
        Toffoli_gate(eng, n[21 - 1], n[23 - 1], w[14 - 1] )  # 3
        CNOT2(eng, w[12 - 1], w[13 - 1], m[40 - 1])
        CNOT | (w[14 - 1], m[40 - 1])

        Toffoli_gate(eng, l[7 - 1], n[24 - 1], w[15 - 1] )  # 3
        Toffoli_gate(eng, n[18 - 1], t[10 - 1], w[16 - 1] )  # 3
        Toffoli_gate(eng, l[11 - 1], n[25 - 1], w[17 - 1] )  # 3
        CNOT2(eng, w[15 - 1], w[16 - 1], m[41 - 1])
        CNOT | (w[17 - 1], m[41 - 1])

        Toffoli_gate(eng, l[16 - 1], n[26 - 1], w[18 - 1] )  # 3
        Toffoli_gate(eng, l[15 - 1], t[13 - 1], w[19 - 1] )  # 3
        CNOT2(eng, w[18 - 1], w[19 - 1], m[42 - 1])

        Toffoli_gate(eng, l[14 - 1], t[23 - 1], n[28 - 1] )  # 3
        Toffoli_gate(eng, n[27 - 1], l[12 - 1], w[20 - 1] )  # 3
        CNOT2(eng, w[20 - 1], n[28 - 1], m[43 - 1])

        Toffoli_gate(eng, n[29 - 1], l[2 - 1], w[21 - 1] )  # 3
        CNOT2(eng, w[21 - 1], n[30 - 1], m[44 - 1])

        Toffoli_gate(eng, l[17 - 1], t[3 - 1], w[22 - 1] )  # 3
        Toffoli_gate(eng, l[18 - 1], n[31 - 1], w[23 - 1] )  # 3
        CNOT2(eng, w[22 - 1], w[23 - 1], m[45 - 1])

        Toffoli_gate(eng, l[10 - 1], t[22 - 1], n[33 - 1] )  # 3
        Toffoli_gate(eng, l[8 - 1], n[32 - 1], w[24 - 1] )  # 3
        CNOT2(eng, w[24 - 1], n[33 - 1], m[46 - 1])

        Toffoli_gate(eng, l[5 - 1], n[35 - 1], w[25 - 1] )  # 3
        CNOT2(eng, w[25 - 1], n[34 - 1], m[47 - 1])

        Toffoli_gate(eng, n[36 - 1], l[6 - 1], w[27 - 1] )  # 3
        Toffoli_gate(eng, n[37 - 1], l[3 - 1], w[28 - 1] )  # 3

        CNOT2(eng, w[26 - 1], w[27 - 1], m[48 - 1])
        CNOT | (w[28 - 1], m[48 - 1])

        Toffoli_gate(eng, l[20 - 1], t[4 - 1], w[29 - 1] )  # 3
        Toffoli_gate(eng, l[21 - 1], n[38 - 1], w[30 - 1] )  # 3
        Toffoli_gate(eng, l[22 - 1], n[39 - 1], w[31 - 1] )  # 3
        CNOT2(eng, w[29 - 1], w[30 - 1], m[49 - 1])
        CNOT | (w[31 - 1], m[49 - 1])

        Toffoli_gate(eng, l[9 - 1], n[40 - 1], w[32 - 1] )  # 3
        Toffoli_gate(eng, l[19 - 1], t[2 - 1], w[33 - 1] )  # 3
        Toffoli_gate(eng, l[13 - 1], n[41 - 1], w[34 - 1] )  # 3
        CNOT2(eng, w[32 - 1], w[33 - 1], m[50 - 1])
        CNOT | (w[34 - 1], m[50 - 1])

        CNOT | (m[26 - 1], l[1 - 1])
        CNOT | (m[26 - 1], l[2 - 1])
        CNOT | (m[26 - 1], l[3 - 1])

        CNOT | (m[28 - 1], l[4 - 1])
        CNOT | (m[28 - 1], l[5 - 1])
        CNOT | (m[28 - 1], l[6 - 1])

        CNOT | (m[29 - 1], l[7 - 1])
        CNOT | (m[29 - 1], l[8 - 1])
        CNOT | (m[29 - 1], l[9 - 1])

        CNOT | (m[30 - 1], l[10 - 1])

        CNOT | (m[31 - 1], l[11 - 1])
        CNOT | (m[31 - 1], l[12 - 1])
        CNOT | (m[31 - 1], l[13 - 1])

        CNOT | (m[32 - 1], l[14 - 1])
        CNOT | (n[2 - 1], l[15 - 1])
        CNOT | (n[3 - 1], l[16 - 1])
        CNOT | (n[8 - 1], l[17 - 1])
        CNOT | (n[9 - 1], l[18 - 1])

        CNOT | (n[18 - 1], l[19 - 1])
        CNOT | (n[19 - 1], l[20 - 1])
        CNOT | (n[20 - 1], l[21 - 1])
        CNOT | (n[21 - 1], l[22 - 1])

        CNOT2(eng, m[48 - 1], m[49 - 1], l[0])
        CNOT2(eng, m[37 - 1], m[43 - 1], l[1])
        CNOT2(eng, m[33 - 1], m[35 - 1], l[2])
        CNOT2(eng, m[34 - 1], m[42 - 1], l[3])
        CNOT2(eng, m[41 - 1], m[45 - 1], l[4])
        CNOT2(eng, m[36 - 1], m[48 - 1], l[5])
        CNOT2(eng, m[49 - 1], l[5], l[6])
        CNOT2(eng, m[33 - 1], l[3], l[7])
        CNOT2(eng, m[38 - 1], m[46 - 1], l[8])
        CNOT2(eng, m[39 - 1], m[40 - 1], l[9])
        CNOT2(eng, m[40 - 1], l[4], l[10])
        CNOT2(eng, m[47 - 1], l[2], l[11])
        CNOT2(eng, m[35 - 1], m[38 - 1], l[12])
        CNOT2(eng, m[37 - 1], l[0], l[13])
        CNOT2(eng, m[39 - 1], m[48 - 1], l[14])
        CNOT2(eng, m[42 - 1], l[1], l[15])
        CNOT2(eng, m[43 - 1], l[0], l[16])
        CNOT2(eng, m[44 - 1], l[1], l[17])
        CNOT2(eng, m[45 - 1], l[8], l[18])
        CNOT2(eng, m[50 - 1], l[4], l[19])
        CNOT2(eng, l[0], l[1], l[20])
        CNOT2(eng, l[1], l[7], l[21])
        CNOT2(eng, l[3], l[12], l[22])
        CNOT2(eng, l[18], l[2], l[23])
        CNOT2(eng, l[15], l[9], l[24])
        CNOT2(eng, l[6], l[10], l[25])
        CNOT2(eng, l[7], l[9], l[26])
        CNOT2(eng, l[8], l[10], l[27])
        CNOT2(eng, l[11], l[14], l[28])
        CNOT2(eng, l[11], l[17], l[29])

    CNOT2(eng, l[6], l[24], s[7])
    CNOT2(eng, l[16], l[26], s[6])
    X | s[6]
    CNOT2(eng, l[19], l[28], s[5])
    X | s[5]

    CNOT2(eng, l[6], l[21], s[4])
    CNOT2(eng, l[20], l[22], s[3])
    CNOT2(eng, l[25], l[29], s[2])
    CNOT2(eng, l[13], l[27], s[1])
    X | s[1]
    CNOT2(eng, l[6], l[23], s[0])
    X | s[0]

    if (round != 9):
        Uncompute(eng)

    return s

def CNOT2(eng, a, b, c):
    CNOT | (a, c)
    CNOT | (b, c)

def Round_constant_XOR(eng, k, rc, bit):
    for i in range(bit):
        if (rc >> i & 1):
            X | k[i]

def AND_Sbox_T3(eng, u_in, t, m, n, w, l, s, and_ancilla, round):
    u = []
    for i in range(8):
        u.append(u_in[7 - i])

    CNOT2(eng, u[0], u[3], t[1 - 1])
    CNOT2(eng, u[0], u[5], t[2 - 1])
    CNOT2(eng, u[0], u[6], t[3 - 1])
    CNOT2(eng, u[3], u[5], t[4 - 1])
    CNOT2(eng, u[4], u[6], t[5 - 1])
    CNOT2(eng, t[1 - 1], t[5 - 1], t[6 - 1])
    CNOT2(eng, u[1], u[2], t[7 - 1])
    CNOT2(eng, u[7], t[6 - 1], t[8 - 1])
    CNOT2(eng, u[7], t[7 - 1], t[9 - 1])
    CNOT2(eng, t[6 - 1], t[7 - 1], t[10 - 1])
    CNOT2(eng, u[1], u[5], t[11 - 1])
    CNOT2(eng, u[2], u[5], t[12 - 1])
    CNOT2(eng, t[3 - 1], t[4 - 1], t[13 - 1])
    CNOT2(eng, t[6 - 1], t[11 - 1], t[14 - 1])
    CNOT2(eng, t[5 - 1], t[11 - 1], t[15 - 1])
    CNOT2(eng, t[5 - 1], t[12 - 1], t[16 - 1])
    CNOT2(eng, t[9 - 1], t[16 - 1], t[17 - 1])
    CNOT2(eng, u[3], u[7], t[18 - 1])
    CNOT2(eng, t[7 - 1], t[18 - 1], t[19 - 1])
    CNOT2(eng, t[1 - 1], t[19 - 1], t[20 - 1])
    CNOT2(eng, u[6], u[7], t[21 - 1])
    CNOT2(eng, t[7 - 1], t[21 - 1], t[22 - 1])
    CNOT2(eng, t[2 - 1], t[22 - 1], t[23 - 1])
    CNOT2(eng, t[2 - 1], t[10 - 1], t[24 - 1])
    CNOT2(eng, t[20 - 1], t[17 - 1], t[25 - 1])
    CNOT2(eng, t[3 - 1], t[16 - 1], t[26 - 1])
    CNOT2(eng, t[1 - 1], t[12 - 1], t[27 - 1])

    AND_gate(eng, t[13 - 1], t[6 - 1], m[1 - 1], and_ancilla[0])
    AND_gate(eng, t[23 - 1], t[8 - 1], m[2 - 1], and_ancilla[1])
    CNOT2(eng, t[14 - 1], m[1 - 1], m[3 - 1])
    AND_gate(eng, t[19 - 1], u[7], m[4 - 1], and_ancilla[2])
    CNOT2(eng, m[4 - 1], m[1 - 1], m[5 - 1])
    AND_gate(eng, t[3 - 1], t[16 - 1], m[6 - 1], and_ancilla[3])
    AND_gate(eng, t[22 - 1], t[9 - 1], m[7 - 1], and_ancilla[4])
    CNOT2(eng, t[26 - 1], m[6 - 1], m[8 - 1])
    AND_gate(eng, t[20 - 1], t[17 - 1], m[9 - 1], and_ancilla[5])
    CNOT2(eng, m[9 - 1], m[6 - 1], m[10 - 1])
    AND_gate(eng, t[1 - 1], t[15 - 1], m[11 - 1], and_ancilla[6])
    AND_gate(eng, t[4 - 1], t[27 - 1], m[12 - 1], and_ancilla[7])
    CNOT2(eng, m[12 - 1], m[11 - 1], m[13 - 1])
    AND_gate(eng, t[2 - 1], t[10 - 1], m[14 - 1], and_ancilla[8])
    CNOT2(eng, m[14 - 1], m[11 - 1], m[15 - 1])
    CNOT2(eng, m[3 - 1], m[2 - 1], m[16 - 1])
    CNOT2(eng, m[5 - 1], t[24 - 1], m[17 - 1])
    CNOT2(eng, m[8 - 1], m[7 - 1], m[18 - 1])
    CNOT2(eng, m[10 - 1], m[15 - 1], m[19 - 1])
    CNOT2(eng, m[16 - 1], m[13 - 1], m[20 - 1])
    CNOT2(eng, m[17 - 1], m[15 - 1], m[21 - 1])
    CNOT2(eng, m[18 - 1], m[13 - 1], m[22 - 1])
    CNOT2(eng, m[19 - 1], t[25 - 1], m[23 - 1])
    CNOT2(eng, m[22 - 1], m[23 - 1], m[24 - 1])

    # ** ** ** ** ** ** *Layer

    # 41

    CNOT | (u[7], m[33 - 1])
    CNOT | (t[1 - 1], m[34 - 1])
    CNOT | (t[1 - 1], m[35 - 1])
    CNOT | (t[2 - 1], m[36 - 1])
    CNOT | (t[4 - 1], m[37 - 1])
    CNOT | (t[10 - 1], m[38 - 1])
    CNOT | (t[15 - 1], m[39 - 1])
    CNOT | (t[15 - 1], m[40 - 1])
    CNOT2(eng, m[20 - 1], m[21 - 1], m[27 - 1])
    CNOT | (t[17 - 1], m[41 - 1])
    CNOT | (t[19 - 1], m[42 - 1])
    CNOT | (t[20 - 1], m[43 - 1])
    CNOT | (t[27 - 1], m[44 - 1])
    CNOT | (m[20 - 1], m[45 - 1])
    CNOT | (m[21 - 1], m[46 - 1])
    CNOT | (m[21 - 1], m[47 - 1])
    CNOT | (m[22 - 1], m[48 - 1])
    CNOT | (m[23 - 1], m[49 - 1])
    CNOT | (m[23 - 1], m[50 - 1])

    CNOT | (m[24 - 1], l[1 - 1])

    CNOT | (m[24 - 1], l[2 - 1])

    CNOT2(eng, m[21 - 1], m[23 - 1], n[15 - 1])

    CNOT | (m[24 - 1], l[3 - 1])
    CNOT | (l[1 - 1], l[4 - 1])
    CNOT | (l[2 - 1], l[5 - 1])
    CNOT | (m[24 - 1], l[6 - 1])
    CNOT | (l[1 - 1], l[7 - 1])
    CNOT | (l[2 - 1], l[8 - 1])
    CNOT | (l[3 - 1], l[9 - 1])
    CNOT | (l[4 - 1], l[10 - 1])
    CNOT | (l[5 - 1], l[11 - 1])

    CNOT | (m[27 - 1], l[12 - 1])
    CNOT | (m[27 - 1], l[13 - 1])
    CNOT | (m[27 - 1], l[14 - 1])
    CNOT | (l[12 - 1], l[15 - 1])
    CNOT | (l[13 - 1], l[16 - 1])
    CNOT | (m[27 - 1], l[17 - 1])
    CNOT | (l[12 - 1], l[18 - 1])
    CNOT | (l[13 - 1], l[19 - 1])
    CNOT | (l[14 - 1], l[20 - 1])
    CNOT | (l[15 - 1], l[21 - 1])
    CNOT | (l[16 - 1], l[22 - 1])

    CNOT | (n[15 - 1], l[23 - 1])

    # # # # # # # # # # # # # # # # # # # # # # # /

    AND_gate(eng, m[22 - 1], m[20 - 1], m[25 - 1], l[23])

    CNOT2(eng, m[23 - 1], m[25 - 1], m[28 - 1])

    CNOT2(eng, m[21 - 1], m[25 - 1], m[26 - 1])

    AND_gate(eng, m[45 - 1], m[23 - 1], m[29 - 1], l[24])
    CNOT2(eng, m[27 - 1], m[25 - 1], m[30 - 1])

    AND_gate(eng, m[21 - 1], m[48 - 1], m[31 - 1], l[25])
    CNOT2(eng, m[24 - 1], m[25 - 1], m[32 - 1])

    # AND_gate(eng, m[28 - 1], m[27 - 1], m[29 - 1])
    # AND_gate(eng, m[26 - 1], m[24 - 1], m[30 - 1])
    # AND_gate(eng, l[2], m[29 - 1], m[32 - 1])
    # AND_gate(eng, l[3], m[31 - 1], m[35 - 1])

    AND_gate(eng, m[24 - 1], t[6 - 1], n[1 - 1], l[26])  # 2
    CNOT2(eng, m[23 - 1], m[32 - 1], n[2 - 1])
    CNOT2(eng, m[26 - 1], m[31 - 1], n[3 - 1])

    AND_gate(eng, l[1 - 1], t[8 - 1], n[4 - 1], l[27])  # 2

    AND_gate(eng, l[2 - 1], u[7], n[6 - 1], l[28])  # 2
    AND_gate(eng, m[49 - 1], m[33 - 1], n[7 - 1], l[29])  # 2

    CNOT2(eng, m[21 - 1], m[30 - 1], n[8 - 1])
    CNOT2(eng, m[28 - 1], m[29 - 1], n[9 - 1])
    AND_gate(eng, m[27 - 1], t[16 - 1], n[10 - 1], s[0])  # 2

    AND_gate(eng, l[12 - 1], t[9 - 1], n[11 - 1], s[1])  # 2

    AND_gate(eng, m[46 - 1], t[17 - 1], n[13 - 1], s[2])  # 2
    AND_gate(eng, l[13 - 1], m[41 - 1], n[14 - 1], s[3])  # 2

    # ** ** ** ** ** ** ** ** ** ** ** ** ** **

    AND_gate(eng, l[14 - 1], t[15 - 1], n[16 - 1], s[4])  # 2
    AND_gate(eng, l[3 - 1], m[39 - 1], n[17 - 1], s[5])  # 2
    AND_gate(eng, n[15 - 1], m[40 - 1], w[9 - 1], s[6])  # 2

    CNOT2(eng, m[30 - 1], m[32 - 1], n[18 - 1])
    CNOT2(eng, n[15 - 1], n[18 - 1], n[19 - 1])
    CNOT2(eng, m[28 - 1], m[29 - 1], n[20 - 1])
    CNOT2(eng, m[26 - 1], m[31 - 1], n[21 - 1])
    AND_gate(eng, l[15 - 1], t[27 - 1], n[22 - 1], s[7])  # 2
    AND_gate(eng, l[4 - 1], m[44 - 1], n[23 - 1], and_ancilla[0])  # 2

    AND_gate(eng, l[16 - 1], t[10 - 1], n[24 - 1], and_ancilla[1])  # 2
    AND_gate(eng, l[5 - 1], m[38 - 1], n[25 - 1], and_ancilla[2])  # 2

    AND_gate(eng, l[6 - 1], t[13 - 1], n[26 - 1], and_ancilla[3])  # 2

    AND_gate(eng, l[7 - 1], t[23 - 1], n[27 - 1], and_ancilla[4])  # 2

    AND_gate(eng, l[8 - 1], t[19 - 1], n[29 - 1], and_ancilla[5])  # 2
    AND_gate(eng, m[50 - 1], m[42 - 1], n[30 - 1], and_ancilla[6])  # 2

    AND_gate(eng, l[17 - 1], t[3 - 1], n[31 - 1], and_ancilla[7])  # 2

    AND_gate(eng, l[18 - 1], t[22 - 1], n[32 - 1], and_ancilla[8])  # 2

    AND_gate(eng, m[47 - 1], t[20 - 1], n[34 - 1], and_ancilla[9])  # 2
    AND_gate(eng, l[19 - 1], m[43 - 1], n[35 - 1], and_ancilla[10])  # 2

    AND_gate(eng, l[20 - 1], t[1 - 1], n[36 - 1], and_ancilla[11])  # 2
    AND_gate(eng, l[9 - 1], m[34 - 1], n[37 - 1], and_ancilla[12])  # 2
    AND_gate(eng, l[23 - 1], m[35 - 1], w[26 - 1], and_ancilla[13])  # 2

    AND_gate(eng, l[21 - 1], t[4 - 1], n[38 - 1], and_ancilla[14])  # 2
    AND_gate(eng, l[10 - 1], m[37 - 1], n[39 - 1], and_ancilla[15])  # 2

    AND_gate(eng, l[22 - 1], t[2 - 1], n[40 - 1], and_ancilla[16])  # 2
    AND_gate(eng, l[11 - 1], m[36 - 1], n[41 - 1], and_ancilla[17])  # 2

    # Clean

    CNOT | (n[15 - 1], l[23 - 1])
    CNOT | (l[16 - 1], l[22 - 1])
    CNOT | (l[15 - 1], l[21 - 1])
    CNOT | (l[14 - 1], l[20 - 1])
    CNOT | (l[13 - 1], l[19 - 1])
    CNOT | (l[12 - 1], l[18 - 1])
    CNOT | (m[27 - 1], l[17 - 1])
    CNOT | (l[13 - 1], l[16 - 1])
    CNOT | (l[12 - 1], l[15 - 1])
    CNOT | (m[27 - 1], l[14 - 1])
    CNOT | (m[27 - 1], l[13 - 1])
    CNOT | (m[27 - 1], l[12 - 1])
    CNOT | (l[5 - 1], l[11 - 1])
    CNOT | (l[4 - 1], l[10 - 1])
    CNOT | (l[3 - 1], l[9 - 1])
    CNOT | (l[2 - 1], l[8 - 1])
    CNOT | (l[1 - 1], l[7 - 1])
    CNOT | (m[24 - 1], l[6 - 1])
    CNOT | (l[2 - 1], l[5 - 1])
    CNOT | (l[1 - 1], l[4 - 1])
    CNOT | (m[24 - 1], l[3 - 1])
    CNOT | (m[24 - 1], l[2 - 1])
    CNOT | (m[24 - 1], l[1 - 1])

    CNOT | (m[23 - 1], m[50 - 1])
    CNOT | (m[23 - 1], m[49 - 1])
    CNOT | (m[22 - 1], m[48 - 1])
    CNOT | (m[21 - 1], m[47 - 1])
    CNOT | (m[21 - 1], m[46 - 1])
    CNOT | (m[20 - 1], m[45 - 1])
    CNOT | (t[27 - 1], m[44 - 1])
    CNOT | (t[20 - 1], m[43 - 1])
    CNOT | (t[19 - 1], m[42 - 1])
    CNOT | (t[17 - 1], m[41 - 1])
    CNOT | (t[15 - 1], m[40 - 1])
    CNOT | (t[15 - 1], m[39 - 1])
    CNOT | (t[10 - 1], m[38 - 1])
    CNOT | (t[4 - 1], m[37 - 1])
    CNOT | (t[2 - 1], m[36 - 1])
    CNOT | (t[1 - 1], m[35 - 1])
    CNOT | (t[1 - 1], m[34 - 1])
    CNOT | (u[7], m[33 - 1])

    # ** ** ** ** ** ** ** *Layer

    CNOT | (m[26 - 1], l[1 - 1])
    CNOT | (m[26 - 1], l[2 - 1])
    CNOT | (m[26 - 1], l[3 - 1])

    CNOT | (m[28 - 1], l[4 - 1])
    CNOT | (m[28 - 1], l[5 - 1])
    CNOT | (m[28 - 1], l[6 - 1])

    CNOT | (m[29 - 1], l[7 - 1])
    CNOT | (m[29 - 1], l[8 - 1])
    CNOT | (m[29 - 1], l[9 - 1])

    CNOT | (m[30 - 1], l[10 - 1])

    CNOT | (m[31 - 1], l[11 - 1])
    CNOT | (m[31 - 1], l[12 - 1])
    CNOT | (m[31 - 1], l[13 - 1])

    CNOT | (m[32 - 1], l[14 - 1])
    CNOT | (n[2 - 1], l[15 - 1])
    CNOT | (n[3 - 1], l[16 - 1])
    CNOT | (n[8 - 1], l[17 - 1])
    CNOT | (n[9 - 1], l[18 - 1])

    CNOT | (n[18 - 1], l[19 - 1])
    CNOT | (n[19 - 1], l[20 - 1])
    CNOT | (n[20 - 1], l[21 - 1])
    CNOT | (n[21 - 1], l[22 - 1])

    AND_gate(eng, n[3 - 1], n[1 - 1], w[1 - 1], l[22])  # 3
    AND_gate(eng, n[2 - 1], t[6 - 1], w[2 - 1], l[23])  # 3
    CNOT2(eng, w[1 - 1], w[2 - 1], m[33 - 1])

    AND_gate(eng, m[32 - 1], t[8 - 1], n[5 - 1], l[24])  # 3
    AND_gate(eng, n[4 - 1], m[31 - 1], w[3 - 1], l[25])  # 3
    CNOT2(eng, w[3 - 1], n[5 - 1], m[34 - 1])

    AND_gate(eng, n[6 - 1], m[26 - 1], w[4 - 1], l[26])  # 3
    CNOT2(eng, w[4 - 1], n[7 - 1], m[35 - 1])

    AND_gate(eng, n[8 - 1], t[16 - 1], w[5 - 1], l[27])  # 3
    AND_gate(eng, n[9 - 1], n[10 - 1], w[6 - 1], l[28])  # 3
    CNOT2(eng, w[5 - 1], w[6 - 1], m[36 - 1])

    AND_gate(eng, m[30 - 1], t[9 - 1], n[12 - 1], l[29])  # 3
    AND_gate(eng, m[29 - 1], n[11 - 1], w[7 - 1], s[0])  # 3
    CNOT2(eng, w[7 - 1], n[12 - 1], m[37 - 1])

    AND_gate(eng, m[28 - 1], n[14 - 1], w[8 - 1], s[1])  # 3
    CNOT2(eng, w[8 - 1], n[13 - 1], m[38 - 1])

    AND_gate(eng, n[16 - 1], l[4 - 1], w[10 - 1], s[2])  # 3
    AND_gate(eng, n[17 - 1], l[1 - 1], w[11 - 1], s[3])  # 3
    CNOT2(eng, w[9 - 1], w[10 - 1], m[39 - 1])
    CNOT | (w[11 - 1], m[39 - 1])

    AND_gate(eng, n[19 - 1], t[27 - 1], w[12 - 1], s[4])  # 3
    AND_gate(eng, n[20 - 1], n[22 - 1], w[13 - 1], s[5])  # 3
    AND_gate(eng, n[21 - 1], n[23 - 1], w[14 - 1], s[6])  # 3
    CNOT2(eng, w[12 - 1], w[13 - 1], m[40 - 1])
    CNOT | (w[14 - 1], m[40 - 1])

    AND_gate(eng, l[7 - 1], n[24 - 1], w[15 - 1], s[7])  # 3
    AND_gate(eng, n[18 - 1], t[10 - 1], w[16 - 1], and_ancilla[0])  # 3
    AND_gate(eng, l[11 - 1], n[25 - 1], w[17 - 1], and_ancilla[1])  # 3
    CNOT2(eng, w[15 - 1], w[16 - 1], m[41 - 1])
    CNOT | (w[17 - 1], m[41 - 1])

    AND_gate(eng, l[16 - 1], n[26 - 1], w[18 - 1], and_ancilla[2])  # 3
    AND_gate(eng, l[15 - 1], t[13 - 1], w[19 - 1], and_ancilla[3])  # 3
    CNOT2(eng, w[18 - 1], w[19 - 1], m[42 - 1])

    AND_gate(eng, l[14 - 1], t[23 - 1], n[28 - 1], and_ancilla[4])  # 3
    AND_gate(eng, n[27 - 1], l[12 - 1], w[20 - 1], and_ancilla[5])  # 3
    CNOT2(eng, w[20 - 1], n[28 - 1], m[43 - 1])

    AND_gate(eng, n[29 - 1], l[2 - 1], w[21 - 1], and_ancilla[6])  # 3
    CNOT2(eng, w[21 - 1], n[30 - 1], m[44 - 1])

    AND_gate(eng, l[17 - 1], t[3 - 1], w[22 - 1], and_ancilla[7])  # 3
    AND_gate(eng, l[18 - 1], n[31 - 1], w[23 - 1], and_ancilla[8])  # 3
    CNOT2(eng, w[22 - 1], w[23 - 1], m[45 - 1])

    AND_gate(eng, l[10 - 1], t[22 - 1], n[33 - 1], and_ancilla[9])  # 3
    AND_gate(eng, l[8 - 1], n[32 - 1], w[24 - 1], and_ancilla[10])  # 3
    CNOT2(eng, w[24 - 1], n[33 - 1], m[46 - 1])

    AND_gate(eng, l[5 - 1], n[35 - 1], w[25 - 1], and_ancilla[11])  # 3
    CNOT2(eng, w[25 - 1], n[34 - 1], m[47 - 1])

    AND_gate(eng, n[36 - 1], l[6 - 1], w[27 - 1], and_ancilla[12])  # 3
    AND_gate(eng, n[37 - 1], l[3 - 1], w[28 - 1], and_ancilla[13])  # 3

    CNOT2(eng, w[26 - 1], w[27 - 1], m[48 - 1])
    CNOT | (w[28 - 1], m[48 - 1])

    AND_gate(eng, l[20 - 1], t[4 - 1], w[29 - 1], and_ancilla[14])  # 3
    AND_gate(eng, l[21 - 1], n[38 - 1], w[30 - 1], and_ancilla[15])  # 3
    AND_gate(eng, l[22 - 1], n[39 - 1], w[31 - 1], and_ancilla[16])  # 3
    CNOT2(eng, w[29 - 1], w[30 - 1], m[49 - 1])
    CNOT | (w[31 - 1], m[49 - 1])

    AND_gate(eng, l[9 - 1], n[40 - 1], w[32 - 1], and_ancilla[17])  # 3
    AND_gate(eng, l[19 - 1], t[2 - 1], w[33 - 1], and_ancilla[18])  # 3
    AND_gate(eng, l[13 - 1], n[41 - 1], w[34 - 1], and_ancilla[19])  # 3
    CNOT2(eng, w[32 - 1], w[33 - 1], m[50 - 1])
    CNOT | (w[34 - 1], m[50 - 1])

    CNOT | (m[26 - 1], l[1 - 1])
    CNOT | (m[26 - 1], l[2 - 1])
    CNOT | (m[26 - 1], l[3 - 1])

    CNOT | (m[28 - 1], l[4 - 1])
    CNOT | (m[28 - 1], l[5 - 1])
    CNOT | (m[28 - 1], l[6 - 1])

    CNOT | (m[29 - 1], l[7 - 1])
    CNOT | (m[29 - 1], l[8 - 1])
    CNOT | (m[29 - 1], l[9 - 1])

    CNOT | (m[30 - 1], l[10 - 1])

    CNOT | (m[31 - 1], l[11 - 1])
    CNOT | (m[31 - 1], l[12 - 1])
    CNOT | (m[31 - 1], l[13 - 1])

    CNOT | (m[32 - 1], l[14 - 1])
    CNOT | (n[2 - 1], l[15 - 1])
    CNOT | (n[3 - 1], l[16 - 1])
    CNOT | (n[8 - 1], l[17 - 1])
    CNOT | (n[9 - 1], l[18 - 1])

    CNOT | (n[18 - 1], l[19 - 1])
    CNOT | (n[19 - 1], l[20 - 1])
    CNOT | (n[20 - 1], l[21 - 1])
    CNOT | (n[21 - 1], l[22 - 1])

    CNOT2(eng, m[48 - 1], m[49 - 1], l[0])
    CNOT2(eng, m[37 - 1], m[43 - 1], l[1])
    CNOT2(eng, m[33 - 1], m[35 - 1], l[2])
    CNOT2(eng, m[34 - 1], m[42 - 1], l[3])
    CNOT2(eng, m[41 - 1], m[45 - 1], l[4])
    CNOT2(eng, m[36 - 1], m[48 - 1], l[5])
    CNOT2(eng, m[49 - 1], l[5], l[6])
    CNOT2(eng, m[33 - 1], l[3], l[7])
    CNOT2(eng, m[38 - 1], m[46 - 1], l[8])
    CNOT2(eng, m[39 - 1], m[40 - 1], l[9])
    CNOT2(eng, m[40 - 1], l[4], l[10])
    CNOT2(eng, m[47 - 1], l[2], l[11])
    CNOT2(eng, m[35 - 1], m[38 - 1], l[12])
    CNOT2(eng, m[37 - 1], l[0], l[13])
    CNOT2(eng, m[39 - 1], m[48 - 1], l[14])
    CNOT2(eng, m[42 - 1], l[1], l[15])
    CNOT2(eng, m[43 - 1], l[0], l[16])
    CNOT2(eng, m[44 - 1], l[1], l[17])
    CNOT2(eng, m[45 - 1], l[8], l[18])
    CNOT2(eng, m[50 - 1], l[4], l[19])
    CNOT2(eng, l[0], l[1], l[20])
    CNOT2(eng, l[1], l[7], l[21])
    CNOT2(eng, l[3], l[12], l[22])
    CNOT2(eng, l[18], l[2], l[23])
    CNOT2(eng, l[15], l[9], l[24])
    CNOT2(eng, l[6], l[10], l[25])
    CNOT2(eng, l[7], l[9], l[26])
    CNOT2(eng, l[8], l[10], l[27])
    CNOT2(eng, l[11], l[14], l[28])
    CNOT2(eng, l[11], l[17], l[29])

    CNOT2(eng, l[6], l[24], s[7])
    CNOT2(eng, l[16], l[26], s[6])
    X | s[6]
    CNOT2(eng, l[19], l[28], s[5])
    X | s[5]

    CNOT2(eng, l[6], l[21], s[4])
    CNOT2(eng, l[20], l[22], s[3])
    CNOT2(eng, l[25], l[29], s[2])
    CNOT2(eng, l[13], l[27], s[1])
    X | s[1]
    CNOT2(eng, l[6], l[23], s[0])
    X | s[0]

    if (round != 9):
        with Dagger(eng):
            CNOT2(eng, u[0], u[3], t[1 - 1])
            CNOT2(eng, u[0], u[5], t[2 - 1])
            CNOT2(eng, u[0], u[6], t[3 - 1])
            CNOT2(eng, u[3], u[5], t[4 - 1])
            CNOT2(eng, u[4], u[6], t[5 - 1])
            CNOT2(eng, t[1 - 1], t[5 - 1], t[6 - 1])
            CNOT2(eng, u[1], u[2], t[7 - 1])
            CNOT2(eng, u[7], t[6 - 1], t[8 - 1])
            CNOT2(eng, u[7], t[7 - 1], t[9 - 1])
            CNOT2(eng, t[6 - 1], t[7 - 1], t[10 - 1])
            CNOT2(eng, u[1], u[5], t[11 - 1])
            CNOT2(eng, u[2], u[5], t[12 - 1])
            CNOT2(eng, t[3 - 1], t[4 - 1], t[13 - 1])
            CNOT2(eng, t[6 - 1], t[11 - 1], t[14 - 1])
            CNOT2(eng, t[5 - 1], t[11 - 1], t[15 - 1])
            CNOT2(eng, t[5 - 1], t[12 - 1], t[16 - 1])
            CNOT2(eng, t[9 - 1], t[16 - 1], t[17 - 1])
            CNOT2(eng, u[3], u[7], t[18 - 1])
            CNOT2(eng, t[7 - 1], t[18 - 1], t[19 - 1])
            CNOT2(eng, t[1 - 1], t[19 - 1], t[20 - 1])
            CNOT2(eng, u[6], u[7], t[21 - 1])
            CNOT2(eng, t[7 - 1], t[21 - 1], t[22 - 1])
            CNOT2(eng, t[2 - 1], t[22 - 1], t[23 - 1])
            CNOT2(eng, t[2 - 1], t[10 - 1], t[24 - 1])
            CNOT2(eng, t[20 - 1], t[17 - 1], t[25 - 1])
            CNOT2(eng, t[3 - 1], t[16 - 1], t[26 - 1])
            CNOT2(eng, t[1 - 1], t[12 - 1], t[27 - 1])

            AND_gate_dag(eng, t[13 - 1], t[6 - 1], m[1 - 1], and_ancilla[0])
            AND_gate_dag(eng, t[23 - 1], t[8 - 1], m[2 - 1], and_ancilla[1])
            CNOT2(eng, t[14 - 1], m[1 - 1], m[3 - 1])
            AND_gate_dag(eng, t[19 - 1], u[7], m[4 - 1], and_ancilla[2])
            CNOT2(eng, m[4 - 1], m[1 - 1], m[5 - 1])
            AND_gate_dag(eng, t[3 - 1], t[16 - 1], m[6 - 1], and_ancilla[3])
            AND_gate_dag(eng, t[22 - 1], t[9 - 1], m[7 - 1], and_ancilla[4])
            CNOT2(eng, t[26 - 1], m[6 - 1], m[8 - 1])
            AND_gate_dag(eng, t[20 - 1], t[17 - 1], m[9 - 1], and_ancilla[5])
            CNOT2(eng, m[9 - 1], m[6 - 1], m[10 - 1])
            AND_gate_dag(eng, t[1 - 1], t[15 - 1], m[11 - 1], and_ancilla[6])
            AND_gate_dag(eng, t[4 - 1], t[27 - 1], m[12 - 1], and_ancilla[7])
            CNOT2(eng, m[12 - 1], m[11 - 1], m[13 - 1])
            AND_gate_dag(eng, t[2 - 1], t[10 - 1], m[14 - 1], and_ancilla[8])
            CNOT2(eng, m[14 - 1], m[11 - 1], m[15 - 1])
            CNOT2(eng, m[3 - 1], m[2 - 1], m[16 - 1])
            CNOT2(eng, m[5 - 1], t[24 - 1], m[17 - 1])
            CNOT2(eng, m[8 - 1], m[7 - 1], m[18 - 1])
            CNOT2(eng, m[10 - 1], m[15 - 1], m[19 - 1])
            CNOT2(eng, m[16 - 1], m[13 - 1], m[20 - 1])
            CNOT2(eng, m[17 - 1], m[15 - 1], m[21 - 1])
            CNOT2(eng, m[18 - 1], m[13 - 1], m[22 - 1])
            CNOT2(eng, m[19 - 1], t[25 - 1], m[23 - 1])
            CNOT2(eng, m[22 - 1], m[23 - 1], m[24 - 1])

            # ** ** ** ** ** ** *Layer

            # 41

            CNOT | (u[7], m[33 - 1])
            CNOT | (t[1 - 1], m[34 - 1])
            CNOT | (t[1 - 1], m[35 - 1])
            CNOT | (t[2 - 1], m[36 - 1])
            CNOT | (t[4 - 1], m[37 - 1])
            CNOT | (t[10 - 1], m[38 - 1])
            CNOT | (t[15 - 1], m[39 - 1])
            CNOT | (t[15 - 1], m[40 - 1])
            CNOT2(eng, m[20 - 1], m[21 - 1], m[27 - 1])
            CNOT | (t[17 - 1], m[41 - 1])
            CNOT | (t[19 - 1], m[42 - 1])
            CNOT | (t[20 - 1], m[43 - 1])
            CNOT | (t[27 - 1], m[44 - 1])
            CNOT | (m[20 - 1], m[45 - 1])
            CNOT | (m[21 - 1], m[46 - 1])
            CNOT | (m[21 - 1], m[47 - 1])
            CNOT | (m[22 - 1], m[48 - 1])
            CNOT | (m[23 - 1], m[49 - 1])
            CNOT | (m[23 - 1], m[50 - 1])

            CNOT | (m[24 - 1], l[1 - 1])

            CNOT | (m[24 - 1], l[2 - 1])

            CNOT2(eng, m[21 - 1], m[23 - 1], n[15 - 1])

            CNOT | (m[24 - 1], l[3 - 1])
            CNOT | (l[1 - 1], l[4 - 1])
            CNOT | (l[2 - 1], l[5 - 1])
            CNOT | (m[24 - 1], l[6 - 1])
            CNOT | (l[1 - 1], l[7 - 1])
            CNOT | (l[2 - 1], l[8 - 1])
            CNOT | (l[3 - 1], l[9 - 1])
            CNOT | (l[4 - 1], l[10 - 1])
            CNOT | (l[5 - 1], l[11 - 1])

            CNOT | (m[27 - 1], l[12 - 1])
            CNOT | (m[27 - 1], l[13 - 1])
            CNOT | (m[27 - 1], l[14 - 1])
            CNOT | (l[12 - 1], l[15 - 1])
            CNOT | (l[13 - 1], l[16 - 1])
            CNOT | (m[27 - 1], l[17 - 1])
            CNOT | (l[12 - 1], l[18 - 1])
            CNOT | (l[13 - 1], l[19 - 1])
            CNOT | (l[14 - 1], l[20 - 1])
            CNOT | (l[15 - 1], l[21 - 1])
            CNOT | (l[16 - 1], l[22 - 1])

            CNOT | (n[15 - 1], l[23 - 1])

            # # # # # # # # # # # # # # # # # # # # # # # /

            AND_gate_dag(eng, m[22 - 1], m[20 - 1], m[25 - 1], l[23])

            CNOT2(eng, m[23 - 1], m[25 - 1], m[28 - 1])

            CNOT2(eng, m[21 - 1], m[25 - 1], m[26 - 1])

            AND_gate_dag(eng, m[45 - 1], m[23 - 1], m[29 - 1], l[24])
            CNOT2(eng, m[27 - 1], m[25 - 1], m[30 - 1])

            AND_gate_dag(eng, m[21 - 1], m[48 - 1], m[31 - 1], l[25])
            CNOT2(eng, m[24 - 1], m[25 - 1], m[32 - 1])

            # AND_gate_dag(eng, m[28 - 1], m[27 - 1], m[29 - 1])
            # AND_gate_dag(eng, m[26 - 1], m[24 - 1], m[30 - 1])
            # AND_gate_dag(eng, l[2], m[29 - 1], m[32 - 1])
            # AND_gate_dag(eng, l[3], m[31 - 1], m[35 - 1])

            AND_gate_dag(eng, m[24 - 1], t[6 - 1], n[1 - 1], l[26])  # 2
            CNOT2(eng, m[23 - 1], m[32 - 1], n[2 - 1])
            CNOT2(eng, m[26 - 1], m[31 - 1], n[3 - 1])

            AND_gate_dag(eng, l[1 - 1], t[8 - 1], n[4 - 1], l[27])  # 2

            AND_gate_dag(eng, l[2 - 1], u[7], n[6 - 1], l[28])  # 2
            AND_gate_dag(eng, m[49 - 1], m[33 - 1], n[7 - 1], l[29])  # 2

            CNOT2(eng, m[21 - 1], m[30 - 1], n[8 - 1])
            CNOT2(eng, m[28 - 1], m[29 - 1], n[9 - 1])
            AND_gate_dag(eng, m[27 - 1], t[16 - 1], n[10 - 1], s[0])  # 2

            AND_gate_dag(eng, l[12 - 1], t[9 - 1], n[11 - 1], s[1])  # 2

            AND_gate_dag(eng, m[46 - 1], t[17 - 1], n[13 - 1], s[2])  # 2
            AND_gate_dag(eng, l[13 - 1], m[41 - 1], n[14 - 1], s[3])  # 2

            # ** ** ** ** ** ** ** ** ** ** ** ** ** **

            AND_gate_dag(eng, l[14 - 1], t[15 - 1], n[16 - 1], s[4])  # 2
            AND_gate_dag(eng, l[3 - 1], m[39 - 1], n[17 - 1], s[5])  # 2
            AND_gate_dag(eng, n[15 - 1], m[40 - 1], w[9 - 1], s[6])  # 2

            CNOT2(eng, m[30 - 1], m[32 - 1], n[18 - 1])
            CNOT2(eng, n[15 - 1], n[18 - 1], n[19 - 1])
            CNOT2(eng, m[28 - 1], m[29 - 1], n[20 - 1])
            CNOT2(eng, m[26 - 1], m[31 - 1], n[21 - 1])
            AND_gate_dag(eng, l[15 - 1], t[27 - 1], n[22 - 1], s[7])  # 2
            AND_gate_dag(eng, l[4 - 1], m[44 - 1], n[23 - 1], and_ancilla[0])  # 2

            AND_gate_dag(eng, l[16 - 1], t[10 - 1], n[24 - 1], and_ancilla[1])  # 2
            AND_gate_dag(eng, l[5 - 1], m[38 - 1], n[25 - 1], and_ancilla[2])  # 2

            AND_gate_dag(eng, l[6 - 1], t[13 - 1], n[26 - 1], and_ancilla[3])  # 2

            AND_gate_dag(eng, l[7 - 1], t[23 - 1], n[27 - 1], and_ancilla[4])  # 2

            AND_gate_dag(eng, l[8 - 1], t[19 - 1], n[29 - 1], and_ancilla[5])  # 2
            AND_gate_dag(eng, m[50 - 1], m[42 - 1], n[30 - 1], and_ancilla[6])  # 2

            AND_gate_dag(eng, l[17 - 1], t[3 - 1], n[31 - 1], and_ancilla[7])  # 2

            AND_gate_dag(eng, l[18 - 1], t[22 - 1], n[32 - 1], and_ancilla[8])  # 2

            AND_gate_dag(eng, m[47 - 1], t[20 - 1], n[34 - 1], and_ancilla[9])  # 2
            AND_gate_dag(eng, l[19 - 1], m[43 - 1], n[35 - 1], and_ancilla[10])  # 2

            AND_gate_dag(eng, l[20 - 1], t[1 - 1], n[36 - 1], and_ancilla[11])  # 2
            AND_gate_dag(eng, l[9 - 1], m[34 - 1], n[37 - 1], and_ancilla[12])  # 2
            AND_gate_dag(eng, l[23 - 1], m[35 - 1], w[26 - 1], and_ancilla[13])  # 2

            AND_gate_dag(eng, l[21 - 1], t[4 - 1], n[38 - 1], and_ancilla[14])  # 2
            AND_gate_dag(eng, l[10 - 1], m[37 - 1], n[39 - 1], and_ancilla[15])  # 2

            AND_gate_dag(eng, l[22 - 1], t[2 - 1], n[40 - 1], and_ancilla[16])  # 2
            AND_gate_dag(eng, l[11 - 1], m[36 - 1], n[41 - 1], and_ancilla[17])  # 2

            # Clean

            CNOT | (n[15 - 1], l[23 - 1])
            CNOT | (l[16 - 1], l[22 - 1])
            CNOT | (l[15 - 1], l[21 - 1])
            CNOT | (l[14 - 1], l[20 - 1])
            CNOT | (l[13 - 1], l[19 - 1])
            CNOT | (l[12 - 1], l[18 - 1])
            CNOT | (m[27 - 1], l[17 - 1])
            CNOT | (l[13 - 1], l[16 - 1])
            CNOT | (l[12 - 1], l[15 - 1])
            CNOT | (m[27 - 1], l[14 - 1])
            CNOT | (m[27 - 1], l[13 - 1])
            CNOT | (m[27 - 1], l[12 - 1])
            CNOT | (l[5 - 1], l[11 - 1])
            CNOT | (l[4 - 1], l[10 - 1])
            CNOT | (l[3 - 1], l[9 - 1])
            CNOT | (l[2 - 1], l[8 - 1])
            CNOT | (l[1 - 1], l[7 - 1])
            CNOT | (m[24 - 1], l[6 - 1])
            CNOT | (l[2 - 1], l[5 - 1])
            CNOT | (l[1 - 1], l[4 - 1])
            CNOT | (m[24 - 1], l[3 - 1])
            CNOT | (m[24 - 1], l[2 - 1])
            CNOT | (m[24 - 1], l[1 - 1])

            CNOT | (m[23 - 1], m[50 - 1])
            CNOT | (m[23 - 1], m[49 - 1])
            CNOT | (m[22 - 1], m[48 - 1])
            CNOT | (m[21 - 1], m[47 - 1])
            CNOT | (m[21 - 1], m[46 - 1])
            CNOT | (m[20 - 1], m[45 - 1])
            CNOT | (t[27 - 1], m[44 - 1])
            CNOT | (t[20 - 1], m[43 - 1])
            CNOT | (t[19 - 1], m[42 - 1])
            CNOT | (t[17 - 1], m[41 - 1])
            CNOT | (t[15 - 1], m[40 - 1])
            CNOT | (t[15 - 1], m[39 - 1])
            CNOT | (t[10 - 1], m[38 - 1])
            CNOT | (t[4 - 1], m[37 - 1])
            CNOT | (t[2 - 1], m[36 - 1])
            CNOT | (t[1 - 1], m[35 - 1])
            CNOT | (t[1 - 1], m[34 - 1])
            CNOT | (u[7], m[33 - 1])

            # ** ** ** ** ** ** ** *Layer

            CNOT | (m[26 - 1], l[1 - 1])
            CNOT | (m[26 - 1], l[2 - 1])
            CNOT | (m[26 - 1], l[3 - 1])

            CNOT | (m[28 - 1], l[4 - 1])
            CNOT | (m[28 - 1], l[5 - 1])
            CNOT | (m[28 - 1], l[6 - 1])

            CNOT | (m[29 - 1], l[7 - 1])
            CNOT | (m[29 - 1], l[8 - 1])
            CNOT | (m[29 - 1], l[9 - 1])

            CNOT | (m[30 - 1], l[10 - 1])

            CNOT | (m[31 - 1], l[11 - 1])
            CNOT | (m[31 - 1], l[12 - 1])
            CNOT | (m[31 - 1], l[13 - 1])

            CNOT | (m[32 - 1], l[14 - 1])
            CNOT | (n[2 - 1], l[15 - 1])
            CNOT | (n[3 - 1], l[16 - 1])
            CNOT | (n[8 - 1], l[17 - 1])
            CNOT | (n[9 - 1], l[18 - 1])

            CNOT | (n[18 - 1], l[19 - 1])
            CNOT | (n[19 - 1], l[20 - 1])
            CNOT | (n[20 - 1], l[21 - 1])
            CNOT | (n[21 - 1], l[22 - 1])

            AND_gate_dag(eng, n[3 - 1], n[1 - 1], w[1 - 1], l[22])  # 3
            AND_gate_dag(eng, n[2 - 1], t[6 - 1], w[2 - 1], l[23])  # 3
            CNOT2(eng, w[1 - 1], w[2 - 1], m[33 - 1])

            AND_gate_dag(eng, m[32 - 1], t[8 - 1], n[5 - 1], l[24])  # 3
            AND_gate_dag(eng, n[4 - 1], m[31 - 1], w[3 - 1], l[25])  # 3
            CNOT2(eng, w[3 - 1], n[5 - 1], m[34 - 1])

            AND_gate_dag(eng, n[6 - 1], m[26 - 1], w[4 - 1], l[26])  # 3
            CNOT2(eng, w[4 - 1], n[7 - 1], m[35 - 1])

            AND_gate_dag(eng, n[8 - 1], t[16 - 1], w[5 - 1], l[27])  # 3
            AND_gate_dag(eng, n[9 - 1], n[10 - 1], w[6 - 1], l[28])  # 3
            CNOT2(eng, w[5 - 1], w[6 - 1], m[36 - 1])

            AND_gate_dag(eng, m[30 - 1], t[9 - 1], n[12 - 1], l[29])  # 3
            AND_gate_dag(eng, m[29 - 1], n[11 - 1], w[7 - 1], s[0])  # 3
            CNOT2(eng, w[7 - 1], n[12 - 1], m[37 - 1])

            AND_gate_dag(eng, m[28 - 1], n[14 - 1], w[8 - 1], s[1])  # 3
            CNOT2(eng, w[8 - 1], n[13 - 1], m[38 - 1])

            AND_gate_dag(eng, n[16 - 1], l[4 - 1], w[10 - 1], s[2])  # 3
            AND_gate_dag(eng, n[17 - 1], l[1 - 1], w[11 - 1], s[3])  # 3
            CNOT2(eng, w[9 - 1], w[10 - 1], m[39 - 1])
            CNOT | (w[11 - 1], m[39 - 1])

            AND_gate_dag(eng, n[19 - 1], t[27 - 1], w[12 - 1], s[4])  # 3
            AND_gate_dag(eng, n[20 - 1], n[22 - 1], w[13 - 1], s[5])  # 3
            AND_gate_dag(eng, n[21 - 1], n[23 - 1], w[14 - 1], s[6])  # 3
            CNOT2(eng, w[12 - 1], w[13 - 1], m[40 - 1])
            CNOT | (w[14 - 1], m[40 - 1])

            AND_gate_dag(eng, l[7 - 1], n[24 - 1], w[15 - 1], s[7])  # 3
            AND_gate_dag(eng, n[18 - 1], t[10 - 1], w[16 - 1], and_ancilla[0])  # 3
            AND_gate_dag(eng, l[11 - 1], n[25 - 1], w[17 - 1], and_ancilla[1])  # 3
            CNOT2(eng, w[15 - 1], w[16 - 1], m[41 - 1])
            CNOT | (w[17 - 1], m[41 - 1])

            AND_gate_dag(eng, l[16 - 1], n[26 - 1], w[18 - 1], and_ancilla[2])  # 3
            AND_gate_dag(eng, l[15 - 1], t[13 - 1], w[19 - 1], and_ancilla[3])  # 3
            CNOT2(eng, w[18 - 1], w[19 - 1], m[42 - 1])

            AND_gate_dag(eng, l[14 - 1], t[23 - 1], n[28 - 1], and_ancilla[4])  # 3
            AND_gate_dag(eng, n[27 - 1], l[12 - 1], w[20 - 1], and_ancilla[5])  # 3
            CNOT2(eng, w[20 - 1], n[28 - 1], m[43 - 1])

            AND_gate_dag(eng, n[29 - 1], l[2 - 1], w[21 - 1], and_ancilla[6])  # 3
            CNOT2(eng, w[21 - 1], n[30 - 1], m[44 - 1])

            AND_gate_dag(eng, l[17 - 1], t[3 - 1], w[22 - 1], and_ancilla[7])  # 3
            AND_gate_dag(eng, l[18 - 1], n[31 - 1], w[23 - 1], and_ancilla[8])  # 3
            CNOT2(eng, w[22 - 1], w[23 - 1], m[45 - 1])

            AND_gate_dag(eng, l[10 - 1], t[22 - 1], n[33 - 1], and_ancilla[9])  # 3
            AND_gate_dag(eng, l[8 - 1], n[32 - 1], w[24 - 1], and_ancilla[10])  # 3
            CNOT2(eng, w[24 - 1], n[33 - 1], m[46 - 1])

            AND_gate_dag(eng, l[5 - 1], n[35 - 1], w[25 - 1], and_ancilla[11])  # 3
            CNOT2(eng, w[25 - 1], n[34 - 1], m[47 - 1])

            AND_gate_dag(eng, n[36 - 1], l[6 - 1], w[27 - 1], and_ancilla[12])  # 3
            AND_gate_dag(eng, n[37 - 1], l[3 - 1], w[28 - 1], and_ancilla[13])  # 3

            CNOT2(eng, w[26 - 1], w[27 - 1], m[48 - 1])
            CNOT | (w[28 - 1], m[48 - 1])

            AND_gate_dag(eng, l[20 - 1], t[4 - 1], w[29 - 1], and_ancilla[14])  # 3
            AND_gate_dag(eng, l[21 - 1], n[38 - 1], w[30 - 1], and_ancilla[15])  # 3
            AND_gate_dag(eng, l[22 - 1], n[39 - 1], w[31 - 1], and_ancilla[16])  # 3
            CNOT2(eng, w[29 - 1], w[30 - 1], m[49 - 1])
            CNOT | (w[31 - 1], m[49 - 1])

            AND_gate_dag(eng, l[9 - 1], n[40 - 1], w[32 - 1], and_ancilla[17])  # 3
            AND_gate_dag(eng, l[19 - 1], t[2 - 1], w[33 - 1], and_ancilla[18])  # 3
            AND_gate_dag(eng, l[13 - 1], n[41 - 1], w[34 - 1], and_ancilla[19])  # 3
            CNOT2(eng, w[32 - 1], w[33 - 1], m[50 - 1])
            CNOT | (w[34 - 1], m[50 - 1])

            CNOT | (m[26 - 1], l[1 - 1])
            CNOT | (m[26 - 1], l[2 - 1])
            CNOT | (m[26 - 1], l[3 - 1])

            CNOT | (m[28 - 1], l[4 - 1])
            CNOT | (m[28 - 1], l[5 - 1])
            CNOT | (m[28 - 1], l[6 - 1])

            CNOT | (m[29 - 1], l[7 - 1])
            CNOT | (m[29 - 1], l[8 - 1])
            CNOT | (m[29 - 1], l[9 - 1])

            CNOT | (m[30 - 1], l[10 - 1])

            CNOT | (m[31 - 1], l[11 - 1])
            CNOT | (m[31 - 1], l[12 - 1])
            CNOT | (m[31 - 1], l[13 - 1])

            CNOT | (m[32 - 1], l[14 - 1])
            CNOT | (n[2 - 1], l[15 - 1])
            CNOT | (n[3 - 1], l[16 - 1])
            CNOT | (n[8 - 1], l[17 - 1])
            CNOT | (n[9 - 1], l[18 - 1])

            CNOT | (n[18 - 1], l[19 - 1])
            CNOT | (n[19 - 1], l[20 - 1])
            CNOT | (n[20 - 1], l[21 - 1])
            CNOT | (n[21 - 1], l[22 - 1])

            CNOT2(eng, m[48 - 1], m[49 - 1], l[0])
            CNOT2(eng, m[37 - 1], m[43 - 1], l[1])
            CNOT2(eng, m[33 - 1], m[35 - 1], l[2])
            CNOT2(eng, m[34 - 1], m[42 - 1], l[3])
            CNOT2(eng, m[41 - 1], m[45 - 1], l[4])
            CNOT2(eng, m[36 - 1], m[48 - 1], l[5])
            CNOT2(eng, m[49 - 1], l[5], l[6])
            CNOT2(eng, m[33 - 1], l[3], l[7])
            CNOT2(eng, m[38 - 1], m[46 - 1], l[8])
            CNOT2(eng, m[39 - 1], m[40 - 1], l[9])
            CNOT2(eng, m[40 - 1], l[4], l[10])
            CNOT2(eng, m[47 - 1], l[2], l[11])
            CNOT2(eng, m[35 - 1], m[38 - 1], l[12])
            CNOT2(eng, m[37 - 1], l[0], l[13])
            CNOT2(eng, m[39 - 1], m[48 - 1], l[14])
            CNOT2(eng, m[42 - 1], l[1], l[15])
            CNOT2(eng, m[43 - 1], l[0], l[16])
            CNOT2(eng, m[44 - 1], l[1], l[17])
            CNOT2(eng, m[45 - 1], l[8], l[18])
            CNOT2(eng, m[50 - 1], l[4], l[19])
            CNOT2(eng, l[0], l[1], l[20])
            CNOT2(eng, l[1], l[7], l[21])
            CNOT2(eng, l[3], l[12], l[22])
            CNOT2(eng, l[18], l[2], l[23])
            CNOT2(eng, l[15], l[9], l[24])
            CNOT2(eng, l[6], l[10], l[25])
            CNOT2(eng, l[7], l[9], l[26])
            CNOT2(eng, l[8], l[10], l[27])
            CNOT2(eng, l[11], l[14], l[28])
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

def check_ancilla(eng, ancilla, length):
    for i in range(length):
        Measure | (ancilla[i])

    for i in range(length):
        print(int(ancilla[i]), end = '')

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

# resource_check = 0
# Resource = ClassicalSimulator()
# eng = MainEngine(Resource)
# Sbox(eng)
# eng.flush()
# print()

resource_check = 1
Resource = ResourceCounter()
eng = MainEngine(Resource)
Sbox(eng)
print(Resource)
eng.flush()