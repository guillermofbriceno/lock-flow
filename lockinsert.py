#!/usr/bin/python3

import argparse

from locking_methods import *

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', nargs='?')
    parser.add_argument('method', nargs='?')
    args = parser.parse_args()

    methods = {
        'sarlock':      SARLock
    }

    bench = methods[args.method](args.input_file)
    bench.lock()
    bench.print_bench()

if __name__ == "__main__":
    main()
