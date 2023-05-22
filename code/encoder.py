import numpy as np
from zigzag import zigzag
from quantization import quantize

m =np.array([[i*10 for i in range(1,9)] for _ in range(8)])

m2 = [[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]]

import numpy as np

def blocs(matrice):
    """découpe en blocs de taille 8x8 une matrice"""
    n = len(matrice)
    p = len(matrice[0])
    # n et p doivent être des multiples de 8
    q1 = n // 8
    q2 = p // 8
    L=[]
    for i in range(q2):
        for j in range(q1):
            M = [[0]*8 for _ in range(8)]
            for k in range(8):
                for l in range(8):
                    M[k][l] = matrice[8*i + k][8*j + l]
            L.append(M)
    return L

def moyenne0(matrice):
    for i in range(len(m)):
        for j in range(len(m[0])):
            matrice[i][j] -= 128
    return matrice

def DCT_bidon(L):
    return(L)

def DCT_ligne(lm):
    """"prend une liste de matrice et applique DCT à chacune des lignes de chacune d'entre elles"""
    for i in range(len(lm)):
        for j in range(len(lm[0])):
            lm[i][j] = DCT_bidon(lm[i][j])
    return(lm)

def transpo(matrice):
    return np.transpose(matrice)

def DCT_colonne(lm):
    "applique DCT sur les colonnes d'une liste de matrices en utilisant la transposée et DCT_ligne"
    lm_T = []
    L = []
    for m in lm:
        lm_T.append(transpo(m))
    
    lm_T = DCT_ligne(lm_T)

    for m in lm_T:
        L.append(transpo(m))

    return L



def quantization_liste_matrice(lm):
    L = []
    for m in lm:
        L.append(quantize(m))
    return L


def zigzag_liste_matrice(lm):
    Z = []
    for m in lm:
        Z.append(zigzag(m))
    return Z



def encoder(image):
    lm = blocs(image)
    lm = DCT_ligne(lm)
    lm = DCT_colonne(lm)
    lm = quantization_liste_matrice(lm)
    return(zigzag_liste_matrice(lm))



    
print(encoder(m))