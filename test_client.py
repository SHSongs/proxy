import urllib.request as ul
import time


def test(url, answer):
    request = ul.Request(url)
    response = ul.urlopen(request)
    rescode = response.getcode()

    if rescode == 200:
        responsedata = response.read()
        data = responsedata.decode('utf8')[1:-1]
        if data == answer:
            return True
        else:
            return data

    return False


while True:
    print(test(f"http://127.0.0.1:9090/10000", "GAME SERVER root router"))
    s = """
    "mapName":"jsonTestMap","mapCode":"ABCDEFG","blocks":[[1,1,1],[2,2,2],[3,3,3]]
    """.strip()
    print(test(f"http://127.0.0.1:9090/10000/map", s))
    print(test(f"http://127.0.0.1:9090/8000", "AI SERVER root router"))
    print(test(f"http://127.0.0.1:9090/8000/ai", "당신은 cat 입니다"))
    time.sleep(0.5)
