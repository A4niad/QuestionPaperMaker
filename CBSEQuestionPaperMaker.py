
def fac(num):
    f = 1
    for i in range(2, num+1):
        f *= i
    return f

print(fac(1010))