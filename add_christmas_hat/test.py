import base64
import urllib.request
import json

with open("test.png", 'rb') as f:
    image = f.read()
    image_base64 = str(base64.b64encode(image), encoding='utf-8')

url = "https://service-ly70xmyz-1256773370.sh.apigw.tencentcs.com/test/addChristmasHat"
data = {
    "pic": image_base64
}
print(urllib.request.urlopen(urllib.request.Request(url=url, data=json.dumps(data).encode("utf-8"))).read().decode("utf-8"))