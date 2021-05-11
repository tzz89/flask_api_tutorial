import requests

BASE = "http://127.0.0.1:5000/"
# response = requests.get(BASE + "helloworld/bill")
# print(response.json())

# data will go to the server as a form

data = [
    {"name": "westpoint", "views": 10, "likes": 10},
    {"name": "how to make videos", "views": 10, "likes": 10},
    {"name": "pigs can fly", "views": 10, "likes": 10}
]

for i in range(len(data)):
    response = requests.put(
        BASE+"video/"+str(i), data=data[i])

    # print(response.json())
    print("status", response)

input()

response = requests.get(
    BASE+"video/2")

print(response.json())
print("status", response)
