#Module transforming RGB images into YUV
import numpy as np
import numpy.linalg as alg

yuv = np.array([[0.299,0.587,0.114],
                [-0.147,-0.289,0.436],
                [0.615,-0.407,-0.079]])


def rgb_to_yuv(rgb:tuple) -> tuple:
       a = np.asarray(rgb)
       b = yuv.dot(a)
       return tuple(b)

def yuv_to_rgb(c:tuple) -> tuple:
       a = np.asarray(c)
       b = alg.inv(yuv)
       d = b.dot(a)
       return tuple(d)