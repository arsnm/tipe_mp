#Module transforming RGB images into YUV

yuv = [[0.299,0.587,0.114],
       [-0.147,-0.289,0.436],
       [0.615,-0.407,-0.079]]


def rgb_to_yuv(rgb:tuple) -> tuple:
    r = rgb[0]
    g = rgb[1]
    b = rgb[2]
    y = yuv[0][0] * r + yuv[0][1] * g + yuv[0][2] * b
    u = yuv[1][0] * r + yuv[1][1] * g + yuv[1][2] * b
    v = yuv[2][0] * r + yuv[2][1] * g + yuv[2][2] * b
    return (y,u,v)

def rgb_to_yuv_block(block:list[list[tuple]]) -> list[list[tuple]]:
    return [[rgb_to_yuv(pixel) for pixel in row] for row in block]

    