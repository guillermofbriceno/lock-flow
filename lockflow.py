#!/usr/bin/python3

import argparse

from locking_methods import *
from logic_units import *

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', nargs='?')
    parser.add_argument('method', nargs='?')
    args = parser.parse_args()

    #methods = {
    #        'sarlock':      sarlock,
    #        'sarlock+sll':  sarlock_sll,
    #        'naive':        naive
    #        }

    #obf_bench = methods[args.method]()
    obf_bench = create_dmux("IN1", ["O0","O1","O2","O3"],["S0","S1"],[])
    for line in obf_bench:
        print(line)

if __name__ == "__main__":
    main()
