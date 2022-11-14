
class polynomial:
    def __init__(self, coefs:list) -> None:
        self.coefs = coefs
        self.len = len(coefs)
        self.deg = self.len - 1
        if self.deg > -1:
            self.max_coef = coefs[-1]

    def litteral_representation(self) -> None:
        str = ""
        for i in reversed(range(self.len)):
            if i == 0:
                str += f'{self.coefs[i]}'
            else:
                str += f'{self.coefs[i]}X^{i} + '
        print(str)

def poly_add(p:polynomial, q:polynomial) -> polynomial:
    sum = polynomial([0 for i in range(max(p.deg, q.deg))])
    for i in range(len(sum.coefs)):
            sum.coefs[i] = p.coefs[i] + q.coefs[i]
    return sum

def poly_product(p:polynomial, q:polynomial) -> polynomial:
    A = polynomial([0 for i in range(p.len + q.len - 1)])
    for i in range(p.len):
        for j in range(q.len):
            A.coefs[i+j] += p.coefs[i] * q.coefs[j]
    return A

def poly_substract(p:polynomial, q:polynomial) -> polynomial:
    return poly_add(p, poly_product(q, polynomial([-1])))

def poly_root_development(coefs:list, acc = polynomial([1])) -> polynomial:
    if len(coefs) == 1:
        return poly_product(polynomial([-coefs[0],1]),acc)
    else:
        a = coefs.pop(0)
        return poly_root_development(coefs, poly_product(polynomial([-a,1]),acc))

class reedSolomon:
    def __init__(self, coefs) -> None:
        self.coefs = coefs
    def encode(self, n:int, k:int, t:int): # method to code an information of k byte(s) to n byte(s) (having t = n-k bytes(s) of redundance)
        pass
    

def cutting(p:polynomial):
    m = (len(p.coefs)+1) // 2
    p0 = polynomial([p.coefs[i] for i in range(m)])
    p1 = polynomial([p.coefs[i] for i in range(m, m + len(p.coefs) - 1)])
    return p0,p1

def poly_expo(p:polynomial, n:int) -> polynomial:
    '''multiply a polynomial by X^n'''
    m = p.deg
    prod = polynomial([0 for i in range(n + m)])
    for i in range(m):
        prod.coefs[i + n] = p.coefs[i]
    return prod

def poly_multi(p:polynomial, q:polynomial) -> polynomial:
    n1 = p.deg
    n2 = q.deg
    m = (n1 + 1) // 2
    if n1 == 0 and n2 == 0:
        return polynomial([p.coefs[0]*q.coefs[0]])
    else:
        a, b = cutting(p)
        c, d = cutting(q)
        e = poly_multi(a,b)
        f = poly_multi(c,d)
        g = poly_multi(poly_add(a,b),poly_add(c,d))
        return poly_add(e,poly_add(poly_expo(poly_substract(poly_substract(g,f),e),m),poly_expo(f,2*m)))

p = polynomial([3,7])
q = polynomial([7,1])
print(poly_multi(p,q).litteral_representation())