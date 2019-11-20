import sys
from word_root import parse_line, get_root_usage

def parse_txt_file(fname, outputfile):
    with open(fname, 'r') as inf:
        txt = inf.read()
        tag_txt = parse_line(txt)
        with open(outputfile, 'w') as outf:
            output = get_root_usage(tag_txt)
            output += tag_txt["view"]
            outf.write(output)

if __name__ == '__main__':
    usage = "python mark_txt.py file.txt output.txt"
    if len(sys.argv) != 3:
        print(usage)
        exit(1)
    parse_txt_file(sys.argv[1], sys.argv[2])
