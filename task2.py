from task1 import EC, Point, point_multiplication
import random

def tonnelli_shanks(n: int, p: int):
    q = p - 1
    s = 0

    while q % 2 == 0:
        q = q // 2
        s += 1

    z = 2

    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1

    m = s
    c = pow(z, q, p)
    t = pow(n, q, p)
    r = pow(n, (q + 1) // 2, p)

    while t != 1:
        if t == 0:
            return 0

        i = 0
        temp = t

        while temp != 1:
            temp = pow(temp, 2, p)
            i += 1

        if i == m:
            return -1

        b = pow(c, pow(2, m - i - 1, p), p)
        m = i
        c = pow(b, 2, p)
        t = pow((t * c), 1, p)
        r = pow((r * b), 1, p)

    return r


def generate_point(ec: EC):
    x = random.randint(0, ec.field - 1)
    y_squared = pow((pow(x, 3, ec.field) + ec.a * x + ec.b), 1, ec.field)
    n = pow(y_squared, 1, ec.field)
    
    y = tonnelli_shanks(n, ec.field)
    if y == -1:
        return generate_point(ec)
    return Point(x, y)


def generate_point_with_order(ec: EC, desired: int):
    for i in range(100):
        p = generate_point(ec)
        m = point_multiplication(p, (ec.order // desired), ec)
        if m != Point(0, 0):
            return m
