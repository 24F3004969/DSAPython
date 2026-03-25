import numpy as np


def floydwarshall(WMat):
    (rows, cols, x) = WMat.shape
    infinity = np.max(WMat) * rows * rows + 1
    SP = np.zeros(shape=(rows, cols, cols + 1))
    for i in range(rows):
        for j in range(cols):
            SP[i, j, 0] = infinity

    for i in range(rows):
        for j in range(cols):
            if WMat[i, j, 0] == 1:
                SP[i, j, 0] = WMat[i, j, 1]

    for k in range(1, cols + 1):
        for i in range(rows):
            for j in range(cols):
                SP[i, j, k] = min(SP[i, j, k - 1],
                                  SP[i, k - 1, k - 1] + SP[k - 1, j, k - 1])

    return SP[:, :, cols]
