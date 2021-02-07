# lock-flow

This is a Python script designed to read HDL files and lock the design using a variety of user-selectable locking methods. It outputs a new Verilog file which can be flashed to an FPGA.

Designed by the UNCC FLOW Senior Design project team.

<img src="https://emptytincan.com/r/781k9" width="180">

## Usage

Run the script with Python3:

`python3 automation.py -step <step> -method <method> <project path>`

## Citation

@INPROCEEDINGS{9322831,
  author={W. {Halaburda} and G. {Briceno} and W. {Obey} and N. N. {BouSaba} and F. {Saqib}},
  booktitle={2020 IEEE 17th International Conference on Smart Communities: Improving Quality of Life Using ICT, IoT and AI (HONET)}, 
  title={A Novel User-Friendly Automated Framework for FPGA Design Logic Encryption}, 
  year={2020},
  volume={},
  number={},
  pages={241-243},
  doi={10.1109/HONET50430.2020.9322831}}
