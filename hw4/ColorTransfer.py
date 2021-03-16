import sys

import cv2
import numpy as np


def main():
    if len(sys.argv) < 7:
        print(f'Error: Expect more arguments.\n'
              f'Usage: python {__file__} -s source.jpg -t target.jpg -o output.jpg\n'
              f'if output filename is not provided, \'output.jpg\' is default.')
        exit()
    outfilename = ''
    for i in range(len(sys.argv)):
        if sys.argv[i] == '-s':
            sourcefilename = sys.argv[i + 1]
        if sys.argv[i] == '-t':
            targetfilename = sys.argv[i + 1]
        if sys.argv[i] == '-o':
            outfilename = sys.argv[i + 1]
    if outfilename == '':
        outfilename = 'output.jpg'
    sourcefile = cv2.imread(sourcefilename)
    targetfile = cv2.imread(targetfilename)
    outputfile = color_transfer(sourcefile, targetfile)
    cv2.imwrite(outfilename, outputfile)


def color_transfer(source, target, sideinfodeci='sideinfodeci.txt'):
    '''
    source, target: both are np.ndarray
    '''
    source_b, source_g, source_r = cv2.split(source)
    (source_mean_r, source_std_r, source_mean_g, source_std_g, source_mean_b, source_std_b) = _get_img_properties(source)
    (target_mean_r, target_std_r, target_mean_g, target_std_g, target_mean_b, target_std_b) = _get_img_properties(target)
    with open(sideinfodeci, 'w') as f:
        f.write('%.4f\n%.4f\n%.4f\n%.4f\n%.4f\n%.4f\n'
                '%.4f\n%.4f\n%.4f\n%.4f\n%.4f\n%.4f'
                %(source_mean_r, source_mean_g, source_mean_b,source_std_r, source_std_g,  source_std_b,
                  target_mean_r, target_mean_g, target_mean_b, target_std_r, target_std_g, target_std_b))
    out_r = source_r.astype(dtype=np.uint8)
    out_g = source_g.astype(dtype=np.uint8)
    out_b = source_b.astype(dtype=np.uint8)
    out_r = (target_std_r / source_std_r) * (out_r - source_mean_r) + target_mean_r
    out_g = (target_std_g / source_std_g) * (out_g - source_mean_g) + target_mean_g
    out_b = (target_std_b / source_std_b) * (out_b - source_mean_b) + target_mean_b
    out = cv2.merge((out_b, out_g, out_r))
    return out


def _get_img_properties(img):
    '''
    helper function for color_transform
    '''
    b, g, r = cv2.split(img)
    mean_r = r.mean()
    std_r = r.std()
    mean_g = g.mean()
    std_g = g.std()
    mean_b = b.mean()
    std_b = b.std()
    return mean_r, std_r, mean_g, std_g, mean_b, std_b


if __name__ == '__main__':
    main()
