from task1 import EC, Point, point_multiplication
from bs4 import BeautifulSoup
from Crypto.Hash import HMAC, SHA256
import requests


def request_server(message: str, hmac: str, key: Point, recipient: str):
    url = "http://localhost:8080/submit"
    data = {
        "recipient": recipient,
        "message": message,
        "hmac": hmac,
        "pkey_x": str(key.x),
        "pkey_y": str(key.y),
    }
    response = requests.post(url, data=data)
    soup = BeautifulSoup(response.text, "html.parser")
    texts = soup.find_all("font", color="black")
    admin_message = texts[0].text.strip()
    server_hmac = texts[1].text.split(": ")[1].strip()
    return admin_message, server_hmac


def calculate_hmac(message: str, key: Point):
    hmac = HMAC.new(str(key).encode(), digestmod=SHA256)
    hmac.update(message.encode())
    return hmac.hexdigest()


def find_secret_key(server_hmac: str, message: str, key: Point, ec: EC):
    for i in range(8):
        shared_key = point_multiplication(key, i, ec)
        hmac = calculate_hmac(message, shared_key)
        print("HMAC:", hmac)
        if hmac == server_hmac:
            return i  # random int between 1 and 7


if __name__ == "__main__":
    ec = EC(-95051, 11279326, 233970423115425145524320034830162017933)
    public_key = Point(16349894185180983439102154383611486412, 224942997200586455214256137069604954919)
    order = 8
    shared_key = "key"

    recipient = "Admin"
    message = "message"
    hmac = calculate_hmac(message, shared_key)

    admin_message, server_hmac = request_server(message, hmac, public_key, recipient)
    print("Admin message:", admin_message)
    print("Server HMAC:", server_hmac)

    secret_key = find_secret_key(server_hmac, message, public_key, ec)

    print("Secret key:", secret_key)