import random
import numpy as np
import matplotlib.pyplot as plt
import argparse


class LogisticMap:
    def __init__(self, inputfilename='input09.txt'):
        try:
            file = open(inputfilename, 'r')
        except FileNotFoundError:
            print(f'{inputfilename} is not found')
            exit(-1)
        self._x0, self._r, self._n, self._seed = map(float, file.readline().strip().split(' '))
        if not (self._r <= 4 or self._r > 3.56995):
            raise NonChaoticBehaviorException()
        self._xn = self._x0
        file.close()

    def next(self) -> float:
        self._xn = self.logistic_map(self._xn, self._r)
        return self._xn

    @staticmethod
    def logistic_map(xn: float, r: float):
        return r * xn * (1 - xn)

    def get_attr(self):
        return self._x0, self._r, int(self._n), int(self._seed)


class NonChaoticBehaviorException(Exception):
    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str)
    parser.add_argument('-o', '--output', type=str)
    args = parser.parse_args()
    infile = 'input09.txt'
    outfile = 'output09.csv'
    if args.input and args.output:
        infile = args.input
        outfile = args.output
    logistic_map = LogisticMap(infile)
    attr = logistic_map.get_attr()
    GEN = attr[2]
    random.seed(attr[3])
    rand_by_default = [random.random() for _ in range(GEN)]
    rand_by_logistc = [logistic_map.next() for _ in range(GEN)]
    r1 = np.asarray(rand_by_default)
    r2 = np.asarray(rand_by_logistc)
    kwargs = dict(histtype='stepfilled', alpha=0.3, bins=10)
    plt.hist(r1, **kwargs, color="red")
    plt.hist(r2, **kwargs, color="blue")
    plt.show()
    with open(outfile, 'w') as f:
        f.write('{},{},{},{}\n'.format(*attr))
        for i in range(GEN):
            f.write('{},{:.6f},{:.6f}\n'.format(i+1, rand_by_logistc[i], rand_by_default[i]))
        f.write('mean,{:.6f},{:.6f}\n'.format(np.mean(r2), np.mean(r1)))
        f.write('std,{:.6f},{:.6f}'.format(np.std(r2), np.std(r1)))
    return


if __name__ == "__main__":
    main()
