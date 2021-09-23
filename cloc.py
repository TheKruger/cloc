import os
import sys
from colorama import init as cinit

cinit()

white = "\033[0m"
lgreen = "\033[92m"
lyellow = "\033[93m"
lblue = "\033[94m"

buf_size = 1024*1024

def GetLinesOfFile(file) -> int:
    f = open(file, "rb")
    lines = 0
    read_f = f.read

    buf = read_f(buf_size)
    while buf:
        lines += buf.count(b'\n')
        buf = read_f(buf_size)

    return lines + 1

def Help():
    
    print("usage: {0} <directory or file> <specific file extensions> <options>".format(sys.argv[0]))

    print("\nOptions:")
    print("  -v, --verbose    Show the file lines (only for directories).")
    print("  -n, --no-color   Disable the colors.")

    print("\nExamples:")
    print("  {0} code.py".format(sys.argv[0]))
    print("  {0} projectdir".format(sys.argv[0]))
    print("  {0} projectdir py,c,h".format(sys.argv[0]))

    sys.exit(0)

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("usage: {0} <directory or file> <specific file extensions> <options>".format(sys.argv[0]))
        print("try '{0} --help'".format(sys.argv[0]))
        sys.exit(0)

    if "-h" in sys.argv or "--help" in sys.argv:
        Help()

    target = sys.argv[1]
    exts = ""

    nocolor = False
    verbose = False

    if "-v" in sys.argv or "--verbose" in sys.argv:
        verbose = True 

    if "-n" in sys.argv or "--no-color" in sys.argv:
        nocolor = True

    if len(sys.argv) >= 3:
        exts = sys.argv[2].split(",")
        for i in range(len(exts)):
            exts[i] = "." + exts[i]
        exts = tuple(exts)

    for i in exts:
        if "-" in i:
            exts = ""

    if os.path.isfile(target):
        
        if not os.path.exists(target):
            print("File {0} not exist.".format(target))

        lines = GetLinesOfFile(target)
        if nocolor:
            print("File {0} have {1} lines.".format(target, "{:,}".format(lines)))
            sys.exit(0)
        print("File {0} have {1} lines.".format(lblue + target + white, lgreen + "{:,}".format(lines) + white))

    else:

        if not os.path.exists(target):
            print("File {0} not exist.".format(target))

        Files = []
        r = 0
        count = 0

        target = os.path.abspath(target)

        # Collect the files.
        if exts == "":
            for root, dirs, files in os.walk(target):
                for file in files:
                    Files.append(os.path.join(root, file))
        else:
            for root, dirs, files in os.walk(target):
                for file in files:
                    if file.endswith(exts):
                        Files.append(os.path.join(root, file))

        # Printing / Counting file lines.
        for file in Files:
            try:
                line = GetLinesOfFile(file)
            except Exception as e:
                print("An error occurred in file:\n\t {0}.\nError: {1}".format(file, e))
            if verbose:
                if nocolor:
                    print("({0}/{1}) File {2} have {3} lines.".format(len(Files), count, file, "{:,}".format(line)))
                else:
                    print("({0}/{1}) File {2} have {3} lines.".format(lyellow + str(len(Files)) + white, lyellow + str(count) + white, lblue + file + white, lgreen + "{:,}".format(line) + white))
            r += line
            count += 1
        if nocolor:
            print("Directory {0} have {1} files with altogether {2} lines.".format(target, "{:,}".format(len(Files)), r))
            sys.exit(0)
        print("Directory {0} have {1} files with altogether {2} lines.".format(lblue + target + white, lgreen + "{:,}".format(len(Files)) + white, lgreen + "{:,}".format(r) + white))