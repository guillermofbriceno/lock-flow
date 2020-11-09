import os
import fileinput
import shutil
import argparse
from subprocess import Popen, PIPE, STDOUT

target_file = basepath = path = path1 = path2 = ""

def clean_env(arg):
    for file in os.listdir(basepath + "/uncc_automation"):
        if file == ".synopsys_dc.setup" or file == "ctrl.v":
            continue
        print("Removing:", "uncc_automation/" + file)
        if os.path.isfile(basepath + "/uncc_automation/" + file):
            os.remove(basepath + "/uncc_automation/" + file)
        if os.path.isdir(basepath + "/uncc_automation/" + file):
            shutil.rmtree(basepath + "/uncc_automation/" + file)

def config_synthesis(file_withExtension):
    print("file_withExtension:", file_withExtension)
    file_name, extension = file_withExtension.split('.', 1)
    with open(basepath+"synthesis_template.tcl", 'r') as file :
        filedata = file.read()
    filedata = filedata.replace('@@@@@', file_withExtension)
    filedata = filedata.replace('$$$$$', file_name)
    filedata = filedata.replace('*****', extensions[extension])
    with open(path+"/synthesis.tcl", 'w') as file:
        file.write(filedata)

def dc_synthesis(arg):
    os.chdir(path)
    os.system("dc_shell -f synthesis.tcl")
    filedata = None
    with open("synthesized_RTL.v", 'r') as file:
        filedata = file.read()
        filedata = filedata.replace('x',"X")

    with open("synthesized_RTL.v", 'w') as file:
        file.write(filedata) 

def pre_insert_tb(arg):
    os.system("sed -i '1,5d' synthesized_RTL.v")
    os.system("cp synthesized_RTL.v ../pre_insertion_testbench/.")
    os.chdir("../pre_insertion_testbench")
    os.system("python py.py")
    os.system("cp opcode.json ../post_insertion_testbench/.")
    os.system("cp synthesized_RTL.v verilog_tb.v ../vivado_Testing_pre")

def vivado_pre_tb(arg):
    os.chdir(path2)
    os.system("vivado -mode tcl")

def lock_insertion(arg):
    os.chdir(path)
    p = Popen(['abc'], stdout=PIPE, stdin=PIPE, stderr=STDOUT,cwd=path)
    grep_stdout = p.communicate(input=b'rlibc\nrv -m synthesized_RTL.v\nstrash\nmap\nstrash\nwrite_bench -l outputBL.bench\nquit')[0]
    os.system("cp outputBL.bench ../insertion/\ncd ../insertion/\n./lockinsert.py outputBL.bench -method {} > out.bench\ncp out.bench ../post_insertion_verilog/\ncp out.bench ../post_insertion_testbench/ ".format(args.insert_method))
    os.chdir(path1)
    p = Popen(['abc'], stdout=PIPE, stdin=PIPE, stderr=STDOUT,cwd=path1)
    grep_stdout = p.communicate(input=b'rlibc\nrb out.bench\nwv out.v\nquit')[0]

def post_insert_tb(arg):
    os.system("cp out.v ../post_insertion_testbench/.")
    os.chdir("../post_insertion_testbench")
    os.system("python py.py")

def vivado_final(arg):
    os.system("cp out.v verilog_tb.v ../vivado_testing_final")
    os.chdir("../vivado_testing_final")
    os.system("vivado -mode tcl")
    print(grep_stdout)

def flash_fpga(arg):
    os.chdir("post_insertion_verilog")
    os.system("vivado -mode tcl")
    #insert keys here

def do_all():
    config_synthesis()
    dc_synthesis()
    pre_insert_tb()
    vivado_pre_tb()
    lock_insertion()
    post_insert_tb()
    vivado_final()

locking_methods = ["sarlock", "random"]

extensions = {
    'v': 'verilog',
    'vhd': 'vhdl',
    'bench': 'verilog'
    }
steps = {
    'clean_env': clean_env,
    'config_synthesis': config_synthesis,
    'dc_synthesis': dc_synthesis,
    'pre_insert_tb': pre_insert_tb,
    'vivado_pre_tb': vivado_pre_tb,
    'lock_insertion': lock_insertion,
    'post_insert_tb': post_insert_tb,
    'vivado_final': vivado_final,
    'all': do_all
}

parser = argparse.ArgumentParser()
parser.add_argument('bpath', nargs='?')
parser.add_argument('-insert_method', help="Locking method", choices=locking_methods, required=True)
parser.add_argument('-step', help="Automation step to execute", choices=steps.keys())
args = parser.parse_args()

basepath = args.bpath
path = basepath + "uncc_automation"
path1 = basepath + "post_insertion_verilog"
path2 = basepath + "vivado_Testing_pre"

shutil.copy('abc.rc', path)
shutil.copy('cadence.genlib', path)

for file in os.listdir(path):
    extension = file.split('.', 1)[-1]
    if extension in extensions.keys():
        target_file = path
        steps[args.step](file)

