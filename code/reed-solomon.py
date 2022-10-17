class polynomial:
    def __init__(self, coefs:list) -> None:
        self.coefs = coefs
        self.len = len(coefs)
        self.deg = self.len - 1
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

def poly_root_development(coefs:list, acc = polynomial([1])) -> polynomial:
    if len(coefs) == 1:
        return poly_product(polynomial([-coefs[0],1]),acc)
    else:
        a = coefs.pop(0)
        return poly_root_development(coefs, poly_product(polynomial([-a,1]),acc))

class reedSolomon:
    def __init__(self, coefs) -> None:
        self.coefs = coefs
    def encode(self, n:int, k:int, t:int) -> list: # method to code an information of k byte(s) to n byte(s) (having t = n-k bytes(s) of redundance)
        pass
    

def cutting(p:polynomial):
    m = (len(p.coefs)+1) // 2
    p0 = polynomial([p.coefs[i] for i in range(m)])
    p1 = polynomial([p.coefs[i] for i in range(m, m + len(p.coefs) - 1)])
    return p0,p1

def poly_expo(n:int, p:polynomial) -> polynomial:
    '''multiply a polynomial by X^n'''
    m = p.deg
    prod = [0 for i in range(n + m)]
    for i in range(m):
        prod[i + n] <- p.coefs[i]
    return prod

def poly_multi(p:polynomial, q:polynomial) -> polynomial:
    n = p.deg
    m = (n + 1) // 2
    if n == 1:
        return polynomial([p.coefs[0]*q.coefs[0]])
    else:
        p0, p1, q0, q1 = cutting(p), cutting(p)
        p0q0,p1q1 = poly_multi(p0,q0), poly_multi(p1,q1)
        mb1  =  poly_expo((2*m), p1q1)
        mb2 = poly_expo(m, (poly_substract(poly_multi((poly_add(p0,p1)),(poly_add(q0, q1))), (poly_add(p0q0, p1q1)))))
        return poly_add(mb1, (poly_add(mb2, p0q0)))


p = polynomial([3])
q = polynomial([7])
print(poly_multi(p,q))