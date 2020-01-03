import base64, json
from PIL import Image
import uuid


def return_msg(error, msg):
    return_data = {
        "uuid": str(uuid.uuid1()),
        "error": error,
        "message": msg
    }
    print(return_data)
    return return_data


def do_circle(base_pic):
    icon_pic = Image.open(base_pic).convert("RGBA")
    icon_pic = icon_pic.resize((500, 500), Image.ANTIALIAS)
    icon_pic_x, icon_pic_y = icon_pic.size
    temp_icon_pic = Image.new('RGBA', (icon_pic_x + 600, icon_pic_y + 600), (255, 255, 255))
    temp_icon_pic.paste(icon_pic, (300, 300), icon_pic)
    ima = temp_icon_pic.resize((200, 200), Image.ANTIALIAS)
    size = ima.size

    # 因为是要圆形，所以需要正方形的图片
    r2 = min(size[0], size[1])
    if size[0] != size[1]:
        ima = ima.resize((r2, r2), Image.ANTIALIAS)

    # 最后生成圆的半径
    r3 = 60
    imb = Image.new('RGBA', (r3 * 2, r3 * 2), (255, 255, 255, 0))
    pima = ima.load()  # 像素的访问对象
    pimb = imb.load()
    r = float(r2 / 2)  # 圆心横坐标

    for i in range(r2):
        for j in range(r2):
            lx = abs(i - r)  # 到圆心距离的横坐标
            ly = abs(j - r)  # 到圆心距离的纵坐标
            l = (pow(lx, 2) + pow(ly, 2)) ** 0.5  # 三角函数 半径

            if l < r3:
                pimb[i - (r - r3), j - (r - r3)] = pima[i, j]
    return imb


def add_decorate(base_pic):
    try:
        base_pic = "./base/%s.png" % (str(base_pic))
        user_pic = Image.open("/tmp/picture.png").convert("RGBA")
        temp_basee_user_pic = Image.new('RGBA', (440, 440), (255, 255, 255))
        user_pic = user_pic.resize((400, 400), Image.ANTIALIAS)
        temp_basee_user_pic.paste(user_pic, (20, 20))
        temp_basee_user_pic.paste(do_circle(base_pic), (295, 295), do_circle(base_pic))
        temp_basee_user_pic.save("/tmp/output.png")
        return True
    except Exception as e:
        print(e)
        return False


def main_handler(event, context):
    try:
        print("将接收到的base64图像转为pic")
        imgData = base64.b64decode(json.loads(event["body"])["pic"].split("base64,")[1])
        with open('/tmp/picture.png', 'wb') as f:
            f.write(imgData)

        basePic = json.loads(event["body"])["base"]
        addResult = add_decorate(basePic)
        if addResult:
            with open("/tmp/output.png", "rb") as f:
                base64Data = str(base64.b64encode(f.read()), encoding='utf-8')
            return return_msg(False, {"picture": base64Data})
        else:
            return return_msg(True, "饰品添加失败")
    except Exception as e:
        return return_msg(True, "数据处理异常： %s" % str(e))


def test():
    with open("test.png", 'rb') as f:
        image = f.read()
        image_base64 = str(base64.b64encode(image), encoding='utf-8')
    event = {
        "requestContext": {
            "serviceId": "service-f94sy04v",
            "path": "/test/{path}",
            "httpMethod": "POST",
            "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
            "identity": {
                "secretId": "abdcdxxxxxxxsdfs"
            },
            "sourceIp": "14.17.22.34",
            "stage": "release"
        },
        "headers": {
            "Accept-Language": "en-US,en,cn",
            "Accept": "text/html,application/xml,application/json",
            "Host": "service-3ei3tii4-251000691.ap-guangzhou.apigateway.myqloud.com",
            "User-Agent": "User Agent String"
        },
        "body": "{\"pic\":\"%s\", \"base\":\"1\"}" % image_base64,
        "pathParameters": {
            "path": "value"
        },
        "queryStringParameters": {
            "foo": "bar"
        },
        "headerParameters": {
            "Refer": "10.0.2.14"
        },
        "stageVariables": {
            "stage": "release"
        },
        "path": "/test/value",
        "queryString": {
            "foo": "bar",
            "bob": "alice"
        },
        "httpMethod": "POST"
    }
    print(main_handler(event, None))


if __name__ == "__main__":
    test()
