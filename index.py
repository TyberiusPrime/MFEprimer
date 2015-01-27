#!/usr/bin/python
import subprocess
import os
import sys

from sys import platform as _platform
if _platform == "linux" or _platform == "linux2":
    platform = 'linux'
    # linux
elif _platform == "darwin":
    platform = 'mac'
    # OS X
elif _platform == "win32":
    raise ValueError("currently no windows support")
else:
    raise ValueError("Operation system detection failed")


def print_usage():
    print 'index.py genome.fasta k'
    print 'k is a small integer, such as 9'
    sys.exit()

def fasta_to_2bit(fasta_filename):
    if not os.path.exists(fasta_filename + '.2bit'):
        cmd = [os.path.join(os.path.dirname(__file__), './bin/' + platform + '/64/faToTwoBit'),
                fasta_filename,
                fasta_filename + '.2bit']
        subprocess.check_call(cmd)

def fasta_to_index(fasta_filename, k):
    cmd = [os.path.join(os.path.dirname(__file__), './chilli/mfe_index_db.py'),
            '-f', os.path.abspath(fasta_filename),
            '-k', str(k)]
    subprocess.check_call(cmd)


def main():
    if len(sys.argv) not in (2, 3):
        print_usage()
    fasta_filename = sys.argv[1]
    if not os.path.exists(fasta_filename):
        raise ValueError("Fasta not found: %s" % fasta_filename)
    if len(sys.argv) == 3:
        try:
            k = int(sys.argv[2])
        except ValueError:
            print_usage()
    else:
        k = 9

    fasta_to_2bit(fasta_filename)
    fasta_to_index(fasta_filename, k)



if __name__ == '__main__': 
    main()
