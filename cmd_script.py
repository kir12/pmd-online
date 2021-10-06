import requests

BASE_URL = "http://127.0.0.1:8000/compile/"

if __name__ == "__main__":
    x = requests.post(BASE_URL, data={'output':"123@#$ace.m2"}, files={'filename': open("requirements.txt", "r")})
    print(x.text)