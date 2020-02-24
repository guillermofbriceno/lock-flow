import random

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

    comp_bench.append(create_gate("AND", and_bits, out_bit))
    return comp_bench
