import random
from logic_units import *

def get_args(line):
    return line[line.find('(')+1:line.find(')')].split(',')

def get_result(line):
    return line[:line.find('=')] if '=' in line else None

def get_func(line):
    return line[line.find('=')+1:] if '=' in line else None

class Bench:
    def __init__(self, bench_file):
        self.input_wires = []
        self.output_wires = []
        self.logic_lines = []
        self.global_wires = []
        self.read_bench(bench_file)
    
    def read_bench(self, bench_file):
        with open(bench_file, 'r') as bench:
            for line in bench:
                line = line.replace(" ","").lower().rstrip()
                if "output(" in line:
                    self.output_wires.append(get_args(line)[0])
                    continue
                if "input(" in line:
                    self.input_wires.append(get_args(line)[0])
                    continue
                
                if line != "":
                    self.logic_lines.append(line)
                    set(self.global_wires).add(get_result(line))

    def print_bench(self):
        print("#Key: {}".format("".join(self.key)))

        for wire in self.input_wires:
            print("INPUT({})".format(wire.upper()))

        for wire in self.output_wires:
            print("OUTPUT({})".format(wire.upper()))

        print("")

        for line in self.logic_lines:
            print(line.upper())

    def new_wire(self):
        return create_wire(self.global_wires)

    def new_gate(self, type_str, input_wires, output_bit):
        return create_multi_gate(type_str,2,input_wires,output_bit,self.global_wires)


class SARLock(Bench):
    def __init(self, bench_file):
        super().__init__(bench_file)

    def lock(self):
        locking_logic = []

        self.key = [str(random.randint(0,1)) for i in range(len(self.input_wires))]
        key_input_generator = generate_wires(self.global_wires, len(self.input_wires))
        key_input_wires = []
        for key_wire in key_input_generator:
            key_input_wires.append("K{}".format(key_wire))

        self.input_wires = self.input_wires + key_input_wires
    
        equals_bit = self.new_wire()
        sarlock_comparator = create_comp(self.input_wires, key_input_wires, equals_bit, self.global_wires)

        correct_key_logic_wires = []
        correct_key_logic = []
        for key_bit, key_wire in zip(self.key, key_input_wires):
            if key_bit == '0':
                outp = self.new_wire()
                correct_key_logic.append(create_gate("NOT", [key_wire], outp))
                correct_key_logic_wires.append(outp)
            if key_bit == '1':
                correct_key_logic_wires.append(key_wire)

        correct_key_bit = self.new_wire()
        correct_key_logic += self.new_gate("AND", correct_key_logic_wires, correct_key_bit)
        invert_correct_key_bit = self.new_wire()
        correct_key_logic += self.new_gate("NOT",[correct_key_bit],invert_correct_key_bit)
        fault_wire = self.new_wire()
        inv_fault_wire = self.new_wire()
        correct_key_logic += self.new_gate("NOT",[fault_wire],inv_fault_wire)
        correct_key_logic += self.new_gate("NAND",[invert_correct_key_bit, equals_bit],inv_fault_wire)

        new_output_wires = []
        new_output_logic = []
        for old_output_wire in self.output_wires:
            locked_output_wire = self.new_wire()
            new_output_wires.append(locked_output_wire)
            new_output_logic += self.new_gate("AND",[inv_fault_wire, old_output_wire],locked_output_wire)

        self.output_wires = new_output_wires

        locking_logic = sarlock_comparator + correct_key_logic + new_output_logic
        self.logic_lines += locking_logic





