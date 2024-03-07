class Point:
    x: int
    y: int


    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    

class EC:
     def __init__(self, a, b, field, order):
        self.a = a
        self.b = b
        self.field = field
        self.order = order


def point_addition(p: Point, q: Point, ec: EC):
    if p == Point(0, 0):
        return q
    
    elif q == Point(0, 0):
        return p
    
    elif p.x == q.x and pow(p.y + q.y, 1, ec.field) == 0:
        return Point(0, 0)
    
    elif p != q:
        # m is slope
        m = (q.y - p.y) * pow(q.x - p.x, -1, ec.field)

    else:
        m = (3 * pow(p.x, 2, ec.field) + ec.a) * pow(2 * p.y, -1, ec.field)

    m = pow(m, 1, ec.field)
    x = pow((pow(m, 2, ec.field) - p.x - q.x), 1, ec.field)
    y = pow((m * (p.x - x) - p.y), 1, ec.field)
    return Point(x, y)


def point_multiplication(p: Point, n: int, ec: EC):
    r = Point(0, 0)

    while n > 0:
        if pow(n, 1, 2) == 1:
            r = point_addition(r, p, ec)

        p = point_addition(p, p, ec)
        n = n // 2
    return r


# Define the curve parameters and field
A = 3
B = 8
field = 13
test_ec = EC(A, B, field, 9)

# Define the test cases
test_cases = [
    (Point(9, 7), Point(1, 8), Point(2, 10)),
    (Point(9, 7), Point(9, 7), Point(9, 6)),
    (Point(12, 11), Point(12, 2), Point(0, 0))
]

# Test the point_addition function
for p1, p2, expected in test_cases:
    result = point_addition(p1, p2, test_ec)
    assert result == expected, f"For {p1} + {p2}, expected {expected} but got {result}"

print("All point addition tests passed.")

# Test the point_multiplication function
# We only have one test case for this function
p = Point(9, 7)
scalar = 2
expected = Point(9, 6)
result = point_multiplication(p, scalar, test_ec)
assert result == expected, f"For {scalar} * {p}, expected {expected} but got {result}"

print("All point multiplication tests passed.")