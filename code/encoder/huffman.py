import numpy as np

MAX_CLEN = 32 # assumed maximum initial code length

def getFreq(data):
    freq = [0] * 257
    for elem in data:
        freq[elem] += 1
    freq[256] = 1
    return freq

def jpegGenerateOptimalTable(freq):
    bits = [0] * (MAX_CLEN + 1)
    bitPos = [0] * (MAX_CLEN + 1)
    codesize = [0] * 257
    nzIndex = [0] * 257

    others = [-1] * 257

    numNzSymbols = 0
    for i in range(257):
        if freq[i]:
            nzIndex[numNzSymbols] = i
            freq[numNzSymbols] = freq[i]
            numNzSymbols += 1

    huffval = [0] * (numNzSymbols - 1)

    while True:
        c1 = -1
        c2 = -1
        v = 1000000000
        v2 = 1000000000
        for i in range(numNzSymbols):
            if freq[i] <= v2:
                if freq[i] <= v:
                    c2 = c1
                    v2 = v
                    v = freq[i]
                    c1 = i
                else:
                    v2 = freq[i]
                    c2 = i
        
        if (c2 < 0):
            break
        
        freq[c1] += freq[c2]
        freq[c2] = 1000000001

        codesize[c1] += 1
        while others[c1] >= 0:
            c1 = others[c1]
            codesize[c1] += 1

        others[c1] = c2

        codesize[c2] += 1
        while others[c2] >= 0:
            c2 = others[c2]
            codesize[c2] += 1
        
    for i in range(numNzSymbols):
        bits[codesize[i]] += 1

    p = 0
    for i in range(1, MAX_CLEN + 1):
        bitPos[i] = p
        p += bits[i] 

    for i in range(MAX_CLEN, 16, -1):
        while bits[i] > 0:
            j = i - 2
            while bits[j] == 0:
                j -= 1
            bits[i] -= 2
            bits[i - 1] += 1
            bits[j + 1] += 2
            bits[j] -= 1
    
    i = MAX_CLEN
    while bits[i] == 0:
        i -= 1
    bits[i] -= 1

    for i in range(numNzSymbols - 1):
        huffval[bitPos[codesize[i]]] = nzIndex[i]
        bitPos[codesize[i]] += 1

    return bits, huffval

def jpegGenerateHuffmanTable(bits, huffval):
    huffsize = [0] * 257
    huffcode = [0] * 257

    p = 0
    for l in range(1, 17):
        i = bits[l]
        while i:
            huffsize[p] = l
            p += 1
            i -= 1
    
    huffsize[p] = 0
    lastp = p

    code = 0
    si = huffsize[0]
    p = 0
    while huffsize[p]:
        while huffsize[p] == si:
            huffcode[p] = code
            code += 1
            p += 1
        code <<= 1
        si += 1

    ehufco = [0] * 257
    ehufsi = [0] * 257 

    for p in range(lastp):
        i = huffval[p]
        ehufco[i] = huffcode[p]
        ehufsi[i] = huffsize[p]

    return ehufsi, ehufco

def jpegTransformTable(ehufsi, ehufco):
    table = {}
    for i in range(len(ehufco)):
        if ehufsi[i] != 0:
            endCode = bin(ehufco[i])[2:]
            nbZeros = ehufsi[i] - len(endCode)
            table[i] = '0' * nbZeros + endCode
    return table

def jpegCreateHuffmanTable(arr):
    freq = getFreq(arr)
    bits, huffval = jpegGenerateOptimalTable(freq)
    ehufsi, ehufco = jpegGenerateHuffmanTable(bits, huffval)
    table = jpegTransformTable(ehufsi, ehufco)
    return table

def convert_huffman_table(table):
    """convert huffman table to count and weigh"""
    # table[int] = string
    pairs = sorted(table.items(), key=lambda x: (len(x[1]), x[1]))
    weigh, codes = zip(*pairs)
    weigh = np.array(weigh, dtype=np.uint8)
    # count[i]: there are count[i] codes of length i+1
    count = np.zeros(16, dtype=np.uint8)
    for c in codes:
        count[len(c)-1] += 1
    return count, weigh


def read_huffman_code(table, stream):
    prefix = ''
    while prefix not in table:
        prefix += str(stream.read_bit())
    return table[prefix]


def reverse(table):
    return {v: k for k, v in table.items()}

# 4 recommended huffman tables in JPEG standard
# luminance DC
RM_Y_DC = {'00': 0, '010': 1, '011': 2, '100': 3, '101': 4, '110': 5,
           '1110': 6, '11110': 7, '111110': 8, '1111110': 9, '11111110': 10,
           '111111110': 11}

