#saves name of registers
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

#saves name of opcodes and their binary representaion
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

#saves name of opcodes and their types
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

#saves name of registers and their values
Register_values = \
    {
        "000": 0,
        "001": 0,
        "010": 0,
        "011": 0,
        "100": 0,
        "101": 0,
        "110": 0,
        "111": 0,
    }

#saves name of flag and their status
FlagS =\
    {
        "E": 0,
        "G": 0,
        "L": 0,
        "V": 0,
    }

#converts decimal numbers to 8 bit binary code
def binary(a):
    bnr = bin(a).replace('0b', '')
    x = bnr[::-1]  # this reverses an array
    while len(x) < 8:
        x += '0'
    bnr = x[::-1]
    return bnr

#the main driver function
def main():
    temp_dic = {}       #to store file
    var_dict = {}       #to store var and location
    var_val = {}        #to store var and value
    label_dict = {}     #to store label and location
    count_line = 0      #setting pointer to 0
    for i in range(0, 257):
        temp_dic[i] = [None, None, None, None, None]
    while True:
        try:
            line = input()
            if line != "":
                count_line = count_line + 1
                temp_dic[count_line-1] = line.split(" ")
        except EOFError:
            break

    num = count_line    #stores lines in code
    count_line = 0      #resetting pointer to 0
    c = num
    to = 0
    hlt_no = 0
    while c > 0:
        le = len(temp_dic[c-1][0])
        if temp_dic[c-1][0][le - 1] == ':':                        #finding labels
            label_dict[temp_dic[c-1][0][0:le - 1]] = c - 1
            if len(temp_dic[c-1]) > 1:
                temp_dic[c - 1] = temp_dic[c - 1][1:]
            else:
                temp_dic[c - 1][0] = "_" #empty label

        if temp_dic[c - 1][0] == "var":                            #finding variables
            if 1 < len(temp_dic[c - 1]) <= 2:
                to = to + 1
                ele = temp_dic[c - 1][1]
                var_dict[ele] = c - 1
                var_val[temp_dic[c - 1][1]] = 0
            else:
                print("Error! VAR name not defined or more than 1 defined in one line in line")
                print(c-1)

        if temp_dic[c-1][0] == "hlt":
            hlt_no = hlt_no + 1
        c = c - 1

    #finding problems with labels,variables and halt commands before checking syntax of prog
    lab_prob = 0
    for i,j in label_dict.items():
        for k in i:
            if (k >= 'a' and k <='z') or (k >= 'A' and k <='Z') or (k >= '1' and k <='9') or (k=='_'):
                lab_prob = 0
            else:
                lab_prob = lab_prob + 1
                print("Error in label naming in line ")
                print(j)
                break

    hlt_prob = 0
    if temp_dic[num-1][0] != "hlt":
        hlt_prob = 1
        print("Error! hlt is missing in last line or overflow has occurred")

    var_prob = 0
    for i in range(0, to):
        if temp_dic[i][0] != "var":
            print("Error! all var not initialized at beginning ")
            var_prob = 1
            break
    if hlt_no>1:
        hlt_prob = 1
        print("Multiple hlt declared")

    #using a func 'output' to find errors and our desired output in binary format
    output(temp_dic, var_dict, label_dict, var_val, count_line, num-1, to, var_prob, hlt_prob ,lab_prob)


