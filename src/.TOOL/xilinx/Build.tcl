set_param general.maxThreads 6
variable current_Location [file normalize [info script]]

# unset ::env(PYTHONPATH)
# unset ::env(PYTHONHOME)

# set ::env(PYTHONPATH) "C:/Program Files/Python38/python38.zip:C:/Program Files/Python38/DLLs:C:/Program Files/Python38/lib:C:/Program Files/Python38:C:/Program Files/Python38/lib/site-packages"
# set ::env(PYTHONHOME) "C:/Program Files/Python38"

set found   0
set showlog 0
set fp [open "./Makefile" r]
while { [gets $fp data] >= 0 } {
	if { [string equal -length 4 $data xc7z] == 1 } {
        set found 1
    }
	if { [string equal -length 6 $data Showlog] == 1 } {
        gets $fp data
		if { [string equal -length 3 $data yes] == 1 } {
        	set showlog 1
    	}
		if { [string equal -length 2 $data no] == 1 } {
        	set showlog 0
    	}
    }
}
close $fp

if {$found == 0 } {
    set_property STEPS.WRITE_BITSTREAM.ARGS.BIN_FILE true [get_runs impl_1]
} 

#run synth
reset_run synth_1 -quiet
launch_run synth_1 -quiet
wait_on_run synth_1 -quiet
if {$showlog == 1} {
	exec python [file dirname $current_Location]/Script/showlog.py -quiet
}
exec python [file dirname $current_Location]/Script/Log.py -quiet
write_checkpoint -force ./prj/xilinx/template.runs/synth_1/TOP.dcp -quiet
#run impl
reset_run impl_1 -quiet
launch_run impl_1 -quiet
wait_on_run impl_1 -quiet
if {$showlog == 1} {
	exec python [file dirname $current_Location]/Script/showlog.py -quiet
}
exec python [file dirname $current_Location]/Script/Log.py -quiet
open_run impl_1 -quiet
report_timing_summary -quiet

write_checkpoint -force ./prj/xilinx/template.runs/impl_1/TOP_routed.dcp -quiet
#Gen boot
if {$found == 0} {
	write_bitstream ./[current_project].bit -force -quiet -bin_file
} 

if {$found == 1} {
	write_bitstream ./[current_project].bit -force -quiet
    exec bootgen -arch zynq -image [file dirname $current_Location]/BOOT/output.bif -o ./BOOT.bin -w on
} 
