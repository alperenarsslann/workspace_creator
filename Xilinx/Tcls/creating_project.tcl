# creating_project.tcl
# Call style:
# vivado -mode batch -source creating_project.tcl -tclargs <workspace_root> <project_name>

start_gui

set workspace_root [file normalize [lindex $argv 0]]
set project_name   [lindex $argv 1]

# Workspace altındaki Vivado klasörü
set vivado_dir [file join $workspace_root "Vivado"]
file mkdir $vivado_dir

# Proje oluştur (logdaki gibi ./Vivado altında)
create_project $project_name $vivado_dir -part xc7z020clg484-1 -force

# Zybo board (senin logda çalışıyor)
set_property board_part digilentinc.com:zybo-z7-20:part0:1.1 [current_project]

# BD oluştur (logdaki gibi "design_1")
set bd_name "${project_name}_design_1"
create_bd_design $bd_name
update_compile_order -fileset sources_1

startgroup
create_bd_cell -type ip -vlnv xilinx.com:ip:processing_system7:5.5 processing_system7_0
create_bd_cell -type ip -vlnv xilinx.com:ip:proc_sys_reset:5.0 proc_sys_reset_0
endgroup

# PS7 automation (logdaki config'e yakın)
apply_bd_automation -rule xilinx.com:bd_rule:processing_system7 \
  -config {make_external "FIXED_IO, DDR" apply_board_preset "1" Master "Disable" Slave "Disable"} \
  [get_bd_cells processing_system7_0]

startgroup
apply_bd_automation -rule xilinx.com:bd_rule:board \
  -config {Manual_Source {Auto}} \
  [get_bd_pins proc_sys_reset_0/ext_reset_in]

apply_bd_automation -rule xilinx.com:bd_rule:clkrst \
  -config {Clk {/processing_system7_0/FCLK_CLK0 (50 MHz)} Freq {50}} \
  [get_bd_pins proc_sys_reset_0/slowest_sync_clk]

connect_bd_net \
  [get_bd_pins processing_system7_0/M_AXI_GP0_ACLK] \
  [get_bd_pins processing_system7_0/FCLK_CLK0]
endgroup


save_bd_design
validate_bd_design

# BD target üret (wrapper yolu doğru oluşsun)
set bd_file [get_files -quiet *.bd]
generate_target all $bd_file
export_ip_user_files -of_objects $bd_file -no_script -sync -force -quiet
create_ip_run $bd_file

# Wrapper üret + projeye ekle (logdaki gibi)
make_wrapper -files $bd_file -top
set wrapper_v [glob -nocomplain "$vivado_dir/$project_name.gen/sources_1/bd/$bd_name/hdl/*_wrapper.v"]
if {[llength $wrapper_v] > 0} {
    add_files -norecurse $wrapper_v
    update_compile_order -fileset sources_1
}

close_project
exit
