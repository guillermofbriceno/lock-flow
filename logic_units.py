import random
import itertools
import math

def create_wire(wires):
    """ Create a new wire. Ensures no wire conflicts and abstracts naming mechanism.
        Adds the generated wire back into the global wire list.
        Args:
            wires (list): Global wire list.
        Returns:
            str: Name of the wire generated"""

    while True:
        wire = "WG{}".format(random.randint(0,999))
        if wire not in wires:
            wires.append(wire)
            return wire

def generate_wires(wires, num_wires):
    for i in range(num_wires):
        wire = ""
        while True:
            wire = "WG{}".format(random.randint(0,999))
            if wire not in wires:
                wires.append(wire)
                break
        yield wire

def create_gate(type_str, inputs, out):
    """ Create a BENCH logic gate
        Args:
            type_str (str): The logic gate name printed in the file.
            inputs (list): The wire inputs used as arguments for the gate.
            out (str): The output wire being assigned
        Returns:
            str: A BENCH gate with wired inputs and outputs"""

    gate_args = ','.join(inputs)
    return "{}={}({})".format(out, type_str, gate_args)

def create_dmux(inp, out, sel, wires):
    """ Create a demultiplexer given an arbitrary number of selection
        bits and outputs. Implemented with a decoder.
        Args:
            inp (str): Single input wire.
            out (list): List of output wires.
            sel (list): List of select wires.
            wires (list): The global wire list.
        Returns:
            list: BENCH snippet of the demultiplexer"""

    dmux_bench = []

    # Create inverted selection bits for each select line
    inverted_sel = [create_wire(wires) for i in range(len(sel))]

    for sel_wire, inv_sel_wire in zip(sel, inverted_sel):
        dmux_bench.append(create_gate("NOT", [sel_wire], inv_sel_wire))

    for i in range(len(out)):
        binary = "{0:032b}".format(i)[::-1]
        and_inputs = []
        for index, sel_wire, inv_sel_wire in zip(range(len(sel)), sel, inverted_sel):
            if binary[index] == '0':
                and_inputs.append(inv_sel_wire)
            else:
                and_inputs.append(sel_wire)
    
        dmux_bench.append(create_gate("AND", [inp] + and_inputs, out[i]))

    return dmux_bench

def create_comp(in1, in2, out_bit, wires):
    comp_bench = []
    and_bits = []
    for wire1, wire2 in zip(in1, in2):
        out_xor = create_wire(wires)
        out_not = create_wire(wires)
        comp_bench.append(create_gate("XOR", [wire1, wire2], out_xor))
        comp_bench.append(create_gate("NOT", [out_xor], out_not))
        and_bits.append(out_not)

    comp_bench += create_multi_gate("AND", 2,and_bits, out_bit, wires)
    return comp_bench

def create_multi_gate(type_str, max_args, inputs, output, global_wires):
    """ Given a limited gate argument size, this function creates
        a waterfall of gates with max_args number of inputs that copies the
        functionality of a gate with len(inputs) number of inputs
        Args:
            type_str     (str): The type of gate being cascaded.
            max_args     (int): Number of inputs desired per gate.
            inputs       (lst): List of input wires.
            output       (str): Output wire.
            global_wires (lst): The global wire list.
        Returns:
            list: BENCH snippet of the multi-gate"""

    multi_input_gate = []

    inputs_grouped = [inputs[n:n+(max_args - 1)] for n in range(1, len(inputs), (max_args - 1))]
    carry_wires = itertools.chain([inputs[0]], generate_wires(global_wires,math.ceil((len(inputs)-1)/(max_args-1) - 1)), [output])
    curr_carry_wire = next(carry_wires)

    for in_wires in inputs_grouped:
        next_carry_wire = next(carry_wires)
        gate = create_gate(type_str, [curr_carry_wire] + in_wires, next_carry_wire)
        curr_carry_wire = next_carry_wire
        multi_input_gate.append(gate)

    return multi_input_gate