#definition of output 
def output(temp_dic, var_dict, label_dict, var_val, count_line, num, to, var_prob, hlt_prob ,lab_prob):
            x = 0 #acts like a flag giving us general errors on some specific values

            #passing if it is var
            if temp_dic[count_line][0] == "var":
                x = x + 1

            #passing if it is empty label,exception
            if temp_dic[count_line][0] == "-":
                x = x + 1

            #setting overload flags if required
            for key,numb in Register_values.items():
                if numb>=65536 or numb<0:
                    FlagS["V"] = 1

            #quitting prog if overload detected   ( not consider)
            # if FlagS["V"] == 1:
            #      print("Error ! 1 of the Registers has overloaded")  
            #      exit()

            #starting checking of type and assigning opcodes
            if 0 <= count_line <= num and var_prob == 0 and hlt_prob == 0 and lab_prob == 0:
                for i, j in opcodes.items():
                    if temp_dic[count_line][0] == j:
                        type_of = opcodes_type[i]

                        #as there are 2 mov and we are directly assigning types, we differentiate bw the 2 mov functions
                        if temp_dic[count_line][0] == "mov":
                            if temp_dic[count_line][2][0] == "R" or temp_dic[count_line][2][0] == "F":
                                type_of = opcodes_type["00011"]
                                i = "00011"
                            else:
                                type_of = opcodes_type["00010"]
                                i = "00010"

                        #conditioning to narrow down to desired result
                        if type_of == "A":
                            #checking if syntax for type is correct
                            if len(temp_dic[count_line]) == 4:
                                if(temp_dic[count_line][1][0] == "R" or temp_dic[count_line][1][0] == "F") and\
                                        (temp_dic[count_line][2][0] == "R") and\
                                        (temp_dic[count_line][3][0] == "R"):
                                    for a, b in Register_dict.items():
                                        for c, d in Register_dict.items():
                                            for e, f in Register_dict.items():
                                                if temp_dic[count_line][1] == b and \
                                                        temp_dic[count_line][2] == d and \
                                                        temp_dic[count_line][3] == f:
                                                            print(i+"00"+a+c+e) #printing the 16 bit instruction
                                                            x = x + 1
                                                            #assigning values to register in accordance to instruction
                                                            if(temp_dic[count_line][0]=="add"):
                                                                Register_values[a] = Register_values[c] + Register_values[e]
                                                            if (temp_dic[count_line][0] == "sub"):
                                                                Register_values[a] = Register_values[c] - Register_values[e]
                                                            if (temp_dic[count_line][0] == "mul"):
                                                                Register_values[a] = Register_values[c] - Register_values[e]
                                                            if (temp_dic[count_line][0] == "xor"):
                                                                Register_values[a] = Register_values[c] ^ Register_values[e]
                                                            if (temp_dic[count_line][0] == "or"):
                                                                Register_values[a] = Register_values[c] or Register_values[e]
                                                            if (temp_dic[count_line][0] == "and"):
                                                                Register_values[a] = Register_values[c] & Register_values[e]
                                                            if (temp_dic[count_line][0] == "or"):
                                                                Register_values[a] = Register_values[c] | Register_values[e]
                                                            break

                        elif type_of == "B":
                            #checking if syntax for type is correct
                            if len(temp_dic[count_line]) == 3:
                                if (temp_dic[count_line][1][0] == "R") and temp_dic[count_line][2][0] == "$":
                                    for q, k in Register_dict.items():
                                        if temp_dic[count_line][1] == k and temp_dic[count_line][2][0] == "$":
                                            if 0 <= int(temp_dic[count_line][2][1:]) <= 255:
                                                z = binary(int(temp_dic[count_line][2][1:]))
                                                print(i+q+z) #printing the 16 bit instruction
                                                x = x+1
                                                #assigning values to register in accordance to instruction
                                                if (temp_dic[count_line][0] == "mov"):
                                                    Register_values[q] = int(temp_dic[count_line][2][1:])
                                                if (temp_dic[count_line][0] == "rs"):
                                                    Register_values[q] >> int(temp_dic[count_line][2][1:])
                                                if (temp_dic[count_line][0] == "ls"):
                                                    Register_values[q] << int(temp_dic[count_line][2][1:])
                                                break
                                            else:
                                                print("Error ! Value should be between 0 and 255 at line:")
                                                print(count_line)
                                                x = x + 1
                                    break
                                else:
                                    x = x + 1
                                    print("Arguments not matching type B arguments in line")
                                    print(count_line)
                                break
                            else:
                                x = x + 1
                                print("Arguments not matching type B arguments in line")
                                print(count_line)

                        elif type_of == "C":
                            #checking if syntax for type is correct
                            if len(temp_dic[count_line]) == 3:
                                if (temp_dic[count_line][1][0] == "R" or temp_dic[count_line][1][0] == "F") and \
                                        (temp_dic[count_line][2][0] == "R" or temp_dic[count_line][2][0] == "F"):
                                    for q, k in Register_dict.items():
                                        for m, n in Register_dict.items():
                                            if temp_dic[count_line][1] == k and temp_dic[count_line][2] == n:
                                                print(i+"00000"+q+m) #printing the 16 bit instruction
                                                x = x + 1
                                                #assigning values to register in accordance to instruction
                                                if (temp_dic[count_line][0] == "mov"):
                                                    Register_values[q] = Register_values[m]
                                                if (temp_dic[count_line][0] == "div"):
                                                    Register_values["000"] = int(Register_values[q] / Register_values[m])
                                                    Register_values["001"] = Register_values[q]%Register_values[m]
                                                if (temp_dic[count_line][0] == "not"):
                                                    Register_values[q] = ~Register_values[m]
                                                if (temp_dic[count_line][0] == "cmp"):
                                                    if Register_values[q] > Register_values[m]:
                                                        FlagS["G"] = 1
                                                    if Register_values[q] == Register_values[m]:
                                                        FlagS["E"] = 1
                                                    if Register_values[q] < Register_values[m]:
                                                        FlagS["L"] = 1
                                    break
                                else:
                                    x = x + 1
                                    print("Arguments not matching type C arguments in line")
                                    print(count_line)
                                break
                            else:
                                x = x + 1
                                print("Arguments not matching type B arguments in line")
                                print(count_line)

                        elif type_of == "D":
                            #checking if syntax for type is correct
                            if len(temp_dic[count_line]) == 3:
                                for q, k in Register_dict.items():
                                    for m, n in var_dict.items():
                                        if temp_dic[count_line][1] == k:
                                            if (temp_dic[count_line][2]) == m:
                                                z = binary(num + n)
                                                print(i+q+z) #printing the 16 bit instruction
                                                x = x + 1
                                                #assigning values to register in accordance to instruction
                                                if (temp_dic[count_line][0] == "ld"):
                                                    var_val[m] = Register_values[q]
                                                if (temp_dic[count_line][0] == "st"):
                                                     Register_values[q] = var_val[m]
                                                break
                                        elif (temp_dic[count_line][2]) != m:
                                            x = x + 1
                                break
                            else:
                                x = x + 1
                                print("Arguments not matching type D arguments in line")
                                print(count_line)
                                break

                        elif type_of == "E":
                            jump = True #value of jump depends on value of flags we use 
                            #checking if syntax for type is correct
                            if len(temp_dic[count_line]) == 2:
                                if len(label_dict) == 0: # excaeption handling
                                    x = x + 1
                                    print("Error ! label not declared in line:")
                                    print(count_line)
                                    break
                                for q, k in label_dict.items(): 
                                    if (temp_dic[count_line][1]) == q:
                                        z = binary(k-to)
                                        x = x + 1
                                        if (temp_dic[count_line][0] == "jmp") or \
                                                (temp_dic[count_line][0] == "jlt" and FlagS["L"] == 0) or \
                                                (temp_dic[count_line][0] == "jgt" and FlagS["G"] == 0) or \
                                                (temp_dic[count_line][0] == "je" and FlagS["E"] == 0):
                                            jump = True
                                            print(i+"000"+z) #printing the 16 bit instruction
                                        else:
                                            jump = False
                                            print(i+"000"+z) #printing the 16 bit instruction
                                        break
                                    elif label_dict != q:
                                        x = x + 1
                                        print("Error ! label not declared in line:")
                                        print(count_line)
                                        break
                                break
                            else:
                                x = x + 1
                                print("Arguments not matching type E arguments in line")
                                print(count_line)
                                break

                        elif type_of == "F":
                            #checking if syntax for type is correct
                            if len(temp_dic[count_line]) == 1:
                                print(i+"00000000000") #printing the 16 bit instruction
                                x = x+1
                                break
                            else:
                                x = x + 1
                                print("Arguments not matching type F arguments in line")
                                print(count_line)
                                break


                        else:
                            #code will never logically reach here
                            print("impossible")

                        break

                if x == 0:
                    p = count_line
                    print("typo in line:")
                    print(p)

                if x == 7:
                    print("Error ! variable not declared in line:")
                    print(count_line)

                output(temp_dic, var_dict, label_dict, var_val, count_line+1, num, to, var_prob, hlt_prob, lab_prob)

if __name__ == "__main__":
    main()

#if code doesnt reach 16 bit instruction then it usually reaches a possible error which user may have made
# Code contributed by Harsh Vardhan Singh and Dheeraj