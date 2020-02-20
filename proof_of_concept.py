#!/usr/bin/python3

""" Proof of concept using naive key gate
    insertion scheme. Temporarily used for reference.
"""

import sys
import random

def get_args(line):
    return line[line.find('(')+1:line.find(')')].split(',')

def get_result(line):
    return line[:line.find('=')] if '=' in line else None

def get_func(line):
    return line[line.find('=')+1:] if '=' in line else None

def main():
    read_bench = []
    output_wires = []
    input_lines = []
    num_outputs = 0
    
    with open(sys.argv[1], 'r') as bench:
        for line in bench:
            line = line.replace(" ", "").lower().rstrip()
            if "output(" in line:
                output_wires.append(get_args(line)[0])
                num_outputs += 1
                continue
            if "input(" in line:
                input_lines.append(line)


            read_bench.append(line)

    key = [str(random.randint(0,1)) for i in range(num_outputs)]
    key_inputs = ["KY{}".format(x) for x in range(len(key))]
    outputs = ["OB{}".format(x) for x in range(len(key))]
    obf_bench = ["INPUT({})".format(x) for x in key_inputs] + ["OUTPUT({})".format(x) for x in outputs]
    print("#Key:", ''.join(key))
    key_bit_idx = 0

    wire_comps = []

    for line in read_bench:
        if ('=' in line) and (get_result(line) in output_wires):
            obf_bench.append(line.upper())
            if key[key_bit_idx] == '0':
                obf_bench.append("{}=XOR({},{})".format(outputs[key_bit_idx], get_result(line), key_inputs[key_bit_idx]).upper())
            else:
                wire_comp = "WC{}".format(random.randint(0,99))
                while(wire_comp in wire_comps):
                    wire_comp = "WC{}".format(random.randint(0,99))
                wire_comps.append(wire_comp)

                obf_bench.append("{}=XOR({},{})".format(wire_comp, get_result(line), key_inputs[key_bit_idx]).upper())
                obf_bench.append("{}=NOT({})".format(outputs[key_bit_idx], wire_comp))

            key_bit_idx += 1
            continue
        
        obf_bench.append(line.upper())

    for line in obf_bench:
        print(line)

if __name__ == "__main__":
    main()