# luminance AC
RM_Y_AC = {'00': 1, '01': 2, '100': 3, '1010': 0, '1011': 4, '1100': 17,
           '11010': 5, '11011': 18, '11100': 33, '111010': 49, '111011': 65,
           '1111000': 6, '1111001': 19, '1111010': 81, '1111011': 97,
           '11111000': 7, '11111001': 34, '11111010': 113, '111110110': 20,
           '111110111': 50, '111111000': 129, '111111001': 145,
           '111111010': 161, '1111110110': 8, '1111110111': 35,
           '1111111000': 66, '1111111001': 177, '1111111010': 193,
           '11111110110': 21, '11111110111': 82, '11111111000': 209,
           '11111111001': 240, '111111110100': 36, '111111110101': 51,
           '111111110110': 98, '111111110111': 114, '111111111000000': 130,
           '1111111110000010': 9, '1111111110000011': 10,
           '1111111110000100': 22, '1111111110000101': 23,
           '1111111110000110': 24, '1111111110000111': 25,
           '1111111110001000': 26, '1111111110001001': 37,
           '1111111110001010': 38, '1111111110001011': 39,
           '1111111110001100': 40, '1111111110001101': 41,
           '1111111110001110': 42, '1111111110001111': 52,
           '1111111110010000': 53, '1111111110010001': 54,
           '1111111110010010': 55, '1111111110010011': 56,
           '1111111110010100': 57, '1111111110010101': 58,
           '1111111110010110': 67, '1111111110010111': 68,
           '1111111110011000': 69, '1111111110011001': 70,
           '1111111110011010': 71, '1111111110011011': 72,
           '1111111110011100': 73, '1111111110011101': 74,
           '1111111110011110': 83, '1111111110011111': 84,
           '1111111110100000': 85, '1111111110100001': 86,
           '1111111110100010': 87, '1111111110100011': 88,
           '1111111110100100': 89, '1111111110100101': 90,
           '1111111110100110': 99, '1111111110100111': 100,
           '1111111110101000': 101, '1111111110101001': 102,
           '1111111110101010': 103, '1111111110101011': 104,
           '1111111110101100': 105, '1111111110101101': 106,
           '1111111110101110': 115, '1111111110101111': 116,
           '1111111110110000': 117, '1111111110110001': 118,
           '1111111110110010': 119, '1111111110110011': 120,
           '1111111110110100': 121, '1111111110110101': 122,
           '1111111110110110': 131, '1111111110110111': 132,
           '1111111110111000': 133, '1111111110111001': 134,
           '1111111110111010': 135, '1111111110111011': 136,
           '1111111110111100': 137, '1111111110111101': 138,
           '1111111110111110': 146, '1111111110111111': 147,
           '1111111111000000': 148, '1111111111000001': 149,
           '1111111111000010': 150, '1111111111000011': 151,
           '1111111111000100': 152, '1111111111000101': 153,
           '1111111111000110': 154, '1111111111000111': 162,
           '1111111111001000': 163, '1111111111001001': 164,
           '1111111111001010': 165, '1111111111001011': 166,
           '1111111111001100': 167, '1111111111001101': 168,
           '1111111111001110': 169, '1111111111001111': 170,
           '1111111111010000': 178, '1111111111010001': 179,
           '1111111111010010': 180, '1111111111010011': 181,
           '1111111111010100': 182, '1111111111010101': 183,
           '1111111111010110': 184, '1111111111010111': 185,
           '1111111111011000': 186, '1111111111011001': 194,
           '1111111111011010': 195, '1111111111011011': 196,
           '1111111111011100': 197, '1111111111011101': 198,
           '1111111111011110': 199, '1111111111011111': 200,
           '1111111111100000': 201, '1111111111100001': 202,
           '1111111111100010': 210, '1111111111100011': 211,
           '1111111111100100': 212, '1111111111100101': 213,
           '1111111111100110': 214, '1111111111100111': 215,
           '1111111111101000': 216, '1111111111101001': 217,
           '1111111111101010': 218, '1111111111101011': 225,
           '1111111111101100': 226, '1111111111101101': 227,
           '1111111111101110': 228, '1111111111101111': 229,
           '1111111111110000': 230, '1111111111110001': 231,
           '1111111111110010': 232, '1111111111110011': 233,
           '1111111111110100': 234, '1111111111110101': 241,
           '1111111111110110': 242, '1111111111110111': 243,
           '1111111111111000': 244, '1111111111111001': 245,
           '1111111111111010': 246, '1111111111111011': 247,
           '1111111111111100': 248, '1111111111111101': 249,
           '1111111111111110': 250}

# chroma DC
RM_C_DC = {'00': 0, '01': 1, '10': 2, '110': 3, '1110': 4, '11110': 5,
           '111110': 6, '1111110': 7, '11111110': 8, '111111110': 9,
           '1111111110': 10, '11111111110': 11}

