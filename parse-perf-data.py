import argparse
import os
import re
# sudo perf list
# sudo perf stat --all-user -e <ev0> -e <ev1> ./prg

# Run on output of:
# $> sudo perf record -b -e cycles ./prg
# $> sudo perf annotate -no-source --asm-raw
# $> sudo perf script -F brstack > file.txt

parser = argparse.ArgumentParser(description="Parse perf.data brstack")

parser.add_argument("-f", action="store", default=None, help="File to parse")
parser.add_argument("--sprase",
                    action="store_true",
                    default=False,
                    help="File to parse")


class BR_Info():
    def __init__(self, br_line):
        self.br_line = br_line
        self.from_addr = None
        self.to_addr = None
        self.pred = None
        self.cycles = None

        self.parse_br_line()

    def parse_br_line(self):
        br_arr = self.br_line.split("/")
        assert len(br_arr) == 6

        self.from_addr = hex(int(br_arr[0], 16))
        self.to_addr = hex(int(br_arr[1], 16))

        assert br_arr[2] == 'P' or br_arr[2] == 'M'
        self.pred = (br_arr[2] == 'P')

        self.cycles = int(br_arr[5])

    def make_output(self):
        return "[{}, {:<4}: {} -> {}]".format('P' if self.pred else 'M',
                                           self.cycles, self.from_addr,
                                           self.to_addr)


class BR_Stack():
    def __init__(self, raw_line):
        self.raw_line = re.sub(' +', ' ', raw_line.lstrip().rstrip())
        self.br_infos = []

        self.parse_br_stack()

    def parse_br_stack(self):
        br_info_arr = self.raw_line.split(" ")
        assert len(
            br_info_arr
        ) == 32, "------------------------------------\n{}\n------------------------------------\n{} -> {}\n".format(
            self.raw_line, len(br_info_arr), str(br_info_arr))

        for br in br_info_arr:
            self.br_infos.insert(0, BR_Info(br))

    def make_output(self):
        out = ""
        for br_info in self.br_infos:
            out += br_info.make_output() + "\n"
        return out


class EXE_Info():
    def __init__(self, fname):
        self.fname = fname
        self.br_stacks = []
        self.parse_exe_info()

    def parse_exe_info(self):
        assert os.access(self.fname, os.R_OK)
        f = open(self.fname, "r")

        for line in f:
            self.br_stacks.append(BR_Stack(line))

    def make_output(self):
        out = ""
        for br_stack in self.br_stacks:
            out += "-------------------------------------------\n" + br_stack.make_output(
            ) + "\n"
        return out


args = parser.parse_args()
fname = args.f

assert fname is not None

exe_info = EXE_Info(fname)
print(exe_info.make_output())
