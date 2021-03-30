import argparse
import struct


def converter(dec: float) -> str:
    n = struct.unpack("I", struct.pack("f", dec))[0]
    # print(n)
    if dec > 0:
        return "0{0:b}".format(n)
    else:
        return "{0:b}".format(n)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input file name", type=str)
    parser.add_argument("-o", "--output", help="output file name", type=str)
    args = parser.parse_args()
    infile_name = args.input
    outfile_name = "sideinfobina.txt" if args.output is None else args.output
    with open(infile_name, 'r') as f:
        with open(outfile_name, 'w') as g:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line != "":
                    dec = float(line)
                    g.writelines(converter(dec)+"\n")


if __name__ == '__main__':
    main()
