import numpy as np

# Module to quantize an 8x8 block

table_quantization = np.array(
    [
        [16, 11, 10, 16, 24, 40, 51, 61],
        [12, 12, 14, 19, 26, 58, 60, 55],
        [14, 13, 16, 24, 40, 57, 69, 56],
        [14, 17, 22, 29, 51, 87, 80, 62],
        [18, 22, 37, 56, 68, 109, 103, 77],
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99],
    ]
)


def quantize(block, quantiz_matrix=table_quantization):
    block = np.array(block)
    return (block / quantiz_matrix).round().astype(np.int32)

def quantize_b(block, color_channel):
    if color_channel == "lum":
        return quantize(block)
    elif color_channel == "chrom":
        return quantize(block)
    else:
        print('Error - Color Channel specified is not supported')



if __name__ == "__main__":
    block_test = [
        [338, 145, -8, 18, -7, 4, 16, -14],
        [162, -41, 3, 2, 3, -1, -13, 9],
        [-17, 57, -2, -2, -20, 16, 2, 10],
        [41, 19, -24, 31, -19, -8, 4, -1],
        [-59, 7, -2, -32, 21, -1, 6, -15],
        [-19, 12, 32, 0, -16, -9, -15, 12],
        [7, -55, -24, 17, 20, 15, -4, 0],
        [15, -11, 10, 11, -18, -13, 10, -10],
    ]

    print(quantize(block_test))
