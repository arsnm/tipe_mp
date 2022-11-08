# functions used for compression purposes

# packages
import numpy as np 


def zigzag(matrix):
    """function that reads the coefficients of a square matrix in zigzag
    
    parameters
    ----------
        - matrix : (array of array)-like (size must be a square)
    
    return
    ------
        - list of coefficients read in zigzag"""
    n = len(matrix)
    if n != len(matrix[0]):
        raise ValueError("given paramater must be a square matrix of at least size 1x1")
    solution = [[] for i in range(n+n-1)]
    for i in range(n):
        for j in range(n):
            sum=i+j
            if(sum%2 ==0):
                #add at beginning
                solution[sum].insert(0,matrix[i][j])
            else:
                #add at end of the list
                solution[sum].append(matrix[i][j])
        
    return [item for sublist in solution for item in sublist]

if __name__ == "__main__":
    test = [[i+j for j in range(8)] for i in range(0,64,8)]
    print(zigzag(test))


        
    
        
