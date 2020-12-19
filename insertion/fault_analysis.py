#!/bin/bash

def hamming(x, y):
    distance = 0
    for bitx, bity in zip(x, y):
        distance += 1 if bitx != bity else 0
    return distance

class HopeWire:
    def __init__(self):
        self.name = ""
        self.sa01 = [0, 0]
        self.sa_dists = [0, 0]

    def stuckat(self, val, dist):
        self.sa01[val] += 1
        self.sa_dists[val] += dist

    def calc_fault_impact(self):
        self.fault_impact = (self.sa01[0] * self.sa_dists[0]) + (self.sa01[1] * self.sa_dists[1])

class HopeLog:
    def __init__(self, log_path):
        self.wire_dict = {}
        self.log_path = log_path

    def process_log(self):
        with open(self.log_path, 'r') as f:
            current_output = ""
            for line in f:
                if "test" in line:
                    current_output = line.split()[-1].rstrip()
                if "*" in line:
                    wire, stuckat, _, outp = line.rstrip().split()
                    stuckat = int(stuckat.replace(":", "").replace("/", ""))
                    if wire not in self.wire_dict.keys():
                        self.wire_dict[wire] = HopeWire()

                    self.wire_dict[wire].stuckat(stuckat, hamming(current_output, outp))

        for wire, name in zip(self.wire_dict.values(), self.wire_dict.keys()):
            wire.calc_fault_impact()
            wire.name = [name.split("->")[0].lower(), name.split("->")[1].lower()] if "->" in name else [name.lower(), name.lower()]

    def get_best_wires(self, amount, output_wire_names):
        wires_list = [wire for wire in self.wire_dict.values() if wire.name[0] not in output_wire_names]
        sorted_wire_list = sorted(wires_list, key=lambda x: x.fault_impact, reverse=True)
        sorted_wire_list = [wire.name for wire in sorted_wire_list]
        return sorted_wire_list[0:amount]

    def print_results(self):
        print("{:20} {:>4} {:>4} {:>4}".format("Wire Name", "sa0", "sa1", "FI"))
        for wire, name in zip(self.wire_dict.values(), self.wire_dict.keys()):
            print("{:20} {:4} {:4} {:4}".format(name, wire.sa01[0], wire.sa01[1], wire.fault_impact))

#log = HopeLog("tests/hope.log")
#log.process_log()
#
#for wire in log.get_best_wires(10, ["G22gat", "G23gat"]):
#    print(wire.name, wire.fault_impact)
