import numpy as np


def load_quantization_table(component):
    # Quantization Table for: Photoshop - (Save For Web 080)
    # (http://www.impulseadventure.com/photo/jpeg-quantization.html)
    if component == "lum":
        q = np.array(
            [
                [2, 2, 2, 2, 3, 4, 5, 6],
                [2, 2, 2, 2, 3, 4, 5, 6],
                [2, 2, 2, 2, 4, 5, 7, 9],
                [2, 2, 2, 4, 5, 7, 9, 12],
                [3, 3, 4, 5, 8, 10, 12, 12],
                [4, 4, 5, 7, 10, 12, 12, 12],
                [5, 5, 7, 9, 12, 12, 12, 12],
                [6, 6, 9, 12, 12, 12, 12, 12],
            ]
        )
    elif component == "chrom":
        q = np.array(
            [
                [3, 3, 5, 9, 13, 15, 15, 15],
                [3, 4, 6, 11, 14, 12, 12, 12],
                [5, 6, 9, 14, 12, 12, 12, 12],
                [9, 11, 14, 12, 12, 12, 12, 12],
                [13, 14, 12, 12, 12, 12, 12, 12],
                [15, 12, 12, 12, 12, 12, 12, 12],
                [15, 12, 12, 12, 12, 12, 12, 12],
                [15, 12, 12, 12, 12, 12, 12, 12],
            ]
        )
    else:
        raise ValueError(
            (
                "component should be either 'lum' or 'chrom', " "but '{comp}' was found"
            ).format(comp=component)
        )

    return q


def bits_required(n):
    n = abs(n)
    result = 0
    while n > 0:
        n >>= 1
        result += 1
    return result


def binstr_flip(binstr):
    # check if binstr is a binary string
    if not set(binstr).issubset("01"):
        raise ValueError("binstr should have only '0's and '1's")
    return "".join(map(lambda c: "0" if c == "1" else "1", binstr))


def uint_to_binstr(number, size):
    return bin(number)[2:][-size:].zfill(size)


def int_to_binstr(n):
    if n == 0:
        return ""

    binstr = bin(abs(n))[2:]

    # change every 0 to 1 and vice versa when n is negative
    return binstr if n > 0 else binstr_flip(binstr)


def flatten(lst):
    return [item for sublist in lst for item in sublist]

def transform_blocks(matrix):
    height, width = matrix.shape
    num_blocks_h = height // 8
    num_blocks_w = width // 8

    blocks = []
    for i in range(num_blocks_h + 1):
        for j in range(num_blocks_w + 1):
            block = matrix[i*8:(i+1)*8, j*8:(j+1)*8]
            if block.shape != (8, 8):
                block_filled = np.zeros(shape=(8,8), dtype=np.uint8)
                for i in range(8):
                    for j in range(8):
                        try:
                            block_filled[i, j] = block[i, j]
                        except:
                            pass
                block = block_filled
            if not (np.array_equal(block, np.zeros(shape=(8,8), dtype=np.uint8))):
                blocks.append(block)

    return blocks


if __name__ == "__main__":
    matrix = np.random.randint(0, 256, size=(64, 81), dtype=np.uint8)
    blocks = transform_blocks(matrix)
    print(blocks)
