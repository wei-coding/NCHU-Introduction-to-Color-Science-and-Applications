import random
import math
from decimal import *
import argparse


class SecretKey:
    def __init__(self, **kwargs):
        self.rx = Decimal(kwargs['rx'])
        self.x0 = Decimal(kwargs['x0'])
        self.ry = Decimal(kwargs['ry'])
        self.y0 = Decimal(kwargs['y0'])
        self.xn = self.x0
        self.yn = self.y0
        self.seed = kwargs['seed']
        self.N = int(kwargs['N'])
        self.L = kwargs['L']
        random.seed(self.seed)

    def next_x(self):
        self.xn = self._next(self.rx, self.xn)
        return self.xn

    def next_y(self):
        self.yn = self._next(self.ry, self.yn)
        return self.yn

    def get_xn(self, n):
        for _ in range(n):
            self.xn = self.next_x()
        return self.xn

    def get_yn(self, n):
        for _ in range(n):
            self.yn = self.next_y()
        return self.yn

    def write_file(self, path='output10.txt'):
        with open(path, 'w') as f:
            f.write("{} {}\n".format(self.x0, self.rx))
            f.write("{} {}\n".format(self.y0, self.ry))
            f.write("%d %d\n" % (self.seed, self.N))
            f.write("%f\n" % self.L)
            r1 = random.randint(1, self.N)
            r2 = random.randint(1, self.N)
            f.write("%d %d %d\n" % (r1, r2, random.randint(1, self.N)))
            xn = self.get_xn(r1)
            yn = self.get_yn(r2)
            f.write(f"{xn} {yn}\n")
            f.write("%d %d\n" % (math.ceil(xn / self.L) + r1, math.ceil(yn / self.L) + r2))

    @staticmethod
    def _next(r: Decimal, a: Decimal) -> Decimal:
        return Decimal(r * a * (1 - a))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', type=str, help='output file path')
    parser.add_argument('input')
    args = parser.parse_args()
    getcontext().prec = 21
    f = open(args.input, "r")
    lines = f.readlines()
    x0, rx = map(Decimal, lines[0].strip().split(' '))
    y0, ry = map(Decimal, lines[1].strip().split(' '))
    seed, N = map(float, lines[2].strip().split(' '))
    L = Decimal(*lines[3].strip().split(' '))
    sk = SecretKey(x0=x0, rx=rx, y0=y0, ry=ry, seed=seed, N=N, L=L)
    if args.output:
        sk.write_file(path=args.output)
    else:
        sk.write_file()
    f.close()


if __name__ == "__main__":
    main()
