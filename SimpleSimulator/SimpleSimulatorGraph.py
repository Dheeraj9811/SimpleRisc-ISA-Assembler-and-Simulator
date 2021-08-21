import matplotlib.pyplot as plt

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

# saves name of opcodes and their types
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
Store_resister = {
    "000": "0",
    "001": "0",
    "010": "0",
    "011": "0",
    "100": "0",
    "101": "0",
    "110": "0",
    "111": "0000000000000000"}

Store_var = {}

temp_dic = {}

def binaryToDecimal(n):
    return int(n, 2)


def binary(a,n):
    bnr = bin(int(a)).replace('0b', '')
    x = bnr[::-1]  # this reverses an array
    while len(x) < n:
        x += '0'
    bnr = x[::-1]
    return bnr


def add(count, line):
    i = line[0][10:13]
    b = int(Store_resister[i])
    i = line[0][13:16]
    c = int(Store_resister[i])
    i = line[0][7:10]
    a = str(b + c)
    Store_resister[i] = a


def subtract(count, line):
    i = line[0][10:13]
    b = int(Store_resister[i])
    i = line[0][13:16]
    c = int(Store_resister[i])
    i = line[0][7:10]
    a = str(b - c)
    Store_resister[i] = a


def multi(count, line):
    i = line[0][10:13]
    b = int(Store_resister[i])
    i = line[0][13:16]
    c = int(Store_resister[i])
    i = line[0][7:10]
    a = str(b * c)
    Store_resister[i] = a


def Take_input():
    count_line = 0
    Take_input.temp_dic = {}  # makeing it function attributes to access anywhere
    while True:
        try:
            line = input()
            if line != "":
                count_line = count_line + 1
                temp_dic[count_line - 1] = line.split(" ")
        except EOFError:
            break


def read(count):
    Type = None
    line = temp_dic[count]

    tempType = line[0][0:5]
    for i in opcodes_type.keys():
        if (tempType == i):
            Type = opcodes_type[i]

    return (Type, line)

def overflow_check():
    for i,j in Store_resister.items():
        if i !="111":
            if int(j)>65535 or int(j)<0 :
                x = binary(j,16)
                j = x[(len(x)-16):len(x)] 
                Store_resister["111"]="0000000000001000"
            

def dump_pc_rf(count):
    print(binary(count, 8), binary(Store_resister["000"], 16), binary(Store_resister["001"], 16),
          binary(Store_resister["010"], 16), binary(Store_resister["011"], 16),
          binary(Store_resister["100"], 16), binary(Store_resister["101"], 16),
          binary(Store_resister["110"], 16), Store_resister["111"])

