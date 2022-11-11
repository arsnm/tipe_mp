import heapq as hp

def table_frequences(L):
    table = {}
    for a in L:
        if a in table:
            table[a] += 1
        else:
            table[a] = 1
    return table


def arbre_huffman(dict):
    tas = [(a, b) for (b, a) in dict.items()]
    hp.heapify(tas)
    while len(tas) >= 2:
        occ1, noeud1 = hp.heappop(tas) # noeud le moins fréquent
        occ2, noeud2 = hp.heappop(tas) # 2e noeud le moins fréquent
        hp.heappush(tas, (occ1 + occ2, {0: noeud1, 1: noeud2}))
    return hp.heappop(tas)[1]


def code_huffman_parcours(arbre, prefixe, code):
    for noeud in arbre:
        if len(arbre[noeud]) == 1:
            code[prefixe+noeud] = arbre[noeud]
        else:
            code_huffman_parcours(arbre[noeud],prefixe+noeud,code)
            
def code_huffman(arbre):
    code = {}
    code_huffman_parcours(arbre, '', code)
    return code


def encodage(L,code):
    code_inv = dict((code[bits], bits) for bits in code)
    texte_binaire = ''
    for c in L:
        texte_binaire = texte_binaire + code_inv[c]
    return texte_binaire


def decodage(code,texte_binaire):
    L = []
    suite_bin = ''
    for a in texte_binaire:
        suite_bin = suite_bin + a
        if suite_bin in code:
            L = L + code[suite_bin]
            suite_bin = ''
    return L