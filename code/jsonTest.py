import json

class JsonObject:
    def __init__(self, d):
        self.__dict__ = d


if __name__ == '__main__':
    test1 = JsonObject(age=10)
    print(test1)

    s = '{"name": "ACME", "shares": 50, "price": 490.1}'
    json1 = json.loads(s, object_hook=JsonObject)
    print(json1)