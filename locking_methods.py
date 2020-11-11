import random

from logic_units import *
from fault_analysis import *

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
        self.num_keys = 0
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
                
                if line != "" and "#" not in line:
                    self.logic_lines.append(line)
                    set(self.global_wires).add(get_result(line))

    def print_bench(self):
        print("#Key: {}".format("".join(self.key)))
        print('#Number of keys: {}'.format(self.num_keys))

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

class FBKI(Bench):
    def __init__(self, bench_file):
        super().__init__(bench_file)

    def lock(self):
        locking_logic = []

        hope_log = HopeLog("tests/hope.log")
        hope_log.process_log()
        
        self.num_keys = int((len(hope_log.wire_dict) - len(self.output_wires)) / 2)
        #self.num_keys = 2
        self.key = [str(random.randint(0,1)) for i in range(self.num_keys)]
        key_input_wires = ["probe_out0[{}]".format(i) for i in range(self.num_keys)][::-1]
        
        high_fault_wires = hope_log.get_best_wires(self.num_keys, self.output_wires)
        random.shuffle(high_fault_wires)
        new_fault_wires = []

        #high_fault_wires = [['g16gat', 'g22gat'], ['g11gat', 'g11gat']]

        for key_bit, key_input_wire, fault_wire in zip(self.key, key_input_wires, high_fault_wires):
            new_wire = self.new_wire()
            new_fault_wires.append(new_wire)
            if key_bit == "1":
                locking_logic += self.new_gate("XNOR", [key_input_wire, fault_wire[0]], new_wire)
            else:
                locking_logic += self.new_gate("XOR", [key_input_wire, fault_wire[0]], new_wire)

        new_logic_lines = []
        for gate in self.logic_lines:
            wire_idx = 0
            for wire, idx in zip(high_fault_wires, range(len(high_fault_wires))):
                if wire[0] in gate:
                    wire_idx = idx

            if (high_fault_wires[wire_idx][0] == high_fault_wires[wire_idx][1]):
                gate = gate.replace(high_fault_wires[wire_idx][0], new_fault_wires[wire_idx])
            elif get_result(gate) == high_fault_wires[wire_idx][1]:
                gate = gate.replace(high_fault_wires[wire_idx][0], new_fault_wires[wire_idx])

            new_logic_lines.append(gate)

        self.logic_lines = new_logic_lines + locking_logic

class SARLock(Bench):
    def __init__(self, bench_file):
        super().__init__(bench_file)

    def lock(self):
        locking_logic = []

        self.key = [str(random.randint(0,1)) for i in range(len(self.input_wires))]
        #key_input_generator = generate_wires(self.global_wires, len(self.input_wires))
        #key_input_wires = []
        #for key_wire in key_input_generator:
        #    key_input_wires.append("K{}".format(key_wire))
        key_input_wires = ["probe_out0[{}]".format(i) for i in range(len(self.input_wires))][::-1]
        self.num_keys = len(key_input_wires)

        #self.input_wires += key_input_wires
    
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
        correct_key_logic.append(create_gate("NOT",[correct_key_bit],invert_correct_key_bit))
        fault_wire = self.new_wire()
        correct_key_logic += self.new_gate("AND",[invert_correct_key_bit, equals_bit],fault_wire)
        #inv_fault_wire = self.new_wire()
        #correct_key_logic.append(create_gate("NOT",[fault_wire],inv_fault_wire))

        new_output_wires = []
        new_output_logic = []
        for old_output_wire, num in zip(self.output_wires, range(len(self.output_wires))):
            #locked_output_wire = self.new_wire()
            locked_output_wire = "O{}".format(num)
            new_output_wires.append(locked_output_wire)
            new_output_logic += self.new_gate("XOR",[fault_wire, old_output_wire],locked_output_wire)

        self.output_wires = new_output_wires

        locking_logic = sarlock_comparator + correct_key_logic + new_output_logic
        self.logic_lines += locking_logic
