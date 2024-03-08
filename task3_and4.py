from task1 import EC, Point, point_multiplication
from task2 import *
from bs4 import BeautifulSoup
from Crypto.Hash import HMAC, SHA256
import requests


def request_server(message: str, hmac: str, p_key: Point, recipient: str) -> str:
    url = "http://localhost:8080/submit"
    data = {
        "recipient": recipient,
        "message": message,
        "hmac": hmac,
        "pkey_x": str(p_key.x),
        "pkey_y": str(p_key.y),
    }
    response = requests.post(url, data=data)
    soup = BeautifulSoup(response.text, "html.parser")
    texts = soup.find_all("font", color="black")
    admin_message = texts[0].text.strip()
    server_hmac = texts[1].text.split(": ")[1].strip()
    return admin_message, server_hmac


def calculate_hmac(message: str, shared_key: Point) -> str:
    hmac = HMAC.new(str(shared_key).encode(), digestmod=SHA256)
    hmac.update(message.encode())
    return hmac.hexdigest()


def get_remainders(curve: EC, factors: set[int]):
    D = {}
    q = 2
    result = []
    while q < pow(2, 16):
        if q not in D:
            if curve.order % q == 0:
                result.append(q)
            D[q * q] = [q]
        else:
            for p in D[q]:
                D.setdefault(p + q, []).append(p)
            del D[q]
        q += 1
    prime_factors = result

    admin_keys = []
    for factor in prime_factors:
        if factor not in factors:

            message = "message"
            shared_key = "key"
            hmac = calculate_hmac(message, shared_key)

            public_key = generate_point_with_order(curve, factor)
            if public_key is None:
                continue
            admin_message, admin_hmac = request_server(message, hmac, public_key, "Admin")

            admin_key = -1
            for i in range(factor):
                test_shared_key = point_multiplication(public_key, i, curve)
                test_hmac = calculate_hmac(admin_message, test_shared_key)
                if admin_hmac == test_hmac:
                    admin_key = i
                    break

            if admin_key != -1:
                admin_keys.append((factor, admin_key))
    return admin_keys


if __name__ == "__main__":
    # Task 3
    # curve = EC(-95051, 11279326, 233970423115425145524320034830162017933, 29246302889428143187362802287225875743)
    # p_key = Point(16349894185180983439102154383611486412, 224942997200586455214256137069604954919)
    # order = 8
    # shared_key = "key"
    # recipient = "Admin"
    # message = "message"
    # hmac = calculate_hmac(message, shared_key)
    
    # admin_message, server_hmac = request_server(message, hmac, p_key, recipient)
    # print("server_hmac:", server_hmac)
    
    # # brute force secret key
    # secret_key = -1
    # for i in range(8):
    #     test_shared_key = point_multiplication(p_key, i, curve)
    #     hmac = calculate_hmac(admin_message, test_shared_key)
    #     print(hmac)
    #     if hmac == server_hmac:
    #         secret_key = i
    #         break
    
    # print(secret_key)


    # Task 4
    server_ec = EC(-95051, 11279326, 233970423115425145524320034830162017933, 29246302889428143187362802287225875743)
    base_point = Point(182, 85518893674295321206118380980485522083)
    ec_list = [
        EC(-95051, 118, 233970423115425145524320034830162017933,
                  233970423115425145528637034783781621127),
        EC(-95051, 727, 233970423115425145524320034830162017933,
                  233970423115425145545378039958152057148),
        EC(-95051, 210, 233970423115425145524320034830162017933,
                  233970423115425145550826547352470124412),
        EC(834, 11279326, 233970423115425145524320034830162017933,
                  233970423115425145548264999925929157572),
        EC(102, 11279326, 233970423115425145524320034830162017933,
                  233970423115425145509961303666413107064),
        EC(-95051, 79, 233970423115425145524320034830162017933,
                  233970423115425145538546862144009931013),
        EC(31, 11279326, 233970423115425145524320034830162017933,
                  233970423115425145499771890762612355342),
        EC(-95051, 504, 233970423115425145524320034830162017933,
                  233970423115425145544350131142039591210),
        EC(303, 11279326, 233970423115425145524320034830162017933,
                  233970423115425145535467383967616574919),
        EC(516, 11279326, 233970423115425145524320034830162017933,
                  233970423115425145519589093288869640865)
    ]
    message = "test message"

    factors = set()
    admin_keys = []
    for curve in ec_list:
        keys = get_remainders(curve, factors)
        for factor, admin_key_mod_factor in keys:
            admin_keys.append(
                (factor, admin_key_mod_factor))
            factors.add(factor)

    product = 1
    for factor, key in admin_keys:
        product *= factor

    admin_secret_key = 0
    for factor, admin_key_remainder in admin_keys:
        m = product // factor
        m_inv = pow(m, -1, factor)
        admin_secret_key += admin_key_remainder * m * m_inv
    admin_secret_key %= product
    print(admin_secret_key)

    admin_secret_key = admin_secret_key
    public_key = point_multiplication(base_point, admin_secret_key, server_ec)

    req = requests.get("http://localhost:8080/users")
    soup = BeautifulSoup(req.text, "html.parser")
    elements = soup.find_all("td")
    x, y = elements[3].text.strip()[1:-1].split(", ")
    bob_public_key = Point(int(x), int(y))

    shared_key = point_multiplication(bob_public_key, admin_secret_key, server_ec)
    hmac = calculate_hmac(message, shared_key)

    # send message as admin
    print(request_server(message, hmac, public_key, "Bob"))