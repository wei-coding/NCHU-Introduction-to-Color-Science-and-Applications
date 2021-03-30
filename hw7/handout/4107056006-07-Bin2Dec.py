import argparse


def converter(n: str, sgn_len=1, exp_len=8, mant_len=23) -> float:
    raw_int = int(n, 2)
    # print(raw_int)
    sign = (raw_int & (2 ** sgn_len - 1) * (2 ** (exp_len + mant_len))) >> (exp_len + mant_len)
    exponent_raw = (raw_int & ((2 ** exp_len - 1) * (2 ** mant_len))) >> mant_len
    mantissa = raw_int & (2 ** mant_len - 1)

    sign_mult = 1
    if sign == 1:
        sign_mult = -1

    if exponent_raw == 2 ** exp_len - 1:  # Could be Inf or NaN
        if mantissa == 2 ** mant_len - 1:
            return float('nan')  # NaN

        return sign_mult * float('inf')  # Inf

    exponent = exponent_raw - (2 ** (exp_len - 1) - 1)

    if exponent_raw == 0:
        mant_mult = 0  # Gradual Underflow
    else:
        mant_mult = 1

    for b in range(mant_len - 1, -1, -1):
        if mantissa & (2 ** b):
            mant_mult += 1 / (2 ** (mant_len - b))

    return sign_mult * (2 ** exponent) * mant_mult


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input file name", type=str)
    parser.add_argument("-o", "--output", help="output file name", type=str)
    args = parser.parse_args()
    infile_name = args.input
    outfile_name = "sideinfodeci.txt" if args.output is None else args.output
    with open(infile_name, 'r') as f:
        with open(outfile_name, 'w') as g:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line != "":
                    g.writelines(str(converter(line)) + "\n")


if __name__ == '__main__':
    main()
