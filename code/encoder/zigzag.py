# functions used for compression purposes

# packages
import numpy as np


def block_to_zigzag(matrix):
    """function that reads the coefficients of a square matrix in zigzag

    parameters
    ----------
        - matrix : (array of array)-like (size must be a square)

    return
    ------
        - list of coefficients read in zigzag"""
    h = 0
    v = 0
    v_min = 0
    h_min = 0
    v_max = matrix.shape[0]
    h_max = matrix.shape[1]
    i = 0
    output = np.empty((v_max * h_max), dtype=np.uint8)

    while (v < v_max) and (h < h_max):
        if ((h + v) % 2) == 0:  # going up
            if v == v_min:
                output[i] = matrix[v, h]  # first line
                if h == h_max:
                    v = v + 1
                else:
                    h = h + 1
                i = i + 1
            elif (h == h_max - 1) and (v < v_max):  # last column
                output[i] = matrix[v, h]
                v = v + 1
                i = i + 1
            elif (v > v_min) and (h < h_max - 1):  # all other cases
                output[i] = matrix[v, h]
                v = v - 1
                h = h + 1
                i = i + 1
        else:  # going down
            if (v == v_max - 1) and (h <= h_max - 1):  # last line
                output[i] = matrix[v, h]
                h = h + 1
                i = i + 1
            elif h == h_min:  # first column
                output[i] = matrix[v, h]
                if v == v_max - 1:
                    h = h + 1
                else:
                    v = v + 1
                i = i + 1
            elif (v < v_max - 1) and (h > h_min):  # all other cases
                output[i] = matrix[v, h]
                v = v + 1
                h = h - 1
                i = i + 1
        if (v == v_max - 1) and (h == h_max - 1):  # bottom right element
            output[i] = matrix[v, h]
            break
    return output



def zigzag_to_block(zigzag_matrix):
    rows, cols = zigzag_matrix.shape
    size = rows * cols
    output = np.zeros((rows, cols), dtype=zigzag_matrix.dtype)
    row, col = 0, 0
    index = 0
    direction = 1

    while index < size:
        output[row, col] = zigzag_matrix[index]
        if row == 0 and col == cols - 1:
            row += 1
        elif col == 0 and row == rows - 1:
            col += 1
        elif row == 0 or col == cols - 1:
            if col == cols - 1:
                row += 1
            else:
                col += 1
            direction = -direction
        elif col == 0 or row == rows - 1:
            if row == rows - 1:
                col += 1
            else:
                row += 1
            direction = -direction
        else:
            row -= direction
            col += direction
        index += 1

    return output

if __name__ == "__main__":
    matrix = np.array([[1, 2, 3, 4],
                   [5, 6, 7, 8],
                   [9, 10, 11, 12]])

    coefficients = block_to_zigzag(matrix)
    print(coefficients)

    test = np.array([[i + j for j in range(8)] for i in range(0, 64, 8)])
    print(block_to_zigzag(test))
