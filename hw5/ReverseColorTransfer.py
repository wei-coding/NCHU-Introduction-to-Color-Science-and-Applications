import sys
import cv2
import numpy as np
import traceback


def reverse_color_transfer(result: np.ndarray, sideinfo) -> np.ndarray:
    """take in numpy array and FILE, return numpy array"""

    inform = sideinfo.read().strip().split('\n')
    for i in range(len(inform)):
        inform[i] = float(inform[i])
    (source_mean_r, source_mean_g, source_mean_b,
     source_std_r, source_std_g, source_std_b,
     target_mean_r, target_mean_g, target_mean_b,
     target_std_r, target_std_g, target_std_b) = (inform[x] for x in range(12))

    result_b, result_g, result_r = cv2.split(result)

    out_r = (source_std_r / target_std_r) * (result_r - target_mean_r) + source_mean_r
    out_g = (source_std_g / target_std_g) * (result_g - target_mean_g) + source_mean_g
    out_b = (source_std_b / target_std_b) * (result_b - target_mean_b) + source_mean_b
    out_r = out_r.astype(dtype=np.uint8)
    out_g = out_g.astype(dtype=np.uint8)
    out_b = out_b.astype(dtype=np.uint8)

    return cv2.merge((out_b, out_g, out_r))


def main():
    if len(sys.argv) < 3:
        print(f'Usage: {sys.argv[0]} resultfile sideinformfile')
        exit()
    resultfile = sys.argv[1]
    sideinformfile = sys.argv[2]
    try:
        result = cv2.imread(resultfile)
        with open(sideinformfile, 'r') as sideinfo:
            img = reverse_color_transfer(result, sideinfo)
    except Exception:
        print(traceback.format_exc())
        print('Error occured! Check whether input format is right!')
        exit()
    cv2.imwrite('output.bmp', img)
    cv2.imshow('input', result)
    cv2.imshow('output', img)
    cv2.waitKey(-1)


if __name__ == '__main__':
    main()
