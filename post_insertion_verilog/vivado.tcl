create_project -force flash_proj -part xc7z020clg400-1
set_property board_part www.digilentinc.com:pynq-z1:part0:1.0 [current_project]
add_files -norecurse final.v
add_files -fileset constrs_1 -norecurse PYNQ-Z1_C.xdc
update_compile_order -fileset sources_1

set_property target_constrs_file PYNQ-Z1_C.xdc [current_fileset -constrset]

source vio.tcl

update_compile_order -fileset sources_1
launch_runs impl_1 -to_step write_bitstream -jobs 4

#start_gui

wait_on_run impl_1
open_hw_manager
connect_hw_server -allow_non_jtag
open_hw_target
set_property PROGRAM.FILE {/home/gbricen2/Thesis_Final/post_insertion_verilog/flash_proj.runs/impl_1/out.bit} [get_hw_devices xc7z020_1]
set_property PROBES.FILE {/home/gbricen2/Thesis_Final/post_insertion_verilog/flash_proj.runs/impl_1/out.ltx} [get_hw_devices xc7z020_1]
set_property FULL_PROBES.FILE {/home/gbricen2/Thesis_Final/post_insertion_verilog/flash_proj.runs/impl_1/out.ltx} [get_hw_devices xc7z020_1]
current_hw_device [get_hw_devices xc7z020_1]
refresh_hw_device [lindex [get_hw_devices xc7z020_1] 0]

refresh_hw_target {localhost:3121/xilinx_tcf/Digilent/003017AD40A1A}
set_property PROBES.FILE {/home/gbricen2/Thesis_Final/post_insertion_verilog/flash_proj.runs/impl_1/out.ltx} [get_hw_devices xc7z020_1]
set_property FULL_PROBES.FILE {/home/gbricen2/Thesis_Final/post_insertion_verilog/flash_proj.runs/impl_1/out.ltx} [get_hw_devices xc7z020_1]
set_property PROGRAM.FILE {/home/gbricen2/Thesis_Final/post_insertion_verilog/flash_proj.runs/impl_1/out.bit} [get_hw_devices xc7z020_1]
program_hw_devices [get_hw_devices xc7z020_1]
refresh_hw_device [lindex [get_hw_devices xc7z020_1] 0]

puts -nonewline "Enter key: "
flush stdout
set key [gets stdin]

set_property OUTPUT_VALUE $key [get_hw_probes probe_out0 -of_objects [get_hw_vios -of_objects [get_hw_devices xc7z020_1] -filter {CELL_NAME=~"vio"}]]
commit_hw_vio [get_hw_probes {probe_out0} -of_objects [get_hw_vios -of_objects [get_hw_devices xc7z020_1] -filter {CELL_NAME=~"vio"}]]
