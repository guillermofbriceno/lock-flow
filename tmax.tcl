read_netlist /home/gbricen2/Thesis_Final/uncc_automation/out_nolibs.v
run_build_model outputBL
run_drc
set_faults -model stuck -fault_coverage
remove_faults -all
add_faults -all
run_atpg -ndetects 1
report_patterns -all -internal > tmax.log
quit
