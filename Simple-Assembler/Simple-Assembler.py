Register_dict = \
    {
        "000": "R0",
        "001": "R1",
        "010": "R2",
        "011": "R3",
        "100": "R4",
        "101": "R5",
        "110": "R6",
        "111": "FLAGS"
    }
opcodes = \
    {
        "00000": "add",
        "00001": "sub",
        "00010": "mov",
        "00011": "mov",
        "00100": "ld",
        "00101": "st",
        "00110": "mul",
        "00111": "div",
        "01000": "rs",
        "01001": "ls",
        "01010": "xor",
        "01011": "or",
        "01100": "and",
        "01101": "not",
        "01110": "cmp",
        "01111": "jmp",
        "10000": "jlt",
        "10001": "jgt",
        "10010": "je",
        "10011": "hlt",
    }
opcodes_type = \
    {
        "00000": "A",
        "00001": "A",
        "00010": "B",
        "00011": "C",
        "00100": "D",
        "00101": "D",
        "00110": "A",
        "00111": "C",
        "01000": "B",
        "01001": "B",
        "01010": "A",
        "01011": "A",
        "01100": "A",
        "01101": "C",
        "01110": "C",
        "01111": "E",
        "10000": "E",
        "10001": "E",
        "10010": "E",
        "10011": "F",
    }


# List_of_Flags = [E, G, L, V]


def binary(a):
    bnr = bin(a).replace('0b', '')
    x = bnr[::-1]  # this reverses an array
    while len(x) < 8:
        x += '0'
    bnr = x[::-1]
    return bnr


def main():
    temp_dic = {}
    var_dict = {}
    label_dict = {}
    count_line = 0
    for i in range(0, 256):
        temp_dic[i] = [None, None, None, None, None]
    while True:
        try:
            line = input()
            if line != "":
                count_line = count_line + 1
                temp_dic[count_line-1] = line.split(" ")
        except EOFError:
            break

    num = count_line
    count_line = 0
    c = num
    to = 0
    while c > 0:
        le = len(temp_dic[c-1][0])
        if temp_dic[c-1][0][le - 1] == ':':
            label_dict[temp_dic[c-1][0][0:le - 1]] = c - 1
            temp_dic[c - 1] = temp_dic[c - 1][1:]

        if temp_dic[c - 1][0] == "var":
            to = to + 1
            ele = temp_dic[c - 1][1]
            var_dict[ele] = c - 1
        c = c - 1

    output(temp_dic, var_dict, label_dict, count_line, num, to)

def output(temp_dic, var_dict, label_dict, count_line, num, to):
            x = 0

            if temp_dic[count_line][0] == "var":
                x = x + 1

            if 0 <= count_line <= num - 1:
                for i, j in opcodes.items():
                    if temp_dic[count_line][0] == j:
                        type_of = opcodes_type[i]
                        if type_of == "A":
                            for a, b in Register_dict.items():
                                for c, d in Register_dict.items():
                                    for e, f in Register_dict.items():
                                        if temp_dic[count_line][1] == b and \
                                                temp_dic[count_line][2] == d and \
                                                temp_dic[count_line][3] == f:
                                            print(i+"00"+a+c+e)
                                            x = x + 1
                                            break

                        elif type_of == "B":
                            for j, k in Register_dict.items():
                                if temp_dic[count_line][1] == k \
                                            and temp_dic[count_line][2][0] == '$' \
                                            and 0 <= int(temp_dic[count_line][2][1:]) <= 255:
                                    z = binary(int(temp_dic[count_line][2][1:]))
                                    print(i+j+z)
                                    x = x+1
                                    break

                        elif type_of == "C":
                            for j, k in Register_dict.items():
                                for m, n in Register_dict.items():
                                    if temp_dic[count_line][1] == k and temp_dic[count_line][2] == n:
                                        print(i+"00000"+j+m)
                                        x = x+1
                                        break

                        elif type_of == "D":
                            for j, k in Register_dict.items():
                                for m, n in var_dict.items():
                                    if temp_dic[count_line][1] == k:
                                        if (temp_dic[count_line][2]) == m:
                                            z = binary(num + n - 1)
                                            print(i+j+z)
                                            x = x + 1
                                            break

                        elif type_of == "E":
                            for j, k in label_dict.items():
                                if (temp_dic[count_line][1]) == j:
                                    z = binary(k-to)
                                    print(i+"000"+z)
                                    x = x + 1
                                    break

                        else:
                            print(i+"00000000000")
                            x = x+1
                            break

                if x == 0:
                    print("Syntax error")

                output(temp_dic, var_dict, label_dict, count_line+1, num, to)

if __name__ == "__main__":
    main()
