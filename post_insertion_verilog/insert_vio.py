#!/bin/python3

import sys

num_keys = 0

with open("out.bench", 'r') as f:
	for line in f:
		if "Number of keys" in line:
			num_keys = int(line[line.index(": ")+2:-1])
			break

new_verilog = []
vio_block = ["wire [{}:0] probe_out0;\n".format(int(num_keys) - 1), "vio_0 vio(\n", ".clk(clk)\n", ".probe_out0(probe_out0)\n", ");\n"]
keys = ["K{}".format(i) for i in range(int(num_keys))]
with open ("out.v", 'r') as f:
	in_wire_block = False
	out_of_wire_block = False
	for line in f:
		if not in_wire_block:
			for key_wire in keys:
				if key_wire in line:
					line = line.replace(key_wire+",", "")
					line = line.replace(key_wire, "")

		else:
			for key_wire in keys:
				if key_wire in line:
					line = line.replace(key_wire, "probe_out0[{}]".format(key_wire[1:]))

		if "wire" in line:
			in_wire_block = True

		new_verilog.append(line)

		if ";" in line and in_wire_block and not out_of_wire_block:
			new_verilog += vio_block
			out_of_wire_block = True


with open ("final.v", 'w') as f:
	for line in new_verilog:
		line = ' '.join(line.split())
		line = line.replace(', ;', ";") + "\n"
		#print(line)
		f.write(line)
	
			
			
