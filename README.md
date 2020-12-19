# lock-flow

This is a Python script designed to read netlists in BENCH format and lock the design using a variety of user-selectable locking methods. It outputs a new BENCH file with the inserted locking mechanism and key.

This is a Python script designed to read HDL files and lock the design using a variety of user-selectable locking methods. It outputs a new Verilog file which can be flashed to an FPGA.

Designed by the UNCC FLOW Senior Design project team.

<img src="https://emptytincan.com/r/781k9" width="180">

## Usage

Run the script with Python3:

`python3 automation.py -step <step> -method <method> <project path>`
