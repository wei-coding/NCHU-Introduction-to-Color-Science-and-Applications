import cv2
import numpy as np
import os
import math
import argparse


def main(**args):
    if args.get('path'):
        args['path'] = os.path.normpath(args['path'])
        file_list = os.listdir(args['path'])
        this_path = args['path']
    else:
        file_list = os.listdir('.\\')
        this_path = '.\\'
    for file in file_list:
        fullpath = os.path.join(this_path, file)
        if os.path.isdir(fullpath):
            images = os.listdir(fullpath)
            if file == "Origi_image":
                calc(fullpath, 'output11.csv')
            elif file == "Encry_image":
                calc(fullpath, 'output11_en.csv')
            elif file == "Decry_image":
                calc(fullpath, 'output11_de.csv')
            else:
                print('the directory have some unrecognized file!')
                exit(1)


def calc(path, filename):
    count = 1
    files = os.listdir(path)
    with open(filename, 'w') as f:
        f.write('No,Images,MIR,MIG,MIB,VHR,VHG,VHB,SER,SEG,SEB\n')
        for file in files:
            fullpath = os.path.join(path, file)
            img = cv2.imread(fullpath, cv2.IMREAD_COLOR)
            b_chan, g_chan, r_chan = cv2.split(img)
            f.write(f'{count},{file},'
                    f'{round(np.mean(r_chan), 2):.2f},{round(np.mean(g_chan), 2):.2f},{round(np.mean(b_chan), 2):.2f},'
                    f'{var(r_chan):.2f},{var(g_chan):.2f},{var(b_chan):.2f},'
                    f'{entropy(r_chan):.6f},{entropy(g_chan):.6f},{entropy(b_chan):.6f}\n')
            count += 1


def var(img):
    stat = get_stat(img)
    size = 256 ** 2
    tot = 0
    for s in stat:
        tot += s ** 2
    tot /= size
    mean = 0
    for s in stat:
        mean += s
    mean /= size
    _var = tot - mean ** 2
    return round(_var, 2)


def entropy(img):
    stat = get_stat(img)
    size = img.shape[0] * img.shape[1]
    # print(size)
    tot = 0
    for i in range(256):
        if stat[i] == 0:
            tot += 0
        else:
            tot += (stat[i] / size) * math.log2(stat[i] / size)
    tot = -tot
    return round(tot, 6)


def get_stat(img):
    _stat = [0 for _ in range(256)]
    for i in range(len(img)):
        for j in range(len(img[i])):
            _stat[img[i, j]] += 1
    # print(_stat)
    return _stat


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str)
    args = parser.parse_args()
    if args.input:
        main(path=args.input)
    else:
        main(path='.\\11-Images')
