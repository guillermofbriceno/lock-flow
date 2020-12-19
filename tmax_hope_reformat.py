#!/bin/python3

test_pattern_list = []
with open("tmax.log", 'r') as f:
  for line in f:
    if "force_all_pis" in line:
      test_pattern_list.append(line.strip().split(" ")[-1])


for test_pattern, count in zip(test_pattern_list, range(1, len(test_pattern_list)+1)):
    print("{}: {}".format(count, test_pattern))
