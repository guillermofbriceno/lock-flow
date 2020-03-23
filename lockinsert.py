#!/usr/bin/python3

import argparse

from locking_methods import *

def main():
    methods = {
        'sarlock':      SARLock
    }

    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', nargs='?')
    parser.add_argument('-method', help="Locking method",choices=methods.keys(), required=True)
    args = parser.parse_args()

    bench = methods[args.method](args.input_file)
    bench.lock()
    bench.print_bench()

if __name__ == "__main__":
    main()
