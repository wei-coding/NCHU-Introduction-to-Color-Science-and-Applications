import ColorTransfer as ct
import sys
import cv2


def reverse_color_transfer(result, sideinform):
    """take in numpy array and FILE, return numpy array"""
    inform = sideinform.read().strip().split('\n')
    pass


def main():
    if len(sys.argv) < 3:
        print(f'Usage: {sys.argv[0]} resultfile sideinformfile')
    resultfile = sys.argv[1]
    sideinformfile = sys.argv[2]
    result = cv2.imread(resultfile)
    sideinform = open(sideinformfile, 'r')
    img = reverse_color_transfer(result, sideinform)
    cv2.imwrite('output.bmp', img)


if __name__ == '__main__':
    main()
