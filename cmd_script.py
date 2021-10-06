import requests

BASE_URL = "http://127.0.0.1:8000/compile/"

if __name__ == "__main__":
    x = requests.post(BASE_URL, data={}, files={'filename': open("../pc98-stuffs/PMD/songs/divine.mml", "r")})
    print(x.text)