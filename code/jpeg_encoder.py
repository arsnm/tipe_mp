import fft, huffman, quantization, yuv, zigzag

def matrix_to_block(matrix, k:int=0, fill:int=0):
    """given a n * p matrix, return a list of k*k blocks(fill is the filler value =0 by default)
    
    parameters
    ----------
        -matrix : list * list
        -k: int
        -fill: Any
    
    return
    ------
        - list of k*k blocks"""
    n = len(matrix)
    try:
        p = len(matrix[0])
    except IndexError:
        print("matrix must be non-empty")
    list_blocks = []
    for r in range(0, n, k):
        for c in range(0, p, k):
            block = [[] for _ in range(k)]
            for i in range(k):
                try:
                    row = matrix[r + i][c:c + k] 
                    while len(row) != k:
                        row.append(fill)
                except:
                    row = [fill] * k
                block[i] = row
            list_blocks.append(block)
    return list_blocks

def compression(block):
    return


if __name__ == "__main__":
    l = [
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10],
        [11, 12, 13, 14, 15]
    ]
    print(matrix_to_block(l, k=2))


                    
