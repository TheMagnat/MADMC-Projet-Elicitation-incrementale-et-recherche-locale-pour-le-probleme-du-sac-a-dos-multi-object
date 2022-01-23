
import numpy as np


size = 10000

a = np.random.randint(size)
b = np.random.randint(size)
c = np.random.randint(size)

ab = np.random.randint(a + b, a + b + size)
ac = np.random.randint(a + c, a + c + size)
bc = np.random.randint(b + c, b + c + size)

abc = np.random.randint(ab + ac + bc - (a + b + c), ab + ac + bc - (a + b + c) + size)

capa = np.array([a, b, c, ab, ac, bc, abc])

capa = np.round(capa/capa.max(), 2)

#capa[4] -= 2

print(capa[4] + capa[5], "<=", capa[6] + capa[2])
print(capa[3] + capa[5], "<=", capa[6] + capa[1])
print(capa[3] + capa[4], "<=", capa[6] + capa[0])

print(capa)

#print(capa/capa.max())