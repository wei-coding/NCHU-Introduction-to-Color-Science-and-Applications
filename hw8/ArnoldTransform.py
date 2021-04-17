import cv2
import numpy as np


def arnold_transfer(inputfile, comaprefile, forward) -> int:
    img = cv2.imread(inputfile)
    N = img.shape[0]
    new_img = np.copy(img)
    cmp = cv2.imread(comaprefile)
    x, y = np.meshgrid(range(N), range(N))
    cycle = 0
    if forward:
        xx = (x + y) % N
        yy = (x + 2 * y) % N
    else:
        xx = (2 * x - y) % N
        yy = (-1 * x + y) % N
    while True:
        new_img = new_img[yy, xx]
        cycle += 1
        cv2.imshow('img', new_img)
        cv2.waitKey(1)
        print(cycle)
        if not (new_img - cmp).any():
            cv2.waitKey(-1)
            break
    return cycle


def main():
    print(arnold_transfer('Alschair-1000.bmp', 'Alschair-1000.bmp', False))


if __name__ == '__main__':
    main()