# chroma AC
RM_C_AC = {'00': 0, '01': 1, '100': 2, '1010': 3, '1011': 17, '11000': 4,
           '11001': 5, '11010': 33, '11011': 49, '111000': 6, '111001': 18,
           '111010': 65, '111011': 81, '1111000': 7, '1111001': 97,
           '1111010': 113, '11110110': 19, '11110111': 34, '11111000': 50,
           '11111001': 129, '111110100': 8, '111110101': 20, '111110110': 66,
           '111110111': 145, '111111000': 161, '111111001': 177,
           '111111010': 193, '1111110110': 9, '1111110111': 35,
           '1111111000': 51, '1111111001': 82, '1111111010': 240,
           '11111110110': 21, '11111110111': 98, '11111111000': 114,
           '11111111001': 209, '111111110100': 10, '111111110101': 22,
           '111111110110': 36, '111111110111': 52, '11111111100000': 225,
           '111111111000010': 37, '111111111000011': 241,
           '1111111110001000': 23, '1111111110001001': 24,
           '1111111110001010': 25, '1111111110001011': 26,
           '1111111110001100': 38, '1111111110001101': 39,
           '1111111110001110': 40, '1111111110001111': 41,
           '1111111110010000': 42, '1111111110010001': 53,
           '1111111110010010': 54, '1111111110010011': 55,
           '1111111110010100': 56, '1111111110010101': 57,
           '1111111110010110': 58, '1111111110010111': 67,
           '1111111110011000': 68, '1111111110011001': 69,
           '1111111110011010': 70, '1111111110011011': 71,
           '1111111110011100': 72, '1111111110011101': 73,
           '1111111110011110': 74, '1111111110011111': 83,
           '1111111110100000': 84, '1111111110100001': 85,
           '1111111110100010': 86, '1111111110100011': 87,
           '1111111110100100': 88, '1111111110100101': 89,
           '1111111110100110': 90, '1111111110100111': 99,
           '1111111110101000': 100, '1111111110101001': 101,
           '1111111110101010': 102, '1111111110101011': 103,
           '1111111110101100': 104, '1111111110101101': 105,
           '1111111110101110': 106, '1111111110101111': 115,
           '1111111110110000': 116, '1111111110110001': 117,
           '1111111110110010': 118, '1111111110110011': 119,
           '1111111110110100': 120, '1111111110110101': 121,
           '1111111110110110': 122, '1111111110110111': 130,
           '1111111110111000': 131, '1111111110111001': 132,
           '1111111110111010': 133, '1111111110111011': 134,
           '1111111110111100': 135, '1111111110111101': 136,
           '1111111110111110': 137, '1111111110111111': 138,
           '1111111111000000': 146, '1111111111000001': 147,
           '1111111111000010': 148, '1111111111000011': 149,
           '1111111111000100': 150, '1111111111000101': 151,
           '1111111111000110': 152, '1111111111000111': 153,
           '1111111111001000': 154, '1111111111001001': 162,
           '1111111111001010': 163, '1111111111001011': 164,
           '1111111111001100': 165, '1111111111001101': 166,
           '1111111111001110': 167, '1111111111001111': 168,
           '1111111111010000': 169, '1111111111010001': 170,
           '1111111111010010': 178, '1111111111010011': 179,
           '1111111111010100': 180, '1111111111010101': 181,
           '1111111111010110': 182, '1111111111010111': 183,
           '1111111111011000': 184, '1111111111011001': 185,
           '1111111111011010': 186, '1111111111011011': 194,
           '1111111111011100': 195, '1111111111011101': 196,
           '1111111111011110': 197, '1111111111011111': 198,
           '1111111111100000': 199, '1111111111100001': 200,
           '1111111111100010': 201, '1111111111100011': 202,
           '1111111111100100': 210, '1111111111100101': 211,
           '1111111111100110': 212, '1111111111100111': 213,
           '1111111111101000': 214, '1111111111101001': 215,
           '1111111111101010': 216, '1111111111101011': 217,
           '1111111111101100': 218, '1111111111101101': 226,
           '1111111111101110': 227, '1111111111101111': 228,
           '1111111111110000': 229, '1111111111110001': 230,
           '1111111111110010': 231, '1111111111110011': 232,
           '1111111111110100': 233, '1111111111110101': 234,
           '1111111111110110': 242, '1111111111110111': 243,
           '1111111111111000': 244, '1111111111111001': 245,
           '1111111111111010': 246, '1111111111111011': 247,
           '1111111111111100': 248, '1111111111111101': 249,
           '1111111111111110': 250}

if __name__ == "__main__":
    arr = np.array([np.random.randint(-127, 128) for _ in range(64)])
    table = jpegCreateHuffmanTable(arr)
    print(table)