def execute(Type, count, line):
    true_jump = 0
    true_address = ""
    true_things = [true_jump, true_address]


    if (Type == "A"):
        temp_opcode = line[0][0:5]

        if (temp_opcode == "00000"):  # add fn
            add(count, line)
            Store_resister["111"] = "0000000000000000"
            
            return true_things

        elif (temp_opcode == "00001"):  # subtract
            subtract(count, line)
            Store_resister["111"] = "0000000000000000"
            
            return true_things


        elif (temp_opcode == "00110"):  # multiplay
            multi(count, line)
            Store_resister["111"] = "0000000000000000"
            
            return true_things

        elif (temp_opcode == "00110"):  # Exclusive Or
            i = line[0][10:13]
            b = int(Store_resister[i])
            i = line[0][13:16]
            c = int(Store_resister[i])
            i = line[0][7:10]
            Store_resister[i] = b ^ c
            Store_resister["111"] = "0000000000000000"
        
            return true_things

        elif (temp_opcode == "01011"):  # or
            i = line[0][10:13]
            b = int(Store_resister[i])
            i = line[0][13:16]
            c = int(Store_resister[i])
            i = line[0][7:10]
            Store_resister[i] = b | c
            Store_resister["111"] = "0000000000000000"
            
            return true_things

        elif (temp_opcode == "01100"):  # And
            i = line[0][10:13]
            b = int(Store_resister[i])
            i = line[0][13:16]
            c = int(Store_resister[i])
            i = line[0][7:10]
            Store_resister[i] = b & c
            Store_resister["111"] = "0000000000000000"
            
            return true_things

    elif (Type == "B"):
        temp_opcode = line[0][0:5]

        if (temp_opcode == "00010"):  # MoveImmediate
            i = line[0][5:8]
            Store_resister[i] = binaryToDecimal(str(line[0][8:]))
            Store_resister["111"] = "0000000000000000"
            
            return true_things

        elif (temp_opcode == "01000"):  # rightshift
            i = line[0][5:8]
            Store_resister[i] = int(Store_resister[i] >> (binaryToDecimal(str(line[0][8:]))))
            Store_resister["111"] = "0000000000000000"
            
            return true_things

        elif (temp_opcode == "01001"):  # leftShift
            i = line[0][5:8]
            Store_resister[i] = int(Store_resister[i] << (binaryToDecimal(str(line[0][8:]))))
            Store_resister["111"] = "0000000000000000"
            
            return true_things


    elif (Type == "C"):
        temp_opcode = line[0][0:5]

        if (temp_opcode == "00011"):  # Move reg
            i = line[0][13:16]
            c = int(Store_resister[i])
            i = line[0][10:13]
            Store_resister[i] = str(c)
            Store_resister["111"] = "0000000000000000"
            
            return true_things

        elif (temp_opcode == "00111"):  # divide
            i = line[0][13:16]
            d = int(Store_resister[i])
            i = line[0][10:13]
            c = int(Store_resister[i])
            a = str(int(c // d))
            b = str(int(c % d))
            Store_resister["000"] = a
            Store_resister["001"] = b
            Store_resister["111"] = "0000000000000000"
            
            return true_things

        elif (temp_opcode == "01101"):  # Inverse
            i = line[0][13:16]
            b = int(Store_resister[i])
            temp_inv = binary(b,16)
            inv = ""
            for index in temp_inv:
                if index=="0":
                    inv = inv + "1"
                elif index=="1":
                    inv = inv + "0"
            final_inv=binaryToDecimal(inv)
            i = line[0][10:13]
            Store_resister[i] = str(final_inv)
            Store_resister["111"] = "0000000000000000"
            
            return true_things

        elif (temp_opcode == "01110"):  # compare
            i = line[0][10:13]
            b = int(Store_resister[i])
            i = line[0][13:16]
            c = int(Store_resister[i])
            if (b > c):
                Store_resister["111"] = "0000000000000010"
                return true_things
            elif (b < c):
                Store_resister["111"] = "0000000000000100"
                return true_things
            else:
                Store_resister["111"] = "0000000000000001"
                return true_things


    elif (Type == "D"):
        temp_opcode = line[0][0:5]

        if (temp_opcode == "00101"):    # store
            i = line[0][5:8]
            b = int(Store_resister[i])
            Store_var[line[0][8:16]] = b
            Store_resister["111"] = "0000000000000000"
            
            return true_things

        elif (temp_opcode == "00100"):    # load
            i = line[0][5:8]
            Store_resister[i] = Store_var[line[0][8:16]]
            Store_resister["111"] = "0000000000000000"
            
            return true_things


    elif (Type == "E"):
        temp_opcode = line[0][0:5]
        if (temp_opcode == "01111"):  # unconditional jump
            address = line[0][8:16]
            true_things[1] = binaryToDecimal(address) - len(Store_var)
            true_things[0] = true_things[0] + 1
            Store_resister["111"] = "0000000000000000"
            
            return true_things

        elif (temp_opcode == "10000" and Store_resister["111"] == "0000000000000100"):  # jump if less than
            address = line[0][8:16]
            true_things[1] = binaryToDecimal(address)-len(Store_var)
            true_things[0] = true_things[0] + 1
            Store_resister["111"] = "0000000000000000"
            
            return true_things

        elif (temp_opcode == "10001" and Store_resister["111"] == "0000000000000010"):  # jump if greater than
            address = line[0][8:16]
            true_things[1] = binaryToDecimal(address)-len(Store_var)
            true_things[0] = true_things[0] + 1
            Store_resister["111"] = "0000000000000000"
            
            return true_things

        elif (temp_opcode == "10010" and Store_resister["111"] == "0000000000000001"):  # jump if equal
            address = line[0][8:16]
            true_things[1] = binaryToDecimal(address)-len(Store_var)
            true_things[0] = true_things[0] + 1
            Store_resister["111"] = "0000000000000000"
            
            return true_things

        else :
            Store_resister["111"] = "0000000000000000"
            
            return true_things

    elif (Type == "F"):
        main.hlted = True
        Store_resister["111"] = "0000000000000000"
        
        return true_things


def dump_mem_logic(count, line):
    true_jump = 0
    true_address = ""
    true_things = [true_jump, true_address]
    if (line == "1001100000000000"):
        main.hlted = True
    print(line[0])
    return true_things

def dump_mem(Pc):
    #dumping code lines
    num = Pc
    Pc = 0
    main.hlted = False
    while (num>Pc):
        Type, line = read(Pc)
        t_t = dump_mem_logic(Pc, line)
        if t_t[0] == 0:
            Pc += 1
        else:
            Pc = t_t[1]

    # dumping variables at end
    if len(Store_var)>0:
        for i, j in Store_var.items():
            print(binary(j, 16))

    # dumping left over lines
    for i in range(0, 256-num-len(Store_var)):
        print("0000000000000000")

def main():
    Take_input()
    main.hlted = False
    Pc = 0
    Cycle = 0
    x_coordinate=[]
    y_coordinate=[]
    while (not main.hlted):
        Type, line = read(Pc)
        t_t = execute(Type, Pc, line)
        x_coordinate.append(Cycle) 
        y_coordinate.append(Pc)
        overflow_check()
        dump_pc_rf(Pc)
        if t_t[0] == 0:
            Pc += 1
        else:
            Pc = t_t[1]
        Cycle = Cycle + 1
    dump_mem(Pc)
    plt.plot(x_coordinate,y_coordinate,marker="D",linestyle="None",color="r")
    plt.title = ("Memory Access Trace")
    plt.xlabel("cycle number")
    plt.ylabel("memory address")
    #plt.show
    plt.savefig("matplotlib.png")
 
if __name__ == "__main__":
    main()

# Code contributed by Dheeraj and Harsh Vardhan Singh  