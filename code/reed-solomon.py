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
        print(str+"sofiane")

# def poly_add(p:polynomial, q:polynomial) -> polynomial:
#     sum = polynomial([0 for i in range(max(p.deg, q.deg))])
#     for i in range(len(sum.coefs)):
#             sum.coefs[i] = p.coefs[i] + q.coefs[i]
#     return sum

def poly_product(p:polynomial, q:polynomial):
    A = [0 for i in range(p.len + q.len - 1)]
    for i in range(p.len):
        for j in range(q.len):
            A[i+j] += p.coefs[i] * q.coefs[j]
    return polynomial(A)

def poly_root_development(coefs:list, acc = polynomial([1])) -> polynomial:
    if len(coefs) == 1:
        return poly_product(polynomial([-coefs[0],1]),acc)
    else:
        a = coefs.pop(0)
        return poly_root_development(coefs, poly_product(polynomial([-a,1]),acc))

class reedSolomon:
    def __init__(self, coefs) -> None:
        self.coefs = coefs
    def encode(self, n:int, k:int, t:int) -> list: # method to code a information of k byte(s) to n byte(s) (having t = n-k bytes(s) of redundance)
        pass

'''let rec poly_multi p q =
let puiss n p = 
let m = Array.length p in
let prod = Array.make (n+m) 0 in
for i=0 to m-1 do
    prod.(i+n) <- p.(i)
done;
prod in
let n = Array.length p in
let m = (n+1)/2 in
match n with
|1 -> let prod = p.(0)*q.(0) in [|prod|]
|_-> let p0,p1 = decoupe p and q0,q1 = decoupe q in 
let p0q0,p1q1 = poly_multi p0 q0, poly_multi p1 q1 in 
let mb1  = puiss (2*m) p1q1 in 
let mb2 = puiss m (difference (poly_multi (somme p0 p1) (somme q0 q1)) (somme p0q0 p1q1)) in
somme mb1 (somme mb2 p0q0);;'''

'''
let decoupe p =
let n = Array.length p in
let m = (n+1)/2 in
let p0 = Array.init m (fun i -> p.(i)) in
let p1 = Array.init (n-m) (fun i -> p.(m+i)) in
(p0,p1);;'''

def cutting(p:polynomial):
    m = int((len(p.coefs)+1) / 2)
    p0 = polynomial([p.coefs[i] for i in range(m)])
    p1 = polynomial([p.coefs[i] for i in range(m, m+len(p.coefs))])
    return p0,p1

def poly_expo(n:int, p:polynomial) -> polynomial:
        m = p.deg()
        prod = [0 for i in range(n+m)]
        for i in range(m):
            prod[i+n] <- p.coefs[i]
        return prod

def poly_multi(p:polynomial, q:polynomial) -> polynomial:
    n = p.deg
    m = int((n+1)/2)
    if n == 1:
        return polynomial([p.coefs[0]*q.coefs[0]])
    else:
        p0, p1, q0, q1 = cutting(p), cutting(p)
        p0q0,p1q1 = poly_multi(p0,q0), poly_multi(p1,q1)
        mb1  =  poly_expo((2*m), p1q1)
        mb2 = poly_expo(m, (poly_substract(poly_multi((poly_add(p0,p1)),(poly_add(q0, q1))), (poly_add(p0q0, p1q1))))) in
        return poly_add(mb1, (poly_add(mb2, p0q0)))

