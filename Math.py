from math import exp

class Activation():
    """implements different activations
    """

    @staticmethod
    def sigmoid(x):
        """sigmoid activation
        """

        return (exp(x)/float(1+exp(x)))

class Matrix():
    """implements matrix ops
    """

    def __init__(self,array):
        """converts multi-dim array
           to matrix obj
        """

        self.array = array

    def sigmoid(self):
        """applies sigmoid function
           to all elements
        """

        n = len(self.array)
        m = len(self.array[0])

        res = [[0 for j in range(m)] for i in range(n)]

        for i in range(n):
            for j in range(m):
                res[i][j] = Activation.sigmoid(self.array[i][j])

        return Matrix(res)


    def __repr__(self):
        """call to print or
           output
        """

        return (str(self.array))

    def __eq__(self,other):

        if self.array == other.array:
            return True
        
        return False

    def __pow__(self,p):
        """power function
        """
        
        x = self
        for i in range(p-1):
            x = x * self

        return x

    def __matmul__(self,other):
        """point wise product
        """

        n1,n2 = len(self.array),len(other.array)
        m1,m2 = len(self.array[0]),len(other.array[0])

        if n1 != n2 or m1 != m2:
            print ('Invalid op')
            exit()

        res = [[0 for j in range(m1)] for i in range(n1)]
        for i in range(n1):
            for j in range(m1):
                res[i][j] = self.array[i][j] * other.array[i][j]

        return Matrix(res)

    def relu(self):
        """performs relu operator
           max(0,x)
        """

        n,m = self.dim()[0],self.dim()[1]

        res = [[0 for j in range(m)] for i in range(n)]

        for i in range(n):
            for j in range(m):
                if res[i][j] > 0:
                    res[i][j] = self.array[i][j]

        return Matrix(res)

    def grad(self,a = 'sigmoid'):
        """computes gradient to every element
        """

        n = len(self.array)
        m = len(self.array[0])
        I = Matrix([[1 for j in range(m)] for i in range(n)])
        
        if a == 'sigmoid':
            return self.sigmoid() @ (I - self.sigmoid())

        elif a == 'lin': #linear activation
            return I

        elif a == 'relu': #rectified linear unit
            grad = [[0 for j in range(m)] for i in range(n)]
            for i in range(n):
                for j in range(m):
                    if self.array[i][j] > 0:
                        grad[i][j] = 1
            return Matrix(grad)

    def __sub__(self,other):
        """adds self with other
        """

        n1,n2 = len(self.array),len(other.array)
        m1,m2 = len(self.array[0]),len(other.array[0])

        if n1 != n2 or m1 != m2:
            print ('Invalid op')
            exit()

        res = [[0 for j in range(m1)] for i in range(n1)]
        for i in range(n1):
            for j in range(m1):
                res[i][j] = self.array[i][j] - other.array[i][j]

        return Matrix(res)
    

    def __add__(self,other):
        """adds self with other
        """

        n1,n2 = len(self.array),len(other.array)
        m1,m2 = len(self.array[0]),len(other.array[0])

        if n1 != n2 or m1 != m2:
            print ('Invalid op')
            exit()

        res = [[0 for j in range(m1)] for i in range(n1)]
        for i in range(n1):
            for j in range(m1):
                res[i][j] = self.array[i][j] + other.array[i][j]

        return Matrix(res)

    def T(self):
        """Transpose of matrix
        """

        n = len(self.array)
        m = len(self.array[0])

        res = [[0 for j in range(n)] for i in range(m)]

        for i in range(m):
            for j in range(n):
                res[i][j] = self.array[j][i]

        return Matrix(res)

    def dim(self):
        """returns rows and cols
        """

        return ((len(self.array),len(self.array[0])))

    def col(self,j):
        """returns jth column
        """

        n = len(self.array)
        return ([self.array[i][j] for i in range(n)])

    def __mul__(self,other):
        """multiplies self with other
        """
        n1,n2 = len(self.array),len(other.array)
        m1,m2 = len(self.array[0]),len(other.array[0])

        if m1 != n2:
            print (m1,n2)
            print ('Invalid op')
            exit()

        res = [[0 for j in range(m2)] for i in range(n1)]

        for i in range(n1):
            row_i = self.array[i]
            for j in range(m2):
                col_j = other.col(j)
                res[i][j] = sum([row_i[k]*col_j[k] for k in range(n2)])

        return Matrix(res)

#============= TEST CODE ================
'''
m1 = Matrix([[1,2],[3,4]])
m2 = Matrix([[1,2],[3,4]])
print (m1 + m2)
print (m1 * m2)
print (m1 == m2)
'''

                

        
        
