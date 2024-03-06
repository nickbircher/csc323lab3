def point_addition(p1, p2, A, B, field):
    # Unpack the points
    x1, y1 = p1
    x2, y2 = p2

    # Origin is infinity, represented as None
    if p1 != p2 and p1 != None and p2 != None:
        # Calculate the slope
        m = (y2 - y1) / (x2 - x1)

        # Calculate the x-coordinate of the third point
        x3 = (m**2 - x1 - x2) % field

        # Calculate the y-coordinate of the third point
        y3 = (m * (x1 - x3) - y1) % field

        # Calculate the negation of the third point
        r_neg = x3
        r_neg = (-y3) % field

        # Return the negation of the third point
        return r_neg, r_neg

    elif p1 == p2:
        # Calculate the slope of the tangent line
        m = (3 * x1**2 + A) / (2 * y1)

        # Calculate the x-coordinate of the intersection point
        x3 = (m**2 - 2 * x1) % field

        # Calculate the y-coordinate of the intersection point
        y3 = (m * (x1 - x3) - y1) % field

        # Calculate the negation of the intersection point
        x_neg = x3
        y_neg = (-y3) % field

        # Return the negation of the intersection point
        return x_neg, y_neg

    return None

def point_multiplication(p, scalar, A, B, field):
    # Initialize the result as the origin
    result = None

    i = scalar
    # Add the point to itself scalar times
    while i > 0:
        if i % 2 == 1:
            result = point_addition(result, p, A, B, field)
        point_addition(p, p, A, B, field)
        if i > 1:
            i = i // 2
        else:
            i -= 1

    return result

# Define the curve parameters and field
A = 3
B = 8
field = 13

# Define the test cases
test_cases = [
    ((9, 7), (1, 8), (2, 10)),
    ((9, 7), (9, 7), (9, 6)),
    ((12, 11), (12, 2), None)
]

# Test the point_addition function
for p1, p2, expected in test_cases:
    result = point_addition(p1, p2, A, B, field)
    assert result == expected, f"For {p1} + {p2}, expected {expected} but got {result}"

print("All point addition tests passed.")

# Test the point_multiplication function
# We only have one test case for this function
p = (9, 7)
scalar = 2
expected = (9, 6)
result = point_multiplication(p, scalar, A, B, field)
assert result == expected, f"For {scalar} * {p}, expected {expected} but got {result}"

print("All point multiplication tests passed.")