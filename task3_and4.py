from task1 import EC, Point, point_multiplication
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


if __name__ == "__main__":
    # Task 3
    curve = EC(-95051, 11279326, 233970423115425145524320034830162017933, 29246302889428143187362802287225875743)
    p_key = Point(16349894185180983439102154383611486412, 224942997200586455214256137069604954919)
    order = 8
    shared_key = "key"
    recipient = "Admin"
    message = "message"
    hmac = calculate_hmac(message, shared_key)
    
    admin_message, server_hmac = request_server(message, hmac, p_key, recipient)
    print("server_hmac:", server_hmac)
    
    # brute force secret key
    secret_key = -1
    for i in range(8):
        test_shared_key = point_multiplication(p_key, i, curve)
        hmac = calculate_hmac(admin_message, test_shared_key)
        print(hmac)
        if hmac == server_hmac:
            secret_key = i
            break
    
    print(secret_key)