set proj_name "flash_proj"
set root_path "/home/gbricen2/Thesis_Final/post_insertion_verilog"

create_ip -name vio -vendor xilinx.com -library ip -version 3.0 -module_name vio_0
#set_property -dict [list CONFIG.C_PROBE_IN0_WIDTH {5} CONFIG.C_NUM_PROBE_OUT {0} CONFIG.C_NUM_PROBE_IN {1}] [get_ips vio_0]
set_property -dict [list CONFIG.C_PROBE_OUT0_WIDTH {5} CONFIG.C_NUM_PROBE_OUT {1} CONFIG.C_EN_PROBE_IN_ACTIVITY {0} CONFIG.C_NUM_PROBE_IN {0}] [get_ips vio_0]
generate_target {instantiation_template} [get_files $root_path/$proj_name.srcs/sources_1/ip/vio_0/vio_0.xci]

update_compile_order -fileset sources_1
generate_target all [get_files  $root_path/$proj_name.srcs/sources_1/ip/vio_0/vio_0.xci]
catch { config_ip_cache -export [get_ips -all vio_0] }
export_ip_user_files -of_objects [get_files $root_path/$proj_name.srcs/sources_1/ip/vio_0/vio_0.xci] -no_script -sync -force -quiet
create_ip_run [get_files -of_objects [get_fileset sources_1] $root_path/$proj_name.srcs/sources_1/ip/vio_0/vio_0.xci]
launch_runs -jobs 4 vio_0_synth_1

export_simulation -of_objects [get_files $root_path/$proj_name.srcs/sources_1/ip/vio_0/vio_0.xci] -directory $root_path/$proj_name.ip_user_files/sim_scripts -ip_user_files_dir $root_path/$proj_name.ip_user_files -ipstatic_source_dir $root_path/$proj_name.ip_user_files/ipstatic -lib_map_path [list {modelsim=$root_path/$proj_name.cache/compile_simlib/modelsim} {questa=$root_path/$proj_name.cache/compile_simlib/questa} {ies=$root_path/$proj_name.cache/compile_simlib/ies} {xcelium=$root_path/$proj_name.cache/compile_simlib/xcelium} {vcs=$root_path/$proj_name.cache/compile_simlib/vcs} {riviera=$root_path/$proj_name.cache/compile_simlib/riviera}] -use_ip_compiled_libs -force -quiet

#export_simulation -of_objects [get_files /home/guillermo/school/senior/vivado/sen_test2/sen_test2.srcs/sources_1/ip/vio_0/vio_0.xci] -directory /home/guillermo/school/senior/vivado/sen_test2/sen_test2.ip_user_files/sim_scripts -ip_user_files_dir /home/guillermo/school/senior/vivado/sen_test2/sen_test2.ip_user_files -ipstatic_source_dir /home/guillermo/school/senior/vivado/sen_test2/sen_test2.ip_user_files/ipstatic -lib_map_path [list {modelsim=/home/guillermo/school/senior/vivado/sen_test2/sen_test2.cache/compile_simlib/modelsim} {questa=/home/guillermo/school/senior/vivado/sen_test2/sen_test2.cache/compile_simlib/questa} {ies=/home/guillermo/school/senior/vivado/sen_test2/sen_test2.cache/compile_simlib/ies} {xcelium=/home/guillermo/school/senior/vivado/sen_test2/sen_test2.cache/compile_simlib/xcelium} {vcs=/home/guillermo/school/senior/vivado/sen_test2/sen_test2.cache/compile_simlib/vcs} {riviera=/home/guillermo/school/senior/vivado/sen_test2/sen_test2.cache/compile_simlib/riviera}] -use_ip_compiled_libs -force -quiet
#
##set_property OUTPUT_VALUE 1 [get_hw_probes p_1_in -of_objects [get_hw_vios -of_objects [get_hw_devices xc7z020_1] -filter {CELL_NAME=~"vio"}]]
##commit_hw_vio [get_hw_probes {p_1_in} -of_objects [get_hw_vios -of_objects [get_hw_devices xc7z020_1] -filter {CELL_NAME=~"vio"}]]
