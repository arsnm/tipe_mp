# fast-fourier transforms

#packages
import complex as cpx
from numpy import log2, pi
from scipy.fft import fft, ifft


#functions
def FFT(poly:list) -> list:
    """caclulate the fast fourier tranform of a polynomial
    
    parameters
    ----------
        -polynomial : list of Complex object
    
    return
    ------
        - 1-D fast fourier transform of the polynomial"""
    n = len(poly) 
    assert log2(n).is_integer(), "make sure that the length of the arguement is a power of 2"
    if n == 1:
        return poly
    poly_even, poly_odd = poly[::2] , poly[1::2]
    res_even, res_odd = FFT(poly_even), FFT(poly_odd)
    res = [cpx.Complex(0)] * n 
    for j in range(n//2):
        w_j = cpx.exp_to_literal(-2*pi*j/n)
        product = w_j * res_odd[j]
        res[j] = res_even[j] + product
        res[j + n//2] = res_even[j] - product
    return res

def IFFT_aux(poly:list) -> list:
    """caclulate the inverse of the fast fourier tranform of a polynomial (in order to have ifft(fft(poly)) == poly)
    
    parameters
    ----------
        -polynomial : list of Complex object
    
    return
    ------
        - inverse of the 1-D fast fourier transform of the polynomial"""
    n = len(poly) 
    assert log2(n).is_integer(), "make sure that the length of the arguement is a power of 2"
    if n == 1:
        return poly
    poly_even, poly_odd = poly[::2] , poly[1::2]
    res_even, res_odd = IFFT_aux(poly_even), IFFT_aux(poly_odd)
    res = [cpx.Complex(0)] * n 
    for j in range(n//2):
        w_j = cpx.exp_to_literal((2 * pi * j) / n)
        product = w_j * res_odd[j]
        res[j] = res_even[j] + product
        res[j + n//2] = res_even[j] - product
    return res

def IFFT(poly:list) -> list:
    n = len(poly)

    res = IFFT_aux(poly)
    for i in range(n):
        res[i] = res[i] / cpx.Complex(n)
    return res


if __name__ == "__main__":
    test = (FFT([cpx.Complex(5.3), cpx.Complex(3.2), cpx.Complex(2.1), cpx.Complex(1)]))
    res_test = IFFT(test)
    print(test)
    print(res_test)

    # Comparaison with values given by scipy
    # try:
    #     from scipy.fft import fft, ifft
    # except ImportError:
    #     raise ImportError
    # np_test = fft([5.3, 3.2, 2.1, 1])
    # print(np_test)
    # np_res_test = ifft(np_test)
    # print(np_res_test)