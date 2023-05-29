#Module transforming RGB images into YCbCr

yCbCr = [[0.299,0.587,0.114],
       [-0.147,-0.289,0.436],
       [0.615,-0.407,-0.079]]


def rgbToYCbCr(rgb:tuple) -> tuple:
    Y = 16 + 65.738*rgb[0]/256 + 129.057*rgb[1]/256 + 25.064*rgb[2]/256
    Cb = 128-37.945*rgb[0]/256 - 74.494*rgb[1]/256 + 112.439*rgb[2]/256
    Cr = 128+112.439*rgb[0]/256 - 94.154*rgb[1]/256 - 18.285*rgb[2]/256
    return Y, Cb, Cr


    