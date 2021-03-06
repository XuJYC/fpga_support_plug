#!/usr/bin/env python
# coding=utf-8

'''
#Author       : sterben(Duan)
#LastAuthor   : sterben(Duan)
#Date         : 2020-02-03 17:09:48
#lastTime     : 2020-02-11 16:49:33
#FilePath     : ./.TOOL/Link/start.py
#Description  : 
'''

import os
import sys
import glob 
import shutil
import linecache

def deldir(path):
	folder = os.path.exists(path)
	if folder:                  
		shutil.rmtree(path.replace("\\", "/"))    

def movedir(sourse_path,target_path,gen_path):
	folder = os.path.exists(os.path.join(sourse_path,gen_path).replace("\\", "/"))
	if folder :                  
		deldir(os.path.join(target_path,gen_path).replace("\\", "/"))
		shutil.move(os.path.join(sourse_path,gen_path).replace("\\", "/"),target_path)
	else :
		if gen_path != "TOP.v" :
			mkdir(os.path.join(target_path,gen_path).replace("\\", "/"))

def file_update(path) :
	fpga_include = linecache.getline(path,7)
	if fpga_include.replace('\n', '') == "none" :
		movedir("./user/Hardware","./user","data")
		movedir("./user/Hardware","./user","src")
		movedir("./user/Hardware","./user","sim")
		movedir("./user/Hardware","./user","TOP.v")
		deldir("./user/Hardware")
		deldir("./user/Software")
	else :
		mkdir("./user/Hardware")
		movedir("./user","./user/Hardware","data")
		movedir("./user","./user/Hardware","src")
		movedir("./user","./user/Hardware","sim")
		movedir("./user","./user/Hardware","TOP.v")
		mkdir("./user/Software/data")
		mkdir("./user/Software/src")

def del_file(file_param):
	for infile in glob.glob(os.path.join(file_param, '*.jou')):
		os.remove(infile)
	for infile in glob.glob(os.path.join(file_param, '*.log')):
		os.remove(infile)
	for infile in glob.glob(os.path.join(file_param, '*.str')):
		os.remove(infile)
	for infile in glob.glob(os.path.join(file_param, "prj/", '*.jou')):
		os.remove(infile)
	for infile in glob.glob(os.path.join(file_param, "prj/", '*.log')):
		os.remove(infile)
	folder = os.path.exists(os.path.join(file_param,".Xil"))
	if folder:
		shutil.rmtree(os.path.join(file_param,".Xil"))

def mkdir(path):
	folder = os.path.exists(path)
	if not folder:                  
		os.makedirs(path)         

def tb_file(path):
	folder = os.path.exists(path)
	if not folder:                  
		tb_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),".TOOL/Xilinx/Data/testbench.v")
		shutil.copy(tb_file_path,path)  

def top_file(path):
	folder = os.path.exists(path)
	if not folder:                  
		tb_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),".TOOL/Xilinx/Data/TOP.v")
		shutil.copy(tb_file_path,path)  

def make_boot():
	folder = os.path.exists("./user/BOOT")
	output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),".TOOL/Xilinx/BOOT/")                  
	f = open(os.path.join(output_path,"output.bif"), 'w')
	if not folder:
		output_file = "//arch = zynq; split = false; format = BIN\nthe_ROM_image:\n{\n\t[bootloader]%sfsbl.elf\n\t./template.bit\n\t%sps_test.elf\n}" % ((output_path.replace("\\", "/")),(output_path.replace("\\", "/")))
		f.write(output_file)
		f.close()
	else :
		output_file = "//arch = zynq; split = false; format = BIN\nthe_ROM_image:\n{\n\t[bootloader]./user/BOOT/fsbl.elf\n\t./template.bit\n\t./user/BOOT/ps_test.elf\n}"
		f.write(output_file)
		f.close()
		
def Handle_file():
	#handle xilinx
	f_list = os.listdir("./prj/xilinx")
	for file in f_list:
		if os.path.splitext(file)[1] == ".xpr":
			tcl_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),".TOOL/Xilinx/run.tcl")
			cmd = "vivado -mode tcl -s %s ./prj/Xilinx/template.xpr -notrace" % (tcl_file.replace("\\", "/"))
			os.system(cmd)
			return 1
	return 0     

def mkconfig(path) :
	mkdir("./prj/xilinx")
	mkdir("./prj/alter")
	mkdir("./prj/modelsim")
	folder = os.path.exists(path)
	if not folder:
		config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),".TOOL/Makefile")
		shutil.copy(config_file_path,path)
	fpga_Version = linecache.getline(path,3)
	fpga_include = linecache.getline(path,7)
	make_boot()
	if Handle_file() : #Open existing project
		return 1
	else:              #Creat New project
		# os.remove("./Makefile")
		# config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),".TOOL/Makefile")
		# shutil.copy(config_file_path,path)
		file_update(path)
		if fpga_include.replace('\n', '') == "none" :
			tb_file("./user/sim/testbench.v")
			top_file("./user/TOP.v")
		else:
			tb_file("./user/Hardware/sim/testbench.v")
			top_file("./user/Hardware/TOP.v")
		if fpga_Version.replace('\n', '') == "xilinx" :
			tcl_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),".TOOL/Xilinx/Start.tcl")
			cmd = "vivado -mode tcl -s %s -notrace" % (tcl_file.replace("\\", "/"))
			os.system(cmd)
		else:
			pass
		return 0

def main():
	del_file("./")
	mkconfig("./Makefile")
	del_file("./")

if __name__ == "__main__":
    main()