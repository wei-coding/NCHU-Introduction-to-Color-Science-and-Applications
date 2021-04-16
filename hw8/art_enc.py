import argparse

import cv2
import numpy as np
import threading


def arnold_transfer(inputfile, outputfile, times, forward) -> int:
    img = cv2.imread(inputfile)
    N = img.shape[0]
    new_img = np.copy(img)
    x, y = np.meshgrid(range(N), range(N))
    cycle = 0
    xx = (2 * x - y) % N
    yy = (-1 * x + y) % N
    while True:
        new_img = new_img[yy, xx]
        cycle += 1
        if not (new_img - img).any():
            break
    if forward:
        xx = (x + y) % N
        yy = (x + 2 * y) % N
    else:
        xx = (2 * x - y) % N
        yy = (-1 * x + y) % N
    for _ in range(times):
        img = img[yy, xx]
    cv2.imwrite(outputfile, img)
    return cycle


def save_data(file_setting, args):
    switch = {
        '+': True,
        '-': False,
    }
    cycle_time = arnold_transfer(
        file_setting[0],
        f'ART{file_setting[1]}{file_setting[2]}_{file_setting[0]}',
        int(file_setting[2]),
        switch[file_setting[1]]
    )
    with open(args.output, 'a') as fo:
        fo.writelines(f'ART{file_setting[1]}{file_setting[2]}_{file_setting[0]}'
                      f' {file_setting[1]} {file_setting[2]} {cycle_time}\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', help='input filename with extension', type=str, required=True)
    parser.add_argument('--output', '-o', help='output filename with extension', type=str, required=True)
    args = parser.parse_args()
    open(args.output, 'w')
    with open(args.input, 'r') as f:
        '''
        txt looks like this:
        Alschari-1000.bmp + 20
        Anturium-512.bmp + 187
        BeaverDam-800.bmp - 27
        Blackcat-1280.jpg + 741
        Cars-1024.bmp - 45
        '''
        lines = f.readlines()
        for line in lines:
            if line.strip() == '':
                break
            file_setting = line.strip().split(' ')
            switch = {
                '+': True,
                '-': False,
            }
            print(f'processing {file_setting[0]} ...')
            cycle_time = arnold_transfer(
                file_setting[0],
                f'ART{file_setting[1]}{file_setting[2]}_{file_setting[0]}',
                int(file_setting[2]),
                switch[file_setting[1]]
            )
            with open(args.output, 'a') as fo:
                fo.writelines(f'ART{file_setting[1]}{file_setting[2]}_{file_setting[0]}'
                              f' {file_setting[1]} {file_setting[2]} {cycle_time}\n')


if __name__ == '__main__':
    main()
